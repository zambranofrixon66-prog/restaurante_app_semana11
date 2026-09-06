# Restaurante App - Semana 12

**Estudiante:** Frixon Jeancarlos Zambrano Ortiz

**Asignatura:** Programación Orientada a Objetos

**Semana:** 12

---

## 1. Descripción del Sistema

Evolución progresiva de la aplicación modular de restaurante implementada en Python bajo el paradigma de Programación Orientada a Objetos (POO). En esta versión correspondiente a la **Semana 12**, se optimizó el rendimiento del sistema mediante el uso estratégico de **colecciones auxiliares (`dict` y `set`)** para realizar búsquedas directas, consultas agrupadas y validaciones de pertenencia en tiempo constante ($O(1)$ promedio).

El sistema conserva intacta la persistencia en archivos JSON (`productos.json`, `usuarios.json` y `ventas.json`), la arquitectura modular y las listas principales para la serialización y recorrido de entidades.

---

## 2. Estructura Modular del Proyecto

```text
restaurante_app_semana12/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── bebida.py
│   ├── cliente.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── .gitignore
├── main.py
└── README.md

```

---

## 3. Responsabilidad de las Clases y Colecciones Auxiliares

* **Producto:** Representa los productos del restaurante (código, nombre, precio y stock). Incluye lógica para validar existencias y descontar unidades tras una venta.
* **Usuario:** Modela a los clientes registrados con su identificación (`usuario_id`), nombre y correo electrónico.
* **Venta:** Representa una transacción realizada, vinculando la identificación del usuario, el código del producto, la cantidad adquirida y el total.
* **ArchivoServicio:** Encargado de la serialización y deserialización de listas de objetos hacia/desde los archivos JSON con codificación UTF-8.
* **Restaurante (Servicio con Colecciones Optimizadas):** Administra las listas principales y gestiona las siguientes estructuras auxiliares en memoria:
* `_indice_productos` (`dict[str, Producto]`): Índice hash que asocia cada código de producto con su objeto, permitiendo búsquedas inmediatas en $O(1)$ promedio.
* `_indice_usuarios` (`dict[str, Usuario]`): Índice hash que vincula la identificación con el objeto usuario para búsquedas directas en $O(1)$ promedio.
* `_indice_ventas_usuario` (`dict[str, list[Venta]]`): Estructura asociativa que agrupa el historial de ventas por cliente, evitando barridos sobre el total de ventas registradas.
* `_correos_registrados` (`set[str]`): Conjunto hash para verificar en $O(1)$ promedio la unicidad de los correos electrónicos durante el registro.



---

## 4. Matriz Comparativa de Rendimiento (Colecciones)

| Operación | Colección Principal | Estructura Auxiliar | Complejidad Previa (Sem 11) | Complejidad Optimizada (Sem 12) | Beneficio Técnico |
| --- | --- | --- | --- | --- | --- |
| **Buscar Producto** | `list` | `dict` (clave: `codigo`) | $O(n)$ | $O(1)$ promedio | Acceso directo por clave sin recorrer toda la lista de productos. |
| **Buscar Usuario** | `list` | `dict` (clave: `usuario_id`) | $O(n)$ | $O(1)$ promedio | Búsqueda inmediata de la entidad previa al cobro o consulta. |
| **Historial de Ventas** | `list` | `dict[str, list[Venta]]` | $O(n)$ | $O(1)$ promedio | Acceso directo a la lista filtrada de compras del usuario consultado. |
| **Validación de Correo** | `list` | `set` (correo) | $O(n)$ | $O(1)$ promedio | Comprobación de membresía instantánea para evitar correos duplicados. |

---

## 5. Persistencia, Sincronización y Reconstrucción de Índices

* **Persistencia JSON:** Los datos continúan guardándose en la carpeta `datos/` dentro de los archivos `productos.json`, `usuarios.json` y `ventas.json`.
* **Sincronización en Tiempo Real:** Cada operación que muta el estado (alta de productos, alta de usuarios o ventas) actualiza paralelamente la lista principal y los índices auxiliares en memoria antes de persistir a disco.
* **Reconstrucción Automática (`_reconstruir_indices`):** Al iniciar la aplicación, el servicio lee los datos desde los archivos JSON y reconstruye inmediatamente los diccionarios `_indice_productos`, `_indice_usuarios`, `_indice_ventas_usuario` y el conjunto `_correos_registrados`, garantizando coherencia absoluta del sistema sin intervención manual.

---

## 6. Manejo de Excepciones

* **FileNotFoundError:** Manejado en `ArchivoServicio`; si el archivo JSON no existe, retorna una lista vacía para permitir inicializaciones limpias.
* **json.JSONDecodeError:** Captura archivos JSON en blanco o corruptos evitando la interrupción del servicio.
* **KeyError y ValueError:** Controlados durante la deserialización de entidades y la lectura de campos numéricos (precios, cantidades y stock).
* **Validación de Claves Duplicadas:** El sistema retorna `False` e informa al usuario cuando se intenta registrar un código o identificación ya presente en los diccionarios, o un correo repetido mediante el `set`.

---

## 7. Instrucciones de Ejecución

1. Abrir la carpeta `restaurante_app_semana12` en Visual Studio Code.
2. Abrir una terminal en el directorio principal del proyecto.
3. Ejecutar la aplicación con Python:
```powershell
python main.py

```


4. Navegar utilizando el menú numérico (opciones 1 a 9).

---

## 8. Pruebas Realizadas y Evidencias de Ejecución

Durante la verificación de funcionamiento en consola se validaron satisfactoriamente los siguientes casos de prueba:

1. **Reconstrucción inicial:** Comprobación de carga automática de datos previos (`P1`, `P001` y el usuario `0802637868`) poblando los diccionarios y conjuntos en memoria al arrancar.
2. **Búsqueda directa de producto ($O(1)$):** Consulta del código `P001`, localizando de inmediato el producto *Encebollado* con su precio ($7.00) y existencias.
3. **Búsqueda directa de usuario ($O(1)$):** Consulta de la cédula `0802637868`, retornando inmediatamente la información del usuario *Frixon Zambrano*.
4. **Venta y decremento de stock:** Ejecución de una venta de 3 unidades del producto `P001` al usuario `0802637868`, validando el decremento del inventario y la emisión del registro.
5. **Consulta de ventas agrupadas ($O(1)$):** Consulta inmediata de compras para el usuario `0802637868`, mostrando sus transacciones asociadas sin realizar iteraciones sobre el universo total de ventas.
6. **Persistencia al cierre:** Salida mediante la opción `9`, confirmando la serialización de los datos actualizados en los archivos JSON.

---

## 9. Conclusión

La implementación de estructuras auxiliares basadas en tablas hash (`dict` y `set`) en la **Semana 12** permitió optimizar drásticamente el rendimiento de las operaciones de búsqueda y validación a una complejidad de $O(1)$ promedio, resolviendo los cuellos de botella generados por las búsquedas lineales $O(n)$. Al mismo tiempo, se logró mantener la arquitectura modular previa, la persistencia en archivos JSON y la integridad referencial entre usuarios, productos y ventas.