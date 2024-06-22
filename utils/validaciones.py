from datetime import date
""" Clase que usare para hacer validaciones """

class Validaciones :
    def __init__(self) :
        self.fecha_actual = date.today()
    
    def validar_dni(self, dni):
        return dni.isalpha()

    def anio_valido(self, anio) :
        """ Funcion que retorna verdadero si el anio pasado por parametro esta en un rango logico """
        return anio > 1950 and anio <= self.fecha_actual.year