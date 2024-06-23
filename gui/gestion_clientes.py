from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
from modelos.cliente import Cliente

class GestionClientes(Frame) :
    
    def __init__(self, master=None) :
        super().__init__(master)
        self.master = master
        self.font = "Comic Sans"
        self.font_form = (self.font, 10, "bold")
        
        self.cliente_man = Cliente()
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
        self.crear_formulario()
        self.crear_barra_busqueda()
        self.crear_grilla()
        self.rellenar_grilla(False)
        self.crar_botones_edicion_eliminacion()
        
    def crear_formulario(self) :
        """ Crea los widgets del formulario """
        ## Etiquetas y Entradas
        etiquetas = [
            ("Documento :", 0),
            ("Nombre :", 1),
            ("Apellido :", 2),
            ("Dirección :", 3),
            ("Teléfono :", 4),
            ("Email :", 5),
        ]
        
        for texto, fila in etiquetas:
            etiqueta = Label(self.form, text=texto, width=13, anchor=E, font=self.font_form)
            etiqueta.grid(row=fila, column=0, padx=5, pady=5)
            
        self.ingreso_documento = Entry(self.form, width=30)
        self.ingreso_documento.grid(row=0, column=1)

        self.ingreso_nombre = Entry(self.form, width=30)
        self.ingreso_nombre.grid(row=1, column=1)

        self.ingreso_apellido = Entry(self.form, width=30)
        self.ingreso_apellido.grid(row=2, column=1)

        self.ingreso_direccion = Entry(self.form, width=30)
        self.ingreso_direccion.grid(row=3, column=1)

        self.ingreso_telefono = Entry(self.form, width=30) #, validate="focusout", validatecommand=(self.validacion_ingreso_anio, "%P")
        self.ingreso_telefono.grid(row=4, column=1)

        self.ingreso_correo = Entry(self.form, width=30)
        self.ingreso_correo.grid(row=5, column=1)
        
        self.btn_guardar_nuevo = Button(self.form, text="Guardar", font=self.font_form, height=2, command=self.crear_cliente)
        self.btn_guardar_nuevo.grid(row=len(etiquetas), columnspan=2, pady=20)
    
    
    def crear_barra_busqueda(self) :
        """ Crea la barra de busqueda """
        self.etiqueta_buscar = Label(self.frame_busqueda, text="Buscar por :")
        self.etiqueta_buscar.place(relx=0.2, rely=0.15, height=20)
        self.combo_tipo_busqueda = ttk.Combobox(self.frame_busqueda, values=["Documento", "Nombre", "Apellido", "Nombre y Apellido"], state="readonly")
        self.combo_tipo_busqueda.place(relx=0.3, rely=0.15, height=24)
        self.combo_tipo_busqueda.set("Documento")
        self.ingreso_busqueda = Entry(self.frame_busqueda)
        self.ingreso_busqueda.place(relx=0.45, rely=0.15, height=24)
        self.btn_buscar = Button(self.frame_busqueda, text="Buscar", font=self.font_form, command=self.buscar_y_actualizar)
        self.btn_buscar.place(relx=0.60, rely=0.15, height=24)
    
    def crear_grilla(self) :
        """ Crea los widgets de la grilla """
        self.grilla = ttk.Treeview(self.area_grilla)
        self.grilla.pack(expand=True, fill=BOTH)
        
        self.grilla['columns'] = ["apellido", "documento", "direccion", "telefono", "correo"]
        self.grilla.column("#0", width=100)
        self.grilla.column("apellido", width=100, anchor=CENTER)
        self.grilla.column("documento", width=100, anchor=CENTER)
        self.grilla.column("direccion", width=200, anchor=CENTER)
        self.grilla.column("telefono", width=100, anchor=CENTER)
        self.grilla.column("correo", width=200, anchor=CENTER)
        
        self.grilla.heading("#0", text="Documento", anchor=CENTER)
        self.grilla.heading("apellido", text="Nombre", anchor=CENTER)
        self.grilla.heading("documento", text="Apellido", anchor=CENTER)
        self.grilla.heading("direccion", text="Direccion", anchor=CENTER)
        self.grilla.heading("telefono", text="Telefono", anchor=CENTER)
        self.grilla.heading("correo", text="Correo", anchor=CENTER)
        
    def crar_botones_edicion_eliminacion(self) :
        """ Crea los widget de los botones de edicion y eliminacion """
        self.btn_editar = Button(self.area_botones_accionarios, text="Editar", font=self.font_form, padx=5, pady=4, command=self.editar_cliente)
        self.btn_editar.place(x=360, y=30, width=50)
        self.btn_editar.configure(padx=8, pady=5)
        
        self.btn_eliminar = Button(self.area_botones_accionarios, text="Eliminar Seleccionado/s", font=self.font_form, padx=5, pady=4, command=self.eliminar_cliente)
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
            clientes = self.cliente_man.obtener_lista_clientes()
        else :
            clientes = self.cliente_man.buscar_cliente(self.combo_tipo_busqueda.get(), self.ingreso_busqueda.get())
        
        self.grilla.delete(*self.grilla.get_children())
        for cliente in clientes :
            dni = cliente['documento']
            nombre = cliente['nombre']
            apellido = cliente['apellido']
            direccion = cliente['direccion']
            telefono = cliente['telefono']
            correo = cliente['correo_electronico']
            
            self.grilla.insert("", END, text=dni, 
                        values=(nombre, apellido, direccion, telefono, correo))
            
    def actualizar_grilla(self) :
        """ Funcion que borra los items de la grilla y los vulve a rellenar """
        self.grilla.delete(*self.grilla.get_children())
        self.rellenar_grilla(False)
        
    def crear_cliente(self) :
        """ Funcion encargada de crear el cliente nuevo """
        # if not self.validar_formulario_completo() :
        #     msg.showwarning("Formulario incompleto", "Por favor, complete todos los campos requeridos antes de enviar el formulario.")
        #     return
        if self.cliente_man.documento_existente(self.ingreso_documento.get()) :
            msg.showwarning("Documento ya existente", "Por favor, verifique el documento")
            return
        
        nuevo_cliente = {
            "id_cliente":self.cliente_man.obtener_ultimo_id() + 1,
            "nombre": self.ingreso_nombre.get().capitalize(),
            "apellido": self.ingreso_apellido.get().capitalize(),
            "documento": int(self.ingreso_documento.get()),
            "direccion": self.ingreso_direccion.get().capitalize(),
            "telefono": self.ingreso_telefono.get(),
            "correo_electronico": self.ingreso_correo.get()
        }
        
        ## Si se creo bien actualizo la grilla y limpio el formulario
        if self.cliente_man.crear_cliente(nuevo_cliente) :
            self.actualizar_grilla()
            self.limpiar_formulario()
            self.ingreso_documento.focus()
            
    def eliminar_cliente(self) :
        """ Funcion encargada de eliminar uno o mas vehiculos """
        clientes_seleccionados = self.grilla.selection() ## Obtiene lo que tenemos seleecionados en la grilla 
        doc_clientes_a_eliminar = []
        if not clientes_seleccionados :
            msg.showwarning("Selección Incorrecta", "Debe seleccionar uno o mas clientes a eliminar")
            return
        
        ## Obtengo las patentes de los registros seleccionados
        for cliente in clientes_seleccionados:
            documento = self.grilla.item(cliente, "text")
            doc_clientes_a_eliminar.append(documento)
            
        ## Confirmacion de eliminacion, si se acepta se eliminan y se actualiza la grilla
        if (msg.askyesno(message=f"Se eliminara {len(doc_clientes_a_eliminar)} registros ¿Desea continuar?", title="Eliminar")) :
            self.cliente_man.eliminar(doc_clientes_a_eliminar)
            self.actualizar_grilla()
            msg.showinfo("Eliminación Completa", f"Se eliminaron los clientes exitosamente.")
            
    def editar_cliente(self) :
        """ Funcion encargada de editar un cliente """
        clientes_seleccionados = self.grilla.selection()
        
        ## Control para que se seleccione un solo registro de la grilla
        if len(clientes_seleccionados) != 1 :
            msg.showwarning("Selección Incorrecta", "Debe seleccionar un cliente a editar")
            return
        
        documento = self.grilla.item(clientes_seleccionados[0], "text")
        ## Obtengo el id del seleccionado, obtengo los datos y lo cargo en el formulario
        id_cliente = self.cliente_man.obtener_id_por_documento(documento)
        self.datos_cliente = self.cliente_man.buscar_cliente_por_id(id_cliente)
        self.limpiar_formulario() ## Si no limpio el formulario no puedo apretar dos veces seguidas "editar"
        self.rellenar_form_edicion()
        self.btn_guardar_nuevo.configure(text="Actualizar", command=self.actualizar_cliente)
        
    def rellenar_form_edicion(self) :
        """ Funcion encargada de rellenar el formulario con los datos del cliente a editar """
        self.ingreso_documento.insert(0, self.datos_cliente.get('documento'))
        self.ingreso_nombre.insert(0, self.datos_cliente.get('nombre'))
        self.ingreso_apellido.insert(0, self.datos_cliente.get('apellido'))
        self.ingreso_direccion.insert(0, self.datos_cliente.get('direccion'))
        self.ingreso_telefono.insert(0, self.datos_cliente.get('telefono'))
        self.ingreso_correo.insert(0, self.datos_cliente.get('correo_electronico'))

    def actualizar_cliente(self) :
        """ Funcion encargada de guardar los datos una vez editado """
        # if not self.validar_formulario_completo() :
        #     msg.showwarning("Formulario incompleto", "Por favor, complete todos los campos requeridos antes de editar un vehiculo.")
        #     return
        if self.cliente_man.documento_existente(self.ingreso_documento.get()) :
            msg.showwarning("Documento ya existente", "Por favor, verifique el documento")
            return
        
        cliente_editado = {
            "id_cliente":self.datos_cliente.get('id_cliente'),
            "nombre": self.ingreso_nombre.get().capitalize(),
            "apellido": self.ingreso_apellido.get().capitalize(),
            "documento": int(self.ingreso_documento.get()),
            "direccion": self.ingreso_direccion.get().capitalize(),
            "telefono": self.ingreso_telefono.get(),
            "correo_electronico": self.ingreso_correo.get()
        }
        
        ## Si se edito bien actualizo la grilla y limpio el formulario
        if self.cliente_man.editar(cliente_editado) :
            self.actualizar_grilla()
            self.limpiar_formulario()
            self.btn_guardar_nuevo.configure(text="Guardar", command=self.crear_cliente)
            self.ingreso_documento.focus()
            msg.showinfo("Edición Exitosa", "El cliente ha sido editado correctamente.")

    
    def limpiar_formulario(self) :        
        """ Funcion encargada de borrar el contenido de los campos del formulario """
        self.ingreso_documento.delete(0, END)
        self.ingreso_nombre.delete(0, END)
        self.ingreso_apellido.delete(0, END)
        self.ingreso_direccion.delete(0, END)
        self.ingreso_telefono.delete(0, END)
        self.ingreso_correo.delete(0, END)