"""
MÓDULO CAJA
Funciones para gestión de caja (apertura, cierre, movimientos)
"""

# from utils import json_handler, constantes, formateadores


def abrir_caja(monto_inicial, cajero):
    """
    Abre una nueva caja
    
    Parámetros:
        monto_inicial (float): Monto inicial de la caja
        cajero (str): Nombre del cajero
    
    Retorna:
        int: ID de la caja abierta
        None: Si hubo error o ya hay una caja abierta
    """
    pass


def cerrar_caja(id_caja, monto_cierre):
    """
    Cierra una caja y genera arqueo
    
    Parámetros:
        id_caja (int): ID de la caja a cerrar
        monto_cierre (float): Monto real contado
    
    Retorna:
        dict: Datos del arqueo (diferencia, totales, etc.)
        None: Si hubo error
    """
    pass


def obtener_caja_actual():
    """
    Obtiene la caja actualmente abierta
    
    Retorna:
        dict: Datos de la caja abierta
        None: Si no hay caja abierta
    """
    pass


def hay_caja_abierta():
    """
    Verifica si hay una caja abierta
    
    Retorna:
        bool: True si hay caja abierta, False si no
    """
    pass


def registrar_movimiento(tipo, monto, descripcion):
    """
    Registra un movimiento en la caja actual
    
    Parámetros:
        tipo (str): Tipo de movimiento (VENTA, RETIRO, INGRESO, etc.)
        monto (float): Monto del movimiento
        descripcion (str): Descripción del movimiento
    
    Retorna:
        bool: True si se registró, False si hubo error
    """
    pass


def obtener_movimientos_caja(id_caja):
    """
    Obtiene todos los movimientos de una caja
    
    Parámetros:
        id_caja (int): ID de la caja
    
    Retorna:
        list: Lista de movimientos
    """
    pass


def calcular_total_caja():
    """
    Calcula el total actual de la caja abierta
    
    Retorna:
        float: Total actual de la caja
        None: Si no hay caja abierta
    """
    pass
