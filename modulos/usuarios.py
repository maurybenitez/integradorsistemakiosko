"""
MÓDULO USUARIOS
Funciones para gestión de usuarios y autenticación
"""

from utils.json_handler import leer_json, escribir_json, obtener_siguiente_id, crear_json_si_no_existe
from utils.constantes import RUTA_USUARIOS, ROL_ADMINISTRADOR, ROL_CAJERO, ESTADO_ACTIVO, ESTADO_INACTIVO
from utils.formateadores import formatear_fecha_hora_completa


def _inicializar_archivo_usuarios():
    """
    Función interna para inicializar el archivo de usuarios si no existe
    """
    estructura_inicial = {
        "usuarios": [
            {
                "id": 1,
                "nombre_usuario": "admin",
                "contrasena": "admin123",
                "nombre_completo": "Administrador del Sistema",
                "rol": ROL_ADMINISTRADOR,
                "activo": True,
                "fecha_creacion": formatear_fecha_hora_completa()
            }
        ]
    }
    crear_json_si_no_existe(RUTA_USUARIOS, estructura_inicial)


def autenticar_usuario(nombre_usuario, contrasena):
    """
    Autentica un usuario verificando credenciales
    
    Parámetros:
        nombre_usuario (str): Nombre de usuario
        contrasena (str): Contraseña del usuario
    
    Retorna:
        dict: Datos del usuario si es correcto
        None: Si las credenciales son incorrectas
    """
    # Inicializar archivo si no existe
    _inicializar_archivo_usuarios()
    
    # Leer usuarios
    datos = leer_json(RUTA_USUARIOS)
    if not datos:
        return None
    
    usuarios = datos.get("usuarios", [])
    
    # Buscar usuario
    for usuario in usuarios:
        if usuario["nombre_usuario"] == nombre_usuario:
            # Verificar contraseña
            if usuario["contrasena"] == contrasena:
                # Verificar que esté activo
                if usuario["activo"]:
                    return usuario
                else:
                    return None  # Usuario deshabilitado
            else:
                return None  # Contraseña incorrecta
    
    return None  # Usuario no encontrado


def obtener_usuario_por_nombre(nombre_usuario):
    """
    Busca un usuario por su nombre
    
    Parámetros:
        nombre_usuario (str): Nombre a buscar
    
    Retorna:
        dict: Datos del usuario si existe
        None: Si no existe
    """
    _inicializar_archivo_usuarios()
    
    datos = leer_json(RUTA_USUARIOS)
    if not datos:
        return None
    
    usuarios = datos.get("usuarios", [])
    
    for usuario in usuarios:
        if usuario["nombre_usuario"] == nombre_usuario:
            return usuario
    
    return None


def crear_usuario_default():
    """
    Crea un usuario administrador por defecto
    
    Retorna:
        dict: Usuario administrador creado
    """
    usuario_admin = {
        "id": 1,
        "nombre_usuario": "admin",
        "contrasena": "admin123",
        "nombre_completo": "Administrador del Sistema",
        "rol": ROL_ADMINISTRADOR,
        "activo": True,
        "fecha_creacion": formatear_fecha_hora_completa()
    }
    return usuario_admin


def listar_usuarios():
    """
    Lista todos los usuarios del sistema
    
    Retorna:
        list: Lista de usuarios
    """
    _inicializar_archivo_usuarios()
    
    datos = leer_json(RUTA_USUARIOS)
    if not datos:
        return []
    
    return datos.get("usuarios", [])


def crear_usuario(nombre, contrasena, rol):
    """
    Crea un nuevo usuario en el sistema
    
    Parámetros:
        nombre (str): Nombre de usuario
        contrasena (str): Contraseña
        rol (str): Rol del usuario (CAJERO o ADMINISTRADOR)
    
    Retorna:
        int: ID del usuario creado
        None: Si hubo error
    """
    _inicializar_archivo_usuarios()
    
    # Verificar que el nombre de usuario no exista
    if obtener_usuario_por_nombre(nombre):
        print(f"Error: El usuario '{nombre}' ya existe")
        return None
    
    # Validar rol
    if rol not in [ROL_ADMINISTRADOR, ROL_CAJERO]:
        print(f"Error: Rol inválido. Debe ser {ROL_ADMINISTRADOR} o {ROL_CAJERO}")
        return None
    
    # Leer usuarios actuales
    datos = leer_json(RUTA_USUARIOS)
    if not datos:
        return None
    
    usuarios = datos.get("usuarios", [])
    
    # Obtener siguiente ID
    nuevo_id = obtener_siguiente_id(usuarios)
    
    # Crear nuevo usuario
    nuevo_usuario = {
        "id": nuevo_id,
        "nombre_usuario": nombre,
        "contrasena": contrasena,
        "nombre_completo": "",
        "rol": rol,
        "activo": True,
        "fecha_creacion": formatear_fecha_hora_completa()
    }
    
    # Agregar a la lista
    usuarios.append(nuevo_usuario)
    
    # Guardar
    datos["usuarios"] = usuarios
    if escribir_json(RUTA_USUARIOS, datos):
        return nuevo_id
    else:
        return None


def modificar_usuario(id_usuario, datos_nuevos):
    """
    Modifica datos de un usuario existente
    
    Parámetros:
        id_usuario (int): ID del usuario a modificar
        datos_nuevos (dict): Diccionario con nuevos datos
    
    Retorna:
        bool: True si se modificó, False si hubo error
    """
    _inicializar_archivo_usuarios()
    
    # Leer usuarios
    datos = leer_json(RUTA_USUARIOS)
    if not datos:
        return False
    
    usuarios = datos.get("usuarios", [])
    
    # Buscar usuario por ID
    usuario_encontrado = False
    for usuario in usuarios:
        if usuario["id"] == id_usuario:
            usuario_encontrado = True
            
            # Actualizar campos permitidos
            if "nombre_completo" in datos_nuevos:
                usuario["nombre_completo"] = datos_nuevos["nombre_completo"]
            
            if "contrasena" in datos_nuevos:
                usuario["contrasena"] = datos_nuevos["contrasena"]
            
            if "rol" in datos_nuevos:
                if datos_nuevos["rol"] in [ROL_ADMINISTRADOR, ROL_CAJERO]:
                    usuario["rol"] = datos_nuevos["rol"]
            
            if "activo" in datos_nuevos:
                usuario["activo"] = datos_nuevos["activo"]
            
            break
    
    if not usuario_encontrado:
        return False
    
    # Guardar cambios
    datos["usuarios"] = usuarios
    return escribir_json(RUTA_USUARIOS, datos)


def eliminar_usuario(id_usuario):
    """
    Elimina (deshabilita) un usuario
    
    Parámetros:
        id_usuario (int): ID del usuario a eliminar
    
    Retorna:
        bool: True si se eliminó, False si hubo error
    """
    # No eliminamos físicamente, solo marcamos como inactivo
    return modificar_usuario(id_usuario, {"activo": False})