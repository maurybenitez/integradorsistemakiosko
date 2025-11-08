"""
VALIDADORES
Funciones para validar datos de entrada
"""

def validar_precio(precio):
    """
    Valida que un precio sea válido (número positivo)
    
    Parámetros:
        precio: Valor a validar
    
    Retorna:
        bool: True si es válido, False en caso contrario
    """
    try:
        # Convertir a float
        precio_float = float(precio)
        
        # Verificar que sea mayor a 0
        if precio_float > 0:
            return True
        else:
            return False
    
    except (ValueError, TypeError):
        return False


def validar_stock(stock):
    """
    Valida que un stock sea válido (número entero >= 0)
    
    Parámetros:
        stock: Valor a validar
    
    Retorna:
        bool: True si es válido, False en caso contrario
    """
    try:
        # Convertir a int
        stock_int = int(stock)
        
        # Verificar que sea mayor o igual a 0
        if stock_int >= 0:
            return True
        else:
            return False
    
    except (ValueError, TypeError):
        return False


def campos_vacios(*campos):
    """
    Verifica si alguno de los campos está vacío
    
    Parámetros:
        *campos: Lista de campos a verificar
    
    Retorna:
        bool: True si hay algún campo vacío, False si todos tienen datos
    """
    for campo in campos:
        # Convertir a string y eliminar espacios
        campo_str = str(campo).strip()
        
        # Si el campo está vacío, retornar True
        if not campo_str or campo_str == "" or campo_str == "None":
            return True
    
    # Si todos los campos tienen datos, retornar False
    return False


def validar_longitud_minima(texto, minimo):
    """
    Valida que un texto tenga longitud mínima
    
    Parámetros:
        texto (str): Texto a validar
        minimo (int): Longitud mínima requerida
    
    Retorna:
        bool: True si cumple, False en caso contrario
    """
    try:
        # Convertir a string y eliminar espacios
        texto_str = str(texto).strip()
        
        # Verificar longitud
        if len(texto_str) >= minimo:
            return True
        else:
            return False
    
    except Exception:
        return False