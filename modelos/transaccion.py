from utils.utils import Utils 

"""
Esta clase contiene funciones de creacion, consulta, modificacion y eliminacion de transacciones.
Tambien contiene funciones de validacion.
"""

class Transaccion :
    def __init__(self) :
        self.ruta_archivo = 'datos/transacciones.json'
        self.utils = Utils()
        self.lista_transacciones = self.utils.leer_archivo_json(self.ruta_archivo)
    
    def obtener_lista_transacciones_compra(self) :
        lista_transacciones_compra = []
        for tran in self.lista_transacciones :
            if tran.get('tipo_transaccion') == "Compra" :
                lista_transacciones_compra.append(tran)
        return lista_transacciones_compra
    
    def obtener_lista_transacciones_venta(self) :
        lista_transacciones_venta = []
        for tran in self.lista_transacciones :
            if tran.get('tipo_transaccion') == "Venta" :
                lista_transacciones_venta.append(tran)
        return lista_transacciones_venta
    
    def crear_transaccion(self, nueva_transaccion) :
        self.lista_transacciones.append(nueva_transaccion)
        exito = self.utils.guardar_archivo_json(self.ruta_archivo, self.lista_transacciones)
        return exito
    
    def obtener_ultimo_id(self) :
        """ Retorna el id del ultimo transaccion o 0 si la lista esta vacia """
        ultima_transaccion = self.lista_transacciones[-1]
        return ultima_transaccion.get('id_transaccion', 0)