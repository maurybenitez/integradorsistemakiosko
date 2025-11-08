# SISTEMA DE GESTIÓN PARA KIOSKO

## Descripción
Sistema de gestión integral para kiosko desarrollado en Python con Tkinter.
Trabajo Integrador Final - Programación I

**Programación Estructurada**

---

## Características Principales

### Módulos del Sistema:
1. **Login** - Autenticación de usuarios (Cajero/Administrador)
2. **Inventario** - Gestión de productos y stock
3. **Ventas** - Registro de ventas en efectivo y cuenta corriente
4. **Caja** - Apertura, cierre y control de caja
5. **Cuentas Corrientes** - Gestión de clientes y fiados
6. **Reportes** - Generación de reportes estadísticos
7. **Configuración** - Gestión de usuarios y parámetros del sistema

---

## Estructura del Proyecto

```
sistema_kiosko/
│
├── main.py                          # Punto de entrada
│
├── data/                            # Archivos JSON de datos
│   ├── usuarios.json
│   ├── productos.json
│   ├── ventas.json
│   ├── caja.json
│   ├── cuentas_corrientes.json
│   └── config.json
│
├── modulos/                         # Lógica de negocio
│   ├── usuarios.py
│   ├── inventario.py
│   ├── ventas.py
│   ├── caja.py
│   ├── cuentas_corrientes.py
│   ├── reportes.py
│   └── configuracion.py
│
├── interfaz/                        # Interfaces gráficas Tkinter
│   ├── login_ui.py
│   ├── menu_principal_ui.py
│   ├── inventario_ui.py
│   ├── ventas_ui.py
│   ├── caja_ui.py
│   ├── cuentas_corrientes_ui.py
│   ├── reportes_ui.py
│   └── configuracion_ui.py
│
├── utils/                           # Utilidades
│   ├── constantes.py
│   ├── json_handler.py
│   ├── formateadores.py
│   └── validadores.py
│
└── documentacion/                   # Documentación académica
    ├── diagramas_flujo/
    └── README.md
```

---

## Requisitos del Sistema

- Python 3.8 o superior
- Tkinter (incluido en Python)
- Módulo json (incluido en Python)
- Sistema Operativo: Windows, Linux o macOS

---

## Instalación

1. Clonar o descargar el proyecto
2. Verificar que Python esté instalado: `python --version`
3. Ejecutar el sistema: `python main.py`

---

## Uso del Sistema

### Usuario Administrador por Defecto:
- **Usuario:** admin
- **Contraseña:** admin123

### Roles y Permisos:

**CAJERO:**
- Realizar ventas
- Abrir/cerrar caja
- Gestionar cuentas corrientes
- Ver reportes

**ADMINISTRADOR:**
- Todas las funciones de cajero
- Gestión de inventario
- Gestión de usuarios
- Configuración del sistema

---

## Flujo de Trabajo

1. **Iniciar sesión** con usuario y contraseña
2. **Abrir caja** (obligatorio para realizar ventas)
3. **Realizar operaciones** según rol
4. **Cerrar caja** al finalizar turno
5. **Cerrar sesión**

---

## Convenciones de Código

### Nombres de Variables:
- Variables: `snake_case` (ej: `monto_total`)
- Constantes: `MAYUSCULAS` (ej: `ROL_ADMINISTRADOR`)
- Funciones: `snake_case` (ej: `calcular_total()`)

### Nombres de Archivos:
- Módulos lógica: `nombre.py` (ej: `inventario.py`)
- Módulos interfaz: `nombre_ui.py` (ej: `ventas_ui.py`)

### Comentarios:
- Usar docstrings en todas las funciones
- Comentarios en español
- Comentar lógica compleja

---

## Autores
Benitez, Mauricio - Thiago Perez - Guillermo Bassi - Alejandro Vargas - Nicolas Esteche
Programación I - Universidad de la Cuenca del Plata
Año 2025

---

