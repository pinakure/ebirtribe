import  inspect
import  pygame
from    pygame._sdl2    import Window
import  interface
from    interface       import JUMP_TABLE, CallBacks
import  os
import  filesys

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
        app.screen      = pygame.display.set_mode(( app.width, app.height ), pygame.NOFRAME)
        pygame          .display.set_caption(f"{ app.name } - { archivo_entrada.split(os.path.sep)[-1] if archivo_entrada is not None else ''}")
        app.resources   = UI.loadResources( app )
        app.backdrop    = app.resources.deck            
        UI.splash       (app)
        UI.loadFonts    (app)        
        app.clock       = pygame.time.Clock()
        return Window.from_display_module()
    
    def loadResources( app ):
        resources = ResourceContainer()
        for key, resource in interface.RESOURCES.items():
            print(f"[RESOURCE] Loading resources.{key} = '{resource}'")
            resources.__setattr__(key, filesys.loadImage(app, resource))
        return resources
        
    def loadFonts( app ):
        app.fonts.ocr       = pygame.font.Font(filesys.path("resources/fonts/ocr.ttf"   ), 22)
        app.fonts.lcd       = pygame.font.Font(filesys.path("resources/fonts/lcd.ttf"   ), 24)
        app.fonts.pbb       = pygame.font.Font(filesys.path("resources/fonts/pbb.otf"   ), 16)
        app.fonts.pb        = pygame.font.Font(filesys.path("resources/fonts/pb.otf"    ), 16)
        app.fonts.combi     = pygame.font.Font(filesys.path("resources/fonts/combi.otf" ), 16)
        app.fonts.tiny      = pygame.font.Font(filesys.path("resources/fonts/combi.otf" ),  8)
        app.fonts.m4g       = pygame.font.Font(filesys.path("resources/fonts/m4g.ttf"   ), 16)
        app.fonts.monospace = pygame.font.SysFont("Consolas", 16)
        
    def splash(app):
        app.screen.fill((20, 20, 25))
        app.fonts.heading   = pygame.font.SysFont("Consolas", 28, bold=True)
        app.screen.blit(app.backdrop, (0, 0))
        txt_titulo = app.fonts.heading.render(app.name.upper(), True, (130, 250, 50))
        app.screen.blit(txt_titulo, (app.width // 2 - txt_titulo.get_width() // 2, app.height // 3 - 40))
        pygame.display.flip()

    def create():
        knobs    = True if hasattr(interface, 'Knobs'    ) and inspect.isclass(getattr(interface, 'Knobs'    )) else False
        sliders  = True if hasattr(interface, 'Sliders'  ) and inspect.isclass(getattr(interface, 'Sliders'  )) else False
        faders   = True if hasattr(interface, 'Faders'   ) and inspect.isclass(getattr(interface, 'Faders'   )) else False
        buttons  = True if hasattr(interface, 'Buttons'  ) and inspect.isclass(getattr(interface, 'Buttons'  )) else False
        pads     = True if hasattr(interface, 'Pads'     ) and inspect.isclass(getattr(interface, 'Pads'     )) else False
        leds     = True if hasattr(interface, 'Leds'     ) and inspect.isclass(getattr(interface, 'Leds'     )) else False
        valves   = True if hasattr(interface, 'Valves'   ) and inspect.isclass(getattr(interface, 'Valves'   )) else False
        lcds     = True if hasattr(interface, 'Lcds'     ) and inspect.isclass(getattr(interface, 'Lcds'     )) else False
        vumeters = True if hasattr(interface, 'Vumeters' ) and inspect.isclass(getattr(interface, 'Vumeters' )) else False
        jogs     = True if hasattr(interface, 'JogWheels') and inspect.isclass(getattr(interface, 'JogWheels')) else False
        widgets  = {}
        widgets  |= interface.Knobs.get()       if knobs    else {}
        widgets  |= interface.Faders.get()      if faders   else {}
        widgets  |= interface.Buttons.get()     if buttons  else {}
        widgets  |= interface.Sliders.get()     if sliders  else {}
        widgets  |= interface.Pads.get()        if pads     else {}
        widgets  |= interface.Leds.get()        if leds     else {}
        widgets  |= interface.Valves.get()      if valves   else {}
        widgets  |= interface.Lcds.get()        if lcds     else {}
        widgets  |= interface.Vumeters.get()    if vumeters else {}   
        widgets  |= interface.JogWheels.get()   if jogs     else {}   
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
                return JUMP_TABLE.get(key, CallBacks.nop)(w, event, app)
                
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