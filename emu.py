#!/usr/bin/env python3
"""
EMX-1 style groovebox / synthesizer emulator
=============================================

A console-controlled, approximate software instrument inspired by the Korg
Electribe EMX-1. It is NOT a bit-accurate or circuit-accurate clone.

Requirements:
    pip install numpy sounddevice

Run:
    python emx_emulator.py

Useful console commands:
    help
    play
    stop
    bpm 135
    part 1
    note 1 C2 1/8
    step 6A 1,5,9,13
    param 1 cutoff 0.35
    motion 1 cutoff smooth 1:0.1,5:0.8,9:0.3,13:0.9
    fx 1 distortion
    send 1 on
    render demo.wav 8
    status
    py print(engine.pattern.parts["SYNTH1"].params)
    quit

Part names:
    SYNTH1..SYNTH5, DRUM1..DRUM5, DRUM6A, DRUM6B,
    DRUM7A, DRUM7B, DRUMACCENT, SYNTHACCENT

The `py` command executes Python in a namespace containing `engine`, `np`,
and the emulator classes. This is intentionally powerful: only run code you
trust.
"""

from __future__     import annotations

import ast
import math
import shlex
import threading
import time
import wave
from dataclasses    import dataclass, field
from pathlib        import Path
from typing         import Dict, List, Optional, Tuple
import numpy as np

SAMPLE_RATE = 44100
BLOCK_SIZE = 512
STEPS_PER_BAR = 16
MAX_STEPS = 128
SYNTH_NAMES = [f"SYNTH{i}" for i in range(1, 6)]
DRUM_NAMES = (
    [f"DRUM{i}" for i in range(1, 6)]
    + ["DRUM6A", "DRUM6B", "DRUM7A", "DRUM7B"]
)
ACCENT_NAMES = ["DRUMACCENT", "SYNTHACCENT"]
PART_NAMES = SYNTH_NAMES + DRUM_NAMES + ACCENT_NAMES

FX_NAMES = [
    "reverb", "bpm_sync_delay", "short_delay", "mod_delay",
    "chorus_flanger", "phaser", "ring_mod", "talking_mod",
    "pitch_shifter", "grain_shifter", "compressor", "distortion",
    "decimator", "eq", "lpf", "hpf",
]
MOD_TYPES = ["saw", "square", "triangle", "sample_hold", "eg"]
MOD_DESTS_SYNTH = ["pitch", "osc_edit1", "osc_edit2", "cutoff", "amp", "pan"]
MOD_DESTS_DRUM = ["pitch", "amp", "pan"]


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, float(x)))


def midi_note(value):
    """Convert note names (C2, F#3, Bb1) or MIDI numbers to MIDI note."""
    try:
        return int(value)
    except (TypeError, ValueError):
        s = str(value).strip().upper()
        names = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
                 "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
                 "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}
        import re
        m = re.fullmatch(r"([A-G](?:#|B)?)(-?\d+)", s)
        if not m or m.group(1) not in names:
            raise ValueError(f"Nota no válida: {value}")
        # MIDI convention: C4 = 60
        return (int(m.group(2)) + 1) * 12 + names[m.group(1)]


def parse_duration(value, bpm):
    """Convert values such as 1/8, 1/16, 1bar or milliseconds to seconds."""
    s = str(value).lower().strip()
    if s.endswith("ms"):
        return max(0.005, float(s[:-2]) / 1000.0)
    if s.endswith("bar"):
        return float(s[:-3]) * 4 * 60.0 / bpm
    if "/" in s:
        a, b = s.split("/", 1)
        return (4.0 * float(a) / float(b)) * 60.0 / bpm
    return float(s)


@dataclass
class MotionSequence:
    """One parameter lane; points are step-indexed and values are 0..1."""
    parameter: str
    mode: str = "smooth"       # smooth or trig_hold
    points: Dict[int, float] = field(default_factory=dict)
    enabled: bool = True

    def value_at(self, step: int, fraction: float = 0.0) -> Optional[float]:
        if not self.enabled or not self.points:
            return None
        keys = sorted(self.points)
        pos = (step + fraction) % MAX_STEPS
        left = keys[-1]
        right = keys[0] + MAX_STEPS
        for k in keys:
            if k <= pos:
                left = k
            elif k > pos:
                right = k
                break
        lv = self.points[left % MAX_STEPS]
        rv = self.points[right % MAX_STEPS]
        if self.mode in ("trig", "trigger", "trig_hold", "trigger_hold"):
            return lv
        span = right - left
        if span <= 0:
            return lv
        t = (pos - left) / span
        return lv + (rv - lv) * t


@dataclass
class Part:
    name: str
    kind: str
    steps: Dict[int, List[int]] = field(default_factory=dict)
    notes: Dict[int, Tuple[int, float, float]] = field(default_factory=dict)
    params: Dict[str, float] = field(default_factory=dict)
    motions: Dict[str, MotionSequence] = field(default_factory=dict)
    fx_select: int = 1
    fx_send: bool = False
    mod_type: str = "triangle"
    mod_dest: str = "cutoff"
    bpm_sync: bool = True
    roll: bool = False
    active: bool = True
    accent: float = 1.0
    voice_phase: float = 0.0
    voice_freq: float = 110.0
    voice_amp: float = 0.0
    voice_age: float = 0.0
    voice_duration: float = 0.2
    voice_note: int = 48
    voice_env: float = 0.0
    filter_state: float = 0.0
    filter_state2: float = 0.0
    noise_state: int = 1

    def __post_init__(self):
        if not self.params:
            if self.kind == "synth":
                self.params = {
                    "wave": 0, "pitch": 0.0, "cutoff": 0.55, "resonance": 0.12,
                    "drive": 0.0, "eg_time": 0.45, "amp": 0.75, "pan": 0.0,
                    "osc_edit1": 0.5, "osc_edit2": 0.5, "lfo_speed": 0.25,
                    "lfo_depth": 0.0, "eg_int": 0.0, "attack": 0.005,
                }
            elif self.kind == "drum":
                self.params = {
                    "pitch": 0.0, "eg_time": 0.35, "amp": 0.8, "pan": 0.0,
                    "tone": 0.5, "decay": 0.35, "noise": 0.15,
                }


class FXProcessor:
    """Lightweight, real-time approximations of the EMX effect families."""
    def __init__(self, sample_rate=SAMPLE_RATE):
        self.sr = sample_rate
        self.name = "reverb"
        self.p1 = 0.35
        self.p2 = 0.5
        self.delay_l = np.zeros(sample_rate * 2, dtype=np.float32)
        self.delay_r = np.zeros(sample_rate * 2, dtype=np.float32)
        self.write = 0
        self.phase = 0.0
        self.lp_l = self.lp_r = 0.0
        self.hp_l = self.hp_r = 0.0
        self.hold = 0.0
        self.counter = 0
        self.last_l = self.last_r = 0.0

    def set_type(self, name):
        name = name.lower().replace("-", "_").replace("/", "_")
        aliases = {"cho_flg": "chorus_flanger", "ring_modulator": "ring_mod",
                   "talking_mod": "talking_mod", "decimator": "decimator",
                   "distortion": "distortion", "eq": "eq", "lpf": "lpf", "hpf": "hpf",
                   "phaser": "phaser", "reverb": "reverb"}
        if name not in FX_NAMES:
            name = aliases.get(name, name)
        if name not in FX_NAMES:
            raise ValueError(f"Efecto desconocido. Opciones: {', '.join(FX_NAMES)}")
        self.name = name

    def process(self, x):
        if x.size == 0:
            return x
        y = x.copy()
        n = len(y)
        name = self.name
        if name in ("bpm_sync_delay", "short_delay", "mod_delay", "reverb",
                    "chorus_flanger", "phaser", "grain_shifter"):
            base = {"bpm_sync_delay": 0.30, "short_delay": 0.085,
                    "mod_delay": 0.018, "reverb": 0.055,
                    "chorus_flanger": 0.012, "phaser": 0.008,
                    "grain_shifter": 0.045}[name]
            for i in range(n):
                mod = 1.0 + (0.35 * math.sin(self.phase) if name in
                             ("mod_delay", "chorus_flanger", "phaser") else 0.0)
                delay = max(1, int(self.sr * base * mod))
                r = (self.write - delay) % len(self.delay_l)
                dl, dr = self.delay_l[r], self.delay_r[r]
                l, rr = y[i, 0], y[i, 1]
                if name == "reverb":
                    wet = 0.28
                    out = (l + dl * 0.55, rr + dr * 0.55)
                    feedback = 0.62
                elif name == "chorus_flanger":
                    wet, feedback = 0.45, 0.0
                    out = (l * 0.75 + dl * wet, rr * 0.75 + dr * wet)
                elif name == "phaser":
                    wet, feedback = 0.45, 0.0
                    out = (l * 0.65 + dl * wet, rr * 0.65 + dr * wet)
                elif name == "grain_shifter":
                    wet, feedback = 0.35, 0.0
                    out = (l * 0.7 + dl * wet, rr * 0.7 + dr * wet)
                else:
                    wet = 0.42 if name == "bpm_sync_delay" else 0.30
                    feedback = 0.42 if name == "bpm_sync_delay" else 0.18
                    out = (l + dl * wet, rr + dr * wet)
                self.delay_l[self.write] = l + dl * feedback
                self.delay_r[self.write] = rr + dr * feedback
                y[i, 0], y[i, 1] = out
                self.write = (self.write + 1) % len(self.delay_l)
                self.phase += 2 * math.pi * 0.25 / self.sr
            return np.tanh(y * 0.9).astype(np.float32)

        if name == "distortion":
            drive = 1.0 + 18.0 * self.p1
            return (np.tanh(y * drive) / max(1.0, math.tanh(drive))).astype(np.float32)
        if name == "compressor":
            peak = np.max(np.abs(y)) + 1e-8
            gain = min(1.0, 0.75 / peak) ** 0.65
            return (y * gain).astype(np.float32)
        if name == "decimator":
            hold_every = 1 + int(30 * self.p1)
            for i in range(n):
                if self.counter % hold_every == 0:
                    self.last_l, self.last_r = y[i]
                y[i] = (self.last_l, self.last_r)
                self.counter += 1
            return y
        if name in ("lpf", "eq", "talking_mod"):
            cutoff = 0.015 + 0.45 * self.p1
            for i in range(n):
                self.lp_l += cutoff * (y[i, 0] - self.lp_l)
                self.lp_r += cutoff * (y[i, 1] - self.lp_r)
                y[i] = (self.lp_l, self.lp_r)
            if name == "talking_mod":
                y *= (0.6 + 0.4 * np.sin(np.arange(n) * (0.03 + self.p2 * 0.2)))[:, None]
            return y.astype(np.float32)
        if name == "hpf":
            cutoff = 0.01 + 0.35 * self.p1
            for i in range(n):
                self.lp_l += cutoff * (y[i, 0] - self.lp_l)
                self.lp_r += cutoff * (y[i, 1] - self.lp_r)
                y[i] -= (self.lp_l, self.lp_r)
            return y.astype(np.float32)
        if name == "ring_mod":
            t = np.arange(n) / self.sr + self.phase
            mod = np.sin(2 * np.pi * (35 + 900 * self.p1) * t)
            y *= mod[:, None]
            self.phase += n / self.sr
            return y.astype(np.float32)
        if name == "pitch_shifter":
            # Simple metallic modulation approximation, not a phase vocoder.
            t = np.arange(n) / self.sr + self.phase
            y *= (0.75 + 0.25 * np.sin(2 * np.pi * 5 * t))[:, None]
            self.phase += n / self.sr
            return y.astype(np.float32)
        return y.astype(np.float32)


class Pattern:
    def __init__(self, name="A01"):
        self.name = name
        self.length = 16
        self.parts: Dict[str, Part] = {}
        for n in SYNTH_NAMES:
            self.parts[n] = Part(n, "synth")
        for n in DRUM_NAMES:
            self.parts[n] = Part(n, "drum")
        for n in ACCENT_NAMES:
            self.parts[n] = Part(n, "accent")
        self.fx = [FXProcessor(), FXProcessor(), FXProcessor()]
        self.master_gain = 0.7
        self.step = 0
        self.bar_count = 0

    def part(self, name):
        key = name.upper()
        aliases = {"S1": "SYNTH1", "S2": "SYNTH2", "S3": "SYNTH3",
                   "S4": "SYNTH4", "S5": "SYNTH5"}
        key = aliases.get(key, key)
        if key not in self.parts:
            raise ValueError(f"Parte desconocida: {name}")
        return self.parts[key]


class Groovebox:
    def __init__(self, sample_rate=SAMPLE_RATE):
        self.sr = sample_rate
        self.pattern = Pattern()
        self.bpm = 120.0
        self.playing = False
        self.global_step = 0
        self.samples_to_step = 0.0
        self.sample_clock = 0
        self.lock = threading.RLock()
        self.stream = None
        self.song = []
        self.current_pattern = 0
        self.tube_gain = 0.0
        self.swing = 0.0
        self._rng = np.random.default_rng(12345)

    @property
    def step_samples(self):
        return self.sr * 60.0 / self.bpm / 4.0

    def set_bpm(self, bpm):
        if not 30 <= float(bpm) <= 300:
            raise ValueError("BPM debe estar entre 30 y 300.")
        self.bpm = float(bpm)

    def trigger(self, part: Part, note=None, velocity=1.0, duration=None):
        part.voice_amp = clamp(velocity) * part.params.get("amp", 0.8)
        part.voice_age = 0.0
        part.voice_env = 1.0
        part.voice_phase = 0.0
        if note is not None:
            part.voice_note = int(note)
        part.voice_freq = 440.0 * (2.0 ** ((part.voice_note - 69) / 12.0))
        part.voice_duration = max(0.03, float(duration) if duration is not None else (0.06 + part.params.get("eg_time", 0.4) * 1.5))

    def _motion_value(self, part, parameter, step, frac):
        seq = part.motions.get(parameter)
        return seq.value_at(step, frac) if seq else None

    def _mod_value(self, part, t, step):
        speed = part.params.get("lfo_speed", 0.25)
        if part.bpm_sync:
            hz = self.bpm / 60.0 / max(0.125, 8.0 * (1.0 - speed) + 0.125)
        else:
            hz = 0.1 + speed * 15.0
        phase = (t * hz) % 1.0
        typ = part.mod_type
        if typ == "saw":
            v = 2 * phase - 1
        elif typ == "square":
            v = 1.0 if phase < 0.5 else -1.0
        elif typ == "triangle":
            v = 1.0 - 4.0 * abs(phase - 0.5)
        elif typ == "sample_hold":
            v = math.sin(math.floor(t * hz) * 12.9898) * 0.5
        else:
            v = max(0.0, 1.0 - (t % max(0.1, 1.0 / max(hz, 0.01))) * hz)
        return v * part.params.get("lfo_depth", 0.0)

    def _oscillator(self, part, n, freq, t0, cutoff, mod):
        p = part.params
        wave_id = int(p.get("wave", 0)) % 8
        phase = part.voice_phase + (2 * math.pi * freq / self.sr) * np.arange(n)
        saw = 2.0 * ((phase / (2 * math.pi)) % 1.0) - 1.0
        if wave_id == 0:
            sig = saw
        elif wave_id == 1:
            sig = np.sign(np.sin(phase))
        elif wave_id == 2:
            sig = np.sin(phase)
        elif wave_id == 3:
            sig = 2 / math.pi * np.arcsin(np.sin(phase))
        elif wave_id == 4:
            sig = np.sin(phase) + 0.35 * np.sin(2 * phase)
        elif wave_id == 5:
            sig = np.sin(phase) + 0.5 * np.sin(3 * phase) + 0.25 * np.sin(5 * phase)
        elif wave_id == 6:
            sig = np.sign(np.sin(phase * (1.0 + p.get("osc_edit1", 0.5) * 4)))
        else:
            sig = np.sin(phase * (1.0 + 5.0 * p.get("osc_edit1", 0.5))) * saw
        sig = np.asarray(sig, dtype=np.float32)
        # One-pole low-pass with resonance feedback approximation.
        fc = clamp(cutoff + mod, 0.005, 0.98)
        alpha = 1.0 - math.exp(-2.0 * math.pi * min(0.45, fc * 0.45))
        out = np.empty(n, dtype=np.float32)
        state = part.filter_state
        state2 = part.filter_state2
        resonance = p.get("resonance", 0.1) * 0.85
        for i, x in enumerate(sig):
            state += alpha * (float(x) - state + resonance * (state - state2))
            state2 += alpha * (state - state2)
            out[i] = state
        part.filter_state, part.filter_state2 = state, state2
        part.voice_phase = (part.voice_phase + 2 * math.pi * freq * n / self.sr) % (2 * math.pi)
        drive = 1.0 + p.get("drive", 0.0) * 10.0
        return np.tanh(out * drive).astype(np.float32)

    def _render_part(self, part, n, t0, step, frac):
        if part.kind == "accent" or part.voice_amp <= 1e-5:
            return np.zeros((n, 2), dtype=np.float32)
        p = part.params
        motion = {}
        for key in list(p):
            val = self._motion_value(part, key, step, frac)
            if val is not None:
                motion[key] = val
        get = lambda k: motion.get(k, p.get(k, 0.0))
        mod = self._mod_value(part, t0, step)
        dest = part.mod_dest
        cutoff_mod = mod if dest == "cutoff" else 0.0
        pitch_mod = mod * 12.0 if dest == "pitch" else 0.0
        freq = part.voice_freq * (2 ** ((get("pitch") * 24.0 + pitch_mod) / 12.0))
        if part.kind == "synth":
            mono = self._oscillator(part, n, freq, t0, get("cutoff"), cutoff_mod)
            age = part.voice_age + np.arange(n) / self.sr
            attack = max(0.001, p.get("attack", 0.005))
            decay = max(0.02, part.voice_duration)
            env = np.minimum(1.0, age / attack) * np.exp(-age / decay)
            if not part.roll:
                env = np.maximum(env, 0.0)
            mono *= env.astype(np.float32) * part.voice_amp
        else:
            # Internal synthetic drum voices: kick, snare, hats and percussion.
            age = part.voice_age + np.arange(n) / self.sr
            name = part.name
            if "1" in name:
                base = 48.0
            elif "2" in name:
                base = 180.0
            elif "3" in name:
                base = 6500.0
            elif "4" in name:
                base = 4200.0
            else:
                base = 320.0 + 900.0 * p.get("tone", 0.5)
            freq_env = base * np.exp(-age * (22.0 if "1" in name else 5.0))
            phase = part.voice_phase + np.cumsum(2 * np.pi * freq_env / self.sr)
            tone = np.sin(phase)
            noise = self._rng.standard_normal(n).astype(np.float32)
            noise_mix = clamp(p.get("noise", 0.15) + (0.75 if "3" in name or "4" in name else 0))
            mono = tone * (1.0 - noise_mix) + noise * noise_mix
            decay = max(0.025, p.get("decay", 0.35) * 1.6)
            env = np.exp(-age / decay)
            mono = (mono * env * part.voice_amp).astype(np.float32)
            part.voice_phase = (part.voice_phase + 2 * math.pi * base * n / self.sr) % (2 * math.pi)
        part.voice_age += n / self.sr
        if part.voice_age > part.voice_duration * 5 + 1.0:
            part.voice_amp = 0.0
        pan = clamp((get("pan") + 1.0) * 0.5)
        left = mono * math.cos(pan * math.pi / 2)
        right = mono * math.sin(pan * math.pi / 2)
        return np.column_stack((left, right)).astype(np.float32)

    def _step_events(self, step):
        p = self.pattern
        for name, part in p.parts.items():
            if part.kind == "accent":
                continue
            if step not in part.steps and step not in part.notes:
                continue
            # Paired drum channels are mutually exclusive: B wins on collision.
            if name == "DRUM6A" and step in p.parts["DRUM6B"].steps:
                continue
            if name == "DRUM7A" and step in p.parts["DRUM7B"].steps:
                continue
            if name in ("DRUM6B", "DRUM7B") and step not in part.steps:
                continue
            if name in ("DRUM6A", "DRUM7A") and step not in part.steps:
                continue
            if part.kind == "synth":
                event = part.notes.get(step, (part.voice_note, 1.0, None))
                note, velocity = event[0], event[1]
                duration = event[2] if len(event) > 2 else None
                self.trigger(part, note, velocity, duration)
            else:
                velocity = part.steps.get(step, [100])[0] / 127.0
                self.trigger(part, None, velocity)

    def render(self, frames):
        out = np.zeros((frames, 2), dtype=np.float32)
        if not self.playing:
            # Voices continue to decay after transport stops.
            for part in self.pattern.parts.values():
                if part.kind != "accent":
                    out += self._render_part(part, frames, self.sample_clock / self.sr,
                                             self.global_step % self.pattern.length, 0)
            self.sample_clock += frames
            return self._master(out)
        offset = 0
        while offset < frames:
            if self.samples_to_step <= 0:
                step = self.global_step % self.pattern.length
                self._step_events(step)
                self.samples_to_step += self.step_samples
                self.global_step += 1
            count = min(frames - offset, max(1, int(self.samples_to_step)))
            t0 = self.sample_clock / self.sr
            step = (self.global_step - 1) % self.pattern.length
            mix = np.zeros((count, 2), dtype=np.float32)
            fx_buses = [np.zeros_like(mix) for _ in range(3)]
            for part in self.pattern.parts.values():
                if part.kind == "accent":
                    continue
                sound = self._render_part(part, count, t0, step, 0.0)
                if part.fx_send:
                    fx_buses[part.fx_select - 1] += sound
                else:
                    mix += sound
            for i, bus in enumerate(fx_buses):
                if np.any(bus):
                    mix += self.pattern.fx[i].process(bus)
            out[offset:offset + count] += mix
            self.samples_to_step -= count
            offset += count
            self.sample_clock += count
        return self._master(out)

    def _master(self, audio):
        """
        Emulación avanzada estilo Valve Force (Triodo 12AX7 / ECC83)
        Reemplaza la función simple de np.tanh por un modelo no lineal asimétrico.
        """
        if audio.size == 0:
            return audio
            
        # 1. Configuración de Ganancia (Tube Gain) e Inyección Dinámica
        # Mapeamos la ganancia maestra combinada con el parámetro tube_gain del instrumento
        gain_drive = self.pattern.master_gain * (1.0 + self.tube_gain * 5.0)
        
        # Amplificamos la señal analógica virtual antes de entrar a la aduana de electrones
        audio_driven = audio * gain_drive
        
        # 2. Factor de Asimetría (Bias del Cátodo Físico)
        # Una válvula real no distorsiona simétricamente debido a la corriente de polarización DC.
        # A mayor ganancia del tubo, mayor es el desplazamiento del punto de operación (Bias Shift).
        bias_shift = self.tube_gain * 0.28
        
        # 3. Procesamiento No Lineal Asimétrico (Flujo de Electrones)
        # Aplicamos la función matemática al audio con offset de continua
        audio_biased = audio_driven + bias_shift
        
        # El soft-clipping emula la saturación natural donde los picos se redondean.
        # Restamos np.tanh(bias_shift) para eliminar el offset DC resultante de la ecuación
        # y evitar dañar los altavoces o generar clics digitales.
        audio_saturated = np.tanh(audio_biased) - np.tanh(bias_shift)
        
        # 4. Filtro de suavizado pasivo (Emulación de la capacitancia interna de placa)
        # Las válvulas físicas absorben de forma natural las frecuencias ultra-altas muy estridentes.
        # Implementamos un filtro pasa-bajos de un solo polo (One-Pole Low Pass Filter).
        if not hasattr(self, '_valve_filter_state'):
            self._valve_filter_state = np.zeros(2, dtype=np.float32) # Estado para L y R
            
        # Coeficiente del filtro (a mayor saturación, el circuito se vuelve ligeramente más oscuro)
        alpha = 0.85 - (self.tube_gain * 0.15) 
        
        for i in range(len(audio_saturated)):
            self._valve_filter_state = self._valve_filter_state + alpha * (audio_saturated[i] - self._valve_filter_state)
            audio_saturated[i] = self._valve_filter_state

        # 5. Limitador de Seguridad Final (Brickwall)
        peak = np.max(np.abs(audio_saturated))
        if peak > 0.98:
            audio_saturated *= 0.98 / peak
            
        return audio_saturated.astype(np.float32)


    def start_audio(self):
        try:
            import sounddevice as sd
        except ImportError:
            raise RuntimeError("Falta sounddevice. Instala con: pip install sounddevice")
        if self.stream:
            return
        def callback(outdata, frames, _time_info, status):
            if status:
                pass
            with self.lock:
                outdata[:] = self.render(frames)
        self.stream = sd.OutputStream(samplerate=self.sr, blocksize=BLOCK_SIZE,
                                      channels=2, dtype="float32", callback=callback)
        self.stream.start()

    def stop_audio(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def play(self):
        self.playing = True
        if self.samples_to_step <= 0:
            self.samples_to_step = 0

    def stop(self):
        self.playing = False

    def clear(self):
        with self.lock:
            self.pattern = Pattern()
            self.global_step = 0
            self.samples_to_step = 0

    def render_file(self, filename, bars=4):
        frames = int(self.sr * (60 / self.bpm) * 4 * bars)
        old_playing = self.playing
        old_step, old_left, old_clock = self.global_step, self.samples_to_step, self.sample_clock
        self.playing = True
        self.global_step = 0
        self.samples_to_step = 0
        chunks = []
        remaining = frames
        while remaining:
            n = min(4096, remaining)
            chunks.append(self.render(n))
            remaining -= n
        audio = np.concatenate(chunks, axis=0)
        self.playing = old_playing
        self.global_step, self.samples_to_step, self.sample_clock = old_step, old_left, old_clock
        pcm = np.int16(np.clip(audio, -1, 1) * 32767)
        with wave.open(str(filename), "wb") as f:
            f.setnchannels(2)
            f.setsampwidth(2)
            f.setframerate(self.sr)
            f.writeframes(pcm.tobytes())
        return frames / self.sr


class Console:
    def __init__(self, engine):
        self.engine = engine
        self.selected = "SYNTH1"
        self.namespace = {"engine": engine, "np": np, "Part": Part,
                          "Pattern": Pattern, "MotionSequence": MotionSequence,
                          "FXProcessor": FXProcessor}

    def help(self):
        print("""
COMANDOS
  help                         Muestra esta ayuda
  status                       Estado del instrumento
  bpm 135                      Cambia el tempo
  play | stop                  Inicia / detiene el secuenciador
  part SYNTH1                  Selecciona una parte
  note SYNTH1 C2 1/8            Añade una nota en el paso actual
  note SYNTH1 C2 1/8 at 1       Añade una nota en el paso 1
  step DRUM1 1,5,9,13           Programa golpes en esos pasos (1..128)
  clear                        Borra el patrón
  length 64                    Longitud del patrón en pasos
  param SYNTH1 cutoff 0.7      Ajusta un parámetro
  fx 1 distortion              Selecciona efecto de FX1, FX2 o FX3
  fxparam 1 0.5 0.7            Ajusta FX EDIT 1 y FX EDIT 2
  send SYNTH1 on               Activa el envío de esa parte
  fxselect SYNTH1 2            Enruta la parte al procesador 2
  motion SYNTH1 cutoff smooth 1:0.1,5:0.8
  motion SYNTH1 cutoff trig_hold 1:0.2,9:0.9
  motiondel SYNTH1 cutoff      Elimina esa automatización
  mod SYNTH1 triangle cutoff 0.3 0.5
  tube 0.4                     Saturación global Valve Force
  render demo.wav 4            Renderiza 4 compases a WAV
  py <código Python>           Ejecuta Python con engine y np disponibles
  quit                         Salir

Valores de wave para sintetizador:
  0 saw, 1 square, 2 sine, 3 triangle, 4 dual-ish, 5 harmonic,
  6 pulse/PWM-like, 7 cross-mod-like. Son aproximaciones.
Parámetros típicos synth: wave, pitch, cutoff, resonance, drive, eg_time,
amp, pan, osc_edit1, osc_edit2, lfo_speed, lfo_depth, eg_int, attack.
Parámetros típicos drum: pitch, eg_time, amp, pan, tone, decay, noise.
""")

    def status(self):
        e, p = self.engine, self.engine.pattern
        print(f"\n{p.name} | {e.bpm:.1f} BPM | length={p.length} steps | "
              f"{'PLAYING' if e.playing else 'STOPPED'}")
        print(f"Selected: {self.selected} | global step: {e.global_step % p.length + 1}")
        for name in PART_NAMES:
            part = p.parts[name]
            if part.kind == "synth":
                content = f"{len(part.notes)} notes"
            elif part.kind == "drum":
                content = f"{len(part.steps)} hits"
            else:
                content = "accent"
            print(f"  {name:13} {content:10} FX{part.fx_select} "
                  f"send={'ON' if part.fx_send else 'OFF'} "
                  f"motions={len(part.motions)}")
        print("FX:", ", ".join(f"{i+1}:{fx.name}" for i, fx in enumerate(p.fx)))

    def execute(self, line):
        args = shlex.split(line)
        if not args:
            return True
        cmd = args[0].lower()
        e, p = self.engine, self.engine.pattern
        if cmd in ("quit", "exit"):
            return False
        if cmd == "help":
            self.help()
        elif cmd == "status":
            self.status()
        elif cmd == "bpm":
            e.set_bpm(args[1]); print(f"BPM = {e.bpm}")
        elif cmd == "play":
            e.start_audio(); e.play(); print("Reproducción iniciada.")
        elif cmd == "stop":
            e.stop(); print("Secuenciador detenido.")
        elif cmd == "part":
            self.selected = p.part(args[1]).name; print("Parte:", self.selected)
        elif cmd == "clear":
            e.clear(); print("Patrón borrado.")
        elif cmd == "length":
            value = int(args[1])
            if not 1 <= value <= MAX_STEPS:
                raise ValueError("La longitud debe estar entre 1 y 128.")
            p.length = value
        elif cmd == "note":
            part = p.part(args[1])
            if part.kind != "synth":
                raise ValueError("note se usa con una parte SYNTH.")
            note = midi_note(args[2])
            duration = parse_duration(args[3], e.bpm)
            step = int(args[5]) - 1 if len(args) >= 6 and args[4].lower() == "at" else e.global_step % p.length
            part.notes[step] = (note, 1.0, duration)
            print(f"{part.name}: {args[2]} en paso {step+1}, duración {duration:.3f}s")
        elif cmd == "step":
            part = p.part(args[1])
            if part.kind != "drum":
                raise ValueError("step se usa con una parte DRUM.")
            steps = [int(x.strip()) - 1 for x in args[2].split(",")]
            if any(x < 0 or x >= MAX_STEPS for x in steps):
                raise ValueError("Pasos válidos: 1..128.")
            part.steps = {s: [100] for s in steps}
            print(f"{part.name}: {', '.join(str(s+1) for s in steps)}")
        elif cmd == "param":
            part = p.part(args[1])
            key, value = args[2].lower(), float(args[3])
            if key not in part.params:
                raise ValueError(f"Parámetro no disponible. Opciones: {', '.join(part.params)}")
            if key == "wave":
                part.params[key] = int(value)
            elif key == "pan":
                part.params[key] = max(-1, min(1, value))
            else:
                part.params[key] = clamp(value)
            print(f"{part.name}.{key} = {part.params[key]}")
        elif cmd == "fx":
            idx = int(args[1]) - 1
            if idx not in range(3):
                raise ValueError("El procesador debe ser 1, 2 o 3.")
            p.fx[idx].set_type(args[2])
            print(f"FX{idx+1} = {p.fx[idx].name}")
        elif cmd == "fxparam":
            idx = int(args[1]) - 1
            p.fx[idx].p1, p.fx[idx].p2 = clamp(args[2]), clamp(args[3])
        elif cmd == "send":
            part = p.part(args[1])
            part.fx_send = args[2].lower() in ("on", "1", "true", "yes")
        elif cmd == "fxselect":
            part = p.part(args[1])
            value = int(args[2])
            if value not in (1, 2, 3):
                raise ValueError("FX SELECT debe ser 1, 2 o 3.")
            part.fx_select = value
        elif cmd == "motion":
            part = p.part(args[1])
            parameter, mode, points = args[2].lower(), args[3].lower(), args[4]
            if parameter not in part.params and parameter not in ("fx_edit1", "fx_edit2"):
                raise ValueError("Parámetro no reconocido para Motion Sequence.")
            parsed = {}
            for pair in points.split(","):
                step, val = pair.split(":")
                parsed[int(step)-1] = clamp(float(val))
            if len(part.motions) >= 24 and parameter not in part.motions:
                raise ValueError("Límite de 24 Motion Sequences por patrón alcanzado.")
            part.motions[parameter] = MotionSequence(parameter, mode, parsed)
            print(f"Motion Sequence creada: {part.name}/{parameter}, {len(parsed)} puntos.")
        elif cmd == "motiondel":
            part = p.part(args[1])
            part.motions.pop(args[2].lower(), None)
        elif cmd == "mod":
            part = p.part(args[1])
            typ, dest = args[2].lower(), args[3].lower()
            if typ not in MOD_TYPES:
                raise ValueError(f"MOD TYPE: {MOD_TYPES}")
            allowed = MOD_DESTS_SYNTH if part.kind == "synth" else MOD_DESTS_DRUM
            if dest not in allowed:
                raise ValueError(f"MOD DEST para {part.kind}: {allowed}")
            part.mod_type, part.mod_dest = typ, dest
            part.params["lfo_speed"] = clamp(float(args[4]))
            part.params["lfo_depth"] = clamp(float(args[5]))
        elif cmd == "tube":
            e.tube_gain = clamp(args[1])
        elif cmd == "render":
            bars = int(args[2]) if len(args) > 2 else 4
            seconds = e.render_file(args[1], bars)
            print(f"Archivo creado: {args[1]} ({seconds:.2f} segundos)")
        elif cmd == "py":
            source = line.partition(" ")[2]
            if not source:
                print("Uso: py <expresión o código Python>")
            else:
                try:
                    exec(source, self.namespace, self.namespace)
                except Exception as exc:
                    print(f"Python: {type(exc).__name__}: {exc}")
        else:
            print("Comando desconocido. Escribe help.")
        return True


def main():
    engine = Groovebox()
    console = Console(engine)
    print("EMX-1 style groovebox emulator (aproximación software)")
    print("Escribe help para ver comandos. No es un clon exacto del hardware.")
    try:
        while True:
            try:
                line = input("EMX> ")
            except EOFError:
                break
            try:
                if not console.execute(line):
                    break
            except Exception as exc:
                print(f"Error: {exc}")
    except KeyboardInterrupt:
        pass
    finally:
        engine.stop()
        engine.stop_audio()
        print("Hasta luego.")


if __name__ == "__main__":
    main()
