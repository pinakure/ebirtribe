import random
import pygame
import math


class LcdDemo(object):
    """Braille LCD demoscene using the Lcd raster and mixed-mode API."""
    lcd         = None
    now         = None
    frame       = None
    narrow      = None
    wide        = None
    lines       = []
    rows        = None
    scene       = None
    phase       = None
    glow        = 1.0
    glyphs      = " .,:;!|/\\\\-_=+*ox%#@"
    shade       = " ▁▂▃▄▅▆▇█"
    blocks      = " ░▒▓█"
    duration    = 6.5

    VERSION     = 1.0
    BOOT_SPLASH = [
        [
            "▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜",
            "▌ ▐▌    ▐▌   ▐▌ ▞▀▀▀▀ ▜▛   ▜▛ ▐",
            "▌ ▐▌    ▐▌   ▐▌ ▀▀▀▀▚ ▐▛▀▀▀▜▌ ▐",
            "▌ ▐▙▄▄▄ ▐▙▄▄▄▟▌ ▄▄▄▄▞ ▟▙   ▟▙ ▐",
            "▙▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▟",
        ],
        [
            "▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▜",
            "▌  ▗▛▀▀▀▀ ▐▛▀▚▞▀▜▌ ▚  ▞   ▜▌  ▐",
            "▌  ▐▛▀▀▀▀ ▐▌ ▐▌ ▐▌ ▗▀▀▖ - ▐▌  ▐",
            "▌   ▀▀▀▀▀ ▀▀ ▀▀ ▀▀ ▘  ▝   ▀▀  ▐",
           f"▚  FW.Ver. {str(VERSION).ljust(4,'0')} / Standalone  ▞",
        ]        
    ]

    def init(lcd):
        LcdDemo.lcd     = lcd
        # Logical geometry never changes.
        # A row may use columns or columns*2 glyphs.
        LcdDemo.narrow  = max(1, lcd.columns)
        LcdDemo.wide    = LcdDemo.narrow * 2
        LcdDemo.rows    = max(1, lcd.rows)
        LcdDemo.run()        

    def fit(value, limit=None):
        limit = LcdDemo.narrow if limit == None else limit
        value = str(value)
        return value[:limit].ljust(limit)

    def center(value, limit=None):
        limit = LcdDemo.narrow if limit == None else limit
        return LcdDemo.fit(str(value).center(limit), limit)

    def scroll(value, offset, limit=None):
        limit = LcdDemo.wide if limit == None else limit
        value = " " * limit + str(value) + " " * limit
        p = int(offset) % len(value)
        return LcdDemo.fit((value + value)[p:p + limit], limit)

    def lines(values):
        return (values + [""] * LcdDemo.rows)[:LcdDemo.rows]

    def canvas(fill=" "):
        return [[fill for _ in range(LcdDemo.wide)] for _ in range(LcdDemo.rows)]

    def put(g, x, y, ch):
        if 0 <= int(x) < LcdDemo.wide and 0 <= int(y) < LcdDemo.rows:
            g[int(y)][int(x)] = ch

    def line(g, x0, y0, x1, y1, ch="╱"):
        x0, y0, x1, y1 = map(int, (round(x0), round(y0), round(x1), round(y1)))
        dx, sx = abs(x1-x0), 1 if x0 < x1 else -1
        dy, sy = -abs(y1-y0), 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            LcdDemo.put(g, x0, y0, ch)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def as_text(g):
        return ["".join(row) for row in g]

    # All graphics are drawn directly into Lcd.raster. The LCD packs the
    # 64x20 (raster) or 64x16 (mixed) pixel buffer into Unicode Braille.
    def pixel_canvas(rows=None):
        lcd = LcdDemo.lcd
        if rows is None:
            lcd.set_mode(lcd.RASTER_MODE)
        else:
            lcd.set_mode(lcd.MIXED_MODE)
        # set_mode() normally hands control to the caller; during the built-in
        # demo we keep the animation enabled.
        lcd._demo_enabled = True
        lcd.clear()
        return lcd.raster

    def pixel_put(g, x, y):
        g.plot(x, y)

    def pixel_line(g, x0, y0, x1, y1):
        g.line(x0, y0, x1, y1)

    def pixel_circle(g, cx, cy, rx, ry, filled=False):
        g.circle(cx, cy, rx, ry, filled)

    def pixel_pack(g):
        return g.get()

    fire_heat = None
    fire_last_update = -100000

    def fire_scene():
        """Cellular-automata fire, refreshed at approximately 30 fps."""
        g = LcdDemo.pixel_canvas()
        h, w = g.height, g.width
        now = LcdDemo.now
        if (LcdDemo.fire_heat is None or
                now - LcdDemo.fire_last_update >= 33):
            heat = LcdDemo.fire_heat
            if heat is None:
                heat = [[0] * w for _ in range(h)]
            # Seed the bottom with a gently varying heat source.
            for x in range(w):
                heat[h - 1][x] = random.randint(5, 9)
                if h > 1:
                    heat[h - 2][x] = random.randint(4, 8)
            # Diffuse upward, retaining more heat than the fast version.
            new_heat = [row[:] for row in heat]
            for y in range(h - 3, -1, -1):
                for x in range(w):
                    samples = [heat[min(h - 1, y + 1)][max(0, min(w - 1, x + d))]
                               for d in (-1, 0, 1)]
                    new_heat[y][x] = max(0, sum(samples) // 3 - random.randint(0, 1))
            LcdDemo.fire_heat = new_heat
            LcdDemo.fire_last_update = now

        for y, row in enumerate(LcdDemo.fire_heat):
            for x, value in enumerate(row):
                if value >= 3:
                    g.plot(x, y)
        return LcdDemo.pixel_pack(g)

    def fireworks_scene():
        """Several looping pixel fireworks with rising sparks and expanding bursts."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        t = LcdDemo.now * .001
        # Deterministic bursts avoid flicker while still looking lively.
        for burst in range(5):
            age = (t * (0.62 + burst * .047) + burst * .73) % 2.8
            cx = w * (.16 + ((burst * 37) % 67) / 100.0)
            cy = h * (.22 + ((burst * 19) % 45) / 100.0)
            if age < .75:
                rise = age / .75
                x = cx + math.sin(t * 2.0 + burst) * 2
                y = h + 2 - rise * (h - cy)
                g.line(x, y + 2, x, y + 5)
                g.plot(x, y)
            else:
                phase = age - .75
                radius = 1.0 + phase * 8.0
                fade = max(0.0, 1.0 - phase / 1.9)
                count = 12
                for k in range(count):
                    angle = math.tau * k / count + burst * .31
                    dist = radius * (0.72 + .22 * math.sin(k * 4.1 + burst))
                    x = cx + math.cos(angle) * dist
                    y = cy + math.sin(angle) * dist * .55
                    if fade > .15 and 0 <= x < w and 0 <= y < h:
                        g.plot(x, y)
                    if fade > .58:
                        tx = cx + math.cos(angle) * max(0, dist - 1.5)
                        ty = cy + math.sin(angle) * max(0, dist - 1.5) * .55
                        g.line(tx, ty, x, y)
        return g.get()

    def starfield_scene():
        """Perspective starfield with expanding streaks."""
        import math
        g=LcdDemo.pixel_canvas(); h,w=len(g),len(g[0]); cx,cy=(w-1)/2,(h-1)/2
        t=LcdDemo.now*.001
        for i in range(max(32,w*2)):
            a=i*2.399963229728653
            z=((i*13.71+t*(.8+(i%7)*.17)*18)%100)/100
            r=.5+z*max(w,h*2)
            x,y=cx+math.cos(a)*r,cy+math.sin(a)*r*.48
            LcdDemo.pixel_put(g,x,y)
            if z>.78: LcdDemo.pixel_line(g,x-math.cos(a)*2,y-math.sin(a),x,y)
        return LcdDemo.pixel_pack(g)

    def geometry_scene():
        """Cube, torus and pyramid: grow, spin, then leave the screen."""
        g = LcdDemo.pixel_canvas()
        h, w = g.height, g.width
        phase = LcdDemo.phase
        shape_index = min(3, int(phase // 6.5))
        local = phase - shape_index * 6.5
        # 0..2.1s: grow from a point; 2.1..4.35s: several rotations;
        # final 2.15s: translate out of the frame in the requested direction.
        grow = min(1.0, max(0.0, local / 2.1))
        if local < 4.35:
            travel = 0.0
        else:
            travel = min(1.0, (local - 4.35) / 2.15)
        spin = local * 2.7

        vertices = []
        edges = []
        if shape_index == 0:  # Cube
            vertices = [(x, y, z) for z in (-1, 1)
                        for y in (-1, 1) for x in (-1, 1)]
            edges = [(0,1),(0,2),(0,4),(1,3),(1,5),(2,3),
                     (2,6),(3,7),(4,5),(4,6),(5,7),(6,7)]
            exit_x, exit_y = -1.45 * w, 0
        elif shape_index == 1:  # Torus mesh
            rings, sides = 8, 12
            for i in range(rings):
                u = math.tau * i / rings
                for j in range(sides):
                    v = math.tau * j / sides
                    radius = 0.62 + 0.30 * math.cos(v)
                    vertices.append((radius * math.cos(u),
                                     radius * math.sin(u),
                                     0.30 * math.sin(v)))
            for i in range(rings):
                for j in range(sides):
                    a = i * sides + j
                    edges.append((a, i * sides + (j + 1) % sides))
                    edges.append((a, ((i + 1) % rings) * sides + j))
            exit_x, exit_y = 1.45 * w, 0
        elif shape_index == 2:  # Square-based pyramid
            vertices = [(-1,-.8,-1),(1,-.8,-1),(1,-.8,1),(-1,-.8,1),
                        (0,1.25,0)]
            edges = [(0,1),(1,2),(2,3),(3,0),(0,4),(1,4),(2,4),(3,4)]
            exit_x, exit_y = 0, -1.5 * h
        else:  # Rotating heart with an extruded J; approaches and fades away.
            outline = []
            for k in range(40):
                a = math.tau * k / 40.0
                hx = 16 * math.sin(a)**3 / 17.0
                hy = -(13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a)) / 17.0
                outline.append((hx, hy, 0.0))
            vertices = outline + [(x, y, .42) for x, y, z in outline]
            for k in range(40):
                j = (k + 1) % 40
                edges.extend([(k, j), (k+40, j+40), (k, k+40)])
            # A simple J in the front plane, duplicated in depth.
            j_strokes = [[(0.48,.45,.46),(0.48,-.48,.46),(-.05,-.48,.46),(-.28,-.25,.46)],
                         [(.22,.45,.46),(.75,.45,.46)]]
            for stroke in j_strokes:
                ids=[]
                for x,y,z in stroke:
                    ids.append(len(vertices)); vertices.append((x,y,z))
                for a,b in zip(ids,ids[1:]): edges.append((a,b))
                back=[]
                for x,y,z in stroke:
                    back.append(len(vertices)); vertices.append((x,y,z+.16))
                for a,b in zip(back,back[1:]): edges.append((a,b))
                for a,b in zip(ids,back): edges.append((a,b))
            exit_x, exit_y = 0, 0

        ax, ay, az = spin * .73, spin * 1.0, spin * .47
        projected = []
        # Scale is chosen for a 64x20 pixel viewport, not a character grid.
        base = min(w * .43, h * 1.85)
        scale = base * grow
        shift_x, shift_y = exit_x * travel, exit_y * travel
        if shape_index == 3:
            # The heart rushes toward the viewer, enlarges, then vanishes.
            approach = min(1.0, max(0.0, local / 6.5))
            scale *= 1.0 + approach * 5.0
            fade_keep = max(0.0, 1.0 - max(0.0, approach - .58) / .42)
        else:
            fade_keep = 1.0
        for x, y, z in vertices:
            yy, zz = y*math.cos(ax)-z*math.sin(ax), y*math.sin(ax)+z*math.cos(ax)
            xx, zz = x*math.cos(ay)+zz*math.sin(ay), -x*math.sin(ay)+zz*math.cos(ay)
            xx, yy = xx*math.cos(az)-yy*math.sin(az), xx*math.sin(az)+yy*math.cos(az)
            depth = zz + 3.6
            px = w/2 + shift_x + (xx * scale * 2.0 / depth)
            py = h/2 + shift_y + (yy * scale * .88 / depth)
            projected.append((px, py))
        for edge_index, (a, b) in enumerate(edges):
            if shape_index == 3 and fade_keep < 1.0:
                # Ordered stipple removal simulates a pixel fade on monochrome LCD.
                threshold = int(fade_keep * 8)
                if (edge_index * 5 + int(local * 17)) % 8 >= threshold:
                    continue
            g.line(projected[a][0], projected[a][1],
                   projected[b][0], projected[b][1])
        # A point at the beginning is deliberately visible before the mesh grows.
        if grow < .08:
            g.plot(w/2 + shift_x, h/2 + shift_y)
        return g.get()

    def pong_scene():
        """Compact animated Pong match, rasterized at full subpixel resolution."""
        g = LcdDemo.pixel_canvas()
        h, w = g.height, g.width
        t = LcdDemo.now * 0.001

        # Dotted centre line.
        for y in range(0, h, 2):
            LcdDemo.pixel_put(g, w // 2, y)

        # Two paddles, kept inside the screen.
        paddle_h = max(3, h // 3)
        left_y = int((h - paddle_h) * (0.5 + 0.34 * math.sin(t * 1.7)))
        right_y = int((h - paddle_h) * (0.5 + 0.34 * math.sin(t * 1.7 + 2.0)))
        for dy in range(paddle_h):
            LcdDemo.pixel_put(g, 1, left_y + dy)
            LcdDemo.pixel_put(g, 2, left_y + dy)
            LcdDemo.pixel_put(g, w - 3, right_y + dy)
            LcdDemo.pixel_put(g, w - 2, right_y + dy)

        # Ball follows a reflected, deterministic trajectory.
        bx = (t * 10.5) % (2 * (w - 6))
        if bx > w - 6:
            bx = 2 * (w - 6) - bx
        bx += 3
        by = h * 0.5 + math.sin(t * 2.35) * h * 0.34
        LcdDemo.pixel_circle(g, bx, by, 1.15, 1.15, True)
        return LcdDemo.pixel_pack(g)

    def vu_vertical_scene():
        """Two stereo level bars with a V-shaped peak pointer above each."""
        g = LcdDemo.pixel_canvas(max(1, LcdDemo.rows - 1))
        w, h = g.width, g.height
        t = LcdDemo.now * .001
        for channel, cy in enumerate((h * .30, h * .78)):
            level = .18 + .78 * (.5 + .5 * math.sin(t * 2.7 + channel * 1.15))
            extent = max(2, min(w - 3, int(level * (w - 2))))
            y = int(cy)
            for x in range(1, w - 1):
                g.plot(x, y)
            for x in range(1, extent + 1):
                for yy in (y-1, y, y+1):
                    g.plot(x, yy)
            for x in range(max(1, w - 9), w - 1, 2):
                for yy in (y-1, y, y+1):
                    g.plot(x, yy)
            tip = min(w - 2, extent)
            vy = max(0, y - 3)
            g.line(tip - 1, vy, tip, vy + 1)
            g.line(tip, vy + 1, tip + 1, vy)
        return LcdDemo.pixel_pack(g)


    def vu_horizontal_scene():
        """Two compact analogue needle meters, left and right."""
        g = LcdDemo.pixel_canvas(max(1, LcdDemo.rows - 1))
        w, h = g.width, g.height
        t = LcdDemo.now * .001
        bands = ((0, h//2-1), (h//2, h-1))
        for channel, (top, bottom) in enumerate(bands):
            cx, cy = w * .5, bottom - .5
            rx = w * .34
            ry = max(2.0, (bottom-top) * .82)
            for step in range(25):
                a = math.pi + math.pi * step / 24.0
                px, py = cx + math.cos(a)*rx, cy + math.sin(a)*ry
                if step % 4 == 0:
                    g.line(cx + math.cos(a)*rx*.88, cy + math.sin(a)*ry*.88, px, py)
                else:
                    g.plot(px, py)
            value = .5 + .43 * math.sin(t * 2.1 + channel * 1.4)
            angle = math.pi + (1.0-value) * math.pi
            g.line(cx, cy, cx + math.cos(angle)*rx*.82,
                   cy + math.sin(angle)*ry*.82)
            g.plot(cx, cy)
        return LcdDemo.pixel_pack(g)


    def vu_12_scene():
        """Twelve animated EMX-style channels: six drum parts and six synth parts."""
        g = LcdDemo.pixel_canvas(max(1, LcdDemo.rows - 1))
        w, h = g.width, g.height
        t = LcdDemo.now * 0.001
        count = 12
        margin = 2
        gap = 1
        usable = w - margin * 2 - gap * 11 - 1
        bar_w = max(2, usable // count)
        for channel in range(count):
            group_offset = 1 if channel >= 6 else 0
            x0 = margin + channel * (bar_w + gap) + group_offset
            x1 = min(w - 1, x0 + bar_w - 2)
            # Drums have punchier envelopes; synth parts have smoother motion.
            if channel < 6:
                pulse = max(0.12, math.sin(t * (3.4 + channel * .12) + channel * 1.8) ** 8)
                level = 0.12 + 0.86 * pulse
            else:
                level = 0.20 + 0.70 * (0.5 + 0.5 * math.sin(t * (1.7 + channel * .07) + channel * .92))
            bar_h = max(1, int(level * (h - 2)))
            # A two-pixel footprint with a clear empty gap between channels.
            for x in range(x0, max(x0 + 1, x1 + 1)):
                for y in range(h - 1, h - 1 - bar_h, -1):
                    g.plot(x, y)
            # Peak dot floats just above each active column.
            peak_y = max(0, h - 2 - bar_h)
            g.plot(x0, peak_y)
            # Midpoint separator divides the six drum parts from six synths.
            if channel == 5:
                sep = min(w - 1, x1 + 1)
                for y in range(h):
                    if y % 2 == 0:
                        g.plot(sep, y)
        return g.get()

    # Sixteen mapped step velocities (MIDI range 0..127). A sequencer can
    # replace this list at runtime with its own mapped values.
    velocity_steps = [112, 76, 98, 42, 120, 64, 88, 24,
                      104, 56, 126, 72, 36, 92, 60, 116]

    def velocity_scene():
        """Sixteen velocity columns: 2 pixels wide x 8 pixels high."""
        values = list(LcdDemo.velocity_steps[:16])
        values += [0] * (16 - len(values))
        g = LcdDemo.pixel_canvas(max(1, LcdDemo.rows - 1))
        h, w = g.height, g.width
        bar_width = max(1, w // 16)
        for step, velocity in enumerate(values):
            velocity = max(0, min(127, int(velocity)))
            bar_height = int(round((velocity / 127.0) * h))
            x0 = step * bar_width
            x1 = min(w, x0 + bar_width)
            for y in range(h - bar_height, h):
                for x in range(x0, x1):
                    g.plot(x, y)
        return g.get()

    def waveform_scene():
        """Oscilloscope waveform in the four-row mixed-mode display area."""
        import math
        g=LcdDemo.pixel_canvas(max(1, LcdDemo.rows - 1)); h,w=len(g),len(g[0]); mid=(h-1)/2; amp=max(.7,h*.46); prev=None
        t=LcdDemo.now*.001
        for x in range(w):
            p=x/max(1,w-1)*math.tau*2
            s=(math.sin(p+t*2.8)+.34*math.sin(2*p-t*1.7)+.16*math.sin(5*p+t*.8))
            s*=.66+.34*math.sin(t*.7+p*.18); y=mid-s*amp
            if prev is not None: LcdDemo.pixel_line(g,x-1,prev,x,y)
            LcdDemo.pixel_put(g,x,y); prev=y
        return LcdDemo.pixel_pack(g)

    def sample_scene():
        """Folded sample waveform with a moving playback scanline and sample label."""
        g = LcdDemo.pixel_canvas(rows=4)
        w, h = g.width, g.height
        t = LcdDemo.now * .001
        mid = h * .50
        amp = h * .43
        previous = None
        for x in range(w):
            p = x / float(max(1, w - 1))
            # Folded/rectified audio: one averaged half-wave envelope.
            wave = abs(math.sin(p * math.pi * 2.0 + .18 * math.sin(t * .7)))
            detail = .72 + .28 * abs(math.sin(p * math.pi * 13.0 + t * .8))
            y = mid - wave * detail * amp
            if previous is not None:
                g.line(x - 1, previous, x, y)
            previous = y
        play_x = int((t * 13.0) % w)
        g.line(play_x, 0, play_x, h - 1)
        lcd = LcdDemo.lcd
        # Mixed mode reserves the last text row below the raster for the sample name.
        if hasattr(lcd, "set_line"):
            lcd.set_line(3, "909_KICK_01.WAV")
        lcd._demo_enabled = True
        return g.get()


    def image_scene():
        """A happy face travelling around the LCD with a smooth bouncing path."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        t = LcdDemo.now * 0.001
        # The face itself stays stable; only the eyes blink at irregular intervals.
        ink = 1
        g.clear(0)
        if not hasattr(LcdDemo, "smile_blink_until"):
            LcdDemo.smile_blink_until = 0.0
            LcdDemo.smile_next_blink = t + 1.1
            LcdDemo.smile_flash_until = 0.0
            LcdDemo.smile_next_flash = t + 2.0
            LcdDemo.smile_shake = (0.0, 0.0)
        if t >= LcdDemo.smile_next_blink:
            LcdDemo.smile_blink_until = t + random.uniform(.07, .16)
            LcdDemo.smile_next_blink = t + random.uniform(1.2, 3.8)
        if t >= LcdDemo.smile_next_flash:
            LcdDemo.smile_flash_until = t + random.uniform(.045, .11)
            LcdDemo.smile_next_flash = t + random.uniform(1.0, 4.2)
        blinking = t < LcdDemo.smile_blink_until
        flashing = t < LcdDemo.smile_flash_until
        if int(t * 24) != getattr(LcdDemo, "smile_shake_tick", -1):
            LcdDemo.smile_shake_tick = int(t * 24)
            LcdDemo.smile_shake = (random.uniform(-1.7, 1.7), random.uniform(-1.3, 1.3))

        radius = max(3.0, min(w * 0.19, h * 0.40))
        # Two incommensurate waves plus random jitter make the face roam and vibrate.
        sx, sy = LcdDemo.smile_shake
        cx = radius + (w - 2 * radius) * (0.5 + 0.5 * math.sin(t * 0.83)) + sx
        cy = radius + (h - 2 * radius) * (0.5 + 0.5 * math.sin(t * 1.17 + 1.2)) + sy
        if flashing:
            # Full-screen inverse-video flash with a jagged lightning bolt
            # cut out as a dark silhouette.
            for yy in range(h):
                for xx in range(w):
                    g.plot(xx, yy)
            bolt = [(cx + radius*.18, cy-radius*.92),
                    (cx-radius*.18, cy-radius*.12),
                    (cx+radius*.12, cy-radius*.12),
                    (cx-radius*.28, cy+radius*.88)]
            for a, b in zip(bolt, bolt[1:]):
                # Bright alternating pixels make the bolt legible in the flash.
                g.line(round(a[0]), round(a[1]), round(b[0]), round(b[1]), value=0)
            return g.get()
        inverted = (int(t * 7.0) % 2) == 1
        if inverted:
            # Negative-video frame: light field around a dark circular face.
            for yy in range(h):
                for xx in range(w):
                    inside_face = (xx-cx)**2 + (yy-cy)**2 <= radius*radius
                    if not inside_face and (xx + yy) % 2 == 0:
                        g.plot(xx, yy)
        # On inverse frames, the face interior remains dark while its outline
        # and expression are lit, like a true negative-video insert.
        g.circle(cx, cy, radius, radius, value=ink)

        eye_dx = radius * 0.38
        eye_top = cy - radius * 0.35
        eye_bottom = cy + radius * 0.02
        for ex in (cx - eye_dx, cx + eye_dx):
            if blinking:
                g.line(round(ex - 1), round(cy - radius * .18), round(ex + 1), round(cy - radius * .18), value=ink)
            else:
                g.line(round(ex), round(eye_top), round(ex), round(eye_bottom), value=ink)

        smile_points = [
            (cx - radius * 0.48, cy + radius * 0.18),
            (cx - radius * 0.28, cy + radius * 0.39),
            (cx,                  cy + radius * 0.46),
            (cx + radius * 0.28, cy + radius * 0.39),
            (cx + radius * 0.48, cy + radius * 0.18),
        ]
        for a, b in zip(smile_points, smile_points[1:]):
            g.line(round(a[0]), round(a[1]), round(b[0]), round(b[1]), value=ink)
        return g.get()

    # Compact 3x5 bitmap font for the full-width pixel text scroller.
    PIXEL_FONT = {
        "A":("010","101","111","101","101"), "B":("110","101","110","101","110"),
        "C":("011","100","100","100","011"), "D":("110","101","101","101","110"),
        "E":("111","100","110","100","111"), "F":("111","100","110","100","100"),
        "G":("011","100","101","101","011"), "H":("101","101","111","101","101"),
        "I":("111","010","010","010","111"), "J":("001","001","001","101","010"),
        "K":("101","101","110","101","101"), "L":("100","100","100","100","111"),
        "M":("101","111","111","101","101"), "N":("101","111","111","111","101"),
        "O":("010","101","101","101","010"), "P":("110","101","110","100","100"),
        "Q":("010","101","101","111","011"), "R":("110","101","110","101","101"),
        "S":("011","100","010","001","110"), "T":("111","010","010","010","010"),
        "U":("101","101","101","101","111"), "V":("101","101","101","101","010"),
        "W":("101","101","111","111","101"), "X":("101","101","010","101","101"),
        "Y":("101","101","010","010","010"), "Z":("111","001","010","100","111"),
        "0":("111","101","101","101","111"), "1":("010","110","010","010","111"),
        "2":("110","001","010","100","111"), "3":("110","001","010","001","110"),
        "4":("101","101","111","001","001"), "5":("111","100","110","001","110"),
        "6":("011","100","110","101","010"), "7":("111","001","010","010","010"),
        "8":("010","101","010","101","010"), "9":("010","101","011","001","110"),
        "/":("001","001","010","100","100"), "-":("000","000","111","000","000"),
        ".":("000","000","000","000","010"), ":":("000","010","000","010","000"),
        " ":("000","000","000","000","000")
    }

    def big_text_scene():
        """Bumping bitmap text: each letter has its own 3D sine motion."""
        g = LcdDemo.pixel_canvas()
        message = "  PIXEL POWER / LCD DEMO / 64X20  "
        glyphs = [LcdDemo.PIXEL_FONT.get(ch, LcdDemo.PIXEL_FONT[" "])
                  for ch in message]
        t = LcdDemo.now * 0.001
        base_advance = 4.0
        total_width = len(glyphs) * base_advance
        travel = (t * 7.0) % (total_width + g.width)
        cursor = g.width - travel

        for index, glyph in enumerate(glyphs):
            # Independent vertical bob, depth/size breathing and lateral wobble.
            phase = t * 2.0 + index * 0.73
            scale = 0.58 + 0.92 * (0.5 + 0.5 * math.sin(phase * 0.82))
            y_shift = math.sin(phase * 1.31) * max(1.0, g.height * 0.17)
            x_shift = math.sin(phase * 0.91 + 0.6) * 1.8
            x0 = cursor + x_shift
            glyph_h = 5.0 * scale
            top = (g.height - glyph_h) / 2.0 + y_shift

            for gy, row in enumerate(glyph):
                for gx, bit in enumerate(row):
                    if bit != "1":
                        continue
                    left = int(math.floor(x0 + gx * scale))
                    right = int(math.ceil(x0 + (gx + 1) * scale))
                    upper = int(math.floor(top + gy * scale))
                    lower = int(math.ceil(top + (gy + 1) * scale))
                    for py in range(upper, lower):
                        for px in range(left, right):
                            g.plot(px, py)
            cursor += base_advance
        return g.get()

    def piano_roll_scene():
        """Piano roll with mirrored keyboard at the left edge and blinking selected note."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        keyboard_w = max(16, w // 4)
        grid_w = w - keyboard_w
        # Semitone order from low C upwards; black keys are C#, D#, F#, G#, A#.
        lane_h = h / 12.0
        black_notes = {1, 3, 6, 8, 10}
        # White keys: bright outlined key faces with clear separating grooves.
        for n in range(12):
            if n in black_notes:
                continue
            y0 = int(round(n * lane_h))
            y1 = min(h - 1, max(y0, int(round((n + 1) * lane_h)) - 1))
            for x in range(keyboard_w):
                for y in range(y0, y1 + 1):
                    if x == keyboard_w - 1 or y in (y0, y1):
                        g.plot(x, y)
        # Black keys are raised, solid blocks, anchored to column zero (mirrored layout).
        black_w = max(7, int(keyboard_w * .58))
        for n in black_notes:
            y0 = int(round(n * lane_h))
            y1 = min(h - 1, max(y0, int(round((n + 1) * lane_h)) - 1))
            for y in range(y0, y1 + 1):
                for x in range(black_w):
                    g.plot(x, y)
            # Short raised-key front lip.
            if y1 >= 0:
                for x in range(black_w):
                    g.plot(x, y1)
        # Subtle measure divisions.
        for bar in range(1, 4):
            x = keyboard_w + int(round(bar * grid_w / 4.0))
            for y in range(h):
                if y % 3 == 0:
                    g.plot(x, y)
        notes = [(0,7,3),(0,4,2),(2,9,2),(3,6,2),(4,10,3),(5,2,2),
                 (7,7,2),(8,3,3),(9,8,2),(10,5,2),(12,11,2),(13,4,2),(14,9,2)]
        step_w = grid_w / 16.0
        selected = (int(LcdDemo.phase * 1.2) % len(notes))
        for ni, (step, pitch, length) in enumerate(notes):
            x0 = keyboard_w + int(round(step * step_w)) + 1
            x1 = min(w - 1, keyboard_w + int(round((step + length) * step_w)) - 1)
            y0 = int(round((11 - pitch) * lane_h))
            y1 = min(h - 1, int(round((12 - pitch) * lane_h)) - 1)
            visible = ni != selected or (int(LcdDemo.now / 180) % 2 == 0)
            if visible:
                for y in range(y0, y1 + 1):
                    for x in range(x0, x1 + 1):
                        g.plot(x, y)
        playhead = keyboard_w + int(round((int(LcdDemo.phase * 2) % 16) * step_w))
        for y in range(h):
            g.plot(playhead, y)
        return g.get()

    def eq_scene():
        """Eight clear EQ handles connected by one editable-looking curve."""
        g = LcdDemo.pixel_canvas(max(1, LcdDemo.rows - 1))
        w, h = g.width, g.height
        t = LcdDemo.now * 0.001
        count = 8
        baseline = h // 2
        centers = [int(round(i * (w - 1) / float(count - 1))) for i in range(count)]
        gains = [0.48 * math.sin(t * 0.42 + i * 0.91) for i in range(count)]
        points = []
        for i, x in enumerate(centers):
            y = max(1, min(h - 2, int(round(baseline - gains[i] * (h * 0.72)))))
            points.append((x, y))

        # A single continuous response line joins all eight control points.
        for a, b in zip(points, points[1:]):
            g.line(a[0], a[1], b[0], b[1])
        # Larger, hollow handles make the eight editable bands unambiguous.
        for x, y in points:
            g.circle(x, y, 1.35, 1.35, filled=False)
            g.plot(x, y)

        lcd = LcdDemo.lcd
        lcd.set_functions("F1:Select", "F2:Gain", "F3:Freq")
        lcd._demo_enabled = True
        return g.get()

    def file_browser_scene():
        """Minimal file browser: one compact path row and four entries."""
        lcd = LcdDemo.lcd
        files = [
            ("..", "<DIR>"),
            ("01_CLASSIC.PAT", "PAT"),
            ("02_ACID.PAT", "PAT"),
            ("909_KICK.WAV", "WAV"),
            ("BASS_303.WAV", "WAV"),
            ("LEAD_SYNC.WAV", "WAV"),
            ("FACTORY.SET", "SET"),
        ]
        selected = int(LcdDemo.phase * 0.55) % len(files)
        top = max(0, min(len(files) - 4, selected - 1))
        # Only one narrow-font row is reserved for the current path.
        rows = [LcdDemo.fit("/EBIRTRIBE/USER/PATTERNS", 32)]
        for row in range(4):
            index = top + row
            if index < len(files):
                name, kind = files[index]
                marker = ">" if index == selected else " "
                rows.append(LcdDemo.fit("{}{:<22} {:>4}".format(
                    marker, name[:22], kind), 32))
            else:
                rows.append(" " * 32)
        lcd.buffer = rows[:5]
        return rows[:5]

    def keyboard_scene():
        """Spanish virtual keyboard; fixed 32-column layout with a dedicated space key slot."""
        lcd = LcdDemo.lcd
        upper = ["  A B C Ç D E F G H I J K L M  ",
                 "  Ñ N O P Q R S T U V W X Y Z  ",
                 "  0 1 2 3 4 5 6 7 8 9 , ; #    "]
        lower = ["  a b ç c d e f g h i j k l m  ",
                 "  ñ n o p q r s t u v w x y z  ",
                 "  ? ! ( ) [ ] { } - _ . : &    "]
        is_lower = int(LcdDemo.phase / 7.0) % 2 == 1
        rows = lower if is_lower else upper
        rows = [line[:32].ljust(32) for line in rows]
        # The first trailing blank in row three is the dedicated SPACE key.
        slots = [(r, c) for r, line in enumerate(rows) for c, ch in enumerate(line)
                 if ch != " " or (r == 2 and c == 31)]
        cursor_index = int(LcdDemo.phase * 1.25) % len(slots)
        cursor_row, cursor_col = slots[cursor_index]
        rendered = []
        block_phase = (int(LcdDemo.now / 210) % 2) == 0
        for r, line in enumerate(rows):
            chars = list(line)
            if r == cursor_row:
                key = chars[cursor_col]
                chars[cursor_col] = "█" if block_phase else key
            rendered.append("".join(chars))
        count = int(LcdDemo.phase * .55)
        pool = "".join(ch for line in rows for ch in line if ch != " ")
        typed = "".join(pool[(i * 7 + 4) % len(pool)] for i in range(count % 18))
        entered = (">" + typed + "▐")[:32].ljust(32)
        footer = "[F1:Insert][F2:Erase][F3:{}]".format("Upper" if is_lower else "Lower")
        lcd.buffer = [*rendered, entered, LcdDemo.fit(footer, 32)]
        return lcd.buffer

    def cassette_scene():
        """Large edge-to-edge cassette with animated reels and sampling status."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        t = LcdDemo.now * 0.001
        # The shell nearly fills the raster, leaving only a narrow outer margin.
        left, right = w * 0.025, w * 0.975
        top, bottom = h * 0.035, h * 0.965
        g.line(left, top, right, top)
        g.line(right, top, right, bottom)
        g.line(right, bottom, left, bottom)
        g.line(left, bottom, left, top)
        # Broad label panel across the upper third.
        g.line(w * .09, h * .12, w * .91, h * .12)
        g.line(w * .09, h * .12, w * .09, h * .34)
        g.line(w * .91, h * .12, w * .91, h * .34)
        g.line(w * .09, h * .34, w * .91, h * .34)
        # Large reel wells and hubs.
        reel_y = h * .57
        reel_rx = w * .205
        reel_ry = h * .30
        angle = t * 5.0
        for cx, direction in ((w * .29, 1.0), (w * .71, -1.0)):
            g.circle(cx, reel_y, reel_rx, reel_ry)
            g.circle(cx, reel_y, reel_rx * .72, reel_ry * .72)
            g.circle(cx, reel_y, max(1.5, reel_rx * .20), max(1.5, reel_ry * .20))
            for spoke in range(3):
                a = angle * direction + spoke * math.tau / 3.0
                x1 = cx + math.cos(a) * reel_rx * .88
                y1 = reel_y + math.sin(a) * reel_ry * .88
                g.line(cx, reel_y, x1, y1)
        # Tape path spans almost the entire width of the cassette.
        tape_y = h * .57 + math.sin(angle) * h * .035
        g.line(w * .29 + reel_rx * .82, tape_y,
               w * .71 - reel_rx * .82, h * .57 - math.sin(angle) * h * .035)
        # Lower tape head / guide assembly.
        g.line(w * .22, h * .91, w * .78, h * .91)
        g.line(w * .32, h * .91, w * .39, h * .78)
        g.line(w * .68, h * .91, w * .61, h * .78)

        # Recording-time feedback: a capacity bar and a live remaining-time
        # readout inside the cassette label. The demo models two minutes free.
        remaining = max(0, 120 - int(LcdDemo.phase * 2.0))
        minutes, seconds = divmod(remaining, 60)
        bar_left, bar_right = w * .20, w * .80
        bar_y = h * .235
        g.line(bar_left, bar_y - 2, bar_right, bar_y - 2)
        g.line(bar_left, bar_y + 2, bar_right, bar_y + 2)
        g.line(bar_left, bar_y - 2, bar_left, bar_y + 2)
        g.line(bar_right, bar_y - 2, bar_right, bar_y + 2)
        available = remaining / 120.0
        fill_right = bar_left + (bar_right - bar_left) * available
        g.line(bar_left + 1, bar_y, fill_right, bar_y)
        # Small ticks make the remaining capacity legible as a meter.
        for tick in range(1, 10):
            tx = bar_left + (bar_right - bar_left) * tick / 10.0
            g.line(tx, bar_y - 1, tx, bar_y + 1)

        lcd = LcdDemo.lcd
        lcd.set_functions("SAMPLING", "LEFT {:01d}:{:02d}".format(minutes, seconds), "EMX-1")
        lcd._demo_enabled = True
        return g.get()

    def metaballs_scene():
        """Organic metaballs merging and separating in a monochrome field."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        t = LcdDemo.now * .001
        balls = [
            (w * (.25 + .12 * math.sin(t * 1.12)), h * (.38 + .18 * math.sin(t * 1.52)), .12),
            (w * (.53 + .16 * math.sin(t * 1.23 + 1.7)), h * (.55 + .17 * math.cos(t * 1.23)), .15),
            (w * (.77 + .10 * math.cos(t * .98)), h * (.38 + .20 * math.sin(t * 1.72 + 2.0)), .11),
            (w * (.43 + .20 * math.cos(t * .70 + 2.4)), h * (.76 + .10 * math.sin(t * 1.07)), .09),
        ]
        # Evaluate the implicit field at every raster pixel; thresholding creates
        # the characteristic smooth necks where neighboring blobs merge.
        for y in range(h):
            for x in range(w):
                field = 0.0
                for bx, by, radius in balls:
                    dx = (x - bx) / max(1.0, w * radius)
                    dy = (y - by) / max(1.0, h * radius * 1.8)
                    field += 1.0 / (dx * dx + dy * dy + .035)
                if field > 1.05:
                    g.plot(x, y)
        return g.get()

    tetris_board = None
    tetris_piece = None
    tetris_last_drop = -100000
    tetris_piece_index = 0
    tetris_last_lateral = -100000

    def tetris_scene():
        """Full-screen Tetris rotated 90 degrees: pieces travel left to right."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        depth, lanes = 32, 10
        cell_w, cell_h = max(1, w // depth), max(1, h // lanes)
        if (LcdDemo.tetris_board is None or len(LcdDemo.tetris_board) != lanes or
                not getattr(LcdDemo, "tetris_rotated", False)):
            LcdDemo.tetris_rotated = True
            LcdDemo.tetris_board = [[0 for _ in range(depth)] for _ in range(lanes)]
            LcdDemo.tetris_piece = None
            LcdDemo.tetris_last_drop = -100000
            LcdDemo.tetris_piece_index = 0
            LcdDemo.tetris_last_lateral = -100000
        shapes = [
            [(0,0),(1,0),(2,0),(3,0)], [(0,0),(1,0),(0,1),(1,1)],
            [(1,0),(0,1),(1,1),(2,1)], [(0,0),(0,1),(0,2),(1,2)],
            [(1,0),(1,1),(0,2),(1,2)], [(0,0),(1,0),(1,1),(2,1)],
            [(1,0),(2,0),(0,1),(1,1)]
        ]
        now = LcdDemo.now
        if LcdDemo.tetris_piece is None:
            shape = shapes[LcdDemo.tetris_piece_index % len(shapes)]
            LcdDemo.tetris_piece_index += 1
            # Random quarter-turns, normalized to a non-negative local box.
            turns = random.randrange(4)
            cells = shape[:]
            for _ in range(turns):
                cells = [(-dy, dx) for dx, dy in cells]
            min_x = min(x for x, y in cells); min_y = min(y for x, y in cells)
            cells = [(x-min_x, y-min_y) for x, y in cells]
            max_y = max(y for x, y in cells)
            lane_start = random.randrange(max(1, lanes-max_y))
            LcdDemo.tetris_piece = {'cells': cells, 'x': 0, 'y': lane_start}
        piece = LcdDemo.tetris_piece
        def collides(px, py):
            for dx, dy in piece['cells']:
                x, y = px + dx, py + dy
                if x < 0 or x >= depth or y < 0 or y >= lanes:
                    return True
                if LcdDemo.tetris_board[y][x]:
                    return True
            return False
        # Random sideways nudges keep the pieces moving across the lanes.
        if now - LcdDemo.tetris_last_lateral >= 95:
            LcdDemo.tetris_last_lateral = now
            lateral = random.choice([-2, -1, 1, 2])
            if not collides(piece['x'], max(0, min(lanes-1, piece['y'] + lateral))):
                piece['y'] = max(0, min(lanes-1, piece['y'] + lateral))
        if now - LcdDemo.tetris_last_drop >= 115:
            LcdDemo.tetris_last_drop = now
            piece['x'] += 1
            if collides(piece['x'], piece['y']):
                piece['x'] -= 1
                for dx, dy in piece['cells']:
                    x, y = piece['x'] + dx, piece['y'] + dy
                    if 0 <= y < lanes and 0 <= x < depth:
                        LcdDemo.tetris_board[y][x] = 1
                # Clear a completed vertical lane, then shift remaining lanes.
                full = [x for x in range(depth)
                        if all(LcdDemo.tetris_board[y][x] for y in range(lanes))]
                for x in reversed(full):
                    for row in LcdDemo.tetris_board:
                        del row[x]
                        row.insert(0, 0)
                LcdDemo.tetris_piece = None
        for y in range(lanes):
            for x in range(depth):
                filled = LcdDemo.tetris_board[y][x]
                if LcdDemo.tetris_piece is not None:
                    q = LcdDemo.tetris_piece
                    if any((x, y) == (q['x']+dx, q['y']+dy) for dx,dy in q['cells']):
                        filled = 1
                if filled:
                    for py in range(y*cell_h, min(h, (y+1)*cell_h)):
                        for px in range(x*cell_w, min(w, (x+1)*cell_w)):
                            g.plot(px, py)
        return g.get()


    snake_body = None
    snake_direction = (1, 0)
    snake_food = None
    snake_last_step = -100000

    def snake_scene():
        """Self-playing Snake with a growing body and animated food target."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        cols, rows = max(12, w // 2), max(8, h)
        now = LcdDemo.now
        if LcdDemo.snake_body is None:
            LcdDemo.snake_body = [(cols // 3 - i, rows // 2) for i in range(5)]
            LcdDemo.snake_direction = (1, 0)
            LcdDemo.snake_food = (cols * 2 // 3, rows // 2)
            LcdDemo.snake_last_step = -100000
        if now - LcdDemo.snake_last_step >= 36:
            LcdDemo.snake_last_step = now
            body = LcdDemo.snake_body
            head_x, head_y = body[0]
            fx, fy = LcdDemo.snake_food
            # Greedy but collision-aware steering keeps the demo alive on screen.
            candidates = [(1,0),(0,1),(-1,0),(0,-1)]
            candidates.sort(key=lambda d: abs((head_x+d[0])-fx) + abs((head_y+d[1])-fy))
            chosen = None
            for direction in candidates:
                nx, ny = head_x + direction[0], head_y + direction[1]
                if nx < 1 or nx >= cols-1 or ny < 1 or ny >= rows-1:
                    continue
                if (nx, ny) in body[:-1]:
                    continue
                chosen = direction
                break
            if chosen is None:
                # Reset cleanly if it has boxed itself in.
                LcdDemo.snake_body = [(cols // 3 - i, rows // 2) for i in range(5)]
                chosen = (1, 0)
            LcdDemo.snake_direction = chosen
            nx, ny = head_x + chosen[0], head_y + chosen[1]
            new_body = [(nx, ny)] + body
            if (nx, ny) == LcdDemo.snake_food:
                LcdDemo.snake_food = (random.randrange(2, cols-2), random.randrange(2, rows-2))
            else:
                new_body.pop()
            LcdDemo.snake_body = new_body
        # No frame: the entire raster is the playground.
        fx, fy = LcdDemo.snake_food
        g.circle(fx * 2, fy, 1.1, 1.0, filled=True)
        for index, (x, y) in enumerate(LcdDemo.snake_body):
            px = min(w-1, x * 2)
            if index == 0:
                g.circle(px, y, 1.4, 1.0, filled=True)
            else:
                g.plot(px, y)
                if px + 1 < w: g.plot(px + 1, y)
        return g.get()

    snow_particles = []
    snow_pile = None
    snow_last_update = -100000

    def snow_scene():
        """Snow collides with actual EMX glyph pixels, rolls off edges and piles on ground."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        now = LcdDemo.now
        label, scale, advance = "EMX-1", 2, 8
        start_x = (w - (len(label) * advance - 2)) // 2
        logo_top = h - 10
        logo_pixels = set()
        for index, ch in enumerate(label):
            glyph = LcdDemo.PIXEL_FONT.get(ch, LcdDemo.PIXEL_FONT[" "])
            for gy, row in enumerate(glyph):
                for gx, bit in enumerate(row):
                    if bit == "1":
                        for sy in range(scale):
                            for sx in range(scale):
                                xx = start_x + index*advance + gx*scale + sx
                                yy = logo_top + gy*scale + sy
                                if 0 <= xx < w and 0 <= yy < h:
                                    logo_pixels.add((xx, yy))
        if LcdDemo.snow_pile is None or len(LcdDemo.snow_pile) != w:
            LcdDemo.snow_pile = [0] * w
            LcdDemo.snow_particles = []
            LcdDemo.snow_rest = []
            LcdDemo.snow_last_update = -100000

        if now - LcdDemo.snow_last_update >= 45:
            LcdDemo.snow_last_update = now
            for _ in range(max(1, w // 22)):
                LcdDemo.snow_particles.append([
                    random.randrange(w), random.uniform(-2, 1),
                    random.uniform(.45, 1.05), random.uniform(-.45, .45)])
            remaining = []
            for particle in LcdDemo.snow_particles:
                particle[1] += particle[2]
                particle[0] += particle[3] + math.sin(now*.004 + particle[1])*.18
                x, y = int(round(particle[0])), int(round(particle[1]))
                if not (0 <= x < w):
                    continue
                if y < 0:
                    remaining.append(particle)
                    continue
                if y >= h:
                    LcdDemo.snow_pile[x] = min(h, LcdDemo.snow_pile[x] + 1)
                    continue

                # A flake only hits a letter where a real lit pixel exists.
                if (x, y) in logo_pixels:
                    direction = random.choice((-1, 1))
                    rolled_x = max(0, min(w-1, x + direction))
                    # Roll along the letter edge; if blocked, leave a tiny cap of snow.
                    if ((rolled_x, y) not in logo_pixels and
                            (rolled_x, min(h-1, y+1)) not in logo_pixels):
                        particle[0] = rolled_x
                        particle[1] += .7
                        remaining.append(particle)
                    else:
                        LcdDemo.snow_rest.append((x, max(0, y-1)))
                    continue

                # Snow below the logo continues falling until it reaches the floor pile.
                ground_y = h - 1 - LcdDemo.snow_pile[x]
                if y >= ground_y:
                    LcdDemo.snow_pile[x] = min(h, LcdDemo.snow_pile[x] + 1)
                    continue
                remaining.append(particle)
            LcdDemo.snow_particles = remaining
            # Granular settling: move over-tall columns into the lower neighbor,
            # producing a continuous, gently sloped snowbank rather than spikes.
            for _ in range(2):
                for sx in range(1, w - 1):
                    left_h = LcdDemo.snow_pile[sx - 1]
                    here_h = LcdDemo.snow_pile[sx]
                    right_h = LcdDemo.snow_pile[sx + 1]
                    target = sx - 1 if left_h <= right_h else sx + 1
                    if here_h > LcdDemo.snow_pile[target] + 1:
                        LcdDemo.snow_pile[sx] -= 1
                        LcdDemo.snow_pile[target] += 1
            if len(LcdDemo.snow_rest) > 180:
                LcdDemo.snow_rest = LcdDemo.snow_rest[-180:]

        # Ground accumulation.
        for x, depth in enumerate(LcdDemo.snow_pile):
            for dy in range(depth):
                yy = h - 1 - dy
                if 0 <= yy < h:
                    g.plot(x, yy)
        # Small caps resting on the letters.
        for x, y in getattr(LcdDemo, "snow_rest", []):
            g.plot(x, y)
        # Falling flakes are drawn last.
        for x, y, speed, drift in LcdDemo.snow_particles:
            if 0 <= int(round(x)) < w and 0 <= int(round(y)) < h:
                g.plot(int(round(x)), int(round(y)))
        for x, y in logo_pixels:
            g.plot(x, y)
        return g.get()


    def fractal_scene():
        """Classic Mandelbrot set with a continuous, looping deep zoom."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        t = LcdDemo.phase
        # Zoom around the iconic Seahorse Valley boundary; wrap only after
        # reaching a deep magnification so the motion feels continuously inward.
        zoom = 1.0 + (math.exp((t % 15.0) * 0.24) - 1.0)
        center_x, center_y = -0.7435, 0.1314
        span_x = 3.2 / zoom
        span_y = span_x * (h / float(max(1, w)))
        max_iter = 34
        for py in range(h):
            ci = center_y + (py / float(max(1, h - 1)) - 0.5) * span_y
            for px in range(w):
                cr = center_x + (px / float(max(1, w - 1)) - 0.5) * span_x
                zr = zi = 0.0
                iteration = 0
                while zr * zr + zi * zi <= 4.0 and iteration < max_iter:
                    zr, zi = zr * zr - zi * zi + cr, 2.0 * zr * zi + ci
                    iteration += 1
                # Braille is monochrome: use escape bands to create contour detail.
                if iteration < max_iter and (iteration % 4 != 0):
                    g.plot(px, py)
        return g.get()

    def hypercube_scene():
        """A rotating tesseract projected from four dimensions into the LCD."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        t = LcdDemo.now * 0.001
        # Sixteen vertices; edges connect vertices differing in one bit.
        vertices = []
        for mask in range(16):
            vertices.append([1.0 if (mask >> axis) & 1 else -1.0
                             for axis in range(4)])
        edges = []
        for i in range(16):
            for axis in range(4):
                j = i ^ (1 << axis)
                if i < j:
                    edges.append((i, j))

        # Four-dimensional rotations in XY, ZW, XZ and YW planes.
        angles = [t * .61, t * 1.12, t * .47, t * .37]
        planes = [(0, 1), (2, 3), (0, 2), (1, 3)]
        projected = []
        scale = min(w * .82, h * 2.05)
        for original in vertices:
            v = original[:]
            for (a, b), angle in zip(planes, angles):
                ca, sa = math.cos(angle), math.sin(angle)
                va, vb = v[a], v[b]
                v[a] = va * ca - vb * sa
                v[b] = va * sa + vb * ca
            # Perspective projection: W first, then a mild Z perspective.
            dw = 3.6 - v[3] * .48
            x3, y3, z3 = v[0] / dw, v[1] / dw, v[2] / dw
            dz = 3.8 - z3 * .30
            px = w * .5 + (x3 / dz) * scale * 3.55
            py = h * .5 + (y3 / dz) * scale * 2.95
            projected.append((px, py))
        for a, b in edges:
            g.line(projected[a][0], projected[a][1],
                   projected[b][0], projected[b][1])
        # Highlight the inner and outer cubes with distinct vertex pulses.
        pulse = int((t * 5) % 16)
        px, py = projected[pulse]
        g.circle(px, py, 1.4, 1.4, filled=True)
        return g.get()

    def staff_scene():
        """Magnified stave with notes snapped to lines/spaces and a playback scanline."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        t = LcdDemo.now * .001
        spacing = 12
        offset = int((t * 2.0) % (spacing * 3))
        base = 4 - offset
        line_ys = [base + i * spacing for i in range(5)]
        for y in line_ys:
            if 0 <= y < h:
                g.line(0, y, w-1, y)
        # Every note is locked to a staff line or the exact space halfway between.
        note_steps = [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 2]
        for i, step in enumerate(note_steps):
            x = 5 + i * 5
            y = base + step * (spacing / 2.0)
            if -1 <= y < h:
                g.circle(x, y, 1.8, 1.25, filled=True)
                # Stems alternate direction but remain attached to noteheads.
                stem_dir = -1 if i % 2 == 0 else 1
                g.line(x + 1, y, x + 1, y + stem_dir * 6)
        # A moving vertical scanline marks playback position.
        scan_x = int(t * 7.0) % w
        g.line(scan_x, 0, scan_x, h-1)
        return g.get()


    def wormhole_scene():
        """Widely spaced sine/cosine wormhole with a roller-coaster centreline."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        t = LcdDemo.now * .001
        # Fewer, more widely separated hoops travel through a strongly undulating tunnel.
        for ring in range(10):
            depth = ((ring / 9.0) + (t * .30)) % 1.0
            radius = 2.0 + depth * max(14, w * .72)
            centre_y = h * .5 + math.sin(depth * math.tau * 1.7 - t * 1.25) * h * .22
            centre_x = w * .5 + math.sin(depth * math.tau * 1.1 + t * .55) * w * .10
            ry = radius * (h / float(max(1, w))) * 1.30
            points = []
            for step in range(64):
                a = math.tau * step / 64.0
                wave = 1.0 + .08 * math.sin(a * 4.0 - t * 2.0 + ring * .6)
                twist = a + depth * 1.6
                points.append((centre_x + math.cos(twist) * radius * wave,
                               centre_y + math.sin(twist) * ry * wave))
            for i in range(len(points)):
                a, b = points[i], points[(i + 1) % len(points)]
                g.line(a[0], a[1], b[0], b[1])
        # Longitudinal rails undulate vertically like a roller-coaster track.
        for rail in range(8):
            angle = math.tau * rail / 8.0
            prev = None
            for step in range(52):
                d = step / 51.0
                r = 2.0 + d * max(14, w * .72)
                cx = w * .5 + math.sin(d * math.tau * 1.1 + t * .55) * w * .10
                cy = h * .5 + math.sin(d * math.tau * 1.7 - t * 1.25) * h * .22
                a = angle + d * 1.6 + .10 * math.sin(t + d * 9)
                pt = (cx + math.cos(a) * r,
                      cy + math.sin(a) * r * (h / float(max(1, w))) * 1.30)
                if prev is not None:
                    g.line(prev[0], prev[1], pt[0], pt[1])
                prev = pt
        return g.get()

    def music_polygon_scene():
        """Audio-reactive polygon with one simulated frequency per vertex."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        t = LcdDemo.now * .001
        cx, cy = w * .5, h * .5
        count = 20
        points = []
        for i in range(count):
            # Incremental frequency assignment across the polygon spectrum.
            freq = .35 + i * .115
            beat = .5 + .5 * math.sin(t * (1.7 + freq * 2.2) + i * 1.37)
            harmonic = .5 + .5 * math.sin(t * (3.1 + freq) - i * .73)
            amplitude = .20 + .80 * (beat ** 2) * (.68 + .32 * harmonic)
            vibration = math.sin(t * (9.0 + i * .7) + i) * (.8 + beat * 1.8)
            radius = min(w * .40, h * 1.35) * (amplitude + vibration * .035)
            angle = math.tau * i / count - t * .32
            points.append((cx + math.cos(angle) * radius,
                           cy + math.sin(angle) * radius * .78))
        for i in range(count):
            a, b = points[i], points[(i + 1) % count]
            g.line(a[0], a[1], b[0], b[1])
            # Radial spokes make the individual frequency bands legible.
            if i % 2 == 0:
                g.line(cx, cy, a[0], a[1])
            g.circle(a[0], a[1], 1.1, 1.0, filled=True)
        g.circle(cx, cy, 1.3, 1.3, filled=True)
        return g.get()

    def emx_logo_3d_scene():
        """Large extruded EMX lettering rotating as a single 3D object."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        t = LcdDemo.now * .001
        # Stroke-font polylines, proportioned to form E, M and X.
        glyphs = [
            [((0,0),(0,10)),((0,0),(6,0)),((0,5),(5,5)),((0,10),(6,10))],
            [((0,10),(0,0),(4,5),(8,0),(8,10))],
            [((0,0),(8,10)),((8,0),(0,10))]
        ]
        points=[]; edges=[]; depth=2.8
        xoff=[-11,-1,10]
        for gi, strokes in enumerate(glyphs):
            for stroke in strokes:
                ids=[]
                for x,y in stroke:
                    ids.append(len(points)); points.append((xoff[gi]+x-4, y-5, 0))
                for a,b in zip(ids,ids[1:]): edges.append((a,b))
                # Extruded duplicate strokes add thickness and 3D depth.
                ids2=[]
                for x,y in stroke:
                    ids2.append(len(points)); points.append((xoff[gi]+x-4, y-5, depth))
                for a,b in zip(ids2,ids2[1:]): edges.append((a,b))
                for a,b in zip(ids,ids2): edges.append((a,b))
        # Start with a dramatic angle, then ease into a stable front-facing pose.
        settle = min(1.0, max(0.0, LcdDemo.phase / 8.0))
        settle = settle * settle * (3.0 - 2.0 * settle)
        # Three full turns are completed while the logo eases into its
        # final, perfectly readable front-facing pose.
        turns = math.tau * 3.0 * (1.0 - settle)
        ax = 1.05 * (1.0 - settle) + turns * .72
        ay = 1.55 * (1.0 - settle) + turns
        az = .62 * (1.0 - settle) + turns * .47
        projected=[]
        start_scale = min(w * .62, h * 1.35)
        fit_scale = min(w * .15, h * .27)
        zoom_progress = min(1.0, max(0.0, LcdDemo.phase / 4.5))
        # Ease out from the dramatic opening close-up to a fully readable fit.
        ease = zoom_progress * zoom_progress * (3.0 - 2.0 * zoom_progress)
        scale = start_scale * (1.0 - ease) + fit_scale * ease
        for x,y,z in points:
            yy,zz=y*math.cos(ax)-z*math.sin(ax),y*math.sin(ax)+z*math.cos(ax)
            xx,zz= x*math.cos(ay)+zz*math.sin(ay),-x*math.sin(ay)+zz*math.cos(ay)
            xx,yy=xx*math.cos(az)-yy*math.sin(az),xx*math.sin(az)+yy*math.cos(az)
            d=3.7+zz*.07
            projected.append((w/2+xx*scale/d,h/2+yy*scale*.92/d))
        for a,b in edges:
            g.line(*projected[a],*projected[b])
        return g.get()

    def travelling_3d_scene():
        """First-person 3D maze: walls, floor grid and visible approaching obstacles."""
        g = LcdDemo.pixel_canvas()
        w, h = g.width, g.height
        # Negative time reverses the apparent direction of travel through the maze.
        t = -LcdDemo.now * .001
        horizon = h * .34
        # Maze corridor boundaries converge toward the vanishing point.
        for side in (-1, 1):
            prev = None
            for step in range(40):
                d = .10 + step / 39.0 * 2.2
                bend = math.sin(t * .55 + d * 1.7) * .13
                x = w * .5 + (side * (.46 + bend)) * w / (d + .35)
                y = horizon + (h - horizon) * (.12 / (d + .12))
                if prev is not None:
                    g.line(prev[0], prev[1], x, y)
                prev = (x, y)
        # Floor cross-lines move toward the viewer, but start at the horizon.
        for row in range(14):
            z = ((row / 14.0 + t * .22) % 1.0)
            depth = .18 + z * 2.1
            y = horizon + (h - horizon) * (1.0 - math.exp(-depth * 1.25))
            half = min(w * .49, w * .08 + depth * w * .19)
            g.line(w * .5 - half, y, w * .5 + half, y)
        # Rectangular maze walls/obstacles approach, grow, and pass the camera.
        for idx in range(5):
            z = ((idx / 5.0 + t * .16) % 1.0)
            depth = .28 + z * 2.0
            side = -1 if idx % 2 == 0 else 1
            centre_x = w * .5 + side * (w * .12 + z * w * .12)
            base_y = horizon + (h - horizon) * (1.0 - math.exp(-depth * 1.25))
            half_w = max(1.0, w * .035 / (depth + .18))
            wall_h = max(2.0, h * .24 / (depth + .18))
            top_y = base_y - wall_h
            left, right = centre_x - half_w, centre_x + half_w
            g.line(left, top_y, right, top_y)
            g.line(left, top_y, left, base_y)
            g.line(right, top_y, right, base_y)
            g.line(left, base_y, right, base_y)
            # Top face gives each obstacle a solid, readable 3D silhouette.
            g.line(left, top_y, centre_x, top_y - wall_h * .22)
            g.line(centre_x, top_y - wall_h * .22, right, top_y)
        return g.get()

    def circle_scene():
        """Orbiting circle with subpixel resolution."""
        import math
        g=LcdDemo.pixel_canvas(); h,w=len(g),len(g[0]); t=LcdDemo.now*.001
        cx=w/2+math.cos(t*1.3)*w*.20; cy=h/2+math.sin(t*1.3)*h*.18
        LcdDemo.pixel_circle(g,cx,cy,max(2,w*.13),max(1,h*.34))
        LcdDemo.pixel_circle(g,cx,cy,1.2,1.2,True)
        return LcdDemo.pixel_pack(g)

    def run():
        LD = LcdDemo
        lcd = LD.lcd
        LD.now = pygame.time.get_ticks()
        time = (LD.now - lcd._demo_started) / 1000.0
        LD.frame = int(time * 16)
        lcd._demo_frame = LD.frame

        # Kawaii firmware-update intro, shown before the original boot splash.
        # The progress animation is deliberately playful but keeps the LCD's
        # five-line text layout and 32-character width.
        if time < 6.0:
            progress = min(1.0, time / 5.5)
            filled = int(progress * 22)
            bar = "█" * filled + "▒" * (22 - filled)
            faces = ["", ]
            face = faces[int(time * 2.2) % len(faces)]
            spark = ["  .  ", " ... ", ".....", ".. ..", ".   .", ][int(time * 5.0) % 5]
            status = "DO NOT POWER OFF THE DEVICE!" if progress < 1.0 else "READY! LET'S GO!"
            lcd.buffer = LD.lines([
                LD.center("SYSTEM UPDATE"),
                LD.center(face + " " + spark,LD.wide),
                LD.center(status,LD.wide),
                LD.center("[" + bar + "]",LD.wide),
                LD.center(str(int(progress * 100)).rjust(3) + "%   PLEASE WAIT", LD.wide)
            ])
            LD.glow = 0.92 + 0.08 * math.sin(time * 7.0)
            lcd.color = (255, 150, 48)
            return

        # Preserve the original logo layout, using the canonical 0x0A glyph.
        if time < 13.0:
            boot_time = time - 6.0
            lcd.buffer = LD.lines(LD.BOOT_SPLASH[0 if boot_time < 2.0 else 1])
            LD.glow = 1.0
            lcd.color = (255, 140, 18)
            return

        demo_time = time - 13.0
        LD.frame = int(demo_time * 16)
        # Geometry gets three consecutive 6.5-second acts; every other
        # scene keeps the normal 6.5-second slot.
        schedule = [
            (29, 12.0), (0, 6.5), (31, 8.0), (1, 6.5), (2, 26.0), (3, 6.5),
            (4, 6.5), (5, 6.5), (6, 6.5), (7, 6.5),
            (8, 6.5), (9, 6.5), (10, 24.0), (11, 6.5),
            (12, 6.5),
            (14, 9.0), (15, 9.0), (16, 9.0), (17, 9.0),
            (18, 9.0), (20, 12.0), (21, 15.0), (19, 15.0),
            (22, 12.0), (23, 12.0), (24, 12.0), (25, 15.0), (26, 12.0),
            (27, 12.0), (28, 12.0), (30, 12.0), (13, 30.0)
        ]
        cycle = sum(item[1] for item in schedule)
        position = demo_time % cycle
        LD.scene, LD.duration = 0, 6.5
        for scene_id, scene_duration in schedule:
            if position < scene_duration:
                LD.scene = scene_id
                LD.phase = position
                LD.duration = scene_duration
                break
            position -= scene_duration
        lcd._demo_frame = LD.frame

        def with_graphic(title, graphic, metadata=None):
            result = [LD.center(title)]
            if metadata:
                result.append(LD.center(metadata))
            result.extend(graphic)
            return LD.lines(result)

        def synth_screen(draw_scene, footer=("[SELECT]", "[MODIFY]", "[DEFAULT]")):
            # The scene draws directly into the 64x16 mixed-mode raster.
            draw_scene()
            lcd.set_functions(*footer)
            lcd._demo_enabled = True

        if LD.scene == 0:
            LD.fire_scene()
        elif LD.scene == 31:
            LD.fireworks_scene()
        elif LD.scene == 1:
            LD.starfield_scene()
        elif LD.scene == 2:
            LD.geometry_scene()
        elif LD.scene == 3:
            LD.pong_scene()
        elif LD.scene == 4:
            synth_screen(LD.vu_vertical_scene)
        elif LD.scene == 5:
            synth_screen(LD.vu_horizontal_scene)
        elif LD.scene == 20:
            synth_screen(LD.vu_12_scene, footer=("DRUMS 1-6", "EMX-1 / 12 PART", "SYNTH 1-6"))
        elif LD.scene == 6:
            synth_screen(LD.waveform_scene)
        elif LD.scene == 7:
            LD.sample_scene()
            lcd.set_functions("", "909_KICK_01.WAV", "")
            lcd._demo_enabled = True
        elif LD.scene == 8:
            synth_screen(LD.velocity_scene)
        elif LD.scene == 9:
            LD.image_scene()
        elif LD.scene == 10:
            LD.big_text_scene()
        elif LD.scene == 11:
            LD.circle_scene()
        elif LD.scene == 14:
            LD.piano_roll_scene()
        elif LD.scene == 15:
            LD.eq_scene()
        elif LD.scene == 16:
            LD.file_browser_scene()
        elif LD.scene == 17:
            LD.keyboard_scene()
        elif LD.scene == 18:
            LD.cassette_scene()
        elif LD.scene == 19:
            LD.fractal_scene()
        elif LD.scene == 21:
            LD.hypercube_scene()
        elif LD.scene == 22:
            LD.snow_scene()
        elif LD.scene == 23:
            LD.staff_scene()
        elif LD.scene == 24:
            synth_screen(LD.metaballs_scene, footer=("METABALLS", "ORGANIC FIELD", "EMX-1"))
        elif LD.scene == 25:
            LD.tetris_scene()
        elif LD.scene == 26:
            LD.snake_scene()
        elif LD.scene == 27:
            LD.wormhole_scene()
        elif LD.scene == 28:
            LD.music_polygon_scene()
        elif LD.scene == 29:
            LD.emx_logo_3d_scene()
        elif LD.scene == 30:
            LD.travelling_3d_scene()
        elif LD.scene == 12:
            lcd.buffer = LD.lines([
                LD.center("PIXEL GLYPH TEST"), LD.fit("0123456789"),
                LD.fit("ABCDEFGHIJKLMN"),
                LD.scroll("RETRO HARDWARE / DIGITAL DREAMS", LD.frame),
                LD.center("1X TEXT / 2X PIXEL ART")])
        else:
            # Final credits: vertical Star-Wars-style pixel crawl plus a fixed 32-char ticker.
            g = LD.pixel_canvas(rows=4)
            credit_lines = [
                "EMX-1 LCD DEMO", "", "AN ORIGINAL DEMO",
                "CONCEPT BY", "PINAKURE", "",
                "GRAPHICS BY", "PINAKURE", "TYPEFACE BY",
                "PINAKURE", "SCREEN DESIGN", "PINAKURE",
                "PROGRAM DESIGN", "PINAKURE", "",
                "AI ASSISTANCE", "CHATGPT", "",
                "BUILT FOR EMX-1", "PIXEL / BRAILLE",
                "SMALL SCREEN", "BIG IDEAS", "",
                "THANK YOU!", "KEEP IT ALIVE",
                "END TRANSMISSION"
            ]
            scroll = (LD.phase * 6.2) % (len(credit_lines) * 7 + 18)
            for i, line in enumerate(credit_lines):
                # Reverse the crawl direction and keep the text almost front-on.
                y = int(15 + (i * 7) - scroll)
                if -4 <= y < g.height:
                    scale = 1.0
                    span = len(line) * 4 - 1
                    x0 = (g.width - span) // 2
                    for ci, ch in enumerate(line):
                        glyph = LD.PIXEL_FONT.get(ch, LD.PIXEL_FONT[" "])
                        for gy, rowbits in enumerate(glyph):
                            py = y + gy
                            if 0 <= py < g.height:
                                for gx, bit in enumerate(rowbits):
                                    px = x0 + ci * 4 + gx
                                    if bit == "1" and 0 <= px < g.width:
                                        g.plot(px, py)
            lcd.set_functions("EMX-1 / CREDITS", "THANKS FOR WATCHING", "END")
            lcd._demo_enabled = True
            ticker = "CONCEPT, GRAPHICS, TYPEFACE AND SCREEN ARCHITECTURE: PINAKURE  /  CREATIVE AI ASSISTANCE: CHATGPT  /  EMX-1 LCD DEMO"
            # Mixed-mode function row is 32 characters; use a single scrolling line there.
            ticker_line = LD.scroll(ticker, LD.frame, 32)
            lcd.functions = [ticker_line[:11], ticker_line[11:22], ticker_line[22:32]]
        # Restore the original steady glow; the random blinking belongs only to the smiley.
        LD.glow = .84 + .16 * math.sin(time * 2.1)
        lcd.color = (255, int(112 + 28 * LD.glow), int(6 + 8 * LD.glow))
