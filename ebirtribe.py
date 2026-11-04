import  pygame
import  logo
import  sys
from    app         import App

def main(archivo_entrada=None):
    App.init(pygame, archivo_entrada)
    while App.run:
        App.update()
    App.exit()
    
if __name__ == "__main__":
    if len(sys.argv) < 2: main()
    else: main(sys.argv[1])