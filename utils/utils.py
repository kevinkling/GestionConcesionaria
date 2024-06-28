import json
from datetime import datetime
""" Funciones utiles """

class Utils :
    def __init__(self) :
        pass
    
    def calcular_posicion_ventana(self, root, ancho_ventana, alto_ventana) :
        """ Esta funcion se encarga de dar las posiciones para que la aplicaion se inicie en la mitad de la pantall """
        x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        return posicion
    
    def leer_archivo_json(self, ruta_archivo) :
        """ Esta funcion lee el archivo que se encuentra en la ruta que le pasamos por parametro """
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                data = json.load(archivo)
            return data
        except FileNotFoundError:
            print(f"Error: El archivo '{ruta_archivo}' no se encontró.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON en '{ruta_archivo}': {e}")
            return None
    
    def guardar_archivo_json(self, ruta_archivo, datos):
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
                return True
        except Exception as e:
            print(f"Error al guardar en '{ruta_archivo}': {e}")
            return False

    def fecha_hoy_yyyy_mm_dd(self) :
        """ Funcion que retorna la fecha de hoy """
        return datetime.today().strftime('%Y-%m-%d')