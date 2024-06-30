from tkinter import *
from tkinter import ttk
from gui.inicio import *
from gui.gestion_clientes import *
from gui.gestion_vehiculos import *
from gui.gestion_transacciones import *

from tkinter import messagebox as msg
from modelos.vehiculo import Vehiculo


class Ventana(Frame) :
    def __init__(self, master=None) :
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill=BOTH)
        self.crear_pestanias()
        
        self.auto = Vehiculo()

    def crear_pestanias(self):
        """ Funcion que crea los frame principales """
        self.ventana = ttk.Notebook(self)
        self.ventana.pack(expand=True, fill=BOTH)
        
        ## Creo los frames
        self.frame_inicio = Inicio(self.ventana)
        self.frame_gestion_vehiculos = GestionVehiculos(self.ventana)
        self.frame_gestion_clientes = GestionClientes(self.ventana)
        self.frame_gestion_transacciones = GestionTransacciones(self.ventana)
        
        ## Añado las pestañas a la notebook
        self.ventana.add(self.frame_inicio, text="Inicio")
        self.ventana.add(self.frame_gestion_vehiculos, text="Gestionar Vehiculos")
        self.ventana.add(self.frame_gestion_clientes, text="Gestionar Clientes")
        self.ventana.add(self.frame_gestion_transacciones, text="Transacciones")
        
        ## Pestaña por defecto
        self.ventana.select(self.frame_gestion_transacciones)

        ## Evento para cambiar de pestaña
        self.ventana.bind("<<NotebookTabChanged>>", self.se_cambio_pestania)
        
    def se_cambio_pestania(self, event) :
        selected_tab = event.widget.tab('current')['text']
        if selected_tab == "Gestionar Vehiculos":
            self.frame_gestion_vehiculos.actualizar_grilla(True)
        if selected_tab == "Transacciones":
            self.frame_gestion_transacciones.actualizar_selectores()