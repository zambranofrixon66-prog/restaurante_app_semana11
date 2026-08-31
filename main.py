from servicios.restaurante import Restaurante

def mostrar_menu():
    print("\n" + "="*50)
    print("        SISTEMA DE GESTIÓN RESTAURANTE APP        ")
    print("="*50)
    print("1. Registrar Producto")
    print("2. Listar Productos (ver stock)")
    print("3. Registrar Usuario")
    print("4. Listar Usuarios")
    print("5. Realizar Venta de Producto")
    print("6. Consultar Ventas por Usuario")
    print("7. Salir")
    print("="*50)

def main():
    servicio = Restaurante()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            print("\n--- Registrar Producto ---")
            codigo = input("Código: ").strip()
            nombre = input("Nombre: ").strip()
            try:
                precio = float(input("Precio ($): "))
                stock = int(input("Stock inicial: "))
                if servicio.registrar_producto(codigo, nombre, precio, stock):
                    print("✓ Producto registrado exitosamente.")
                else:
                    print("✗ Error: El código ya existe.")
            except ValueError as e:
                print(f"✗ Error: {e}")

        elif opcion == "2":
            print("\n--- Lista de Productos ---")
            if not servicio.productos:
                print("No hay productos registrados.")
            else:
                for p in servicio.productos:
                    print(f" - {p}")

        elif opcion == "3":
            print("\n--- Registrar Usuario ---")
            identificacion = input("Identificación / Cédula: ").strip()
            nombre = input("Nombre completo: ").strip()
            correo = input("Correo electrónico: ").strip()
            try:
                if servicio.registrar_usuario(identificacion, nombre, correo):
                    print("✓ Usuario registrado exitosamente.")
                else:
                    print("✗ Error: La identificación ya existe.")
            except ValueError as e:
                print(f"✗ Error: {e}")

        elif opcion == "4":
            print("\n--- Lista de Usuarios ---")
            if not servicio.usuarios:
                print("No hay usuarios registrados.")
            else:
                for u in servicio.usuarios:
                    print(f" - {u}")

        elif opcion == "5":
            print("\n--- Operación de Venta ---")
            identificacion = input("Identificación del Usuario: ").strip()
            codigo = input("Código del Producto: ").strip()
            try:
                cantidad = int(input("Cantidad a comprar: "))
                if servicio.vender_producto(codigo, identificacion, cantidad):
                    print("✓ ¡Venta registrada con éxito!")
                else:
                    print("✗ Error: Verifique usuario, producto y stock disponible.")
            except ValueError as e:
                print(f"✗ Error: {e}")

        elif opcion == "6":
            print("\n--- Consultar Ventas de un Usuario ---")
            identificacion = input("Identificación del Usuario: ").strip()
            user = servicio.buscar_usuario(identificacion)
            if not user:
                print("✗ Error: El usuario no existe.")
            else:
                ventas = servicio.consultar_ventas_usuario(identificacion)
                print(f"\nHistorial de compras de {user.nombre}:")
                if not ventas:
                    print("No registra compras.")
                else:
                    for v in ventas:
                        prod = servicio.buscar_producto(v.producto_codigo)
                        nombre_prod = prod.nombre if prod else "Desconocido"
                        print(f" • Producto: {v.producto_codigo} ({nombre_prod}) | Cantidad: {v.cantidad}")

        elif opcion == "7":
            servicio.guardar_productos()
            servicio.guardar_usuarios()
            servicio.guardar_ventas()
            print("\nPrograma finalizado.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()