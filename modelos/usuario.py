class Usuario:
    def __init__(self, usuario_id: str, nombre: str, correo: str = ""):
        if not usuario_id or not nombre:
            raise ValueError("El ID y el nombre del usuario son obligatorios.")

        self.usuario_id = str(usuario_id).strip()
        self.nombre = str(nombre).strip()
        self.correo = str(correo).strip()

    @property
    def identificacion(self) -> str:
        return self.usuario_id

    def to_dict(self) -> dict:
        return {
            "usuario_id": self.usuario_id,
            "nombre": self.nombre,
            "correo": self.correo
        }

    @staticmethod
    def from_dict(data: dict) -> "Usuario":
        try:
            u_id = data.get("usuario_id") or data.get("identificacion")
            if not u_id:
                raise KeyError("usuario_id")

            return Usuario(
                usuario_id=u_id,
                nombre=data["nombre"],
                correo=data.get("correo", "")
            )
        except KeyError as e:
            raise KeyError(f"Clave faltante en JSON de Usuario: {e}")

    def __str__(self) -> str:
        if self.correo:
            return f"ID: {self.usuario_id} | Nombre: {self.nombre} | Correo: {self.correo}"
        return f"ID: {self.usuario_id} | Nombre: {self.nombre}"