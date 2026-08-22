from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class Restaurante:
    def __init__(
        self,
        ruta_archivo: str = "data/productos.json"
    ) -> None:
        self.productos: list[Producto] = []
        self.usuarios: list[Usuario] = []

        self.productos_por_codigo: dict[str, Producto] = {}

        self.categorias_permitidas: tuple[str, ...] = (
            "Entrada",
            "Plato fuerte",
            "Postre",
            "Bebida"
        )

        self.categorias_registradas: set[str] = set()
        self.identificaciones_usuarios: set[str] = set()

        self.archivo_servicio = ArchivoServicio(ruta_archivo)
        self._cargar_productos()

    def _cargar_productos(self) -> None:
        productos_guardados = (
            self.archivo_servicio.cargar_productos()
        )

        for producto in productos_guardados:
            codigo = producto.codigo.strip().upper()
            categoria = self.normalizar_categoria(
                producto.categoria
            )

            if codigo in self.productos_por_codigo:
                print(
                    f"El producto con código {codigo} "
                    "está repetido y no fue cargado."
                )
                continue

            if categoria is None:
                print(
                    f"El producto {codigo} tiene una "
                    "categoría no permitida."
                )
                continue

            producto.codigo = codigo
            producto.categoria = categoria

            self.productos.append(producto)
            self.productos_por_codigo[codigo] = producto

        self._actualizar_categorias()

    def _guardar_productos(self) -> bool:
        return self.archivo_servicio.guardar_productos(
            self.productos
        )

    def normalizar_categoria(
        self,
        categoria: str
    ) -> str | None:
        for categoria_permitida in self.categorias_permitidas:
            if (
                categoria.strip().lower()
                == categoria_permitida.lower()
            ):
                return categoria_permitida

        return None

    def registrar_producto(
        self,
        producto: Producto
    ) -> bool:
        codigo = producto.codigo.strip().upper()
        categoria = self.normalizar_categoria(
            producto.categoria
        )

        if codigo in self.productos_por_codigo:
            return False

        if categoria is None:
            return False

        producto.codigo = codigo
        producto.categoria = categoria

        self.productos.append(producto)
        self.productos_por_codigo[codigo] = producto
        self._actualizar_categorias()

        if not self._guardar_productos():
            self.productos.remove(producto)
            del self.productos_por_codigo[codigo]
            self._actualizar_categorias()
            return False

        return True

    def buscar_producto(
        self,
        codigo: str
    ) -> Producto | None:
        codigo = codigo.strip().upper()
        return self.productos_por_codigo.get(codigo)

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float
    ) -> bool:
        producto = self.buscar_producto(codigo)
        categoria_normalizada = self.normalizar_categoria(
            categoria
        )

        if producto is None:
            return False

        if categoria_normalizada is None:
            return False

        producto_validado = Producto(
            codigo=producto.codigo,
            nombre=nombre,
            categoria=categoria_normalizada,
            precio=precio
        )

        datos_anteriores = (
            producto.nombre,
            producto.categoria,
            producto.precio
        )

        producto.nombre = producto_validado.nombre
        producto.categoria = producto_validado.categoria
        producto.precio = producto_validado.precio
        self._actualizar_categorias()

        if not self._guardar_productos():
            producto.nombre = datos_anteriores[0]
            producto.categoria = datos_anteriores[1]
            producto.precio = datos_anteriores[2]
            self._actualizar_categorias()
            return False

        return True

    def eliminar_producto(
        self,
        codigo: str
    ) -> bool:
        producto = self.buscar_producto(codigo)

        if producto is None:
            return False

        posicion = self.productos.index(producto)

        self.productos.remove(producto)
        del self.productos_por_codigo[producto.codigo]
        self._actualizar_categorias()

        if not self._guardar_productos():
            self.productos.insert(posicion, producto)
            self.productos_por_codigo[
                producto.codigo
            ] = producto
            self._actualizar_categorias()
            return False

        return True

    def listar_productos(self) -> None:
        if not self.productos:
            print("No hay productos registrados.")
            return

        print("\nLISTA DE PRODUCTOS")

        for producto in self.productos:
            print(producto.mostrar_informacion())

    def registrar_usuario(
        self,
        usuario: Usuario
    ) -> bool:
        identificacion = usuario.identificacion.strip()

        if identificacion in self.identificaciones_usuarios:
            return False

        usuario.identificacion = identificacion
        self.usuarios.append(usuario)
        self.identificaciones_usuarios.add(
            identificacion
        )
        return True

    def listar_usuarios(self) -> None:
        if not self.usuarios:
            print("No hay usuarios registrados.")
            return

        print("\nLISTA DE USUARIOS")

        for usuario in self.usuarios:
            print(usuario.mostrar_informacion())

    def mostrar_categorias_permitidas(self) -> None:
        print("Categorías permitidas:")

        for categoria in self.categorias_permitidas:
            print(f"- {categoria}")

    def mostrar_categorias(self) -> None:
        if not self.categorias_registradas:
            print("No hay categorías registradas.")
            return

        print("\nCATEGORÍAS REGISTRADAS")

        for categoria in sorted(
            self.categorias_registradas
        ):
            print(f"- {categoria}")

    def _actualizar_categorias(self) -> None:
        self.categorias_registradas = {
            producto.categoria
            for producto in self.productos
        }