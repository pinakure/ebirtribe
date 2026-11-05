import random
import pygame

class LedTypes:
    HUGE_OFF    = 0x00
    HUGE_RED    = 0x01
    HUGE_AMBER  = 0x02
    HUGE_GREEN  = 0x03
    BIG_OFF     = 0x04
    BIG_RED     = 0x05
    BIG_AMBER   = 0x06
    BIG_GREEN   = 0x07
    MID_OFF     = 0x08
    MID_RED     = 0x09
    MID_AMBER   = 0x0A
    MID_GREEN   = 0x0B
    SMALL_OFF   = 0x0C
    SMALL_RED   = 0x0D
    SMALL_AMBER = 0x0E
    SMALL_GREEN = 0x0F
    TINY_OFF    = 0x10
    TINY_RED    = 0x11
    TINY_AMBER  = 0x12
    TINY_GREEN  = 0x13
    FLAT_OFF    = 0x14
    FLAT_RED    = 0x15
    FLAT_AMBER  = 0x16
    FLAT_GREEN  = 0x17
    V_BVM_OFF   = 0x18
    V_BVM_G00   = 0x19
    V_BVM_G01   = 0x1A
    V_BVM_G02   = 0x1B
    V_BVM_G03   = 0x1C
    V_BVM_G04   = 0x1D
    V_BVM_Y00   = 0x1E
    V_BVM_Y01   = 0x1F
    V_BVM_Y02   = 0x20
    V_BVM_Y03   = 0x21
    V_BVM_Y04   = 0x22
    V_BVM_R00   = 0x23
    V_BVM_R01   = 0x24
    V_BVM_R02   = 0x25
    V_BVM_R03   = 0x26
    V_BVM_R04   = 0x27
    H_BVM_OFF   = 0x28
    H_BVM_G00   = 0x29
    H_BVM_G01   = 0x2A
    H_BVM_G02   = 0x2B
    H_BVM_G03   = 0x2C
    H_BVM_G04   = 0x2D
    H_BVM_Y00   = 0x2E
    H_BVM_Y01   = 0x2F
    H_BVM_Y02   = 0x30
    H_BVM_Y03   = 0x31
    H_BVM_Y04   = 0x32
    H_BVM_R00   = 0x33
    H_BVM_R01   = 0x34
    H_BVM_R02   = 0x35
    H_BVM_R03   = 0x36
    H_BVM_R04   = 0x37
    V_SVM_OFF   = 0x38
    V_SVM_G00   = 0x39
    V_SVM_G01   = 0x3A
    V_SVM_G02   = 0x3B
    V_SVM_G03   = 0x3C
    V_SVM_G04   = 0x3D
    V_SVM_Y00   = 0x3E
    V_SVM_Y01   = 0x3F
    V_SVM_Y02   = 0x40
    V_SVM_Y03   = 0x41
    V_SVM_Y04   = 0x42
    V_SVM_R00   = 0x43
    V_SVM_R01   = 0x44
    V_SVM_R02   = 0x45
    V_SVM_R03   = 0x46
    V_SVM_R04   = 0x47
    H_SVM_OFF   = 0x48
    H_SVM_G00   = 0x49
    H_SVM_G01   = 0x4A
    H_SVM_G02   = 0x4B
    H_SVM_G03   = 0x4C
    H_SVM_G04   = 0x4D
    H_SVM_Y00   = 0x4E
    H_SVM_Y01   = 0x4F
    H_SVM_Y02   = 0x50
    H_SVM_Y03   = 0x51
    H_SVM_Y04   = 0x52
    H_SVM_R00   = 0x53
    H_SVM_R01   = 0x54
    H_SVM_R02   = 0x55
    H_SVM_R03   = 0x56
    H_SVM_R04   = 0x57

    TYPE_HUGE   = 0x00
    TYPE_BIG    = 0x01
    TYPE_MID    = 0x02
    TYPE_SMALL  = 0x03
    TYPE_TINY   = 0x04
    TYPE_FLAT   = 0x05
    TYPE_VUH_XL = 0x06
    TYPE_VUV_XL = 0x07
    TYPE_VUH_XS = 0x08
    TYPE_VUV_XS = 0x09

    SIZES       = {
        TYPE_HUGE   : 32,
        TYPE_BIG    : 32,
        TYPE_MID    : 24,
        TYPE_SMALL  : 8,
        TYPE_TINY   : 8,
        TYPE_FLAT   : 8,
        TYPE_VUH_XL : 4,
        TYPE_VUV_XL : 4,
        TYPE_VUH_XS : 4,
        TYPE_VUV_XS : 4,
    }

    def init():
        LedTypes.geometry = LedTypes.getGeometry()

    def getGeometry():
        def __getGeometry(x, y, size):
            return ( x, y, LedTypes.SIZES[size], LedTypes.SIZES[size] )
        return {
            LedTypes.HUGE_OFF    : __getGeometry(    0,  0, LedTypes.TYPE_HUGE     ),
            LedTypes.HUGE_RED    : __getGeometry(   32,  0, LedTypes.TYPE_HUGE     ),
            LedTypes.HUGE_AMBER  : __getGeometry(   64,  0, LedTypes.TYPE_HUGE     ),
            LedTypes.HUGE_GREEN  : __getGeometry(   96,  0, LedTypes.TYPE_HUGE     ),
            LedTypes.BIG_OFF     : __getGeometry(    0, 32, LedTypes.TYPE_BIG      ),
            LedTypes.BIG_RED     : __getGeometry(   32, 32, LedTypes.TYPE_BIG      ),
            LedTypes.BIG_AMBER   : __getGeometry(   64, 32, LedTypes.TYPE_BIG      ),
            LedTypes.BIG_GREEN   : __getGeometry(   96, 32, LedTypes.TYPE_BIG      ),
            LedTypes.MID_OFF     : __getGeometry(    0, 64, LedTypes.TYPE_MID      ),
            LedTypes.MID_RED     : __getGeometry(   24, 64, LedTypes.TYPE_MID      ),
            LedTypes.MID_AMBER   : __getGeometry(   48, 64, LedTypes.TYPE_MID      ),
            LedTypes.MID_GREEN   : __getGeometry(   72, 64, LedTypes.TYPE_MID      ),
            LedTypes.SMALL_OFF   : __getGeometry(   96, 64, LedTypes.TYPE_SMALL    ),
            LedTypes.SMALL_RED   : __getGeometry(  104, 64, LedTypes.TYPE_SMALL    ),
            LedTypes.SMALL_AMBER : __getGeometry(  112, 64, LedTypes.TYPE_SMALL    ),
            LedTypes.SMALL_GREEN : __getGeometry(  120, 64, LedTypes.TYPE_SMALL    ),
            LedTypes.TINY_OFF    : __getGeometry(   96, 72, LedTypes.TYPE_TINY     ),
            LedTypes.TINY_RED    : __getGeometry(  104, 72, LedTypes.TYPE_TINY     ),
            LedTypes.TINY_AMBER  : __getGeometry(  112, 72, LedTypes.TYPE_TINY     ),
            LedTypes.TINY_GREEN  : __getGeometry(  120, 72, LedTypes.TYPE_TINY     ),
            LedTypes.FLAT_OFF    : __getGeometry(   96, 80, LedTypes.TYPE_FLAT     ),
            LedTypes.FLAT_RED    : __getGeometry(  104, 80, LedTypes.TYPE_FLAT     ),
            LedTypes.FLAT_AMBER  : __getGeometry(  112, 80, LedTypes.TYPE_FLAT     ),
            LedTypes.FLAT_GREEN  : __getGeometry(  120, 80, LedTypes.TYPE_FLAT     ),
            LedTypes.V_BVM_OFF   : __getGeometry(    0, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_G00   : __getGeometry(    8, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_G01   : __getGeometry(   16, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_G02   : __getGeometry(   24, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_G03   : __getGeometry(   32, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_G04   : __getGeometry(   40, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_Y00   : __getGeometry(   48, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_Y01   : __getGeometry(   56, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_Y02   : __getGeometry(   64, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_Y03   : __getGeometry(   72, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_Y04   : __getGeometry(   80, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_R00   : __getGeometry(   88, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_R01   : __getGeometry(   96, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_R02   : __getGeometry(  104, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_R03   : __getGeometry(  112, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.V_BVM_R04   : __getGeometry(  120, 88, LedTypes.TYPE_VUV_XL   ),
            LedTypes.H_BVM_OFF   : __getGeometry(    0, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_G00   : __getGeometry(    8, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_G01   : __getGeometry(   16, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_G02   : __getGeometry(   24, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_G03   : __getGeometry(   32, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_G04   : __getGeometry(   40, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_Y00   : __getGeometry(   48, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_Y01   : __getGeometry(   56, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_Y02   : __getGeometry(   64, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_Y03   : __getGeometry(   72, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_Y04   : __getGeometry(   80, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_R00   : __getGeometry(   88, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_R01   : __getGeometry(   96, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_R02   : __getGeometry(  104, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_R03   : __getGeometry(  112, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.H_BVM_R04   : __getGeometry(  120, 96, LedTypes.TYPE_VUH_XL   ),
            LedTypes.V_SVM_OFF   : __getGeometry(    0,104, LedTypes.TYPE_VUV_XS   ),
            LedTypes.V_SVM_G00   : __getGeometry(    4,104, LedTypes.TYPE_VUV_XS   ),
            LedTypes.V_SVM_G01   : __getGeometry(    8,104, LedTypes.TYPE_VUV_XS   ),
            LedTypes.V_SVM_G02   : __getGeometry(   12,104, LedTypes.TYPE_VUV_XS   ),
            LedTypes.V_SVM_Y00   : __getGeometry(   16,104, LedTypes.TYPE_VUV_XS   ),
            LedTypes.V_SVM_Y01   : __getGeometry(   20,104, LedTypes.TYPE_VUV_XS   ),
            LedTypes.V_SVM_Y02   : __getGeometry(   24,104, LedTypes.TYPE_VUV_XS   ),
            LedTypes.V_SVM_R00   : __getGeometry(   28,104, LedTypes.TYPE_VUV_XS   ),
            LedTypes.V_SVM_R01   : __getGeometry(   32,104, LedTypes.TYPE_VUV_XS   ),
            LedTypes.V_SVM_R02   : __getGeometry(   36,104, LedTypes.TYPE_VUV_XS   ),
            LedTypes.H_SVM_OFF   : __getGeometry(   40,104, LedTypes.TYPE_VUH_XS   ),
            LedTypes.H_SVM_G00   : __getGeometry(   44,104, LedTypes.TYPE_VUH_XS   ),
            LedTypes.H_SVM_G01   : __getGeometry(   48,104, LedTypes.TYPE_VUH_XS   ),
            LedTypes.H_SVM_G02   : __getGeometry(   52,104, LedTypes.TYPE_VUH_XS   ),
            LedTypes.H_SVM_Y00   : __getGeometry(   56,104, LedTypes.TYPE_VUH_XS   ),
            LedTypes.H_SVM_Y01   : __getGeometry(   60,104, LedTypes.TYPE_VUH_XS   ),
            LedTypes.H_SVM_Y02   : __getGeometry(   64,104, LedTypes.TYPE_VUH_XS   ),
            LedTypes.H_SVM_R00   : __getGeometry(   68,104, LedTypes.TYPE_VUH_XS   ),
            LedTypes.H_SVM_R01   : __getGeometry(   72,104, LedTypes.TYPE_VUH_XS   ),
            LedTypes.H_SVM_R02   : __getGeometry(   76,104, LedTypes.TYPE_VUH_XS   ),
        }

class Widget:
    KNOB        = 0x0   # Rotary de 96x96 pixels, 24 posibles estados gráficos
    SLIDER      = 0x1   # Barra de desplazamiento Horizontal
    FADER       = 0x2   # Barra de desplazamiento Vertical
    BUTTON      = 0x3   # Botón bi-estado (estado normal invisible)
    PAD         = 0x4   # Botón cuyo estado depende de una variable, no de que se pulse
    LED         = 0x5   # Elemento de feedback visual, puede tener 4 estados: 0->invisible | 1->rojo | 2->ambar | 3->verde
    VALVE       = 0x6   # Feedback visual de válvulas, si su valor es 1.0, la valvula se ilumina a máxima potencia. Si su valor es 0.0, la valvula se muestra apagada.
    LCD         = 0x7   # Display LCD, para mostrar mensajes al usuario
    VUMETER     = 0x8   # Feedback visual de vumetro (no se implementará en esta versión )
    JOG_WHEEL   = 0x9   # Jog wheel, con valor infinito

    def __init__(self, type, name, x, y, width, height, min, value, max):
        self.type           = type
        self.x              = int(x)
        self.y              = int(y)
        self.min            = float(min)
        self.max            = float(max) if max is not None else None
        self.value          = float(value)
        self.width          = int(width)
        self.height         = int(height)
        self.name           = name
        self.bitmap         = None
        self.interactive    = True
        self.drag           = False
        self.last           = 0
        self.knob           = pygame.Rect(0,0,15,16)
        self.rect           = pygame.Rect(x,y,width,height)
        self.uuid           = 0x0000
        self.update()

    def _setValue(self, value):
        self.value = value

    def setUUID(self, uuid):
        self.uuid = uuid
        return uuid

    def mouseDown   (self, event): return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
    def mouseUp     (self, event): return event.type == pygame.MOUSEBUTTONUP   and event.button == 1
    def mouseMove   (self, event): return event.type == pygame.MOUSEMOTION
    def touches     (self, event): return self.knob.collidepoint(event.pos) or self.rect.collidepoint(event.pos)
    def touchesRect (self, event): return self.rect.collidepoint(event.pos)
    def touchesKnob (self, event): return self.knob.collidepoint(event.pos)

    def render(self, app):
        surface         = app.screen
        txt             = app.fonts.tiny.render(f"{self.name}", True, (255, 255, 255))
        val             = app.fonts.tiny.render(f"{str(self.value).rjust(4, '0').ljust(8,'0')}"[0:8], True, (255, 55, 0))
        tw, th          = txt.get_size()
        vw, vh          = val.get_size()
        mid             = ( (self.rect.x+(self.rect.width >>1)), (self.rect.y+(self.rect.height>>1)) )
        tpos            = ( mid[0]-(tw>>1), mid[1]-(th))
        vpos            = ( mid[0]-(vw>>1), mid[1]+(vh))
        surface.blit    ( txt, tpos)
        surface.blit    ( val, vpos)

    def update(self):
        rango           = self.max - self.min
        delta           = (self.value - self.min) / rango if rango != 0 else 0
        self.knob.x     = self.rect.x + int(delta * (self.rect.width - self.knob.width))
        self.knob.y     = self.y

    def handle(self, event, app):
        return False

class Knob(Widget):

    def __init__(self, name="UnnamedKnob", x=0, y=0, width=96, height=96, min=0, value=0, max=255):
        super().__init__(Widget.KNOB, name, x, y, width, height, min, value, max)
        self.knob = pygame.Rect(self.x, self.y, 96, 96)

        # Rotado 90° adicionales en sentido horario (112.5° + 90° = 202.5°)
        # Mantiene el arco de 315° de recorrido útil
        self.ANGULO_MIN = 202.5
        self.ANGULO_MAX = 517.5
        self.update()

    def handle(self, event, app):
        if self.mouseDown(event):
            if self.touches(event):
                self.drag = True
                self.last = event.pos[1]  # Guardar solo el componente Y
                return True
        elif self.mouseUp(event):
            self.drag = False
        elif self.mouseMove(event) and self.drag:
            y_actual    = event.pos[1]   # Extrar solo el componente Y
            delta_y     = y_actual - self.last
            self.last   = y_actual

            factor      = 0.1 if app.pygame.key.get_mods() & app.pygame.KMOD_SHIFT else 1.0
            pixels_sensibilidad = 200.0
            units       = (self.max - self.min) / pixels_sensibilidad

            self.value -= delta_y * units * factor
            if self.value < self.min: self.value = self.min
            if self.value > self.max: self.value = self.max
            self.update()
            return True
        return False

    def update(self):
        self.knob.x = self.x
        self.knob.y = self.y

    def render(self, app):
        # Mapear el valor actual al arco físico del potenciómetro
        rango_valores = self.max - self.min
        factor = (self.value - self.min) / rango_valores if rango_valores != 0 else 0
        angulo_físico = self.ANGULO_MIN + factor * (self.ANGULO_MAX - self.ANGULO_MIN)

        # Normalizar a un rango circular de 0 a 360 grados
        angulo_normalizado = angulo_físico % 360.0
        grados_por_frame = 15.0  # (360 / 24)

        # Calcular índices de frames y ponderación para el cross-fade
        posicion_exacta_frame = angulo_normalizado / grados_por_frame
        indice_frame_actual = int(posicion_exacta_frame) % 24
        indice_frame_siguiente = (indice_frame_actual + 1) % 24

        # Fracción decimal que indica qué tan cerca estamos del siguiente frame (0.0 a 1.0)
        fraccion_siguiente = posicion_exacta_frame - int(posicion_exacta_frame)

        # Opacidad del frame que entra (0 a 255)
        alpha_siguiente = int(fraccion_siguiente * 255)

        # Rotación fina por software
        rotacion_fina = angulo_normalizado % grados_por_frame

        # Extraer y procesar los dos sub-sprites independientes
        # --- FRAME ACTUAL (Base 100% Opaca) ---
        surface_actual = pygame.Surface((96, 96), pygame.SRCALPHA)
        surface_actual.blit(app.resources.knob, (0, 0), area=(indice_frame_actual * 96, 0, 96, 96))
        # Mantenemos este frame al máximo de opacidad para que sirva de base sólida

        # --- FRAME SIGUIENTE + PRE-ROTACIÓN (Capas con Alpha Dinámico) ---
        raw_siguiente = pygame.Surface((96, 96), pygame.SRCALPHA)
        raw_siguiente.blit(app.resources.knob, (0, 0), area=(indice_frame_siguiente * 96, 0, 96, 96))

        # Pre-rotar el frame siguiente 15° hacia atrás para alinearlo algebraicamente
        surface_siguiente_rotada = pygame.transform.rotate(raw_siguiente, grados_por_frame)

        surface_siguiente = pygame.Surface((96, 96), pygame.SRCALPHA)
        rect_siguiente = surface_siguiente_rotada.get_rect()
        rect_siguiente.center = (48, 48)
        surface_siguiente.blit(surface_siguiente_rotada, rect_siguiente.topleft)
        # Aplicar la transparencia únicamente al cuadro que se va superponiendo
        surface_siguiente.set_alpha(alpha_siguiente)

        # Combinar ambos sub-sprites manteniendo la solidez del pixel base
        combined_surface = pygame.Surface((96, 96), pygame.SRCALPHA)
        combined_surface.blit(surface_actual, (0, 0))     # Base sólida
        combined_surface.blit(surface_siguiente, (0, 0))  # Capa superior interpolada

        # Aplicar la rotación fina definitiva sobre el resultado combinado opaco
        rotated_surface = pygame.transform.rotate(combined_surface, -rotacion_fina)
        new_rect = rotated_surface.get_rect()

        # Centrar dinámicamente en pantalla para evitar oscilaciones
        new_rect.center = (self.x + 48, self.y + 48)

        app.screen.blit(rotated_surface, new_rect.topleft)

        super().render(app)

class Slider(Widget):
    def __init__(self, name="UnnamedSlider", x=0, y=0, width=200, height=20, min=0, value=0, max=255):
        super().__init__(Widget.SLIDER, name, x, y, width, height, min, value, max)

    def handle(self, event, app):
        if self.mouseDown(event):
            if self.touches(event):
                self.drag = True
                self.last = event.pos[0]
                if not self.touchesKnob(event):
                    delta  = (event.pos[0] - self.rect.x) / (self.rect.width - self.knob.width)
                    self.value  = self.min + delta * (self.max - self.min)
                    self.update()
                return True
        elif self.mouseUp(event): self.drag = False
        elif self.mouseMove(event) and self.drag:
            x_actual    = event.pos[0]
            delta_x     = x_actual - self.last
            self.last   = x_actual
            factor      = 0.1 if app.pygame.key.get_mods() & app.pygame.KMOD_SHIFT else 1.0
            units       = (self.max - self.min) / (self.rect.width - self.knob.width)
            self.value += delta_x * units * factor
            if self.value < self.min: self.value = self.min
            if self.value > self.max: self.value = self.max
            self.update()
            return True
        return False

    def update(self):
        rango           = self.max - self.min
        delta           = (self.value - self.min) / rango if rango != 0 else 0
        self.knob.x     = self.rect.x + int(delta * (self.rect.width - self.knob.width))
        self.knob.y     = self.y

    def render(self, app):
        super().render(app)
        app.screen.blit( app.resources.slider, (self.knob.x, self.knob.y-6))

class Fader(Widget):
    def __init__(self, name="UnnamedFader", x=0, y=0, width=32, height=200, min=0, value=0, max=255):
        super().__init__(Widget.FADER, name, x, y, width, height, min, value, max)
        self.knob = pygame.Rect(self.x,self.y,85,48)
        self.update()

    def handle(self, event, app):
        if self.mouseDown(event):
            if self.touches(event):
                self.drag = True
                self.last = event.pos[1]
                if not self.touchesKnob(event):
                    delta  = (event.pos[1] - self.rect.y) / (self.rect.height - (self.knob.height/3))
                    self.value  = self.max - delta * (self.max - self.min)
                    if self.value < self.min: self.value = self.min
                    if self.value > self.max: self.value = self.max
                    self.update()
                return True
        elif self.mouseUp(event): self.drag = False
        elif self.mouseMove(event) and self.drag:
            y_actual    = event.pos[1]
            delta_y     = y_actual - self.last
            self.last   = y_actual
            factor      = 0.1 if app.pygame.key.get_mods() & app.pygame.KMOD_SHIFT else 1.0
            units       = (self.max - self.min) / (self.rect.height - self.knob.height)
            self.value -= delta_y * units * factor
            if self.value < self.min: self.value = self.min
            if self.value > self.max: self.value = self.max
            self.update()
            return True
        return False

    def update(self):
        rango           = self.max - self.min
        delta           = (self.value - self.min) / rango if rango != 0 else 0
        self.knob.x     = self.x
        self.knob.y     = self.rect.y + (self.rect.height - self.knob.height) - int(delta * (self.rect.height - self.knob.height))

    def render(self, app):
        super().render(app)
        app.screen.blit( app.resources.fader, (self.knob.x, self.knob.y))

class Button(Widget):
    def __init__(self, name="UnnamedButton", x=0, y=0, width=128, height=56, gfx_pos=(0,0), value=0, gfx_size=(96,64), callback=None):
        super().__init__(Widget.BUTTON, name, x, y, width, height, 0, value, 1)
        self.gfx_pos    = gfx_pos
        self.gfx_size   = gfx_size
        self.value      = True if value else False
        self.knob       = None
        self.callback   = callback
        self.highlight  = False
        self.middle     = (self.x+(self.rect.width//2), self.y+(self.rect.height//2))
        self.position   = (self.middle[0] - (self.gfx_size[0]//2),self.middle[1] - (self.gfx_size[1]//2))

    def handle(self, event, app):
        if self.mouseDown(event):
            if self.touchesRect(event):
                if self.callback is not None:
                    self.callback(self, event, app)
                self.value = 1
                self.update()
                return True
        elif self.mouseUp(event):
            self.value = 0
            self.update()
            return True
        return False

    def update(self):
        pass

    def demo(self):
        if random.randint(0,10)==7:
            self.value = True if random.randint(0,10)==7 else False
        self.update()

    def render(self, app):
        if self.value or self.highlight:
            app.screen.blit( app.resources.buttons, self.position, area=(*self.gfx_pos, *self.gfx_size))

class Pad(Button):
    def __init__(self, name="UnnamedPad", x=0, y=0, width=96, height=96, gfx_pos=(0,0), value=0, gfx_size=(96,64), callback=None):
        super().__init__(name, x, y, width, height, gfx_pos, value, gfx_size, callback)
        self.type = Widget.PAD

    def handle(self, event, app):
        if self.mouseDown(event):
            if self.touchesRect(event):
                self.highlight = 1
                if self.callback is not None:
                    self.callback(self, event, app)
                else:
                    self.value ^=1
                self.update()
                return True
        elif self.mouseUp(event):
            self.highlight = 0
            self.update()
            return True
        return False

class Led(Widget):
    def __init__(self, name="UnnamedLed", x=0, y=0, width=16, height=16, kind=0, value=0, max=None):
        self.kind           = kind
        super().__init__(Widget.LED, name, x, y, width, height, kind, value, max)
        self.interactive    = False
        self.knob           = None

    def update(self):
        if random.randint(0,50)==7:
            self.value = random.randint(0,3)
        pass

    def render( self, app ):
        self.update()
        geometry = LedTypes.geometry[ (self.kind * 4)+self.value ]
        app.screen.blit( app.resources.leds, (self.x, self.y), area=geometry)

class Valve(Widget):
    def __init__(self, name="UnnamedValve", x=0, y=0, width=128, height=128, min=0.0, value=0.0, max=1.0):
        super().__init__(Widget.VALVE, name, x, y, width, height, min, float(value), max)
        self.interactive    = False
        self.knob           = None

    def render(self, app):
        super().render(app)
        width, height = app.resources.valve.get_size()
        if self.value > 0.0:
            self.value *= 0.97
        if random.randint(0,32)==7:
            self.value = 1.0
        app.resources.valve.set_alpha(int(self.value*256))
        app.screen.blit( app.resources.valve, (self.x, self.y), area=(0, 0, width, height))

###############################################################################
# TODO ########################################################################
###############################################################################
class Lcd(Widget):
    def __init__(self, name="UnnamedLcd", x=0, y=0, width=96, height=96, columns=16, rows=5, skin=0):
        self.columns        = columns
        self.rows           = rows
        self.row_height     = (height-4) // rows
        self.column_width   = (width-4) // columns
        self.skin           = skin
        self.color          = (255,128,0)
        self.buffer         = ["" for _ in range(rows)]
        super().__init__(Widget.LCD, name, x, y, width, height, 0, 0, 0)
        self.interactive    = False

    def demo(self):
        self.buffer[0]      = "Hello World!"
        self.buffer[1]      = "0123456789ABCDEF"
        self.buffer[2]      = "0123456789ABCDEF"
        self.buffer[3]      = "0123456789ABCDEF"
        self.buffer[4]      = "0123456789ABCDEF0123456789ABCDEF"

    def update(self):
        self.demo()

    def render(self, app):
        self.update()
        surface = app.screen
        y       = 0
        for line in self.buffer:
            font    = app.fonts.dot_m if len(line)<=16 else app.fonts.dot_xs
            txt     = font.render(f"{line}", True, self.color)
            tpos    = ( self.x, self.y + y + font.offset)
            y       += self.row_height
            surface.blit    ( txt, tpos, area=(0,0,self.width-8, self.row_height))
        # pygame.draw.rect( app.screen, self.color, self.rect, 1)

class JogWheel(Widget):
    def __init__(self, name="UnnamedJogWheel", x=0, y=0, width=224, height=224, min=0, value=0, max=255):
        super().__init__(Widget.JOG_WHEEL, name, x, y, width, height, min, value, max)

    def render( self, app ):
        super().render( app )
        pygame.draw.circle( app.screen, (255,255,0), (self.rect[0]+(self.rect[2]//2),self.rect[1]+(self.rect[3]//2)), self.rect[2]/2, 2)
        width, height = app.resources.jog_wheel.get_size()
        width //= 24
        factor = self.value / self.max
        frame  = factor * 24
        app.screen.blit( app.resources.jog_wheel, (self.x, self.y))
        
class Vumeter(Widget):
    def __init__(self, name="UnnamedVumeter", x=0, y=0, width=32, height=96, min=0, value=0, max=255):
        super().__init__(Widget.VUMETER, name, x, y, width, height, min, value, max)
        self.interactive = False

    def render(self, app):
        super().render(app)
        pygame.draw.rect( app.screen, (0, 255,128), self.rect, 1)
