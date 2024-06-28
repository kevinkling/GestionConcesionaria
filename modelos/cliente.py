from utils.utils import Utils 

"""
Esta clase contiene funciones de creacion, consulta, modificacion y eliminacion de clientes.
Tambien contiene funciones de validacion.
"""
class Cliente :
    def __init__(self):
        self.ruta_archivo = 'datos/clientes.json'
        self.utils = Utils()
        self.lista_clientes = self.utils.leer_archivo_json(self.ruta_archivo)
        # self.lista_clientes_encontrados = []
    
    def obtener_lista_clientes(self) :
        """ Retorna los clientes """
        return self.lista_clientes
      
    def crear_cliente(self, nuevo_cliente) :
        self.lista_clientes.append(nuevo_cliente)
        exito = self.utils.guardar_archivo_json(self.ruta_archivo, self.lista_clientes)
        return exito
    
    def obtener_ultimo_id(self) :
        """ Retorna el id del ultimo cliente o 0 si la lista esta vacia """
        ultimo_cliente = self.lista_clientes[-1]
        return ultimo_cliente.get('id_cliente', 0)
    
    def buscar_cliente(self, criterio, busqueda) :        
        match criterio :
            case "Documento" :
                return self.buscar_cliente_documento(busqueda)
            case "Apellido" :
                return self.buscar_cliente_apellido(busqueda)
            case "Nombre" :
                return self.buscar_cliente_nombre(busqueda)
            case "Nombre y Apellido" :
                return self.buscar_cliente_apellido_nombre(busqueda)
            
    def buscar_cliente_documento(self, documento) :
        lista_clientes = []
        for cliente in self.lista_clientes :
            if cliente.get('documento') == documento :
                lista_clientes.append(cliente)                
        return lista_clientes
    
    def buscar_cliente_apellido(self, apellido) :
        lista_clientes = []
        for cliente in self.lista_clientes :
            if cliente.get('apellido') == apellido :
                lista_clientes.append(cliente)                
        return lista_clientes
    
    def buscar_cliente_nombre(self, nombre) :
        lista_clientes = []
        for cliente in self.lista_clientes :
            if cliente.get('nombre') == nombre :
                lista_clientes.append(cliente)                
        return lista_clientes
    
    def buscar_cliente_apellido_nombre(self, nombre_apellido) :
        ## TODO - HACER LOGICA
        # lista_clientes = []
        # for cliente in self.lista_clientes :
        #     if cliente.get('documento') == documento :
        #         lista_clientes.append(cliente)                
        # return lista_clientes
        pass
    
    def eliminar(self, documentos_a_eliminar) :
        ## Crea la lista filtrando los documentos que recive
        self.lista_clientes = [cliente for cliente in self.lista_clientes if cliente['documento'] not in documentos_a_eliminar]

        exito = self.utils.guardar_archivo_json(self.ruta_archivo, self.lista_clientes)
        return exito
    
    def editar(self, cliente_edicion) :
        for cliente in self.lista_clientes :
            # Si o si lo tengo que hacer por id porque si es por patente, no puedo editar patente
            if cliente.get('id_cliente') == cliente_edicion.get('id_cliente'):
                cliente.update(cliente_edicion)
                break
        exito = self.utils.guardar_archivo_json(self.ruta_archivo, self.lista_clientes)
        return exito
    
    def obtener_id_por_documento(self, documento) :
        """ Recibe la patente de un vehiculo y retorna el id de dicho vehiculo """
        for cliente in self.lista_clientes :
            if cliente.get('documento') == documento : 
                return cliente.get('id_cliente', 0) # Si no encuentra el id, retorna 0
            
    def buscar_cliente_por_id(self, id_cliente) : 
        for cliente in self.lista_clientes :
            if cliente.get('id_cliente') == id_cliente : 
                return cliente
        return None
    
    def obtener_nombre_apellido_por_id(self, id_cliente) :
        """ Recibe un id y devuelve un string con el nombre y apellido  """
        for cliente in self.lista_clientes :
            if cliente.get('id_cliente') == id_cliente : 
                return f"{cliente.get('nombre')} {cliente.get('apellido')}"
        return None
    

    # def listar_clientes(self) :
        
     
    
    
    ### FUNCIONES VALIDADORAS
    
    def documento_existente(self, documento) :
        for cliente in self.lista_clientes :
            if cliente.get('documento') == documento :
                return True
        return False