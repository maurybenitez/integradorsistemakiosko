"""
MÓDULO VENTAS
Funciones para gestión de ventas
"""

# from utils import json_handler, constantes, formateadores
# from modulos import inventario, caja


def crear_venta_nueva():
    """
    Crea una nueva venta vacía (temporal)
    
    Retorna:
        dict: Estructura de venta nueva
    """
    pass


def agregar_item_venta(venta, id_producto, cantidad):
    """
    Agrega un producto a la venta temporal
    
    Parámetros:
        venta (dict): Venta temporal
        id_producto (int): ID del producto
        cantidad (int): Cantidad a vender
    
    Retorna:
        bool: True si se agregó, False si hubo error
    """
    pass


def eliminar_item_venta(venta, indice):
    """
    Elimina un item de la venta temporal
    
    Parámetros:
        venta (dict): Venta temporal
        indice (int): Índice del item a eliminar
    
    Retorna:
        bool: True si se eliminó, False si hubo error
    """
    pass


def calcular_total_venta(venta):
    """
    Calcula el total de una venta
    
    Parámetros:
        venta (dict): Venta temporal
    
    Retorna:
        float: Total de la venta
    """
    pass


def finalizar_venta_efectivo(venta, monto_pagado):
    """
    Finaliza una venta en efectivo
    
    Parámetros:
        venta (dict): Venta a finalizar
        monto_pagado (float): Monto que pagó el cliente
    
    Retorna:
        dict: Datos de la venta finalizada (con vuelto)
        None: Si hubo error
    """
    pass


def finalizar_venta_cuenta_corriente(venta, id_cliente):
    """
    Finaliza una venta en cuenta corriente
    
    Parámetros:
        venta (dict): Venta a finalizar
        id_cliente (int): ID del cliente
    
    Retorna:
        dict: Datos de la venta finalizada
        None: Si hubo error
    """
    pass


def guardar_venta(venta):
    """
    Guarda una venta en el archivo JSON
    
    Parámetros:
        venta (dict): Venta a guardar
    
    Retorna:
        int: ID de la venta guardada
        None: Si hubo error
    """
    pass


def listar_ventas():
    """
    Lista todas las ventas
    
    Retorna:
        list: Lista de ventas
    """
    pass
