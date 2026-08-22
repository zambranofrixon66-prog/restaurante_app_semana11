from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante import Restaurante


RUTA_PRODUCTOS = (
    Path(__file__).resolve().parent
    / "data"
    / "productos.json"
)


def solicitar_texto(mensaje: str) -> str:
    while True:
        texto = input(mensaje).strip()

        if texto:
            return texto

        print("Este dato no puede quedar vacío.")


def solicitar_precio() -> float:
    while True:
        try:
            precio = float(
                input("Precio del producto: ")
            )

            if precio <= 0:
                print(
                    "El precio debe ser mayor que cero."
                )
                continue

            return precio

        except ValueError:
            print("Ingrese un precio válido.")


def solicitar_categoria(
    restaurante: Restaurante
) -> str:
    while True:
        restaurante.mostrar_categorias_permitidas()

        categoria = solicitar_texto(
            "Categoría del producto: "
        )

        categoria_normalizada = (
            restaurante.normalizar_categoria(
                categoria
            )
        )

        if categoria_normalizada is not None:
            return categoria_normalizada

        print(
            "La categoría ingresada no está permitida."
        )


def registrar_producto(
    restaurante: Restaurante
) -> None:
    try:
        codigo = solicitar_texto(
            "Código del producto: "
        )
        nombre = solicitar_texto(
            "Nombre del producto: "
        )
        categoria = solicitar_categoria(restaurante)
        precio = solicitar_precio()

        producto = Producto(
            codigo,
            nombre,
            categoria,
            precio
        )

        if restaurante.registrar_producto(producto):
            print(
                "Producto registrado correctamente."
            )
        else:
            print(
                "No se pudo registrar el producto. "
                "Compruebe que el código no esté repetido."
            )

    except ValueError as error:
        print(f"Error: {error}")


def buscar_producto(
    restaurante: Restaurante
) -> None:
    codigo = solicitar_texto(
        "Código del producto que desea buscar: "
    )

    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
    else:
        print(producto.mostrar_informacion())


def actualizar_producto(
    restaurante: Restaurante
) -> None:
    codigo = solicitar_texto(
        "Código del producto que desea actualizar: "
    )

    producto = restaurante.buscar_producto(codigo)

    if producto is None:
        print("Producto no encontrado.")
        return

    try:
        nombre = solicitar_texto("Nuevo nombre: ")
        categoria = solicitar_categoria(restaurante)
        precio = solicitar_precio()

        if restaurante.actualizar_producto(
            codigo,
            nombre,
            categoria,
            precio
        ):
            print(
                "Producto actualizado correctamente."
            )
        else:
            print(
                "No se pudo actualizar el producto."
            )

    except ValueError as error:
        print(f"Error: {error}")


def eliminar_producto(
    restaurante: Restaurante
) -> None:
    codigo = solicitar_texto(
        "Código del producto que desea eliminar: "
    )

    if restaurante.eliminar_producto(codigo):
        print("Producto eliminado correctamente.")
    else:
        print("Producto no encontrado.")


def registrar_usuario(
    restaurante: Restaurante
) -> None:
    identificacion = solicitar_texto(
        "Identificación del usuario: "
    )
    nombre = solicitar_texto(
        "Nombre del usuario: "
    )
    correo = solicitar_texto(
        "Correo del usuario: "
    )

    usuario = Usuario(
        identificacion,
        nombre,
        correo
    )

    if restaurante.registrar_usuario(usuario):
        print("Usuario registrado correctamente.")
    else:
        print(
            "Ya existe un usuario con esa "
            "identificación."
        )


def mostrar_menu() -> None:
    print("\n===================================")
    print("        SISTEMA DE RESTAURANTE")
    print("===================================")
    print("1. Registrar producto")
    print("2. Buscar producto")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Listar productos")
    print("-----------------------------------")
    print("6. Registrar usuario")
    print("7. Listar usuarios")
    print("-----------------------------------")
    print("8. Mostrar categorías")
    print("9. Salir")


def main() -> None:
    restaurante = Restaurante(
        str(RUTA_PRODUCTOS)
    )

    acciones = {
        "1": registrar_producto,
        "2": buscar_producto,
        "3": actualizar_producto,
        "4": eliminar_producto,
        "5": Restaurante.listar_productos,
        "6": registrar_usuario,
        "7": Restaurante.listar_usuarios,
        "8": Restaurante.mostrar_categorias
    }

    while True:
        mostrar_menu()

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        if opcion == "9":
            print("Programa finalizado.")
            break

        accion = acciones.get(opcion)

        if accion is None:
            print(
                "Opción inválida. Intente nuevamente."
            )
        else:
            accion(restaurante)


if __name__ == "__main__":
    main()