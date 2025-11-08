"""
MANEJADOR DE ARCHIVOS JSON
Funciones para leer y escribir datos en archivos JSON
"""

import json
import os


def leer_json(nombre_archivo):
    """
    Lee un archivo JSON y retorna su contenido
    
    Parámetros:
        nombre_archivo (str): Ruta del archivo JSON
    
    Retorna:
        dict/list: Contenido del archivo JSON
        None: Si hay error o no existe
    """
    try:
        # Verificar si el archivo existe
        if not os.path.exists(nombre_archivo):
            print(f"Error: El archivo {nombre_archivo} no existe")
            return None
        
        # Abrir y leer el archivo JSON
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            return datos
    
    except json.JSONDecodeError:
        print(f"Error: El archivo {nombre_archivo} no tiene formato JSON válido")
        return None
    
    except Exception as e:
        print(f"Error al leer {nombre_archivo}: {e}")
        return None


def escribir_json(nombre_archivo, datos):
    """
    Escribe datos en un archivo JSON
    
    Parámetros:
        nombre_archivo (str): Ruta del archivo JSON
        datos (dict/list): Datos a guardar
    
    Retorna:
        bool: True si se guardó correctamente, False si hubo error
    """
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(nombre_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        # Escribir el archivo JSON con formato legible
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Error al escribir {nombre_archivo}: {e}")
        return False


def crear_json_si_no_existe(nombre_archivo, estructura_inicial):
    """
    Crea un archivo JSON con estructura inicial si no existe
    
    Parámetros:
        nombre_archivo (str): Ruta del archivo JSON
        estructura_inicial (dict/list): Estructura inicial del archivo
    
    Retorna:
        bool: True si se creó, False si ya existía
    """
    # Verificar si el archivo ya existe
    if os.path.exists(nombre_archivo):
        return False
    
    # Crear el archivo con la estructura inicial
    exito = escribir_json(nombre_archivo, estructura_inicial)
    
    if exito:
        print(f"Archivo {nombre_archivo} creado con estructura inicial")
    
    return exito


def obtener_siguiente_id(lista_objetos):
    """
    Obtiene el siguiente ID disponible en una lista de objetos
    
    Parámetros:
        lista_objetos (list): Lista de diccionarios con campo 'id'
    
    Retorna:
        int: Siguiente ID disponible (último ID + 1)
    """
    # Si la lista está vacía, comenzar desde 1
    if not lista_objetos:
        return 1
    
    # Obtener todos los IDs existentes
    ids_existentes = [obj['id'] for obj in lista_objetos if 'id' in obj]
    
    # Si no hay IDs, comenzar desde 1
    if not ids_existentes:
        return 1
    
    # Retornar el máximo ID + 1
    return max(ids_existentes) + 1