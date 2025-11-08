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
    ventana.geometry("950x750")
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
        height=10
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
    
    # Precio Costo
    label_precio_costo = tk.Label(frame_form_interno, text="Precio Costo:", font=("Arial", 10), bg=constantes.COLOR_FONDO)
    label_precio_costo.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entries["precio_costo"] = tk.Entry(frame_form_interno, font=("Arial", 10), width=15)
    entries["precio_costo"].grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    # Stock
    label_stock = tk.Label(frame_form_interno, text="Stock:", font=("Arial", 10), bg=constantes.COLOR_FONDO)
    label_stock.grid(row=1, column=2, sticky="w", padx=5, pady=5)
    entries["stock"] = tk.Entry(frame_form_interno, font=("Arial", 10), width=15)
    entries["stock"].grid(row=1, column=3, padx=5, pady=5, sticky="w")
    
    # ========== CALCULADORA DE GANANCIA ==========
    frame_ganancia = tk.LabelFrame(
        frame_form_interno,
        text="Calcular Precio de Venta (con ganancia)",
        font=("Arial", 9, "bold"),
        bg=constantes.COLOR_FONDO,
        fg=constantes.COLOR_SECUNDARIO
    )
    frame_ganancia.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=10)
    
    frame_ganancia_interno = tk.Frame(frame_ganancia, bg=constantes.COLOR_FONDO)
    frame_ganancia_interno.pack(padx=10, pady=8)
    
    # Botones de porcentaje predeterminado
    label_predefinidos = tk.Label(
        frame_ganancia_interno,
        text="Aplicar ganancia:",
        font=("Arial", 9),
        bg=constantes.COLOR_FONDO
    )
    label_predefinidos.grid(row=0, column=0, padx=5, pady=2, sticky="w")
    
    boton_30 = tk.Button(
        frame_ganancia_interno,
        text="30%",
        font=("Arial", 9, "bold"),
        bg="#27AE60",
        fg="white",
        width=8,
        cursor="hand2",
        command=lambda: aplicar_ganancia(entries, 30)
    )
    boton_30.grid(row=0, column=1, padx=3, pady=2)
    
    boton_40 = tk.Button(
        frame_ganancia_interno,
        text="40%",
        font=("Arial", 9, "bold"),
        bg="#16A085",
        fg="white",
        width=8,
        cursor="hand2",
        command=lambda: aplicar_ganancia(entries, 40)
    )
    boton_40.grid(row=0, column=2, padx=3, pady=2)
    
    boton_50 = tk.Button(
        frame_ganancia_interno,
        text="50%",
        font=("Arial", 9, "bold"),
        bg="#2980B9",
        fg="white",
        width=8,
        cursor="hand2",
        command=lambda: aplicar_ganancia(entries, 50)
    )
    boton_50.grid(row=0, column=3, padx=3, pady=2)
    
    # Porcentaje personalizado
    label_personalizado = tk.Label(
        frame_ganancia_interno,
        text="Personalizado:",
        font=("Arial", 9),
        bg=constantes.COLOR_FONDO
    )
    label_personalizado.grid(row=1, column=0, padx=5, pady=2, sticky="w")
    
    entries["ganancia_custom"] = tk.Entry(frame_ganancia_interno, font=("Arial", 9), width=10)
    entries["ganancia_custom"].grid(row=1, column=1, padx=3, pady=2, sticky="w")
    
    label_porcentaje = tk.Label(
        frame_ganancia_interno,
        text="%",
        font=("Arial", 9),
        bg=constantes.COLOR_FONDO
    )
    label_porcentaje.grid(row=1, column=1, padx=3, pady=2, sticky="e")
    
    boton_aplicar_custom = tk.Button(
        frame_ganancia_interno,
        text="Aplicar",
        font=("Arial", 9, "bold"),
        bg="#8E44AD",
        fg="white",
        width=8,
        cursor="hand2",
        command=lambda: aplicar_ganancia_personalizada(entries)
    )
    boton_aplicar_custom.grid(row=1, column=2, padx=3, pady=2)
    
    # Precio de Venta (resultado)
    label_precio_venta = tk.Label(frame_form_interno, text="Precio Venta:", font=("Arial", 10, "bold"), bg=constantes.COLOR_FONDO, fg=constantes.COLOR_EXITO)
    label_precio_venta.grid(row=3, column=0, sticky="w", padx=5, pady=5)
    entries["precio"] = tk.Entry(frame_form_interno, font=("Arial", 11, "bold"), width=15, fg=constantes.COLOR_EXITO)
    entries["precio"].grid(row=3, column=1, padx=5, pady=5, sticky="w")
    
    # Categoría
    label_categoria = tk.Label(frame_form_interno, text="Categoría:", font=("Arial", 10), bg=constantes.COLOR_FONDO)
    label_categoria.grid(row=3, column=2, sticky="w", padx=5, pady=5)
    entries["categoria"] = ttk.Combobox(
        frame_form_interno,
        font=("Arial", 10),
        width=13,
        values=constantes.CATEGORIAS,
        state="readonly"
    )
    entries["categoria"].grid(row=3, column=3, padx=5, pady=5, sticky="w")
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
        entries["precio_costo"].config(state="disabled")
        entries["precio"].config(state="disabled")
        entries["stock"].config(state="disabled")
        entries["categoria"].config(state="disabled")
        entries["ganancia_custom"].config(state="disabled")


def aplicar_ganancia(entries, porcentaje):
    """
    Aplica un porcentaje de ganancia al precio costo
    
    Parámetros:
        entries: Diccionario con los Entry widgets
        porcentaje: Porcentaje de ganancia a aplicar
    """
    precio_costo = entries["precio_costo"].get().strip()
    
    if not precio_costo:
        messagebox.showwarning("Advertencia", "Primero ingrese el precio de costo")
        entries["precio_costo"].focus()
        return
    
    if not validadores.validar_precio(precio_costo):
        messagebox.showerror("Error", "El precio de costo debe ser un número mayor a 0")
        return
    
    # Calcular precio de venta
    precio_venta = inventario.calcular_precio_con_ganancia(precio_costo, porcentaje)
    
    # Actualizar campo de precio
    entries["precio"].delete(0, tk.END)
    entries["precio"].insert(0, f"{precio_venta:.2f}")


def aplicar_ganancia_personalizada(entries):
    """
    Aplica un porcentaje personalizado de ganancia
    
    Parámetros:
        entries: Diccionario con los Entry widgets
    """
    precio_costo = entries["precio_costo"].get().strip()
    ganancia_custom = entries["ganancia_custom"].get().strip()
    
    if not precio_costo:
        messagebox.showwarning("Advertencia", "Primero ingrese el precio de costo")
        entries["precio_costo"].focus()
        return
    
    if not ganancia_custom:
        messagebox.showwarning("Advertencia", "Ingrese el porcentaje de ganancia")
        entries["ganancia_custom"].focus()
        return
    
    if not validadores.validar_precio(precio_costo):
        messagebox.showerror("Error", "El precio de costo debe ser un número mayor a 0")
        return
    
    if not formateadores.validar_numero(ganancia_custom):
        messagebox.showerror("Error", "El porcentaje debe ser un número válido")
        return
    
    porcentaje = float(ganancia_custom)
    
    if porcentaje < 0:
        messagebox.showerror("Error", "El porcentaje no puede ser negativo")
        return
    
    # Calcular precio de venta
    precio_venta = inventario.calcular_precio_con_ganancia(precio_costo, porcentaje)
    
    # Actualizar campo de precio
    entries["precio"].delete(0, tk.END)
    entries["precio"].insert(0, f"{precio_venta:.2f}")
    
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
    # Por ahora no tenemos precio_costo guardado, mostramos precio de venta
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
    Si está ACTIVO: lo marca como INACTIVO
    Si está INACTIVO: lo elimina PERMANENTEMENTE
    
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
    estado_producto = valores[5]  # "Activo" o "Inactivo"
    
    # Determinar acción según el estado
    if estado_producto == "Activo":
        # Confirmar inactivación
        respuesta = messagebox.askyesno(
            "Confirmar Inactivación",
            f"¿Está seguro que desea INACTIVAR el producto:\n\n'{nombre_producto}'?\n\n"
            f"El producto quedará marcado como inactivo pero no se borrará.\n"
            f"Puede volver a eliminarlo para borrarlo permanentemente."
        )
        
        if not respuesta:
            return
        
        # Eliminar producto (lo marca como inactivo)
        resultado = inventario.eliminar_producto(id_producto)
        
        if resultado == "inactivado":
            messagebox.showinfo("Éxito", f"Producto '{nombre_producto}' marcado como INACTIVO")
            cargar_productos_en_tabla(tabla)
        else:
            messagebox.showerror("Error", "No se pudo inactivar el producto")
    
    else:  # estado_producto == "Inactivo"
        # Confirmar eliminación permanente
        respuesta = messagebox.askyesno(
            "⚠️ CONFIRMAR ELIMINACIÓN PERMANENTE ⚠️",
            f"¿Está seguro que desea ELIMINAR PERMANENTEMENTE el producto:\n\n'{nombre_producto}'?\n\n"
            f"Esta acción NO SE PUEDE DESHACER.\n"
            f"El producto se borrará completamente del sistema.",
            icon="warning"
        )
        
        if not respuesta:
            return
        
        # Eliminar producto permanentemente
        resultado = inventario.eliminar_producto(id_producto)
        
        if resultado == "eliminado":
            messagebox.showinfo("Éxito", f"Producto '{nombre_producto}' ELIMINADO PERMANENTEMENTE")
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
    entries["precio_costo"].delete(0, tk.END)
    entries["precio"].delete(0, tk.END)
    entries["stock"].delete(0, tk.END)
    entries["ganancia_custom"].delete(0, tk.END)
    if constantes.CATEGORIAS:
        entries["categoria"].current(0)