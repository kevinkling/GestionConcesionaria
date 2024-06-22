from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
from modelos.vehiculo import Vehiculo

class GestionVehiculos(Frame) :
    
    def __init__(self, master=None) :
        super().__init__(master)
        self.master = master
        self.font = "Comic Sans"
        self.font_form = (self.font, 10, "bold")
        
        self.vehiculo_man = Vehiculo()
        self.crear_widgets()
        
    def crear_widgets(self):
        """ Funcion encargada de crear los frames y llamar a las fuciones que crean los widget """

        ## Frame del area de grilla y busqueda
        self.area_busqueda_grilla = Frame(self)
        self.area_busqueda_grilla.pack(side=LEFT, expand=True, fill=BOTH)
        
        ## Frame del formulario
        self.form = Frame(self, width=350, height=300)
        self.form.pack(side=TOP, after=self.area_busqueda_grilla, pady=80, padx=5)

        ## Frame de busqueda
        self.frame_busqueda = LabelFrame(self.area_busqueda_grilla, text="Búsqueda")
        self.frame_busqueda.pack(side=TOP, expand=False, fill=X, padx=5, pady=5)
        self.frame_busqueda.configure(height=70)
        
        ## Frame de grilla
        self.area_grilla = Frame(self.area_busqueda_grilla)
        self.area_grilla.pack(expand=True, fill=BOTH, padx=5)

        ## Frame de botones de edicion y eliminacion
        self.area_botones_accionarios = Frame(self.area_busqueda_grilla)
        self.area_botones_accionarios.pack(side=BOTTOM, expand=True, fill=BOTH, padx=5, pady=5)
        
        ## Llamada a funciones creadoras de widgets
        self.crear_barra_busqueda()
        self.crear_grilla()
        self.rellenar_grilla(False)
        self.crear_formulario()
        self.crar_botones_edicion_eliminacion()

    def crear_formulario(self) :
        """ Crea los widgets del formulario """
        ## Etiquetas y Entradas
        etiquetas = [
            ("Patente :", 0),
            ("Marca :", 1),
            ("Modelo :", 2),
            ("Tipo :", 3),
            ("Año :", 4),
            ("Kilometraje :", 5),
            ("Precio Compra :", 6),
            ("Precio Venta :", 7),
            ("Estado :", 8)
        ]
        
        for texto, fila in etiquetas:
            etiqueta = Label(self.form, text=texto, width=13, anchor=E, font=self.font_form)
            etiqueta.grid(row=fila, column=0, padx=5, pady=5)
            
            ## Hice esto para la personalizacion del widget de estado solo
            if texto == 'Estado :' :
                self.ingreso_estado = ttk.Combobox(self.form, values=["Disponible", "Reservado"], state="readonly", width=17)
                self.ingreso_estado.set("Disponible") # Seteo el estado a disponible
                self.ingreso_estado.grid(row=8, column=1)
                continue
            
        self.ingreso_patente = Entry(self.form)
        self.ingreso_patente.grid(row=0, column=1)

        self.ingreso_marca = Entry(self.form)
        self.ingreso_marca.grid(row=1, column=1)

        self.ingreso_modelo = Entry(self.form)
        self.ingreso_modelo.grid(row=2, column=1)

        self.ingreso_tipo = Entry(self.form)
        self.ingreso_tipo.grid(row=3, column=1)

        self.ingreso_anio = Entry(self.form, validate="focusout", validatecommand=(self.validacion_ingreso_anio, "%P"))
        self.ingreso_anio.grid(row=4, column=1)

        self.ingreso_kms = Entry(self.form)
        self.ingreso_kms.grid(row=5, column=1)

        self.ingreso_precio_compra = Entry(self.form)
        self.ingreso_precio_compra.grid(row=6, column=1)

        self.ingreso_precio_venta = Entry(self.form)
        self.ingreso_precio_venta.grid(row=7, column=1)     
        
        self.btn_guardar_nuevo = Button(self.form, text="Guardar", command=self.crear_vehiculo, font=self.font_form, height=2)
        self.btn_guardar_nuevo.grid(row=len(etiquetas), columnspan=2, pady=20)

    def crear_barra_busqueda(self) :
        """ Crea la barra de busqueda """
        self.etiqueta_buscar = Label(self.frame_busqueda, text="Buscar por :")
        self.etiqueta_buscar.place(relx=0.2, rely=0.15, height=20)
        self.combo_tipo_busqueda = ttk.Combobox(self.frame_busqueda, values=["Patente", "Marca", "Modelo", "Precio de compra", "Precio de venta"], state="readonly")
        self.combo_tipo_busqueda.place(relx=0.3, rely=0.15, height=24)
        self.combo_tipo_busqueda.set("Patente")
        self.ingreso_busqueda = Entry(self.frame_busqueda)
        self.ingreso_busqueda.place(relx=0.45, rely=0.15, height=24)
        self.btn_buscar = Button(self.frame_busqueda, text="Buscar", command=self.buscar_y_actualizar, font=self.font_form)
        self.btn_buscar.place(relx=0.60, rely=0.15, height=24)
    
    def crear_grilla(self) :
        """ Crea los widgets de la grilla """
        self.grilla = ttk.Treeview(self.area_grilla)
        self.grilla.pack(expand=True, fill=BOTH)
        
        self.grilla['columns'] = ["marca", "modelo", "tipo", "anio", "kms", "pre_compra", "pre_venta", "estado"]
        self.grilla.column("#0", width=100)
        self.grilla.column("marca", width=100, anchor=CENTER)
        self.grilla.column("modelo", width=100, anchor=CENTER)
        self.grilla.column("tipo", width=100, anchor=CENTER)
        self.grilla.column("anio", width=100, anchor=CENTER)
        self.grilla.column("kms", width=100, anchor=CENTER)
        self.grilla.column("pre_compra", width=100, anchor=CENTER)
        self.grilla.column("pre_venta", width=100, anchor=CENTER)
        self.grilla.column("estado", width=100, anchor=CENTER)
        
        self.grilla.heading("#0", text="Patente", anchor=CENTER)
        self.grilla.heading("marca", text="Marca", anchor=CENTER)
        self.grilla.heading("modelo", text="Modelo", anchor=CENTER)
        self.grilla.heading("tipo", text="Tipo", anchor=CENTER)
        self.grilla.heading("anio", text="Año", anchor=CENTER)
        self.grilla.heading("kms", text="Kilometros", anchor=CENTER)
        self.grilla.heading("pre_compra", text="Precio Compra", anchor=CENTER)
        self.grilla.heading("pre_venta", text="Precio Venta", anchor=CENTER)
        self.grilla.heading("estado", text="Estado", anchor=CENTER)
    
    def crar_botones_edicion_eliminacion(self) :
        """ Crea los widget de los botones de edicion y eliminacion """
        self.btn_editar = Button(self.area_botones_accionarios, text="Editar", command=self.editar_vehiculo, font=self.font_form, padx=5, pady=4)
        self.btn_editar.place(x=360, y=30, width=50)
        self.btn_editar.configure(padx=8, pady=5)
        
        self.btn_eliminar = Button(self.area_botones_accionarios, text="Eliminar Seleccionado/s", command=self.eliminar_vehiculo, font=self.font_form, padx=5, pady=4)
        self.btn_eliminar.place(x=460, y=30, width=170)
        self.btn_eliminar.configure(padx=8, pady=5)
        
    def buscar_y_actualizar(self) :
        """ Funcion que realiza la busqueda y actualiza la grilla """
        self.grilla.delete(*self.grilla.get_children())
        ## Si el campo de busqueda no contiene nada me muestra la grilla sin filtros
        if self.ingreso_busqueda.get() == '' :
            self.rellenar_grilla(False)
        else :
            self.rellenar_grilla(True)

    def rellenar_grilla(self, es_busqueda) :
        """ Funcion que se encarga de rellenar la grilla.
            Si es_busqueda es false, mostrara todos los vehiculos"""
        if not es_busqueda :
            vehiculos = self.vehiculo_man.obtener_lista_vehiculos()
        else :
            vehiculos = self.vehiculo_man.buscar_vehiculo(self.combo_tipo_busqueda.get(), self.ingreso_busqueda.get())
        
        self.grilla.delete(*self.grilla.get_children())
        for auto in vehiculos :
            patente = auto['patente']
            marca = auto['marca']
            modelo = auto['modelo']
            tipo = auto['tipo']
            anio = auto['año']
            kms = auto['kilometraje']
            pre_compra = auto['precio_compra']
            pre_venta = auto['precio_venta']
            estado = auto['estado']
            
            self.grilla.insert("", END, text=patente, 
                        values=(marca, modelo, tipo, anio, kms, pre_compra, pre_venta, estado))
   
    def actualizar_grilla(self) :
        """ Funcion que borra los items de la grilla y los vulve a rellenar """
        self.grilla.delete(*self.grilla.get_children())
        self.rellenar_grilla(False)    

    def crear_vehiculo(self) :
        """ Funcion encargada de crear el vehiculo nuevo """
        if not self.validar_formulario_completo() :
            msg.showwarning("Formulario incompleto", "Por favor, complete todos los campos requeridos antes de enviar el formulario.")
            return
        patente = self.ingreso_patente.get().upper()
        patente_formato_valido = self.vehiculo_man.validar_formato_patente(patente)
        if not patente_formato_valido :
            msg.showwarning("Patente con Formato Incorrecto", "Por favor, ingrese la patente con formato correcto.")
            return
        if self.vehiculo_man.patente_existente(patente) :
            msg.showwarning("Patente ya existente", "Por favor, verifique la patente")
            return
        
        nuevo_vehiculo = {
            "id_vehiculo": self.vehiculo_man.obtener_ultimo_id() + 1,
            "patente": self.ingreso_patente.get().upper(),
            "marca": self.ingreso_marca.get().capitalize(),
            "modelo": self.ingreso_modelo.get().capitalize(),
            "tipo": self.ingreso_tipo.get().capitalize(),
            "año": int(self.ingreso_anio.get()),
            "kilometraje": int(self.ingreso_kms.get()),
            "precio_compra": float(self.ingreso_precio_compra.get()),
            "precio_venta": float(self.ingreso_precio_venta.get()),
            "estado": self.ingreso_estado.get()
        }
        
        ## Si se creo bien actualizo la grilla y limpio el formulario
        if self.vehiculo_man.crear_vehiculo(nuevo_vehiculo) :
            self.actualizar_grilla()
            self.limpiar_formulario()
            self.ingreso_patente.focus()
        
    def eliminar_vehiculo(self) :
        """ Funcion encargada de eliminar uno o mas vehiculos """
        patentes_seleccionadas = self.grilla.selection() ## Obtiene lo que tenemos seleecionados en la grilla 
        vehiculos_a_eliminar = []
        if not patentes_seleccionadas :
            msg.showwarning("Selección Incorrecta", "Debe seleccionar uno o mas vehiculos a eliminar")
            return
        
        ## Obtengo las patentes de los registros seleccionados
        for vehiculo in patentes_seleccionadas:
            patente = self.grilla.item(vehiculo, "text")
            vehiculos_a_eliminar.append(patente)
        
        ## Confirmacion de eliminacion, si se acepta se eliminan y se actualiza la grilla
        if (msg.askyesno(message=f"Se eliminara {len(vehiculos_a_eliminar)} registros ¿Desea continuar?", title="Eliminar")) :
            self.vehiculo_man.eliminar(vehiculos_a_eliminar)
            self.actualizar_grilla()
            msg.showinfo("Eliminación Completa", f"Se eliminaron los vehículos con patentes: {', '.join(vehiculos_a_eliminar)}")
            
    def editar_vehiculo(self) :
        """ Funcion encargada de editar un vehiculo """
        patentes_seleccionada = self.grilla.selection()
        
        ## Control para que se seleccione un solo registro de la grilla
        if len(patentes_seleccionada) != 1 :
            msg.showwarning("Selección Incorrecta", "Debe seleccionar un vehiculo a editar")
            return
        
        patente = self.grilla.item(patentes_seleccionada[0], "text")
        ## Obtengo el id del seleccionado, obtengo los datos y lo cargo en el formulario
        id_vehiculo = self.vehiculo_man.obtener_id_por_patente(patente)
        self.datos_vehiculo_edicion = self.vehiculo_man.buscar_vehiculo_por_id(id_vehiculo)
        self.limpiar_formulario() ## Si no limpio el formulario no puedo apretar dos veces seguidas "editar"
        self.rellenar_form_edicion()
        self.btn_guardar_nuevo.configure(text="Actualizar", command=self.actualizar_vehiculo)

    def rellenar_form_edicion(self) :
        """ Funcion encargada de rellenar el formulario con los datos del vehiculo a editar """
        self.ingreso_patente.insert(0, self.datos_vehiculo_edicion.get('patente'))
        self.ingreso_marca.insert(0, self.datos_vehiculo_edicion.get('marca'))
        self.ingreso_modelo.insert(0, self.datos_vehiculo_edicion.get('modelo'))
        self.ingreso_tipo.insert(0, self.datos_vehiculo_edicion.get('tipo'))
        self.ingreso_anio.insert(0, self.datos_vehiculo_edicion.get('año'))
        self.ingreso_kms.insert(0, self.datos_vehiculo_edicion.get('kilometraje'))
        self.ingreso_precio_compra.insert(0, self.datos_vehiculo_edicion.get('precio_compra'))
        self.ingreso_precio_venta.insert(0, self.datos_vehiculo_edicion.get('precio_venta'))
        self.ingreso_estado.set(self.datos_vehiculo_edicion.get('estado'))

    def actualizar_vehiculo(self) :
        """ Funcion encargada de guardar los datos una vez editado """
        
        if not self.validar_formulario_completo() :
            msg.showwarning("Formulario incompleto", "Por favor, complete todos los campos requeridos antes de editar un vehiculo.")
            return
        patente = self.ingreso_patente.get().upper()
        patente_formato_valido = self.vehiculo_man.validar_formato_patente(patente)
        if not patente_formato_valido :
            msg.showwarning("Patente con Formato Incorrecto", "Por favor, ingrese la patente con formato correcto.")
            return
        if self.vehiculo_man.patente_existente(patente) :
            msg.showwarning("Patente ya existente", "Por favor, verifique la patente")
            return
        
        vehiculo_editado = {
            "id_vehiculo": self.datos_vehiculo_edicion.get('id_vehiculo'),
            "patente": self.ingreso_patente.get().upper(),
            "marca": self.ingreso_marca.get().capitalize(),
            "modelo": self.ingreso_modelo.get().capitalize(),
            "tipo": self.ingreso_tipo.get().capitalize(),
            "año": int(self.ingreso_anio.get()),
            "kilometraje": int(self.ingreso_kms.get()),
            "precio_compra": float(self.ingreso_precio_compra.get()),
            "precio_venta": float(self.ingreso_precio_venta.get()),
            "estado": self.ingreso_estado.get()
        }
        
        ## Si se edito bien actualizo la grilla y limpio el formulario
        if self.vehiculo_man.editar(vehiculo_editado) :
            self.actualizar_grilla()
            self.limpiar_formulario()
            self.btn_guardar_nuevo.configure(text="Guardar", command=self.crear_vehiculo)
            self.ingreso_patente.focus()
            msg.showinfo("Edición Exitosa", "El vehículo ha sido editado correctamente.")
              
    def limpiar_formulario(self) :
        """ Funcion encargada de borrar el contenido de los campos del formulario """
        self.ingreso_patente.delete(0, END)
        self.ingreso_marca.delete(0, END)
        self.ingreso_modelo.delete(0, END)
        self.ingreso_tipo.delete(0, END)
        self.ingreso_anio.delete(0, END)
        self.ingreso_kms.delete(0, END)
        self.ingreso_precio_compra.delete(0, END)
        self.ingreso_precio_venta.delete(0, END)
        self.ingreso_estado.set("Disponible")
           
    ### FUNCIONES VALIDADORAS
    
    def validar_formulario_completo(self) :
        """ Funcion encargada de validar que todos los campos del formulario esten completos """
        if not (self.ingreso_patente.get() and self.ingreso_marca.get() and self.ingreso_modelo.get() and self.ingreso_tipo.get()
                and self.ingreso_anio.get() and self.ingreso_kms.get() and self.ingreso_precio_compra.get() and self.ingreso_precio_venta.get()) :
            return False
        return True
    
    #REVIEW - WIP
    def validar_y_ejecutar_accion(valor):
        if valor.isdigit():
            numero = int(valor)
            if numero > 0:
                msg.showinfo("Validación Exitosa", f"El número {numero} es positivo.")
            elif numero < 0:
                msg.showinfo("Validación Exitosa", f"El número {numero} es negativo.")
            else:
                msg.showinfo("Validación Exitosa", "El número ingresado es 0.")
        else:
            msg.showerror("Error de Validación", "Por favor ingrese un número válido.")

    #REVIEW - WIP
    def validacion_ingreso_anio(self) :
        self.validar_y_ejecutar_accion()
        return True