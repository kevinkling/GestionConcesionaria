import re
from utils.utils import Utils 

"""
Esta clase contiene funciones de creacion, consulta, modificacion y eliminacion de vehiculos.
Tambien contiene funciones de validacion.
"""

class Vehiculo :
    def __init__(self) :
        self.ruta_archivo = 'datos/vehiculos.json'
        self.utils = Utils()
        self.lista_vehiculos = self.utils.leer_archivo_json(self.ruta_archivo)
        self.lista_vehiculos_encontrados = []

    def obtener_lista_vehiculos(self) :
        """ Retorna los vehiculos  """
        return self.lista_vehiculos
    
    def obtener_lista_vehiculos_disponibles(self, actulizado=False) :
        if actulizado :
            lista_vehiculos = self.utils.leer_archivo_json(self.ruta_archivo)
        else :
            lista_vehiculos = self.lista_vehiculos
        lista_vehiculos_disponibles = []
        for vehiculo in lista_vehiculos :
            if vehiculo.get('estado') == "Disponible" :
                lista_vehiculos_disponibles.append(vehiculo)
        return lista_vehiculos_disponibles
    
    def obtener_lista_vehiculos_actualizada(self) :
        return self.utils.leer_archivo_json(self.ruta_archivo)

    def crear_vehiculo(self, nuevo_vehiculo) :
        self.lista_vehiculos.append(nuevo_vehiculo)
        exito = self.utils.guardar_archivo_json(self.ruta_archivo, self.lista_vehiculos)
        return exito

    def obtener_ultimo_id(self) :
        """ Retorna el id del ultimo vehiculo o 0 si la lista esta vacia """
        ultimo_vehiculo = self.lista_vehiculos[-1]
        return ultimo_vehiculo.get('id_vehiculo', 0)

    def buscar_vehiculo(self, tipo_busqueda, busqueda) :
        """ Esta funcion es la principal que realiza la busqueda, dependiendo la busqueda llamara a su respectiva funcion """
        self.lista_vehiculos_encontrados.clear() ## Limpio la lista porque sino queda la busqueda anterior
        
        match tipo_busqueda:
            case "Patente":
                return self.buscar_vehiculo_patente(busqueda.upper())
            case "Marca":
                return self.buscar_vehiculo_marca(busqueda.capitalize())
            case "Modelo":
                return self.buscar_vehiculo_modelo(busqueda.capitalize())
            case "Precio de compra":
                return self.buscar_vehiculo_precio_compra(busqueda)
            case "Precio de venta":
                return self.buscar_vehiculo_precio_venta(busqueda)
                
        return self.lista_vehiculos_encontrados

    def buscar_vehiculo_patente(self, patente) :
        lista_vehiculos = []
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('patente') == patente : 
                lista_vehiculos.append(vehiculo)
        return lista_vehiculos

    def buscar_vehiculo_marca(self, marca) :
        lista_vehiculos = []      
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('marca') == marca : 
                lista_vehiculos.append(vehiculo)
        return lista_vehiculos

    def buscar_vehiculo_modelo(self, modelo) :
        lista_vehiculos = []
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('modelo') == modelo : 
                lista_vehiculos.append(vehiculo)
        return lista_vehiculos
        
    def buscar_vehiculo_precio_compra(self, precio) :
        lista_vehiculos = []
        precio = float(precio)
        
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('precio_compra') == precio : 
                lista_vehiculos.append(vehiculo)
        return lista_vehiculos

    def buscar_vehiculo_precio_venta(self, precio) :
        lista_vehiculos = []
        precio = float(precio)
            
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('precio_venta') == precio : 
                lista_vehiculos.append(vehiculo)
        return lista_vehiculos

    def eliminar(self, patentes_a_eliminar) :
        ## Crea la lista filtrando los documentos que recive
        self.lista_vehiculos = [vehiculo for vehiculo in self.lista_vehiculos if vehiculo["patente"] not in patentes_a_eliminar]

        exito = self.utils.guardar_archivo_json(self.ruta_archivo, self.lista_vehiculos)
        return exito

    def editar(self, vehiculo_edicion) :
        for vehiculo in self.lista_vehiculos :
            # Si o si lo tengo que hacer por id porque si es por patente, no puedo editar patente
            if vehiculo.get('id_vehiculo') == vehiculo_edicion.get('id_vehiculo'):
                vehiculo.update(vehiculo_edicion)
                break
        exito = self.utils.guardar_archivo_json(self.ruta_archivo, self.lista_vehiculos)
        return exito

    def obtener_id_por_patente(self, patente) :
        """ Recibe la patente de un vehiculo y retorna el id de dicho vehiculo """
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('patente') == patente : 
                return vehiculo.get('id_vehiculo', 0) # Si no encuentra el id, retorna 0
     
    def buscar_vehiculo_por_id(self, id_vehiculo) : 
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('id_vehiculo') == id_vehiculo : 
                return vehiculo
        return None
    
    def obtener_monto_venta(self, patente) :
        """ Funcion que retorna el monto de venta de un vehiculo """
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('patente') == patente : 
                return vehiculo.get('precio_venta')
    
    def obtener_monto_compra(self, patente) :
        """ Funcion que retorna el monto de compra de un vehiculo """        
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('patente') == patente : 
                return vehiculo.get('precio_compra')
            
    def obtener_marca_modelo_por_id(self, id_vehiculo) :
        """ Recibe un id y devuelve un string con el nombre y apellido  """
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('id_vehiculo') == id_vehiculo : 
                return f"{vehiculo.get('marca')} {vehiculo.get('modelo')}"
        return None

    def marcar_como_vendido(self, id_vehiculo) :
        """ Recibe un id y setea como vendido el vehiculo """
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('id_vehiculo') == id_vehiculo : 
                vehiculo['estado'] = "Vendido"
                self.utils.guardar_archivo_json(self.ruta_archivo, self.lista_vehiculos)
        
    
    ### FUNCIONES VALIDADORAS
    
    def patente_existente(self, patente) :
        for vehiculo in self.lista_vehiculos :
            if vehiculo.get('patente') == patente : 
                return True
        return False
    
    def validar_formato_patente(self, patente) :
        """ Funcion que retorna verdadero si la patente coincide con algunos de los formatos validos.
        Formatos validos : XX000XX - XXX000
        Donde xxx es cualquier letra y 000 cualquier numero"""
        formato_valido = r"^[A-Z-Ñ]{3}\d{3}$|^[A-Z-Ñ]{2}\d{3}[A-Z-Ñ]{2}$|^[A-Z-Ñ]{3} \d{3}$|^[A-Z-Ñ]{2} \d{3} [A-Z-Ñ]{2}$"
        if re.fullmatch(formato_valido, patente) :
            return True
        else :
            return False
        
