"""
INTERFAZ INVENTARIO
Pantalla de gestión de productos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from modulos import inventario
from utils import constantes, formateadores, validadores


def mostrar_inventario():
    """
    Muestra la ventana de gestión de inventario
    """
    # Verificar que haya un usuario logueado
    if not constantes.usuario_actual:
        messagebox.showerror("Error", "No hay un usuario logueado")
        return
    
    # Verificar si es modo consulta (CAJERO)
    es_admin = constantes.usuario_actual['rol'] == constantes.ROL_ADMINISTRADOR
    modo_consulta = not es_admin
    
    # Crear ventana
    ventana = tk.Toplevel()
    ventana.title("Sistema Kiosko - Inventario" + (" (Modo Consulta)" if modo_consulta else ""))
    ventana.geometry(constantes.VENTANA_MODULO)
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
    
    # Frame superior - Título
    frame_superior = tk.Frame(ventana, bg=constantes.COLOR_PRIMARIO, height=60)
    frame_superior.pack(fill="x")
    frame_superior.pack_propagate(False)
    
    label_titulo = tk.Label(
        frame_superior,
        text="📦 GESTIÓN DE INVENTARIO" + (" - MODO CONSULTA" if modo_consulta else ""),
        font=("Arial", 16, "bold"),
        bg=constantes.COLOR_PRIMARIO,
        fg="white"
    )
    label_titulo.pack(expand=True)
    
    # Frame principal
    frame_principal = tk.Frame(ventana, bg=constantes.COLOR_FONDO)
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
    
    # ========== SECCIÓN BÚSQUEDA ==========
    frame_busqueda = tk.LabelFrame(
        frame_principal,
        text="Buscar Producto",
        font=("Arial", 10, "bold"),
        bg=constantes.COLOR_FONDO,
        fg=constantes.COLOR_PRIMARIO
    )
    frame_busqueda.pack(fill="x", pady=(0, 10))
    
    frame_busqueda_interno = tk.Frame(frame_busqueda, bg=constantes.COLOR_FONDO)
    frame_busqueda_interno.pack(padx=10, pady=10)
    
    label_buscar = tk.Label(
        frame_busqueda_interno,
        text="Nombre:",
        font=("Arial", 10),
        bg=constantes.COLOR_FONDO
    )
    label_buscar.pack(side="left", padx=(0, 10))
    
    entry_buscar = tk.Entry(
        frame_busqueda_interno,
        font=("Arial", 10),
        width=30
    )
    entry_buscar.pack(side="left", padx=(0, 10))
    
    boton_buscar = tk.Button(
        frame_busqueda_interno,
        text="🔍 Buscar",
        font=("Arial", 9),
        bg=constantes.COLOR_SECUNDARIO,
        fg="white",
        cursor="hand2",
        command=lambda: buscar_y_actualizar(entry_buscar, tabla)
    )
    boton_buscar.pack(side="left", padx=(0, 5))
    
    boton_mostrar_todos = tk.Button(
        frame_busqueda_interno,
        text="📋 Mostrar Todos",
        font=("Arial", 9),
        bg=constantes.COLOR_SECUNDARIO,
        fg="white",
        cursor="hand2",
        command=lambda: cargar_productos_en_tabla(tabla)
    )
    boton_mostrar_todos.pack(side="left")
    
    # ========== SECCIÓN TABLA ==========
    frame_tabla = tk.Frame(frame_principal, bg=constantes.COLOR_FONDO)
    frame_tabla.pack(fill="both", expand=True, pady=(0, 10))
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_tabla)
    scrollbar.pack(side="right", fill="y")
    
    # Tabla (Treeview)
    columnas = ("ID", "Nombre", "Precio", "Stock", "Categoría", "Estado")
    tabla = ttk.Treeview(
        frame_tabla,
        columns=columnas,
        show="headings",
        yscrollcommand=scrollbar.set,
        height=12
    )
    scrollbar.config(command=tabla.yview)
    
    # Configurar columnas
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre del Producto")
    tabla.heading("Precio", text="Precio")
    tabla.heading("Stock", text="Stock")
    tabla.heading("Categoría", text="Categoría")
    tabla.heading("Estado", text="Estado")
    
    tabla.column("ID", width=50, anchor="center")
    tabla.column("Nombre", width=250, anchor="w")
    tabla.column("Precio", width=100, anchor="e")
    tabla.column("Stock", width=80, anchor="center")
    tabla.column("Categoría", width=120, anchor="center")
    tabla.column("Estado", width=80, anchor="center")
    
    tabla.pack(fill="both", expand=True)
    
    # Evento de selección en tabla
    tabla.bind("<<TreeviewSelect>>", lambda e: cargar_producto_en_formulario(tabla, entries))
    
    # ========== SECCIÓN FORMULARIO ==========
    frame_formulario = tk.LabelFrame(
        frame_principal,
        text="Datos del Producto",
        font=("Arial", 10, "bold"),
        bg=constantes.COLOR_FONDO,
        fg=constantes.COLOR_PRIMARIO
    )
    frame_formulario.pack(fill="x", pady=(0, 10))
    
    frame_form_interno = tk.Frame(frame_formulario, bg=constantes.COLOR_FONDO)
    frame_form_interno.pack(padx=10, pady=10)
    
    # Diccionario para guardar referencias de los entries
    entries = {}
    
    # ID (oculto, solo para referencia)
    entries["id"] = tk.IntVar(value=0)
    
    # Nombre
    label_nombre = tk.Label(frame_form_interno, text="Nombre:", font=("Arial", 10), bg=constantes.COLOR_FONDO)
    label_nombre.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entries["nombre"] = tk.Entry(frame_form_interno, font=("Arial", 10), width=40)
    entries["nombre"].grid(row=0, column=1, padx=5, pady=5, columnspan=3)
    
    # Precio
    label_precio = tk.Label(frame_form_interno, text="Precio:", font=("Arial", 10), bg=constantes.COLOR_FONDO)
    label_precio.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entries["precio"] = tk.Entry(frame_form_interno, font=("Arial", 10), width=15)
    entries["precio"].grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    # Stock
    label_stock = tk.Label(frame_form_interno, text="Stock:", font=("Arial", 10), bg=constantes.COLOR_FONDO)
    label_stock.grid(row=1, column=2, sticky="w", padx=5, pady=5)
    entries["stock"] = tk.Entry(frame_form_interno, font=("Arial", 10), width=15)
    entries["stock"].grid(row=1, column=3, padx=5, pady=5, sticky="w")
    
    # Categoría
    label_categoria = tk.Label(frame_form_interno, text="Categoría:", font=("Arial", 10), bg=constantes.COLOR_FONDO)
    label_categoria.grid(row=2, column=0, sticky="w", padx=5, pady=5)
    entries["categoria"] = ttk.Combobox(
        frame_form_interno,
        font=("Arial", 10),
        width=18,
        values=constantes.CATEGORIAS,
        state="readonly"
    )
    entries["categoria"].grid(row=2, column=1, padx=5, pady=5, sticky="w")
    if constantes.CATEGORIAS:
        entries["categoria"].current(0)
    
    # ========== SECCIÓN BOTONES ==========
    frame_botones = tk.Frame(frame_principal, bg=constantes.COLOR_FONDO)
    frame_botones.pack(fill="x")
    
    # Botones solo habilitados para ADMINISTRADOR
    if not modo_consulta:
        boton_agregar = tk.Button(
            frame_botones,
            text="➕ Agregar Producto",
            font=("Arial", 10, "bold"),
            bg=constantes.COLOR_EXITO,
            fg="white",
            width=18,
            cursor="hand2",
            command=lambda: agregar_producto_ui(entries, tabla)
        )
        boton_agregar.pack(side="left", padx=5)
        
        boton_modificar = tk.Button(
            frame_botones,
            text="✏️ Modificar",
            font=("Arial", 10, "bold"),
            bg=constantes.COLOR_ADVERTENCIA,
            fg="white",
            width=18,
            cursor="hand2",
            command=lambda: modificar_producto_ui(tabla, entries)
        )
        boton_modificar.pack(side="left", padx=5)
        
        boton_eliminar = tk.Button(
            frame_botones,
            text="🗑️ Eliminar",
            font=("Arial", 10, "bold"),
            bg=constantes.COLOR_ERROR,
            fg="white",
            width=18,
            cursor="hand2",
            command=lambda: eliminar_producto_ui(tabla)
        )
        boton_eliminar.pack(side="left", padx=5)
    
    boton_limpiar = tk.Button(
        frame_botones,
        text="🔄 Limpiar Formulario",
        font=("Arial", 10),
        bg="#95A5A6",
        fg="white",
        width=18,
        cursor="hand2",
        command=lambda: limpiar_formulario(entries)
    )
    boton_limpiar.pack(side="left", padx=5)
    
    boton_cerrar = tk.Button(
        frame_botones,
        text="❌ Cerrar",
        font=("Arial", 10),
        bg="#7F8C8D",
        fg="white",
        width=18,
        cursor="hand2",
        command=ventana.destroy
    )
    boton_cerrar.pack(side="right", padx=5)
    
    # Mensaje de modo consulta
    if modo_consulta:
        label_info = tk.Label(
            frame_botones,
            text="ℹ️ Modo consulta: Solo puede visualizar productos",
            font=("Arial", 9, "italic"),
            bg=constantes.COLOR_FONDO,
            fg=constantes.COLOR_ADVERTENCIA
        )
        label_info.pack(side="left", padx=20)
    
    # Cargar productos inicialmente
    cargar_productos_en_tabla(tabla)
    
    # Deshabilitar entries en modo consulta
    if modo_consulta:
        entries["nombre"].config(state="disabled")
        entries["precio"].config(state="disabled")
        entries["stock"].config(state="disabled")
        entries["categoria"].config(state="disabled")


def cargar_productos_en_tabla(tabla):
    """
    Carga los productos en la tabla
    
    Parámetros:
        tabla: Widget Treeview donde mostrar los productos
    """
    # Limpiar tabla
    for item in tabla.get_children():
        tabla.delete(item)
    
    # Obtener productos
    productos = inventario.listar_productos()
    
    # Cargar productos en la tabla
    for producto in productos:
        precio_formateado = formateadores.formatear_precio(producto["precio"])
        estado = "Activo" if producto.get("activo", True) else "Inactivo"
        
        # Color según estado
        tag = "activo" if producto.get("activo", True) else "inactivo"
        
        tabla.insert(
            "",
            "end",
            values=(
                producto["id"],
                producto["nombre"],
                precio_formateado,
                producto["stock"],
                producto["categoria"],
                estado
            ),
            tags=(tag,)
        )
    
    # Configurar colores
    tabla.tag_configure("activo", background="white")
    tabla.tag_configure("inactivo", background="#FFCDD2", foreground="gray")
    
    # Mostrar cantidad total
    print(f"Total de productos: {len(productos)}")


def buscar_y_actualizar(entry_buscar, tabla):
    """
    Busca productos y actualiza la tabla
    """
    termino = entry_buscar.get().strip()
    
    if not termino:
        messagebox.showwarning("Advertencia", "Ingrese un término de búsqueda")
        return
    
    # Limpiar tabla
    for item in tabla.get_children():
        tabla.delete(item)
    
    # Buscar productos
    productos = inventario.buscar_productos(termino)
    
    if not productos:
        messagebox.showinfo("Búsqueda", f"No se encontraron productos con '{termino}'")
        return
    
    # Cargar resultados en la tabla
    for producto in productos:
        precio_formateado = formateadores.formatear_precio(producto["precio"])
        estado = "Activo" if producto.get("activo", True) else "Inactivo"
        tag = "activo" if producto.get("activo", True) else "inactivo"
        
        tabla.insert(
            "",
            "end",
            values=(
                producto["id"],
                producto["nombre"],
                precio_formateado,
                producto["stock"],
                producto["categoria"],
                estado
            ),
            tags=(tag,)
        )
    
    # Configurar colores
    tabla.tag_configure("activo", background="white")
    tabla.tag_configure("inactivo", background="#FFCDD2", foreground="gray")
    
    messagebox.showinfo("Búsqueda", f"Se encontraron {len(productos)} producto(s)")


def cargar_producto_en_formulario(tabla, entries):
    """
    Carga los datos del producto seleccionado en el formulario
    """
    # Obtener selección
    seleccion = tabla.selection()
    if not seleccion:
        return
    
    # Obtener datos del item seleccionado
    item = tabla.item(seleccion[0])
    valores = item["values"]
    
    # Cargar en el formulario
    id_producto = valores[0]
    
    # Obtener producto completo
    producto = inventario.obtener_producto_por_id(id_producto)
    if not producto:
        return
    
    # Limpiar formulario
    limpiar_formulario(entries)
    
    # Cargar datos
    entries["id"].set(producto["id"])
    entries["nombre"].insert(0, producto["nombre"])
    entries["precio"].insert(0, str(producto["precio"]))
    entries["stock"].insert(0, str(producto["stock"]))
    
    # Seleccionar categoría
    try:
        index = constantes.CATEGORIAS.index(producto["categoria"])
        entries["categoria"].current(index)
    except ValueError:
        pass


def agregar_producto_ui(entries, tabla):
    """
    Agrega un producto desde la interfaz
    
    Parámetros:
        entries: Diccionario con los Entry widgets
        tabla: Tabla a actualizar
    """
    # Obtener valores
    nombre = entries["nombre"].get().strip()
    precio = entries["precio"].get().strip()
    stock = entries["stock"].get().strip()
    categoria = entries["categoria"].get()
    
    # Validar campos vacíos
    if validadores.campos_vacios(nombre, precio, stock, categoria):
        messagebox.showerror("Error", "Complete todos los campos")
        return
    
    # Validar precio
    if not validadores.validar_precio(precio):
        messagebox.showerror("Error", "El precio debe ser un número mayor a 0")
        return
    
    # Validar stock
    if not validadores.validar_stock(stock):
        messagebox.showerror("Error", "El stock debe ser un número entero mayor o igual a 0")
        return
    
    # Agregar producto
    id_nuevo = inventario.agregar_producto(nombre, float(precio), int(stock), categoria)
    
    if id_nuevo:
        messagebox.showinfo("Éxito", f"Producto agregado con ID: {id_nuevo}")
        limpiar_formulario(entries)
        cargar_productos_en_tabla(tabla)
    else:
        messagebox.showerror("Error", "No se pudo agregar el producto")


def modificar_producto_ui(tabla, entries):
    """
    Modifica un producto seleccionado
    
    Parámetros:
        tabla: Tabla de productos
        entries: Diccionario con los Entry widgets
    """
    # Verificar que haya un producto seleccionado
    if entries["id"].get() == 0:
        messagebox.showwarning("Advertencia", "Seleccione un producto de la tabla para modificar")
        return
    
    # Obtener valores
    id_producto = entries["id"].get()
    nombre = entries["nombre"].get().strip()
    precio = entries["precio"].get().strip()
    stock = entries["stock"].get().strip()
    categoria = entries["categoria"].get()
    
    # Validar campos vacíos
    if validadores.campos_vacios(nombre, precio, stock, categoria):
        messagebox.showerror("Error", "Complete todos los campos")
        return
    
    # Validar precio
    if not validadores.validar_precio(precio):
        messagebox.showerror("Error", "El precio debe ser un número mayor a 0")
        return
    
    # Validar stock
    if not validadores.validar_stock(stock):
        messagebox.showerror("Error", "El stock debe ser un número entero mayor o igual a 0")
        return
    
    # Confirmar modificación
    respuesta = messagebox.askyesno(
        "Confirmar",
        f"¿Está seguro que desea modificar el producto '{nombre}'?"
    )
    
    if not respuesta:
        return
    
    # Modificar producto
    datos_nuevos = {
        "nombre": nombre,
        "precio": float(precio),
        "stock": int(stock),
        "categoria": categoria
    }
    
    if inventario.actualizar_producto(id_producto, datos_nuevos):
        messagebox.showinfo("Éxito", "Producto modificado correctamente")
        limpiar_formulario(entries)
        cargar_productos_en_tabla(tabla)
    else:
        messagebox.showerror("Error", "No se pudo modificar el producto")


def eliminar_producto_ui(tabla):
    """
    Elimina un producto seleccionado
    
    Parámetros:
        tabla: Tabla de productos
    """
    # Obtener selección
    seleccion = tabla.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un producto de la tabla para eliminar")
        return
    
    # Obtener datos del item seleccionado
    item = tabla.item(seleccion[0])
    valores = item["values"]
    id_producto = valores[0]
    nombre_producto = valores[1]
    
    # Confirmar eliminación
    respuesta = messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Está seguro que desea eliminar el producto:\n\n'{nombre_producto}'?\n\nEsta acción marcará el producto como inactivo."
    )
    
    if not respuesta:
        return
    
    # Eliminar producto
    if inventario.eliminar_producto(id_producto):
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")
        cargar_productos_en_tabla(tabla)
    else:
        messagebox.showerror("Error", "No se pudo eliminar el producto")


def limpiar_formulario(entries):
    """
    Limpia el formulario de producto
    
    Parámetros:
        entries: Diccionario con los Entry widgets
    """
    entries["id"].set(0)
    entries["nombre"].delete(0, tk.END)
    entries["precio"].delete(0, tk.END)
    entries["stock"].delete(0, tk.END)
    if constantes.CATEGORIAS:
        entries["categoria"].current(0)