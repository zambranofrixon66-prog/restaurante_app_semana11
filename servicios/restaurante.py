from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class Restaurante:
    def __init__(self):
        # 1. Colecciones principales (Listas para persistencia y recorrido secuencial)
        self._productos: list[Producto] = []
        self._usuarios: list[Usuario] = []
        self._ventas: list[Venta] = []

        # 2. Estructuras auxiliares en memoria para optimización (Semana 12)
        # Índice por clave única (dict) -> Búsqueda O(1)
        self._indice_productos: dict[str, Producto] = {}
        # Índice por identificación de usuario (dict) -> Búsqueda O(1)
        self._indice_usuarios: dict[str, Usuario] = {}
        # Índice de ventas agrupadas por usuario (dict de listas) -> Consulta O(1)
        self._indice_ventas_usuario: dict[str, list[Venta]] = {}
        # Conjunto para validación rápida de unicidad (set) -> Comprobación O(1)
        self._correos_registrados: set[str] = set()

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

    # --- CARGA Y RECONSTRUCCIÓN DE ÍNDICES ---
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

        # Reconstruir las estructuras auxiliares en memoria a partir de los datos cargados
        self._reconstruir_indices()

    def _reconstruir_indices(self):
        """Reconstruye todos los índices y conjuntos en memoria tras leer los JSON."""
        # Índice de productos por código normalizado
        self._indice_productos = {p.codigo.strip().lower(): p for p in self._productos}

        # Índice de usuarios por usuario_id normalizado
        self._indice_usuarios = {u.usuario_id.strip().lower(): u for u in self._usuarios}

        # Conjunto de correos únicos registrados
        self._correos_registrados = {
            getattr(u, "correo", "").strip().lower() 
            for u in self._usuarios 
            if getattr(u, "correo", "").strip()
        }

        # Índice de ventas agrupadas por usuario
        self._indice_ventas_usuario = {}
        for venta in self._ventas:
            u_id = venta.usuario_id.strip().lower()
            if u_id not in self._indice_ventas_usuario:
                self._indice_ventas_usuario[u_id] = []
            self._indice_ventas_usuario[u_id].append(venta)

    # --- MÉTODOS DE PERSISTENCIA ---
    def guardar_productos(self):
        ArchivoServicio.guardar_json("productos.json", [p.to_dict() for p in self._productos])

    def guardar_usuarios(self):
        ArchivoServicio.guardar_json("usuarios.json", [u.to_dict() for u in self._usuarios])

    def guardar_ventas(self):
        ArchivoServicio.guardar_json("ventas.json", [v.to_dict() for v in self._ventas])

    # --- BÚSQUEDAS OPTIMIZADAS (O(1)) ---
    def buscar_producto(self, codigo_producto: str) -> Producto | None:
        """Búsqueda directa mediante diccionario auxiliar sin recorrer la lista."""
        clave = str(codigo_producto).strip().lower()
        return self._indice_productos.get(clave, None)

    def buscar_usuario(self, identificacion_usuario: str) -> Usuario | None:
        """Búsqueda directa mediante diccionario auxiliar sin recorrer la lista."""
        clave = str(identificacion_usuario).strip().lower()
        return self._indice_usuarios.get(clave, None)

    # --- REGISTRO CON SINCRONIZACIÓN DE ÍNDICES ---
    def registrar_producto(self, codigo: str, nombre: str, precio: float, stock: int) -> bool:
        clave = str(codigo).strip().lower()
        # Verificación inmediata con el diccionario auxiliar
        if clave in self._indice_productos:
            return False

        nuevo_p = Producto(codigo, nombre, precio, stock)

        # Sincronización: lista principal + índice en memoria
        self._productos.append(nuevo_p)
        self._indice_productos[clave] = nuevo_p

        self.guardar_productos()
        return True

    def registrar_usuario(self, identificacion: str, nombre: str, correo: str = "") -> bool:
        clave_id = str(identificacion).strip().lower()
        correo_limpio = str(correo).strip().lower()

        # Validación inmediata: dict para ID y set para unicidad de correo
        if clave_id in self._indice_usuarios:
            return False

        if correo_limpio and correo_limpio in self._correos_registrados:
            return False

        nuevo_u = Usuario(identificacion, nombre, correo)

        # Sincronización: lista + dict + set
        self._usuarios.append(nuevo_u)
        self._indice_usuarios[clave_id] = nuevo_u
        if correo_limpio:
            self._correos_registrados.add(correo_limpio)

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

            # Sincronización: lista general de ventas + índice por usuario
            self._ventas.append(nueva_venta)

            u_id = usuario.usuario_id.strip().lower()
            if u_id not in self._indice_ventas_usuario:
                self._indice_ventas_usuario[u_id] = []
            self._indice_ventas_usuario[u_id].append(nueva_venta)

            self.guardar_ventas()
            self.guardar_productos()
            return True

        return False

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
        """Consulta directa en O(1) usando el índice agrupador sin iterar toda la lista de ventas."""
        clave = str(identificacion_usuario).strip().lower()
        return self._indice_ventas_usuario.get(clave, [])