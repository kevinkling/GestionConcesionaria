from tkinter import *

class GestionClientes(Frame) :
    
    def __init__(self, master=None) :
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill=BOTH)
        self.config(bg="red")
        self.crear_widgets()
        
    def crear_widgets(self):
        label = Label(self, text="Gestión de Vehículos")
        label.pack(pady=10, padx=10)
