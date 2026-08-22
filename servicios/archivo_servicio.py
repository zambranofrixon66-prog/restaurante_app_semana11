import json

from modelos.producto import Producto


class ArchivoServicio:
    def __init__(self, ruta_archivo: str) -> None:
        self.ruta_archivo = ruta_archivo

    def guardar_productos(self, productos: list) -> bool:
        try:
            datos = [
                producto.a_diccionario()
                for producto in productos
            ]

            with open(
                self.ruta_archivo,
                "w",
                encoding="utf-8"
            ) as archivo:
                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=4
                )

            return True

        except PermissionError:
            print("No se tienen permisos para guardar el archivo.")
            return False

        except OSError as error:
            print(f"No se pudo guardar la información: {error}")
            return False

    def cargar_productos(self) -> list:
        try:
            with open(
                self.ruta_archivo,
                "r",
                encoding="utf-8"
            ) as archivo:
                datos = json.load(archivo)

            if not isinstance(datos, list):
                raise ValueError(
                    "El contenido del archivo JSON debe ser una lista."
                )

            productos = []

            for posicion, dato in enumerate(datos, start=1):
                try:
                    producto = Producto.desde_diccionario(dato)
                    productos.append(producto)

                except (KeyError, TypeError, ValueError) as error:
                    print(
                        f"El producto de la posición {posicion} "
                        f"no pudo cargarse: {error}"
                    )

            return productos

        except FileNotFoundError:
            print(
                "El archivo productos.json no existe. "
                "Se iniciará con una lista vacía."
            )
            return []

        except json.JSONDecodeError:
            print(
                "El archivo productos.json contiene un formato inválido. "
                "Se iniciará con una lista vacía."
            )
            return []

        except PermissionError:
            print("No se tienen permisos para leer productos.json.")
            return []

        except ValueError as error:
            print(f"Error en los datos guardados: {error}")
            return []

        except OSError as error:
            print(f"No se pudo leer la información: {error}")
            return []