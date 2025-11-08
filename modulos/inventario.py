"""
MÓDULO INVENTARIO
Funciones para gestión de productos y stock
"""

from utils.json_handler import leer_json, escribir_json, obtener_siguiente_id, crear_json_si_no_existe
from utils.constantes import RUTA_PRODUCTOS, CATEGORIAS, ESTADO_ACTIVO
from utils.formateadores import formatear_fecha


def _inicializar_archivo_productos():
    """
    Función interna para inicializar el archivo de productos si no existe
    """
    estructura_inicial = {
        "productos": []
    }
    crear_json_si_no_existe(RUTA_PRODUCTOS, estructura_inicial)


def agregar_producto(nombre, precio, stock, categoria):
    """
    Agrega un nuevo producto al inventario
    
    Parámetros:
        nombre (str): Nombre del producto
        precio (float): Precio del producto
        stock (int): Cantidad en stock
        categoria (str): Categoría del producto
    
    Retorna:
        int: ID del producto creado
        None: Si hubo error
    """
    _inicializar_archivo_productos()
    
    # Validar categoría
    if categoria not in CATEGORIAS:
        print(f"Error: Categoría inválida. Debe ser una de: {CATEGORIAS}")
        return None
    
    # Leer productos actuales
    datos = leer_json(RUTA_PRODUCTOS)
    if not datos:
        return None
    
    productos = datos.get("productos", [])
    
    # Obtener siguiente ID
    nuevo_id = obtener_siguiente_id(productos)
    
    # Crear nuevo producto
    nuevo_producto = {
        "id": nuevo_id,
        "nombre": nombre,
        "precio": float(precio),
        "stock": int(stock),
        "categoria": categoria,
        "activo": True,
        "fecha_alta": formatear_fecha()
    }
    
    # Agregar a la lista
    productos.append(nuevo_producto)
    
    # Guardar
    datos["productos"] = productos
    if escribir_json(RUTA_PRODUCTOS, datos):
        return nuevo_id
    else:
        return None


def obtener_producto_por_id(id_producto):
    """
    Obtiene un producto por su ID
    
    Parámetros:
        id_producto (int): ID del producto
    
    Retorna:
        dict: Datos del producto
        None: Si no existe
    """
    _inicializar_archivo_productos()
    
    datos = leer_json(RUTA_PRODUCTOS)
    if not datos:
        return None
    
    productos = datos.get("productos", [])
    
    for producto in productos:
        if producto["id"] == id_producto:
            return producto
    
    return None


def listar_productos():
    """
    Lista todos los productos del inventario
    
    Retorna:
        list: Lista de productos
    """
    _inicializar_archivo_productos()
    
    datos = leer_json(RUTA_PRODUCTOS)
    if not datos:
        return []
    
    return datos.get("productos", [])


def listar_productos_activos():
    """
    Lista solo los productos activos
    
    Retorna:
        list: Lista de productos activos
    """
    todos = listar_productos()
    return [p for p in todos if p.get("activo", True)]


def actualizar_producto(id_producto, datos_nuevos):
    """
    Actualiza datos de un producto
    
    Parámetros:
        id_producto (int): ID del producto
        datos_nuevos (dict): Nuevos datos
    
    Retorna:
        bool: True si se actualizó, False si hubo error
    """
    _inicializar_archivo_productos()
    
    # Leer productos
    datos = leer_json(RUTA_PRODUCTOS)
    if not datos:
        return False
    
    productos = datos.get("productos", [])
    
    # Buscar producto por ID
    producto_encontrado = False
    for producto in productos:
        if producto["id"] == id_producto:
            producto_encontrado = True
            
            # Actualizar campos permitidos
            if "nombre" in datos_nuevos:
                producto["nombre"] = datos_nuevos["nombre"]
            
            if "precio" in datos_nuevos:
                producto["precio"] = float(datos_nuevos["precio"])
            
            if "stock" in datos_nuevos:
                producto["stock"] = int(datos_nuevos["stock"])
            
            if "categoria" in datos_nuevos:
                if datos_nuevos["categoria"] in CATEGORIAS:
                    producto["categoria"] = datos_nuevos["categoria"]
            
            if "activo" in datos_nuevos:
                producto["activo"] = datos_nuevos["activo"]
            
            break
    
    if not producto_encontrado:
        return False
    
    # Guardar cambios
    datos["productos"] = productos
    return escribir_json(RUTA_PRODUCTOS, datos)


def eliminar_producto(id_producto):
    """
    Elimina (deshabilita) un producto ACTIVO o borra permanentemente un producto INACTIVO
    
    Parámetros:
        id_producto (int): ID del producto
    
    Retorna:
        str: "inactivado" si se marcó como inactivo, "eliminado" si se borró permanentemente
        None: Si hubo error
    """
    _inicializar_archivo_productos()
    
    # Obtener el producto
    producto = obtener_producto_por_id(id_producto)
    if not producto:
        return None
    
    # Si está ACTIVO, marcarlo como INACTIVO
    if producto.get("activo", True):
        if actualizar_producto(id_producto, {"activo": False}):
            return "inactivado"
        else:
            return None
    
    # Si está INACTIVO, eliminarlo permanentemente
    else:
        # Leer productos
        datos = leer_json(RUTA_PRODUCTOS)
        if not datos:
            return None
        
        productos = datos.get("productos", [])
        
        # Filtrar el producto (eliminarlo de la lista)
        productos_nuevos = [p for p in productos if p["id"] != id_producto]
        
        # Guardar cambios
        datos["productos"] = productos_nuevos
        if escribir_json(RUTA_PRODUCTOS, datos):
            return "eliminado"
        else:
            return None


def buscar_productos(termino):
    """
    Busca productos por nombre
    
    Parámetros:
        termino (str): Término de búsqueda
    
    Retorna:
        list: Lista de productos que coinciden
    """
    _inicializar_archivo_productos()
    
    # Obtener todos los productos
    productos = listar_productos()
    
    # Filtrar por término (insensible a mayúsculas)
    termino_lower = termino.lower()
    resultados = []
    
    for producto in productos:
        nombre_lower = producto["nombre"].lower()
        if termino_lower in nombre_lower:
            resultados.append(producto)
    
    return resultados


def actualizar_stock(id_producto, cantidad):
    """
    Actualiza el stock de un producto (suma o resta)
    
    Parámetros:
        id_producto (int): ID del producto
        cantidad (int): Cantidad a sumar (positivo) o restar (negativo)
    
    Retorna:
        bool: True si se actualizó, False si hubo error
    """
    _inicializar_archivo_productos()
    
    # Obtener producto
    producto = obtener_producto_por_id(id_producto)
    if not producto:
        return False
    
    # Calcular nuevo stock
    nuevo_stock = producto["stock"] + cantidad
    
    # Validar que no sea negativo
    if nuevo_stock < 0:
        print(f"Error: Stock insuficiente. Stock actual: {producto['stock']}, Cantidad solicitada: {abs(cantidad)}")
        return False
    
    # Actualizar stock
    return actualizar_producto(id_producto, {"stock": nuevo_stock})


def hay_stock_suficiente(id_producto, cantidad):
    """
    Verifica si hay stock suficiente de un producto
    
    Parámetros:
        id_producto (int): ID del producto
        cantidad (int): Cantidad requerida
    
    Retorna:
        bool: True si hay stock, False si no hay
    """
    _inicializar_archivo_productos()
    
    producto = obtener_producto_por_id(id_producto)
    if not producto:
        return False
    
    return producto["stock"] >= cantidad


def listar_productos_bajo_stock(minimo=10):
    """
    Lista productos con stock bajo
    
    Parámetros:
        minimo (int): Stock mínimo
    
    Retorna:
        list: Productos con stock bajo
    """
    productos = listar_productos_activos()
    return [p for p in productos if p["stock"] < minimo]


def calcular_precio_con_ganancia(precio_costo, porcentaje_ganancia):
    """
    Calcula el precio de venta aplicando un porcentaje de ganancia
    
    Parámetros:
        precio_costo (float): Precio de costo del producto
        porcentaje_ganancia (float): Porcentaje de ganancia a aplicar
    
    Retorna:
        float: Precio de venta con ganancia
    """
    try:
        costo = float(precio_costo)
        ganancia = float(porcentaje_ganancia)
        
        if costo <= 0 or ganancia < 0:
            return 0
        
        precio_venta = costo * (1 + ganancia / 100)
        return round(precio_venta, 2)
    except (ValueError, TypeError):
        return 0