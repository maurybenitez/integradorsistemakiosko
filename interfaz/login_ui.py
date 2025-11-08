"""
INTERFAZ LOGIN
Pantalla de inicio de sesión
"""

import tkinter as tk
from tkinter import messagebox
from modulos import usuarios
from utils import constantes


def mostrar_login():
    """
    Muestra la ventana de login
    Retorna True si login exitoso, False si se cerró
    """
    # Variable para controlar si el login fue exitoso
    login_exitoso = [False]  # Usamos lista para poder modificarla dentro de funciones internas
    
    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Sistema Kiosko - Inicio de Sesión")
    ventana.geometry(constantes.VENTANA_LOGIN)
    ventana.resizable(False, False)
    ventana.configure(bg=constantes.COLOR_FONDO)
    
    # Centrar ventana en la pantalla
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()
    alto_ventana = ventana.winfo_height()
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana.geometry(f"+{x}+{y}")
    
    # Frame principal
    frame_principal = tk.Frame(ventana, bg=constantes.COLOR_FONDO)
    frame_principal.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Título
    label_titulo = tk.Label(
        frame_principal,
        text="SISTEMA DE GESTIÓN\nKIOSKO",
        font=("Arial", 18, "bold"),
        bg=constantes.COLOR_FONDO,
        fg=constantes.COLOR_PRIMARIO
    )
    label_titulo.pack(pady=(0, 30))
    
    # Frame del formulario
    frame_form = tk.Frame(frame_principal, bg=constantes.COLOR_FONDO)
    frame_form.pack()
    
    # Usuario
    label_usuario = tk.Label(
        frame_form,
        text="Usuario:",
        font=("Arial", 11),
        bg=constantes.COLOR_FONDO,
        fg=constantes.COLOR_PRIMARIO
    )
    label_usuario.grid(row=0, column=0, sticky="w", pady=5)
    
    entry_usuario = tk.Entry(
        frame_form,
        font=("Arial", 11),
        width=25
    )
    entry_usuario.grid(row=0, column=1, pady=5, padx=(10, 0))
    entry_usuario.focus()  # Foco inicial
    
    # Contraseña
    label_contrasena = tk.Label(
        frame_form,
        text="Contraseña:",
        font=("Arial", 11),
        bg=constantes.COLOR_FONDO,
        fg=constantes.COLOR_PRIMARIO
    )
    label_contrasena.grid(row=1, column=0, sticky="w", pady=5)
    
    entry_contrasena = tk.Entry(
        frame_form,
        font=("Arial", 11),
        width=25,
        show="●"  # Ocultar contraseña
    )
    entry_contrasena.grid(row=1, column=1, pady=5, padx=(10, 0))
    
    # Label para mensajes de error
    label_mensaje = tk.Label(
        frame_principal,
        text="",
        font=("Arial", 9),
        bg=constantes.COLOR_FONDO,
        fg=constantes.COLOR_ERROR
    )
    label_mensaje.pack(pady=(10, 0))
    
    # Función para validar login
    def validar_login_interno():
        validar_login(ventana, entry_usuario, entry_contrasena, label_mensaje, login_exitoso)
    
    # Botón Ingresar
    boton_ingresar = tk.Button(
        frame_principal,
        text="INGRESAR",
        font=("Arial", 11, "bold"),
        bg=constantes.COLOR_SECUNDARIO,
        fg="white",
        width=20,
        cursor="hand2",
        command=validar_login_interno
    )
    boton_ingresar.pack(pady=(20, 10))
    
    # Permitir Enter para hacer login
    entry_usuario.bind("<Return>", lambda e: validar_login_interno())
    entry_contrasena.bind("<Return>", lambda e: validar_login_interno())
    
    # Información de ayuda
    label_ayuda = tk.Label(
        frame_principal,
        text="Usuario por defecto: admin / admin123",
        font=("Arial", 8, "italic"),
        bg=constantes.COLOR_FONDO,
        fg="gray"
    )
    label_ayuda.pack(side="bottom", pady=(10, 0))
    
    # Ejecutar ventana
    ventana.mainloop()
    
    return login_exitoso[0]


def validar_login(ventana, entry_usuario, entry_contrasena, label_mensaje, login_exitoso):
    """
    Valida las credenciales ingresadas
    
    Parámetros:
        ventana: Ventana de tkinter
        entry_usuario: Entry del nombre de usuario
        entry_contrasena: Entry de la contraseña
        label_mensaje: Label para mostrar mensajes
        login_exitoso: Lista con boolean para indicar éxito
    """
    # Obtener valores
    nombre_usuario = entry_usuario.get().strip()
    contrasena = entry_contrasena.get()
    
    # Limpiar mensaje anterior
    label_mensaje.config(text="")
    
    # Validar campos vacíos
    if not nombre_usuario or not contrasena:
        label_mensaje.config(text="⚠ Complete todos los campos")
        return
    
    # Autenticar usuario
    usuario = usuarios.autenticar_usuario(nombre_usuario, contrasena)
    
    if usuario:
        # Login exitoso
        # Guardar usuario actual en variable global
        constantes.usuario_actual = usuario
        
        # Marcar login como exitoso
        login_exitoso[0] = True
        
        # Cerrar ventana de login
        ventana.destroy()
    else:
        # Login fallido
        label_mensaje.config(text="✗ Usuario o contraseña incorrectos")
        entry_contrasena.delete(0, tk.END)  # Limpiar contraseña
        entry_usuario.focus()