from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class Restaurante:
    def __init__(self):
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []
        self.cargar_datos()

    @property
    def productos(self) -> list[Producto]:
        return self._productos

    @property
    def usuarios(self) -> list[Usuario]:
        return self._usuarios

    @property
    def ventas(self) -> list[Venta]:
        return self._ventas

    def cargar_datos(self):
        datos_prod = ArchivoServicio.cargar_json("productos.json")
        self._productos = []
        for p in datos_prod:
            try:
                self._productos.append(Producto.from_dict(p))
            except (KeyError, ValueError) as e:
                print(f"[Error al reconstruir producto]: {e}")

        datos_user = ArchivoServicio.cargar_json("usuarios.json")
        self._usuarios = []
        for u in datos_user:
            try:
                self._usuarios.append(Usuario.from_dict(u))
            except (KeyError, ValueError) as e:
                print(f"[Error al reconstruir usuario]: {e}")

        datos_vent = ArchivoServicio.cargar_json("ventas.json")
        self._ventas = []
        for v in datos_vent:
            try:
                self._ventas.append(Venta.from_dict(v))
            except (KeyError, ValueError) as e:
                print(f"[Error al reconstruir venta]: {e}")

    def guardar_productos(self):
        ArchivoServicio.guardar_json("productos.json", [p.to_dict() for p in self._productos])

    def guardar_usuarios(self):
        ArchivoServicio.guardar_json("usuarios.json", [u.to_dict() for u in self._usuarios])

    def guardar_ventas(self):
        ArchivoServicio.guardar_json("ventas.json", [v.to_dict() for v in self._ventas])

    def buscar_producto(self, codigo_producto: str) -> Producto | None:
        for p in self._productos:
            if p.codigo.lower() == str(codigo_producto).strip().lower():
                return p
        return None

    def buscar_usuario(self, identificacion_usuario: str) -> Usuario | None:
        for u in self._usuarios:
            if u.usuario_id.lower() == str(identificacion_usuario).strip().lower():
                return u
        return None

    def registrar_producto(self, codigo: str, nombre: str, precio: float, stock: int) -> bool:
        if self.buscar_producto(codigo) is not None:
            return False
        nuevo_p = Producto(codigo, nombre, precio, stock)
        self._productos.append(nuevo_p)
        self.guardar_productos()
        return True

    def registrar_usuario(self, identificacion: str, nombre: str, correo: str = "") -> bool:
        if self.buscar_usuario(identificacion) is not None:
            return False
        nuevo_u = Usuario(identificacion, nombre, correo)
        self._usuarios.append(nuevo_u)
        self.guardar_usuarios()
        return True

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None or producto is None:
            return False

        if cantidad <= 0 or not producto.hay_stock(cantidad):
            return False

        if producto.vender(cantidad):
            nueva_venta = Venta(
                usuario_id=usuario.usuario_id,
                producto_codigo=producto.codigo,
                cantidad=cantidad
            )
            self._ventas.append(nueva_venta)
            self.guardar_ventas()
            self.guardar_productos()
            return True

        return False

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
        ventas_usuario: list[Venta] = []
        for venta in self._ventas:
            if venta.usuario_id.lower() == str(identificacion_usuario).strip().lower():
                ventas_usuario.append(venta)
        return ventas_usuario