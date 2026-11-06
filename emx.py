import  numpy       as np

class EMXPartHandler(object):
    def __init__(self, emx):
        self.emx        = emx
        app             = emx.app
        self.buttons    = [ app.ui.widgets[k] for k,w in app.ui.widgets.items() if 'SELECT_' in w.name ]
        
    def handle(self, button_index):
        [ self.buttons[k]._setValue(True if k == button_index else False) for k in range(len(self.buttons)) ]
        button = self.buttons[ button_index ]
        # button.

class EMXEffectHandler(object):
    COMPRESSOR      = 0x00     
    DELAY           = 0x01 
    DISTORTION      = 0x02     
    EQUALIZER       = 0x03     
    FILTER          = 0x04 
    PITCH           = 0x05 
    REVERB          = 0x06 
    RING_MOD        = 0x07
    
    def __init__(self, emx):
        self.emx            = emx
        self.active_effect  = 0x00
    
    def select_effect(self, effect ):
        self.active_effect = effect

class EMXMenuHandler(object):
    def __init__(self, emx):
        self.emx    = emx
        self.menu    = False
        self.exit    = False
        self.enter   = False
        self.f1      = False
        self.f2      = False
        self.f3      = False
    
    def update(self):
        # Do stuff 
        
        # Restore switches
        self.menu    = False
        self.exit    = False
        self.enter   = False
        self.f1      = False
        self.f2      = False
        self.f3      = False

class EMXFileSystem(object):
    def __init__(self, emx):
        self.emx = emx
    
    def load_song(self, song):
        """ Returns song data """
    
    def save_song(self, song):
        """ Stores song data """
        
    def get_song_list(self, page=0):
        """ Returns requested song list page """
        
    def load_patch_from_file(self, filename):
        """ Load a specific patch from file """
        self.filename = filename
        try:
            with open( filename, "rb" ) as f:
                self.data       = f.read()        
                self.filesize   = len( self.data )
            if not self.process():
                self.emx.debug(f"Invalid patch data @ '{filename}'")
        except FileNotFoundError:
            self.emx.debug(f"File '{filename}' not found.")
            return
        
class EMXSongData(object):
    def __init__(self, emx):
        self.emx  = emx
        self.data = self.allocate()
        
    def allocate(self):
        """ Reserve memory for song patterns """

class EMX1(object):    
    
    def debug(self, message):
        print(f'[ EMX-1 ]{message}')
    
    def __init__(self, app, filename=None, bpm=120):
        self.bpm        = float(bpm)
        self.pitch      = 0
        self.timer      = 0
        self.data       = None
        self.app        = app        
        self.fx         = EMXEffectHandler(self)
        self.fs         = EMXFileSystem(self)
        self.song_data  = EMXSongData(self)
        self.menu       = EMXMenuHandler(self)
        self.part       = EMXPartHandler(self)
        if filename is not None:
            self.fs.load_patch_from_file(filename)
    
    def allocate(self):
        """ Pre-asignación de buffers de audio para evitar el Garbage Collector en tiempo real """
        self.BLOCK_SIZE                 = 1024
        self.idx_base                   = np.arange(0, self.BLOCK_SIZE, dtype=np.float32)
        self.buf_l_pitched              = np.zeros(self.BLOCK_SIZE, dtype=np.float32)
        self.buf_r_pitched              = np.zeros(self.BLOCK_SIZE, dtype=np.float32)
         
    def process(self):
        """ Process patch parameters, reinitialize oscilators and DSP chains, set up ui elements accordingly with the patch parameters """
        return True
    
    def update(self):
        if not self.app.run: return 
        """ Do EMX stuff """
        
    def destroy(self):
        stream = getattr(self.app, "stream", None)
        if stream is not None:
            try:
                stream.stop()
            except Exception:
                pass
            try:
                stream.close()
            except Exception:
                pass
            self.app.stream = None
        