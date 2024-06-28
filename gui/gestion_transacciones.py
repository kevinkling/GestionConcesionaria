from tkcalendar import DateEntry 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
from modelos.cliente import Cliente
from modelos.vehiculo import Vehiculo
from modelos.transaccion import Transaccion
from utils.utils import Utils 

class GestionTransacciones(Frame) :
    
    def __init__(self, master=None) :
        super().__init__(master)
        self.master = master
        self.font = "Comic Sans"
        self.font_form = (self.font, 10, "bold")
        
        self.transaccion_man = Transaccion()
        self.cliente_man = Cliente()
        self.vehiculo_man = Vehiculo()
        self.utils_man = Utils()
        self.crear_widgets()
        
    def crear_widgets(self) :
        """ Funcion encargada de crear los frames y llamar a las fuciones que crean los widget """
        ## Frame que contiene el formulario para nueva transaccion
        self.area_form = Frame(self, width=300) 
        self.area_form.pack(side=RIGHT, expand=True, fill=Y)
        
        # Frame que contiene el listado de compras y sus filtros de busqueda
        self.area_listado_compra = LabelFrame(self, text="Listado Compras", font="arial 11", width=1000, height=10)
        self.area_listado_compra.pack(side=TOP, expand=True, fill=BOTH)
        
        # Frame que contiene el listado de compras y sus filtros de busqueda
        self.area_listado_venta = LabelFrame(self, text="Listado Ventas", font="arial 11", width=1000, height=325)
        self.area_listado_venta.pack(side=BOTTOM, expand=True, fill=BOTH)

        self.crear_widgets_formulario()
        self.crear_widgets_listado_compras()
        self.crear_widgets_listado_ventas()
        
        
    def crear_widgets_formulario(self) :
        self.lbl_cliente = Label(self.area_form, text="Cliente")
        self.lbl_cliente.pack(padx=10, pady=10)
        
        ## Crea el widget de seleccion de clientes
        self.lista_nombre_clientes = [""]
        for cliente in self.cliente_man.obtener_lista_clientes() :
            self.lista_nombre_clientes.append(f"{cliente.get('nombre')} {cliente.get('apellido')} - {cliente.get('documento')}")
        self.ingreso_cliente = ttk.Combobox(self.area_form, values=self.lista_nombre_clientes, state="readonly", width=35)
        self.ingreso_cliente.pack(padx=10, pady=10)
        
        self.lbl_vehiculo = Label(self.area_form, text="Vehiculo")
        self.lbl_vehiculo.pack(padx=10, pady=10)
        
        ## Crea el widget de seleccion de vehiculos
        lista_autos = [""]
        for vehiculo in self.vehiculo_man.obtener_lista_vehiculos_disponibles() :
            lista_autos.append(f"{vehiculo.get('marca')} {vehiculo.get('modelo')} - {vehiculo.get('patente')}")
        self.ingreso_vehiculo = ttk.Combobox(self.area_form, values=lista_autos, state="readonly", width=25)
        self.ingreso_vehiculo.pack(padx=10, pady=10)
        
        self.lbl_operacion = Label(self.area_form, text="Tipo de Operación : ")
        self.lbl_operacion.pack(padx=10, pady=10)
        
        # FIXME - Hacer que cuando levante el form, las dos opciones esten deselccionadas
        self.value_radio_btn = StringVar()
        
        self.radio_btn_compra = Radiobutton(self.area_form, text="Compra", variable=self.value_radio_btn, value="Compra")
        self.radio_btn_compra.pack(padx=10, pady=10)
        
        self.radio_btn_venta = Radiobutton(self.area_form, text="Venta", variable=self.value_radio_btn, value="Venta")
        self.radio_btn_venta.pack(padx=10, pady=10)
        
        
        self.lbl_observacion = Label(self.area_form, text="Observaciónes")
        self.lbl_observacion.pack(padx=10, pady=10)
        
        self.txt_area = Text(self.area_form, wrap='word', width=40, height=10)
        self.txt_area.pack(padx=10, pady=10)
        
        self.btn_realizar_tran = Button(self.area_form, text="Realizar Transaccion", font=self.font_form, command=self.crear_transaccion_nueva, padx=5, pady=4)
        self.btn_realizar_tran.pack(padx=10, pady=10)
        
        

    def crear_widgets_listado_compras(self) :
        self.crear_widgets_seccion_busqueda_compra()
        self.grilla_compra = self.crear_grilla(self.area_listado_compra)
        self.rellenar_grilla(True, False)

    def crear_widgets_listado_ventas(self) :
        self.crear_widgets_seccion_busqueda_venta()
        self.grilla_venta = self.crear_grilla(self.area_listado_venta)
        self.rellenar_grilla(False, False)
    
    def filtrado_listado_compras(self) :
        """ Funcion que realiza la busqueda y actualiza la grilla de transacciones de compra"""
        # self.grilla_compra.delete(*self.grilla_compra.get_children())
        ## Si el campo de busqueda no contiene nada me muestra la grilla sin filtros
        msg.showinfo("", "POR HACER FILTRO DE LISTA DE COMPRAS")

    
    def filtrado_listado_ventas(self) :
        msg.showinfo("", "POR HACER FILTRO DE LISTA DE VENTAS")
    
    def crear_grilla(self, area) :
        columnas = ["ID","Vehiculo", "Cliente", "Fecha", "Monto", "Observaciones"]
        self.grilla = ttk.Treeview(area, columns=columnas, show="headings")
        for col in columnas :
            self.grilla.heading(col, text=col)
            self.grilla.column(col, minwidth=9, width=100)
        self.grilla.pack(expand=True, fill=BOTH)
        return self.grilla
    

    def rellenar_grilla(self, es_compra, es_busqueda=False) :
        if es_compra :
            transacciones = self.transaccion_man.obtener_lista_transacciones_compra()
        else :
            transacciones = self.transaccion_man.obtener_lista_transacciones_venta()
                  
        self.borrar_elementos_lista(es_compra)
        for tran in transacciones :
            id = tran.get('id_transaccion')
            vehiculo = self.vehiculo_man.obtener_marca_modelo_por_id(tran.get('id_vehiculo'))
            cliente =  self.cliente_man.obtener_nombre_apellido_por_id(tran.get('id_cliente'))
            fecha = tran.get('fecha')
            monto = tran.get('monto')
            observaciones = tran.get('observaciones')
            if es_compra :
                self.grilla_compra.insert("", END, values=(id, vehiculo, cliente, fecha, monto, observaciones))
            else : 
                self.grilla_venta.insert("", END, values=(id, vehiculo, cliente, fecha, monto, observaciones))
            
    
    def actualizar_grilla(self, es_compra) :
        self.rellenar_grilla(es_compra)
    
    def borrar_elementos_lista(self, es_compra) :
        """ Funcion que borra los elementos de grilla.
        Si es_compra = True, entonces borra los elementos de la grilla de compra 
        Si es_compra = False, entonces borra los elementos de la grilla de venta. """
        if es_compra :
            self.grilla_compra.delete(*self.grilla_compra.get_children())
        else : 
            self.grilla_venta.delete(*self.grilla_venta.get_children())
            
        
    def crear_widgets_seccion_busqueda_compra(self) :
        seccion_busqueda = Frame(self.area_listado_compra)
        seccion_busqueda.pack()
        
        self.lbl_fecha_desde_compra = Label(seccion_busqueda, text="Fecha Desde: ", padx=10, pady=10)
        self.lbl_fecha_desde_compra.grid(row=0, column=0)
        
        self.entry_fecha_desde_compra = DateEntry(seccion_busqueda, padx=10, pady=10)
        self.entry_fecha_desde_compra.grid(row=0, column=1)
        
        self.lbl_fecha_hasta_compra = Label(seccion_busqueda, text="Fecha Hasta: ", padx=10, pady=10)
        self.lbl_fecha_hasta_compra.grid(row=0, column=2)
        
        self.entry_fecha_hasta_compra = DateEntry(seccion_busqueda, padx=10, pady=10)
        self.entry_fecha_hasta_compra.grid(row=0, column=3)
        
        self.lbl_cliente_compra = Label(seccion_busqueda, text="Cliente: ", padx=10, pady=10)
        self.lbl_cliente_compra.grid(row=0, column=4)
        
        
        self.lista_nombre_clientes = []
        for cliente in self.cliente_man.obtener_lista_clientes() :
            self.lista_nombre_clientes.append(f"{cliente.get('nombre')} {cliente.get('apellido')} - {cliente.get('documento')}")
            
        self.combo_lista_clientes_compra = ttk.Combobox(seccion_busqueda, values=self.lista_nombre_clientes, state="readonly", width=25)
        self.combo_lista_clientes_compra.grid(row=0, column=5)
        
        self.lbl_vehiculo_compra = Label(seccion_busqueda, text="Vehiculo: ", padx=10, pady=10)
        self.lbl_vehiculo_compra.grid(row=0, column=7)
        
        lista_autos = []
        for vehiculo in self.vehiculo_man.obtener_lista_vehiculos() :
            lista_autos.append(f"{vehiculo.get('marca')} {vehiculo.get('modelo')} - {vehiculo.get('patente')}")
        
        self.combo_lista_vehiculos = ttk.Combobox(seccion_busqueda, values=lista_autos, state="readonly", width=25)
        self.combo_lista_vehiculos.grid(row=0, column=8)
        
        self.btn_buscar_compra = Button(seccion_busqueda, text="Filtrar", font=self.font_form, command=self.filtrado_listado_compras)
        self.btn_buscar_compra.grid(row=0, column=9, padx=10)
        
        
    def crear_widgets_seccion_busqueda_venta(self) :
        seccion_busqueda = Frame(self.area_listado_compra)
        seccion_busqueda.pack()
        
        self.lbl_fecha_desde_venta = Label(seccion_busqueda, text="Fecha Desde: ", padx=10, pady=10)
        self.lbl_fecha_desde_venta.grid(row=0, column=0)
        
        self.entry_fecha_desde_venta = DateEntry(seccion_busqueda, padx=10, pady=10)
        self.entry_fecha_desde_venta.grid(row=0, column=1)
        
        self.lbl_fecha_hasta_venta = Label(seccion_busqueda, text="Fecha Hasta: ", padx=10, pady=10)
        self.lbl_fecha_hasta_venta.grid(row=0, column=2)
        
        self.entry_fecha_hasta_venta = DateEntry(seccion_busqueda, padx=10, pady=10)
        self.entry_fecha_hasta_venta.grid(row=0, column=3)
        
        self.lbl_cliente_venta = Label(seccion_busqueda, text="Cliente: ", padx=10, pady=10)
        self.lbl_cliente_venta.grid(row=0, column=4)
        
        
        lista_nombre_clientes = []
        for cliente in self.cliente_man.obtener_lista_clientes() :
            lista_nombre_clientes.append(f"{cliente.get('nombre')} {cliente.get('apellido')} - {cliente.get('documento')}")
            
        self.combo_lista_clientes_venta = ttk.Combobox(seccion_busqueda, values=lista_nombre_clientes, state="readonly", width=25)
        self.combo_lista_clientes_venta.grid(row=0, column=5)
        
        self.lbl_vehiculo_venta = Label(seccion_busqueda, text="Vehiculo: ", padx=10, pady=10)
        self.lbl_vehiculo_venta.grid(row=0, column=7)
        
        lista_autos = []
        for vehiculo in self.vehiculo_man.obtener_lista_vehiculos() :
            lista_autos.append(f"{vehiculo.get('marca')} {vehiculo.get('modelo')} - {vehiculo.get('patente')}")
        
        self.combo_lista_vehiculos_venta = ttk.Combobox(seccion_busqueda, values=lista_autos, state="readonly", width=25)
        self.combo_lista_vehiculos_venta.grid(row=0, column=8)
        
        self.btn_buscar_venta = Button(seccion_busqueda, text="Filtrar", font=self.font_form, command=self.filtrado_listado_ventas)
        self.btn_buscar_venta.grid(row=0, column=9, padx=10)
        
        
        
    def crear_transaccion_nueva(self) :
        """ Funcion encargada de crear la transaccion nueva """
        
        # CONTROL DE QUE HAYA SELECCIONADO UNA SOLA BUTTON
        # CONTROL DE QUE HAYA COMPLETADO TODO
        
        patente_auto_elegido =  self.ingreso_vehiculo.get().split('-')[1].strip()
        documento_cliente_elegido = int(self.ingreso_cliente.get().split('-')[1].strip())
        id_vehiculo = self.vehiculo_man.obtener_id_por_patente(patente_auto_elegido)
        
        nueva_transaccion = {
            "id_transaccion": self.transaccion_man.obtener_ultimo_id() + 1,
            "id_vehiculo": id_vehiculo,
            "id_cliente": self.cliente_man.obtener_id_por_documento(documento_cliente_elegido),
            "tipo_transaccion": self.value_radio_btn.get(), 
            "fecha": self.utils_man.fecha_hoy_yyyy_mm_dd(), ## Fecha de hoy
            "monto": self.obtener_monto(self.value_radio_btn.get(), patente_auto_elegido),
            "observaciones": self.txt_area.get("1.0", END).strip()
        }
        
        if self.transaccion_man.crear_transaccion(nueva_transaccion) :
            self.limpiar_formulario()
            ## Hago este control para que actualice solo la grilla necesaria 
            if self.value_radio_btn.get() == "Compra" :
                self.actualizar_grilla(True)
            else :
                self.vehiculo_man.marcar_como_vendido(id_vehiculo)
                self.actualizar_grilla(False)

    def obtener_monto(self, tipo_operacion, patente_auto_elegido) :
        if tipo_operacion == "Compra" :
            ## Si la operacion es de tipo compra voy a buscar el monto de venta del vehiculo
            return self.vehiculo_man.obtener_monto_venta(patente_auto_elegido)
        else :
            ## Sino buscare el precio de compra
            return self.vehiculo_man.obtener_monto_compra(patente_auto_elegido)
        
    
    def limpiar_formulario(self) :
        # TODO FALTA LIMPIAR LOS RADDIO BUTON
        self.ingreso_cliente.set("")
        self.ingreso_vehiculo.set("")
        self.txt_area.delete("1.0", END)
        