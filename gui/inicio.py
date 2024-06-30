import tkinter as tk
from tkinter import ttk
from tkinter import *

class Inicio(Frame) :
    def __init__(self, master=None) :
        super().__init__(master)
        self.master = master
        # self.pack()
        self.crear_widgets()

    def crear_widgets(self):
        # Cargar la imagen con tkinter PhotoImage
        self.imagen = tk.PhotoImage(file="img/logo_generico.png")
        

        # Crear un Label y asignar la imagen
        self.label_imagen = ttk.Label(self, image=self.imagen)
        self.label_imagen.pack()