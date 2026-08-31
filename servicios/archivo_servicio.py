import json
import os

class ArchivoServicio:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "datos")

    @classmethod
    def _obtener_ruta(cls, nombre_archivo: str) -> str:
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        return os.path.join(cls.DATA_DIR, nombre_archivo)

    @classmethod
    def guardar_json(cls, nombre_archivo: str, datos: list):
        """Guarda una lista de diccionarios en formato JSON con indentación y UTF-8."""
        ruta = cls._obtener_ruta(nombre_archivo)
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except PermissionError:
            print(f"[Error de Permiso] No se tienen permisos para escribir en el archivo {nombre_archivo}.")
        except Exception as e:
            print(f"[Error inesperado al guardar {nombre_archivo}]: {e}")

    @classmethod
    def cargar_json(cls, nombre_archivo: str) -> list:
        """Carga datos desde un archivo JSON controlando FileNotFoundError y JSONDecodeError."""
        ruta = cls._obtener_ruta(nombre_archivo)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"[Aviso] {nombre_archivo} tiene un formato JSON inválido o está vacío. Se inicia colección vacía.")
            return []
        except PermissionError:
            print(f"[Error de Permiso] No se tienen permisos para leer el archivo {nombre_archivo}.")
            return []