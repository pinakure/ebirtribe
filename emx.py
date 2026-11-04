import  numpy       as np

class EMXPlayer(object):    
    def __init__(self, app, filename=None, bpm=120):
        self.bpm                        = float(bpm)
        self.pitch                      = 0
        self.timer                      = 0
        self.data                       = None
        self.app                        = app        
        self.allocate()        
        if filename is not None:
            self.load(filename)
    
    def allocate(self):
        """ Pre-asignación de buffers de audio para evitar el Garbage Collector en tiempo real """
        self.BLOCK_SIZE                 = 1024
        self.idx_base                   = np.arange(0, self.BLOCK_SIZE, dtype=np.float32)
        self.buf_l_pitched              = np.zeros(self.BLOCK_SIZE, dtype=np.float32)
        self.buf_r_pitched              = np.zeros(self.BLOCK_SIZE, dtype=np.float32)
    
    def load(self, filename):
        """ Load a specific patch from file """
        self.filename = filename
        try:
            with open( filename, "rb" ) as f:
                self.data       = f.read()        
                self.filesize   = len( self.data )
            if not self.process():
                print(f"Parche no válido: {filename}")
        except FileNotFoundError:
            print(f"Archivo no encontrado: {filename}")
            return
        
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
        