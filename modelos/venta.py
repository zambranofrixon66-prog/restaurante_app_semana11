class Venta:
    def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int):
        if not usuario_id or not producto_codigo:
            raise ValueError("El usuario y el producto son obligatorios para la venta.")
        if int(cantidad) <= 0:
            raise ValueError("La cantidad vendida debe ser mayor a 0.")
            
        self.usuario_id = str(usuario_id).strip()
        self.producto_codigo = str(producto_codigo).strip()
        self.cantidad = int(cantidad)

    def to_dict(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad
        }

    @staticmethod
    def from_dict(data: dict) -> "Venta":
        try:
            return Venta(
                usuario_id=data["usuario_id"],
                producto_codigo=data["producto_codigo"],
                cantidad=int(data["cantidad"])
            )
        except KeyError as e:
            raise KeyError(f"Clave faltante en JSON de Venta: {e}")

    def __str__(self) -> str:
        return f"Venta -> Usuario ID: {self.usuario_id} | Código Producto: {self.producto_codigo} | Cantidad: {self.cantidad}"