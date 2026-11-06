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
        shape_index = min(2, int(phase // 6.5))
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
        else:  # Square-based pyramid
            vertices = [(-1,-.8,-1),(1,-.8,-1),(1,-.8,1),(-1,-.8,1),
                        (0,1.25,0)]
            edges = [(0,1),(1,2),(2,3),(3,0),(0,4),(1,4),(2,4),(3,4)]
            exit_x, exit_y = 0, -1.5 * h

        ax, ay, az = spin * .73, spin * 1.0, spin * .47
        projected = []
        # Scale is chosen for a 64x20 pixel viewport, not a character grid.
        base = min(w * .43, h * 1.85)
        scale = base * grow
        shift_x, shift_y = exit_x * travel, exit_y * travel
        for x, y, z in vertices:
            yy, zz = y*math.cos(ax)-z*math.sin(ax), y*math.sin(ax)+z*math.cos(ax)
            xx, zz = x*math.cos(ay)+zz*math.sin(ay), -x*math.sin(ay)+zz*math.cos(ay)
            xx, yy = xx*math.cos(az)-yy*math.sin(az), xx*math.sin(az)+yy*math.cos(az)
            depth = zz + 3.6
            px = w/2 + shift_x + (xx * scale * 2.0 / depth)
            py = h/2 + shift_y + (yy * scale * .88 / depth)
            projected.append((px, py))
        for a, b in edges:
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
        """Animated stereo vertical level meters."""
        import math
        g=LcdDemo.pixel_canvas(max(1, LcdDemo.rows - 1)); h,w=g.height,g.width; t=LcdDemo.now*.001
        for c in range(max(2,min(8,w//7))):
            x=int((c+.5)*w/max(2,min(8,w//7)))
            level=.12+.84*(.5+.5*math.sin(t*3.2+c*.83))
            height=int(level*h)
            for y in range(h-height,h):
                LcdDemo.pixel_put(g,x,y); LcdDemo.pixel_put(g,x+1,y)
            LcdDemo.pixel_put(g,x,max(0,h-height-1-int(2*(.5+.5*math.sin(t*4+c)))))
        return LcdDemo.pixel_pack(g)

    def vu_horizontal_scene():
        """Two clearly separated stereo bars on the bottom two LCD rows."""
        g = LcdDemo.pixel_canvas(max(1, LcdDemo.rows - 1))
        h, w = g.height, g.width
        t = LcdDemo.now * 0.001

        # Each meter occupies exactly one LCD character row (two pixel rows).
        # The two rows are the bottom two rows of the display.
        first_y = max(0, h - 4)
        second_y = max(0, h - 2)
        for channel, y in enumerate((first_y, second_y)):
            level = 0.12 + 0.84 * (0.5 + 0.5 * math.sin(t * 3.0 + channel * 1.4))
            extent = max(1, min(w, int(level * w)))
            for x in range(extent):
                g.plot(x, y)
                g.plot(x, min(h - 1, y + 1))
            # Peak marker, clamped to the right edge.
            peak = min(w - 1, extent + 1 + int(2 * (0.5 + 0.5 * math.sin(t * 5.0 + channel))))
            g.plot(peak, y)
            g.plot(peak, min(h - 1, y + 1))
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
        """Readable 909 kick waveform using four LCD rows of the display."""
        g = LcdDemo.pixel_canvas(max(1, LcdDemo.rows - 1))
        h, w = g.height, g.width
        mid = (h - 1) / 2.0
        amp = max(1.0, h * 0.43)
        previous = None
        t = LcdDemo.now * 0.001

        # Centre reference line, then a strong decaying kick transient.
        for x in range(w):
            g.plot(x, int(round(mid)))
        for x in range(w):
            p = x / float(max(1, w - 1))
            envelope = math.exp(-p * 4.6)
            cycles = 4.7 - 3.0 * p
            signal = math.sin(p * math.tau * cycles + t * 0.25) * envelope
            y = mid - signal * amp
            if previous is not None:
                g.line(x - 1, previous, x, y)
            # Show the amplitude envelope as a vertical fill from the centre.
            g.line(x, mid, x, mid - abs(signal) * amp)
            previous = y
        return g.get()

    def image_scene():
        """Stroboscopic pixel smiley."""
        g = LcdDemo.pixel_canvas()
        # A crisp full-screen face, flashed on/off at 5 Hz.
        if (LcdDemo.now // 100) % 2 == 0:
            cx, cy = g.width / 2.0, g.height / 2.0
            radius = min(g.width * 0.22, g.height * 0.44)
            g.circle(cx, cy, radius, radius)
            eye_dx = max(2, int(radius * 0.42))
            eye_dy = -max(1, int(radius * 0.22))
            g.plot(cx - eye_dx, cy + eye_dy)
            g.plot(cx + eye_dx, cy + eye_dy)
            # Curved, pixel-stepped smile, scaled to the face.
            smile = max(2, int(radius * 0.42))
            for x, y in [(-2,1),(-1,2),(0,2),(1,2),(2,1)]:
                g.plot(cx + x * smile / 2.0, cy + y * smile / 2.0)
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
        """Continuous 3x5 bitmap-font scroller over a 64x20 pixel canvas."""
        g = LcdDemo.pixel_canvas()
        message = "  PIXEL POWER  /  LCD DEMO  /  64X20  "
        glyphs = [LcdDemo.PIXEL_FONT.get(ch, LcdDemo.PIXEL_FONT[" "])
                  for ch in message]
        text_width = len(glyphs) * 4
        offset = int(LcdDemo.now * 0.008) % (text_width + g.width)
        cursor = g.width - offset
        for glyph in glyphs:
            for gy, row in enumerate(glyph):
                for gx, bit in enumerate(row):
                    if bit == "1":
                        g.plot(cursor + gx, 2 + gy)
            cursor += 4
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

        # Preserve the original logo layout, using the canonical 0x0A glyph.
        if time < 7.0:
            lcd.buffer = LD.lines(LD.BOOT_SPLASH[0 if time < 2.0 else 1])
            LD.glow = 1.0
            lcd.color = (255, 140, 18)
            return

        demo_time = time - 7.0
        LD.frame = int(demo_time * 16)
        # Geometry gets three consecutive 6.5-second acts; every other
        # scene keeps the normal 6.5-second slot.
        schedule = [
            (0, 6.5), (1, 6.5), (2, 19.5), (3, 6.5),
            (4, 6.5), (5, 6.5), (6, 6.5), (7, 6.5),
            (8, 6.5), (9, 6.5), (10, 24.0), (11, 6.5),
            (12, 6.5), (13, 6.5)
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
        elif LD.scene == 6:
            synth_screen(LD.waveform_scene)
        elif LD.scene == 7:
            synth_screen(LD.sample_scene)
        elif LD.scene == 8:
            synth_screen(LD.velocity_scene)
        elif LD.scene == 9:
            LD.image_scene()
        elif LD.scene == 10:
            LD.big_text_scene()
        elif LD.scene == 11:
            LD.circle_scene()
        elif LD.scene == 12:
            lcd.buffer = LD.lines([
                LD.center("PIXEL GLYPH TEST"), LD.fit("0123456789"),
                LD.fit("ABCDEFGHIJKLMN"),
                LD.scroll("RETRO HARDWARE / DIGITAL DREAMS", LD.frame),
                LD.center("1X TEXT / 2X PIXEL ART")])
        else:
            credits = ["CODE: LCD DEMO", "GFX: SUBPIXEL",
                       "SOUND: 909 KICK", "THANKS FOR WATCHING"]
            i = int(LD.phase / (LD.duration / len(credits))) % len(credits)
            lcd.buffer = LD.lines([
                LD.center("A SMALL DISPLAY PRODUCTION"),
                LD.center("P R E S E N T S"),
                LD.center(credits[i]),
                LD.scroll("SEE YOU NEXT FRAME - REWINDING", LD.frame),
                LD.center("*** END OF TRANSMISSION ***")])
        LD.glow = .84 + .16 * math.sin(time * 2.1)
        lcd.color = (255, int(112 + 28 * LD.glow), int(6 + 8 * LD.glow))
