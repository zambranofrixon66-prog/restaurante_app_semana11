class Producto:
    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float
    ) -> None:
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código no puede estar vacío.")

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if not isinstance(categoria, str) or not categoria.strip():
            raise ValueError("La categoría no puede estar vacía.")

        try:
            precio = float(precio)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un número válido.")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        self.codigo = codigo.strip()
        self.nombre = nombre.strip()
        self.categoria = categoria.strip()
        self.precio = precio

    def mostrar_informacion(self) -> str:
        return (
            f"Código: {self.codigo} | "
            f"Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | "
            f"Precio: ${self.precio:.2f}"
        )

    def a_diccionario(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio
        }

    @classmethod
    def desde_diccionario(cls, datos: dict) -> "Producto":
        try:
            return cls(
                codigo=datos["codigo"],
                nombre=datos["nombre"],
                categoria=datos["categoria"],
                precio=datos["precio"]
            )
        except KeyError as error:
            raise ValueError(
                f"Falta el dato obligatorio: {error.args[0]}"
            ) from error