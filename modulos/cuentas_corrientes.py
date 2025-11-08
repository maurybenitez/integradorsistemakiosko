"""
MÓDULO CUENTAS CORRIENTES
Funciones para gestión de clientes y fiados
"""

# from utils import json_handler, constantes, formateadores


def agregar_cliente(nombre, telefono, limite_credito):
    """
    Agrega un nuevo cliente
    
    Parámetros:
        nombre (str): Nombre del cliente
        telefono (str): Teléfono del cliente
        limite_credito (float): Límite de crédito permitido
    
    Retorna:
        int: ID del cliente creado
        None: Si hubo error
    """
    pass


def obtener_cliente_por_id(id_cliente):
    """
    Obtiene un cliente por su ID
    
    Parámetros:
        id_cliente (int): ID del cliente
    
    Retorna:
        dict: Datos del cliente
        None: Si no existe
    """
    pass


def listar_clientes():
    """
    Lista todos los clientes
    
    Retorna:
        list: Lista de clientes
    """
    pass


def registrar_venta_fiada(id_cliente, monto, detalle):
    """
    Registra una venta fiada para un cliente
    
    Parámetros:
        id_cliente (int): ID del cliente
        monto (float): Monto de la venta
        detalle (str): Detalle de la venta
    
    Retorna:
        bool: True si se registró, False si hubo error
    """
    pass


def registrar_pago(id_cliente, monto):
    """
    Registra un pago de un cliente
    
    Parámetros:
        id_cliente (int): ID del cliente
        monto (float): Monto del pago
    
    Retorna:
        bool: True si se registró, False si hubo error
    """
    pass


def obtener_deuda_actual(id_cliente):
    """
    Obtiene la deuda actual de un cliente
    
    Parámetros:
        id_cliente (int): ID del cliente
    
    Retorna:
        float: Deuda actual del cliente
    """
    pass


def obtener_historial_cliente(id_cliente):
    """
    Obtiene el historial de movimientos de un cliente
    
    Parámetros:
        id_cliente (int): ID del cliente
    
    Retorna:
        list: Lista de movimientos (compras y pagos)
    """
    pass


def validar_limite_credito(id_cliente, monto_nueva_venta):
    """
    Valida si un cliente puede realizar una nueva compra fiada
    
    Parámetros:
        id_cliente (int): ID del cliente
        monto_nueva_venta (float): Monto de la nueva venta
    
    Retorna:
        bool: True si puede comprar, False si excede límite
    """
    pass
