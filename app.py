from    ui          import UI, Fonts
from    filesys     import FileMan
from    emx         import EMX1

class App:
    name        = "LUSH EbirTribE EMX-1"
    version     = "1.0"
    description = "Music Production Workstation"
    width       = 1497
    height      = 955
    backdrop    = None
    clock       = None
    drag        = False
    run         = True
    screen      = None
    stream      = None
    emx         = None 
    ui          = None
    waveforms   = []
    mouse_x     = 0
    mouse_y     = 0
    mouse_state = [0,0,0,0,0,0]
    pygame      = None
    window      = None
    window_ox   = 0
    window_oy   = 0
    window_x    = 0
    window_y    = 0
    
    def init( pygame, archivo_entrada ):
        App.pygame  = pygame
        App.ui      = UI
        App.window  = App.ui.init( App, archivo_entrada )
        App.emx     = EMX1(App, archivo_entrada)
        FileMan.init( pygame, App )
        #App.stream.start()
        
    def update():
        App.clock.tick(60)
        App.mouse_x, App.mouse_y = App.pygame.mouse.get_pos()
        App.mouse_state          = App.pygame.mouse.get_pressed()
        for evento in App.pygame.event.get():
            App.run = App.ui.handle( evento, App )   
        UI.redraw()
        #FileMan.update()
        #FileMan.render(App)
        #App.rex.update()
        App.pygame.display.flip()

    def exit():
        App.emx.destroy()
        App.pygame.quit()
    