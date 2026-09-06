from servicios.restaurante import Restaurante

def mostrar_menu():
    print("\n" + "="*55)
    print("      SISTEMA DE GESTIÓN RESTAURANTE APP (SEMANA 12)     ")
    print("="*55)
    print("1. Registrar Producto")
    print("2. Listar Productos (ver stock)")
    print("3. Buscar Producto por Código [Optimizado O(1) promedio]")
    print("4. Registrar Usuario")
    print("5. Listar Usuarios")
    print("6. Buscar Usuario por Identificación [Optimizado O(1) promedio]")
    print("7. Realizar Venta de Producto (Control de Stock)")
    print("8. Consultar Ventas por Usuario [Agrupado O(1) promedio]")
    print("9. Salir")
    print("="*55)

def main():
    servicio = Restaurante()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-9): ").strip()

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
                    print("✗ Error: El código ya existe (validado en índice dict).")
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
            print("\n--- Búsqueda Directa de Producto por Código ---")
            codigo = input("Ingrese el código a buscar: ").strip()
            prod = servicio.buscar_producto(codigo)
            if prod:
                print(f"✓ Encontrado: {prod.nombre} | Precio: ${prod.precio} | Stock: {prod.stock}")
            else:
                print("✗ Error: Producto no encontrado.")

        elif opcion == "4":
            print("\n--- Registrar Usuario ---")
            identificacion = input("Identificación / Cédula: ").strip()
            nombre = input("Nombre completo: ").strip()
            correo = input("Correo electrónico: ").strip()
            try:
                if servicio.registrar_usuario(identificacion, nombre, correo):
                    print("✓ Usuario registrado exitosamente.")
                else:
                    print("✗ Error: La identificación o el correo ya se encuentran registrados.")
            except ValueError as e:
                print(f"✗ Error: {e}")

        elif opcion == "5":
            print("\n--- Lista de Usuarios ---")
            if not servicio.usuarios:
                print("No hay usuarios registrados.")
            else:
                for u in servicio.usuarios:
                    print(f" - {u}")

        elif opcion == "6":
            print("\n--- Búsqueda Directa de Usuario por Identificación ---")
            identificacion = input("Ingrese la identificación a buscar: ").strip()
            user = servicio.buscar_usuario(identificacion)
            if user:
                print(f"✓ Encontrado: {user.nombre} | ID: {user.usuario_id} | Correo: {getattr(user, 'correo', 'Sin correo')}")
            else:
                print("✗ Error: Usuario no registrado.")

        elif opcion == "7":
            print("\n--- Operación de Venta ---")
            identificacion = input("Identificación del Usuario: ").strip()
            codigo = input("Código del Producto: ").strip()
            try:
                cantidad = int(input("Cantidad a comprar: "))
                if servicio.vender_producto(codigo, identificacion, cantidad):
                    print("✓ ¡Venta registrada y stock actualizado con éxito!")
                else:
                    print("✗ Error: Verifique usuario, producto o stock suficiente.")
            except ValueError as e:
                print(f"✗ Error: {e}")

        elif opcion == "8":
            print("\n--- Consultar Ventas de un Usuario (Índice Agrupador) ---")
            identificacion = input("Identificación del Usuario: ").strip()
            user = servicio.buscar_usuario(identificacion)
            if not user:
                print("✗ Error: El usuario no existe.")
            else:
                ventas = servicio.consultar_ventas_usuario(identificacion)
                print(f"\nHistorial de compras de {user.nombre} ({len(ventas)} ventas):")
                if not ventas:
                    print("No registra compras.")
                else:
                    for v in ventas:
                        prod = servicio.buscar_producto(v.producto_codigo)
                        nombre_prod = prod.nombre if prod else "Desconocido"
                        print(f" • Producto: {v.producto_codigo} ({nombre_prod}) | Cantidad: {v.cantidad}")

        elif opcion == "9":
            servicio.guardar_productos()
            servicio.guardar_usuarios()
            servicio.guardar_ventas()
            print("\nDatos sincronizados en JSON. Programa finalizado.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()