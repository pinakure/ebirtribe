import random 
import pygame

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
        self.max            = float(max)
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
        self.update()   
        
    def mouseDown   (self, event): return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
    def mouseUp     (self, event): return event.type == pygame.MOUSEBUTTONUP   and event.button == 1
    def mouseMove   (self, event): return event.type == pygame.MOUSEMOTION
    def touches     (self, event): return self.knob.collidepoint(event.pos) or self.rect.collidepoint(event.pos)
    def touchesKnob (self, event): return self.knob.collidepoint(event.pos) 
        
    def render(self, app):
        surface         = app.screen
        txt             = app.fonts.tiny.render(f"{self.name}=", True, (255, 255, 255))
        val             = app.fonts.tiny.render(f"{str(self.value).ljust(8)}", True, (255, 55, 0))
        
        surface.blit    ( txt, (self.rect.x, self.rect.y + self.rect.height + 1))
        surface.blit    ( val, (self.rect.x + txt.get_size()[0], self.rect.y + self.rect.height + 1))
    
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
        
    def render( self, app ):
        super().render( app )
        pygame.draw.circle( app.screen, (255,255,0), (self.rect[0]+(self.rect[2]//2),self.rect[1]+(self.rect[3]//2)), self.rect[2]/2, 2)
        width, height = app.resources.knob.get_size()
        width //= 24        
        factor = self.value / self.max
        frame  = factor * 24
        app.screen.blit( app.resources.knob, (self.knob.x, self.knob.y), area=(frame*96, 0, width, height))

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


class Slider(Widget):
    def __init__(self, name="UnnamedSlider", x=0, y=0, width=200, height=20, min=0, value=0, max=255):
        super().__init__(Widget.SLIDER, name, x, y, width, height, min, value, max)
    
    def handle(self, event, app):
        if self.mouseDown(event):        
            if self.touches(event):
                self.drag = True
                self.last = event.pos[0]
                if not self.touchesKnob(event.pos):
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
    
    def render(self, app):
        super().render(app)
        app.screen.blit( app.resources.slider, (self.knob.x, self.knob.y-6))
                     

class Fader(Widget):
    def __init__(self, name="UnnamedFader", x=0, y=0, width=32, height=200, min=0, value=0, max=255):
        super().__init__(Widget.FADER, name, x, y, width, height, min, value, max)
        
    def render(self, app):
        super().render(app)
        app.screen.blit( app.resources.fader, (self.knob.x, self.knob.y))                        

class Button(Widget):
    def __init__(self, name="UnnamedButton", x=0, y=0, width=128, height=56, min=0, value=0, max=1):
        super().__init__(Widget.BUTTON, name, x, y, width, height, min, value, max)
        
    def render(self, app):
        super().render(app)
        pygame.draw.rect( app.screen, (255,255,0), self.rect, 3, border_radius=10)

class Pad(Widget):
    def __init__(self, name="UnnamedPad", x=0, y=0, width=96, height=96, min=0, value=0, max=1):
        super().__init__(Widget.PAD, name, x, y, width, height, min, value, max)
        
    def render(self, app):
        super().render(app)
        color = (220, 220, 120,64) if self.drag else (220, 64, 0)
        pygame.draw.rect( app.screen, color, self.rect, 1)
        pygame.draw.rect( app.screen, color, self.knob)

class Led(Widget):
    def __init__(self, name="UnnamedLed", x=0, y=0, width=16, height=16, min=0, value=0, max=3):
        super().__init__(Widget.LED, name, x, y, width, height, min, value, max)
        self.interactive = False
        
    def render( self, app ):
        super().render( app )
        pygame.draw.circle( app.screen, (255,255,0), (self.rect[0]+(self.rect[2]//2),self.rect[1]+(self.rect[3]//2)), self.rect[2]/2, 2)
        width, height = app.resources.knob.get_size()
        width //= 4        
        factor = self.value / self.max
        frame  = factor * 4
        app.screen.blit( app.resources.knob, (self.knob.x, self.knob.y), area=(frame*96, 0, width, height))

class Valve(Widget):
    def __init__(self, name="UnnamedValve", x=0, y=0, width=128, height=128, min=0.0, value=0.0, max=1.0):
        super().__init__(Widget.VALVE, name, x, y, width, height, min, float(value), max)
        self.interactive = False
        
    def render(self, app):
        super().render(app)
        width, height = app.resources.valve.get_size()
        if self.value > 0.0: 
            self.value *= 0.97
        if random.randint(0,32)==7:
            self.value = 1.0
        app.resources.valve.set_alpha(int(self.value*256))
        app.screen.blit( app.resources.valve, (self.knob.x, self.knob.y), area=(0, 0, width/2, height))

class Lcd(Widget):
    def __init__(self, name="UnnamedLcd", x=0, y=0, width=96, height=96, min=0, value=0, max=0):
        super().__init__(Widget.LCD, name, x, y, width, height, min, value, max)
        self.interactive = False
        
    def render(self, app):
        #super().render(app)
        pygame.draw.rect( app.screen, (255,128,0), self.rect, 1)
        

class Vumeter(Widget):
    def __init__(self, name="UnnamedVumeter", x=0, y=0, width=32, height=96, min=0, value=0, max=255):
        super().__init__(Widget.VUMETER, name, x, y, width, height, min, value, max)
        self.interactive = False

    def render(self, app):
        super().render(app)
        pygame.draw.rect( app.screen, (0, 255,128), self.rect, 1)
        