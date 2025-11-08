"""
INTERFAZ MENÚ PRINCIPAL
Menú principal del sistema según rol de usuario
"""

import tkinter as tk
from tkinter import messagebox
from utils import constantes


def abrir_modulo_inventario():
    """
    Abre el módulo de inventario
    """
    messagebox.showinfo("Inventario", "Módulo de Inventario\n(Próximamente en FASE 3)")
    # from interfaz import inventario_ui
    # inventario_ui.mostrar_inventario()


def abrir_modulo_ventas():
    """
    Abre el módulo de ventas
    """
    # Verificar si hay caja abierta
    if not constantes.caja_abierta:
        messagebox.showwarning(
            "Advertencia",
            "Debe abrir la caja antes de realizar ventas.\n\n"
            "Vaya al módulo CAJA y presione 'Abrir Caja'."
        )
        return
    
    messagebox.showinfo("Ventas", "Módulo de Ventas\n(Próximamente en FASE 5)")
    # from interfaz import ventas_ui
    # ventas_ui.mostrar_ventas()


def abrir_modulo_caja():
    """
    Abre el módulo de caja
    """
    messagebox.showinfo("Caja", "Módulo de Caja\n(Próximamente en FASE 4)")
    # from interfaz import caja_ui
    # caja_ui.mostrar_caja()


def abrir_modulo_cuentas_corrientes():
    """
    Abre el módulo de cuentas corrientes
    """
    messagebox.showinfo("Cuentas Corrientes", "Módulo de Cuentas Corrientes\n(Próximamente en FASE 6)")
    # from interfaz import cuentas_corrientes_ui
    # cuentas_corrientes_ui.mostrar_cuentas_corrientes()


def abrir_modulo_reportes():
    """
    Abre el módulo de reportes
    """
    messagebox.showinfo("Reportes", "Módulo de Reportes\n(Próximamente en FASE 7)")
    # from interfaz import reportes_ui
    # reportes_ui.mostrar_reportes()


def abrir_modulo_configuracion():
    """
    Abre el módulo de configuración
    """
    messagebox.showinfo("Configuración", "Módulo de Configuración\n(Próximamente en FASE 8)")
    # from interfaz import configuracion_ui
    # configuracion_ui.mostrar_configuracion()


def cerrar_sesion(ventana):
    """
    Cierra la sesión del usuario actual
    
    Parámetros:
        ventana: Ventana principal a cerrar
    """
    # Confirmar cierre de sesión
    respuesta = messagebox.askyesno(
        "Cerrar Sesión",
        "¿Está seguro que desea cerrar sesión?"
    )
    
    if respuesta:
        # Limpiar usuario actual
        constantes.usuario_actual = None
        
        # Cerrar ventana
        ventana.destroy()


def mostrar_menu_principal():
    """
    Muestra el menú principal según el rol del usuario actual
    """
    # Verificar que haya un usuario logueado
    if not constantes.usuario_actual:
        messagebox.showerror("Error", "No hay un usuario logueado")
        return
    
    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Sistema Kiosko - Menú Principal")
    ventana.geometry(constantes.VENTANA_MENU)
    ventana.resizable(False, False)
    ventana.configure(bg=constantes.COLOR_FONDO)
    
    # Centrar ventana
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()
    alto_ventana = ventana.winfo_height()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana.geometry(f"+{x}+{y}")
    
    # Frame superior - Información del usuario
    frame_superior = tk.Frame(ventana, bg=constantes.COLOR_PRIMARIO, height=80)
    frame_superior.pack(fill="x")
    frame_superior.pack_propagate(False)
    
    # Información del usuario
    usuario = constantes.usuario_actual
    label_bienvenida = tk.Label(
        frame_superior,
        text=f"Bienvenido/a",
        font=("Arial", 12),
        bg=constantes.COLOR_PRIMARIO,
        fg="white"
    )
    label_bienvenida.pack(pady=(15, 0))
    
    label_nombre = tk.Label(
        frame_superior,
        text=f"{usuario['nombre_completo'] if usuario['nombre_completo'] else usuario['nombre_usuario']}",
        font=("Arial", 16, "bold"),
        bg=constantes.COLOR_PRIMARIO,
        fg="white"
    )
    label_nombre.pack()
    
    label_rol = tk.Label(
        frame_superior,
        text=f"Rol: {usuario['rol']}",
        font=("Arial", 10),
        bg=constantes.COLOR_PRIMARIO,
        fg="lightgray"
    )
    label_rol.pack()
    
    # Frame principal - Botones del menú
    frame_principal = tk.Frame(ventana, bg=constantes.COLOR_FONDO)
    frame_principal.pack(expand=True, fill="both", padx=40, pady=30)
    
    # Título del menú
    label_titulo = tk.Label(
        frame_principal,
        text="MENÚ PRINCIPAL",
        font=("Arial", 18, "bold"),
        bg=constantes.COLOR_FONDO,
        fg=constantes.COLOR_PRIMARIO
    )
    label_titulo.pack(pady=(0, 20))
    
    # Frame para botones
    frame_botones = tk.Frame(frame_principal, bg=constantes.COLOR_FONDO)
    frame_botones.pack()
    
    # Obtener rol del usuario
    es_admin = usuario['rol'] == constantes.ROL_ADMINISTRADOR
    
    # Configuración de botones
    config_boton = {
        "font": ("Arial", 12),
        "width": 25,
        "height": 2,
        "cursor": "hand2",
        "relief": "raised",
        "bd": 2
    }
    
    # BOTONES PARA TODOS LOS USUARIOS (CAJERO Y ADMINISTRADOR)
    
    # Botón Ventas
    boton_ventas = tk.Button(
        frame_botones,
        text="💰 VENTAS",
        bg=constantes.COLOR_EXITO,
        fg="white",
        command=abrir_modulo_ventas,
        **config_boton
    )
    boton_ventas.grid(row=0, column=0, padx=10, pady=8)
    
    # Botón Caja
    boton_caja = tk.Button(
        frame_botones,
        text="💵 CAJA",
        bg=constantes.COLOR_SECUNDARIO,
        fg="white",
        command=abrir_modulo_caja,
        **config_boton
    )
    boton_caja.grid(row=0, column=1, padx=10, pady=8)
    
    # Botón Inventario (MODO CONSULTA para Cajero, COMPLETO para Admin)
    texto_inventario = "📦 INVENTARIO (Consulta)" if not es_admin else "📦 INVENTARIO"
    boton_inventario = tk.Button(
        frame_botones,
        text=texto_inventario,
        bg="#9B59B6",
        fg="white",
        command=abrir_modulo_inventario,
        **config_boton
    )
    boton_inventario.grid(row=1, column=0, padx=10, pady=8)
    
    # Botón Cuentas Corrientes
    boton_cuentas = tk.Button(
        frame_botones,
        text="📒 CUENTAS CORRIENTES",
        bg=constantes.COLOR_ADVERTENCIA,
        fg="white",
        command=abrir_modulo_cuentas_corrientes,
        **config_boton
    )
    boton_cuentas.grid(row=1, column=1, padx=10, pady=8)
    
    # BOTONES SOLO PARA ADMINISTRADORES
    
    if es_admin:
        # Botón Reportes
        boton_reportes = tk.Button(
            frame_botones,
            text="📊 REPORTES",
            bg="#34495E",
            fg="white",
            command=abrir_modulo_reportes,
            **config_boton
        )
        boton_reportes.grid(row=2, column=0, padx=10, pady=8)
        
        # Botón Configuración
        boton_config = tk.Button(
            frame_botones,
            text="⚙️ CONFIGURACIÓN",
            bg="#7F8C8D",
            fg="white",
            command=abrir_modulo_configuracion,
            **config_boton
        )
        boton_config.grid(row=2, column=1, padx=10, pady=8)
    
    # Frame inferior - Botones de acción
    frame_inferior = tk.Frame(ventana, bg=constantes.COLOR_FONDO)
    frame_inferior.pack(fill="x", padx=40, pady=(0, 20))
    
    # Botón Cerrar Sesión
    boton_cerrar_sesion = tk.Button(
        frame_inferior,
        text="🚪 Cerrar Sesión",
        font=("Arial", 10),
        bg=constantes.COLOR_ERROR,
        fg="white",
        width=20,
        cursor="hand2",
        command=lambda: cerrar_sesion(ventana)
    )
    boton_cerrar_sesion.pack(side="left")
    
    # Botón Salir
    boton_salir = tk.Button(
        frame_inferior,
        text="❌ Salir del Sistema",
        font=("Arial", 10),
        bg="#95A5A6",
        fg="white",
        width=20,
        cursor="hand2",
        command=ventana.quit
    )
    boton_salir.pack(side="right")
    
    # Ejecutar ventana
    ventana.mainloop()