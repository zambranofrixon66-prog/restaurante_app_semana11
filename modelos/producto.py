class Producto:
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int = 0, categoria: str = "General"):
        if not codigo or not nombre:
            raise ValueError("El código y el nombre son obligatorios.")

        if float(precio) <= 0:
            raise ValueError("El precio debe ser mayor a 0.")

        if int(stock) < 0:
            raise ValueError("El stock no puede ser negativo.")

        self.codigo = str(codigo).strip()
        self.nombre = str(nombre).strip()
        self.precio = float(precio)
        self.stock = int(stock)
        self.categoria = str(categoria).strip()

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "categoria": self.categoria
        }

    @staticmethod
    def from_dict(data: dict) -> "Producto":
        try:
            return Producto(
                codigo=data["codigo"],
                nombre=data["nombre"],
                precio=float(data["precio"]),
                stock=int(data.get("stock", 0)),
                categoria=data.get("categoria", "General")
            )
        except KeyError as e:
            raise KeyError(f"Clave faltante en JSON de Producto: {e}")

    def hay_stock(self, cantidad: int) -> bool:
        return self.stock >= int(cantidad)

    def reducir_stock(self, cantidad: int):
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        if cantidad > self.stock:
            raise ValueError("No hay suficiente stock disponible.")
        self.stock -= cantidad

    def vender(self, cantidad: int) -> bool:
        if self.hay_stock(cantidad):
            self.reducir_stock(cantidad)
            return True
        return False

    def __str__(self) -> str:
        return (
            f"Código: {self.codigo} | "
            f"Producto: {self.nombre} | "
            f"Precio: ${self.precio:.2f} | "
            f"Stock: {self.stock}"
        )