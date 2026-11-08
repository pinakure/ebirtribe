import  inspect
import  pygame
from    pygame._sdl2    import Window
import  interface
import  os
import  filesys
from    widget          import LedTypes,Widget

class Fonts:
    ocr         = None 
    dot_xs      = None
    dot_m       = None
    dot_l       = None
    dot_xl      = None
    segments    = None
    digital     = None
    tiny        = None
    m4g         = None

class Font(pygame.font.Font):
    def __init__(self, filename, size=8, offset=0):
        super().__init__(filename, size)
        self.offset = offset

class ResourceContainer:
    pass

class UI:
    
    widgets = {}
    input   = {}
    app     = None
            
    def init( app, archivo_entrada ):
        pygame          .init()
        pygame          .font.init()
        UI.app          = app      
        app.fonts       = Fonts  
        app.screen      = pygame.display.set_mode(( app.width, app.height ), pygame.NOFRAME)
        pygame          .display.set_caption(f"{ app.name } - { archivo_entrada.split(os.path.sep)[-1] if archivo_entrada is not None else ''}")
        app.resources   = UI.loadResources( app )
        app.backdrop    = app.resources.deck            
        UI.splash       (app)
        UI.initWidgets  (app)
        UI.loadFonts    (app)
        app.clock       = pygame.time.Clock()
        UI.create       ()
        return Window.from_display_module()
    
    def initWidgets( app ):
        # Preinitialize Geometry and blit positions
        LedTypes.init()
    
    def loadResources( app ):
        resources = ResourceContainer()
        for key, resource in interface.RESOURCES.items():
            print(f"[RESOURCE] Loading resources.{key} = '{resource}'")
            resources.__setattr__(key, filesys.loadImage(app, resource))
        return resources
        
    def loadFonts( app ):
        app.fonts.ocr       = Font(filesys.path("resources/fonts/ocr.ttf"   ), 36)
        app.fonts.dot_xs    = Font(filesys.path("resources/fonts/dotim3.ttf"), 28)
        app.fonts.dot_m     = Font(filesys.path("resources/fonts/dotim5.ttf"), 37)
        app.fonts.dot_l     = Font(filesys.path("resources/fonts/dotim7.ttf"), 28)
        app.fonts.dot_xl    = Font(filesys.path("resources/fonts/dotted.ttf"), 26)
        app.fonts.segments  = Font(filesys.path("resources/fonts/lcd.ttf"   ), 24)
        app.fonts.digital   = Font(filesys.path("resources/fonts/graph.ttf" ), 13)
        app.fonts.tiny      = Font(filesys.path("resources/fonts/graph.ttf" ),  8)
        app.fonts.m4g       = Font(filesys.path("resources/fonts/m4g.ttf"   ), 22)
        app.fonts.monospace = pygame.font.SysFont("Consolas", 16)
        
        app.fonts.ocr       .offset = -2
        app.fonts.dot_xs    .offset = 2
        app.fonts.dot_m     .offset = -2
        app.fonts.dot_l     .offset = +3
        app.fonts.dot_xl    .offset = +4
        app.fonts.segments  .offset = +6
        app.fonts.digital   .offset = +9
        app.fonts.tiny      .offset = 0
        app.fonts.m4g       .offset = 4
        
    def splash(app):
        app.screen.fill((20, 20, 25))
        app.fonts.heading   = pygame.font.SysFont("Consolas", 28, bold=True)
        app.screen.blit(app.backdrop, (0, 0))
        txt_titulo = app.fonts.heading.render(app.name.upper(), True, (130, 250, 50))
        app.screen.blit(txt_titulo, (app.width // 2 - txt_titulo.get_width() // 2, app.height // 3 - 40))
        pygame.display.flip()
    
    def autoload(class_name, offset=0x0000):
        def vars(cls):
            return [
                attr for attr, value in cls.__dict__.items()
                if not attr.startswith('__')                  # Filter out internal dunder attributes
                and not inspect.isfunction(value)             # Filter out regular methods
                and not isinstance(value, classmethod)        # Filter out @classmethods
                and not isinstance(value, staticmethod)       # Filter out @staticmethods
            ]
        condition   = True if hasattr(interface, class_name) and inspect.isclass(getattr(interface, class_name)) else False
        if condition == False: return {}
        instance    = eval(f'interface.{class_name}') 
        # Auto Mangle widget IDs (separate each group of ids by a 0x1000 offset amongst each category ), if defined        
        for k in vars(instance): setattr(instance, k, eval(f'interface.{class_name}.{k}')+offset)                        
        data        = instance.get()
        print(f'[ UI ] Loading {len(data)} {class_name} widgets...')
        [ print(f'[ UI ] Initializing {class_name} widget {w.name} {hex(w.setUUID(k))}') for k,w in data.items()]
        return data
    
    def create():
        widgets  = {}
        widgets |= UI.autoload('Knobs'           , 0x0000)
        widgets |= UI.autoload('Sliders'         , 0x1000)
        widgets |= UI.autoload('Faders'          , 0x2000)
        widgets |= UI.autoload('Buttons'         , 0x3000)
        widgets |= UI.autoload('Pads'            , 0x4000)
        widgets |= UI.autoload('Leds'            , 0x5000)
        widgets |= UI.autoload('Valves'          , 0x6000)
        widgets |= UI.autoload('Lcds'            , 0x7000)
        widgets |= UI.autoload('Vumeters'        , 0x8000)
        widgets |= UI.autoload('JogWheels'       , 0x9000)        
        UI.widgets = widgets
            
    def redraw( ):
        app = UI.app
        app.screen.blit(app.backdrop, (0, 0))
        for _,w in UI.widgets.items():
            w.render( app )            
            
    def handle( event, app ):
        # Comprobar si el evento es recibido por un widget
        for key,w in UI.widgets.items():
            if w.handle( event, app ) and w.drag:
                return True
                
        # Comprobar si el evento es recibido por el gestor de ficheros (desactivado)
        # if FileMan.handle(app, event ): return True
        
        # Comprobar si el evento es recibido por el interfaz 
        ventana  = app.window
        kind     = event.type
        if   kind == pygame.QUIT: return False
        elif kind == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                if event.pos[1] <= 32:  # Solo en los primeros 32px
                    app.drag = True
                    app.window_x, app.window_y = ventana.position
                    app.window_ox = event.pos[0]
                    app.window_oy = event.pos[1]
                else:
                    print(f"Click @ {event.pos}")
                return True
        elif event.type == pygame.MOUSEBUTTONUP: 
            if event.button == 1: app.drag = False
        elif event.type == pygame.MOUSEMOTION:
            if app.drag:
                app.window_x, app.window_y = ventana.position
                nueva_x = app.window_x + (event.pos[0] - app.window_ox)
                nueva_y = app.window_y + (event.pos[1] - app.window_oy)
                ventana.position = (nueva_x, nueva_y)
            else:
                # otros eventos de movimiento aquí
                pass            
        elif event.type == pygame.KEYDOWN:
            app.ui.finetune     = True if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else False
            app.ui.input['alt'] = True if (pygame.key.get_mods() & pygame.KMOD_ALT) else False
            if   event.key == pygame.K_SPACE    : app.ui.input['space'] = True
            elif event.key == pygame.K_RETURN   : app.ui.input['enter'] = True 
            elif event.key == pygame.K_F4 and app.ui.input['alt']: return False
        elif event.type == pygame.KEYUP:
            app.ui.finetune     = True if (pygame.key.get_mods() & pygame.KMOD_SHIFT) else False
            app.ui.input['alt'] = True if (pygame.key.get_mods() & pygame.KMOD_ALT) else False
            if   event.key == pygame.K_SPACE    : app.ui.input['space'] = False
            elif event.key == pygame.K_RETURN   : app.ui.input['enter'] = False        
        return True                    