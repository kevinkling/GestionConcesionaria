from tkinter import * 
from gui.ventana import *
from utils.utils import Utils
from utils.requeriments import InstalarRequerimientos

def main() :
    utils = Utils()
    instalar_requerimiento = InstalarRequerimientos()
    instalar_requerimiento.install_packages()
    
    root = Tk()
    root.title("Hola Mundo | Luz - Cerross - Kevin")
    root.resizable(False, False)
    root.geometry(utils.calcular_posicion_ventana(root, 1300, 650))
    # ventana.iconbitmap('img/logo.ico')

    app = Ventana(root)     
    app.mainloop()

if __name__ == '__main__' :
    main()