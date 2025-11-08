"""
FORMATEADORES
Funciones para formatear datos (precios, fechas, horas)
"""

from datetime import datetime


def formatear_precio(numero):
    """
    Formatea un número como precio argentino
    
    Parámetros:
        numero (float): Número a formatear
    
    Retorna:
        str: Precio formateado (ej: "$1.500,00")
    """
    try:
        # Convertir a float por si viene como string
        numero = float(numero)
        
        # Formatear con separador de miles y 2 decimales
        # Primero formateamos con punto decimal
        precio_formateado = f"{numero:,.2f}"
        
        # Reemplazar punto por coma (decimal argentino)
        # y coma por punto (separador de miles argentino)
        precio_formateado = precio_formateado.replace(",", "TEMP")
        precio_formateado = precio_formateado.replace(".", ",")
        precio_formateado = precio_formateado.replace("TEMP", ".")
        
        # Agregar símbolo de peso
        return f"${precio_formateado}"
    
    except (ValueError, TypeError):
        return "$0,00"


def formatear_fecha(fecha=None):
    """
    Formatea una fecha en formato DD/MM/AAAA
    
    Parámetros:
        fecha (datetime): Fecha a formatear (si es None, usa fecha actual)
    
    Retorna:
        str: Fecha formateada (ej: "08/11/2025")
    """
    try:
        # Si no se pasa fecha, usar la actual
        if fecha is None:
            fecha = datetime.now()
        
        # Formatear como DD/MM/AAAA
        return fecha.strftime("%d/%m/%Y")
    
    except Exception:
        # Si hay error, retornar fecha actual
        return datetime.now().strftime("%d/%m/%Y")


def formatear_hora(hora=None):
    """
    Formatea una hora en formato HH:MM:SS
    
    Parámetros:
        hora (datetime): Hora a formatear (si es None, usa hora actual)
    
    Retorna:
        str: Hora formateada (ej: "14:30:55")
    """
    try:
        # Si no se pasa hora, usar la actual
        if hora is None:
            hora = datetime.now()
        
        # Formatear como HH:MM:SS
        return hora.strftime("%H:%M:%S")
    
    except Exception:
        # Si hay error, retornar hora actual
        return datetime.now().strftime("%H:%M:%S")


def formatear_fecha_hora_completa():
    """
    Obtiene fecha y hora actual en formato completo
    
    Retorna:
        str: Fecha y hora formateada (ej: "08/11/2025 14:30:55")
    """
    ahora = datetime.now()
    fecha = formatear_fecha(ahora)
    hora = formatear_hora(ahora)
    return f"{fecha} {hora}"


def limpiar_string(texto):
    """
    Limpia un string eliminando espacios extras
    
    Parámetros:
        texto (str): Texto a limpiar
    
    Retorna:
        str: Texto limpio
    """
    if not texto:
        return ""
    
    # Convertir a string por si viene otro tipo
    texto = str(texto)
    
    # Eliminar espacios al inicio y final
    texto = texto.strip()
    
    # Reemplazar múltiples espacios por uno solo
    while "  " in texto:
        texto = texto.replace("  ", " ")
    
    return texto


def validar_numero(texto):
    """
    Valida si un texto es un número válido
    
    Parámetros:
        texto (str): Texto a validar
    
    Retorna:
        bool: True si es número válido, False en caso contrario
    """
    try:
        # Intentar convertir a float
        float(texto)
        return True
    except (ValueError, TypeError):
        return False