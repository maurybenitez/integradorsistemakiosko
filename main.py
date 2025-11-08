"""
SISTEMA DE GESTIÓN PARA KIOSKO
Trabajo Integrador Final - Programación I
Programación Estructurada (Sin POO)

Punto de entrada principal del sistema
"""
from interfaz import login_ui, menu_principal_ui
from utils import constantes


def main():
    """
    Función principal que inicia el sistema
    - Carga configuración inicial
    - Muestra pantalla de login
    - Controla el flujo del programa
    """
    print("  SISTEMA DE GESTIÓN PARA KIOSKO")
    print("  Programación I - Trabajo Integrador Final")
  
    # Bucle principal del sistema
    while True:
        login_exitoso = login_ui.mostrar_login()
        
        # Si el login no fue exitoso, salir del sistema
        if not login_exitoso:
            print("  Sistema cerrado por el usuario")
            break
        
        # Login exitoso
        print(f"  Login exitoso")
        print(f"  Usuario: {constantes.usuario_actual['nombre_usuario']}")
        print(f"  Rol: {constantes.usuario_actual['rol']}")
        print()
        
        # Mostrar menú principal
        menu_principal_ui.mostrar_menu_principal()
        
        # Al cerrar el menú, verificar si el usuario cerró sesión o salió
        if constantes.usuario_actual is None:
            # Usuario cerró sesión, volver al login
            print("  Sesión cerrada. Volviendo al login...")
            print()
            continue
        else:
            # Usuario salió del sistema
            print("  Saliendo del sistema")
            break


if __name__ == "__main__":
    main()
