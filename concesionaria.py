from tkinter import * 
from gui.ventana import *
from utils.utils import Utils

def main() :
    utils = Utils()
    
    root = Tk()
    root.title("Hola Mundo | Luz - Cerro - Kevin")
    root.resizable(False, False)
    root.geometry(utils.calcular_posicion_ventana(root, 1300, 650))
    # ventana.iconbitmap('img/logo.ico')

    app = Ventana(root)     
    app.mainloop()

if __name__ == '__main__' :
    main()