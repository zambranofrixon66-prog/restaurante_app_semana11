# Sistema de restaurante con persistencia JSON

## Estudiante

**Nombre:** Frixon Zambrano

## Descripción del proyecto

Este proyecto presenta un sistema para administrar los productos y usuarios de un restaurante. Fue desarrollado con Programación Orientada a Objetos en Python y funciona mediante un menú interactivo en la consola.

El sistema permite registrar, buscar, actualizar, eliminar y listar productos. También permite registrar usuarios, consultar la lista de usuarios y mostrar las categorías utilizadas.

En la Semana 10 se incorporó la persistencia de productos en formato JSON. Gracias a esta funcionalidad, los productos permanecen guardados después de cerrar el programa y se recuperan automáticamente al volver a ejecutarlo.

## Objetivo

Aplicar el manejo de archivos, la persistencia de datos, la reconstrucción de objetos y el control de excepciones dentro de un proyecto modular desarrollado con Programación Orientada a Objetos.

## Estructura del proyecto

```text
restaurante_app/
├── data/
│   └── productos.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   ├── bebida.py
│   └── cliente.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
├── .gitignore
└── README.md
```

Los archivos `bebida.py` y `cliente.py` se conservan como parte del trabajo realizado en las semanas anteriores.

## Responsabilidad de los componentes

### Producto

Representa un producto del restaurante y almacena su código, nombre, categoría y precio. También permite convertir un producto en diccionario y reconstruirlo desde la información guardada en JSON.

### Usuario

Representa a una persona registrada en el sistema. Guarda su identificación, nombre y correo electrónico. En esta actividad los usuarios no se guardan en JSON porque la persistencia se aplica solamente a los productos.

### ArchivoServicio

Se encarga de leer y escribir el archivo `productos.json`. Utiliza `with open()`, `json.load()` y `json.dump()` para administrar la información.

### Restaurante

Administra las colecciones de productos y usuarios. Contiene las operaciones de registro, búsqueda, actualización, eliminación y listado. También solicita el guardado de los productos después de cada cambio.

### main.py

Es el punto de inicio del programa. Presenta el menú, solicita los datos y conecta las opciones seleccionadas con los métodos de la clase `Restaurante`.

## Estructuras de datos utilizadas

### Lista

Se utilizan listas para almacenar los productos y usuarios porque permiten agregar y eliminar objetos durante la ejecución.

### Tupla

Se utiliza una tupla para guardar las categorías permitidas: entrada, plato fuerte, postre y bebida.

### Diccionario

Se utiliza un diccionario para relacionar el código de cada producto con su objeto. Esto permite realizar búsquedas rápidas mediante el código.

### Conjunto

Se utilizan conjuntos para guardar categorías únicas y evitar identificaciones de usuarios duplicadas.

## Funcionalidades

- Registrar productos
- Buscar productos mediante su código
- Actualizar productos
- Eliminar productos
- Listar los productos registrados
- Registrar usuarios
- Listar los usuarios registrados
- Evitar códigos de productos duplicados
- Evitar identificaciones de usuarios duplicadas
- Mostrar las categorías utilizadas
- Validar que los campos no estén vacíos
- Validar que el precio sea numérico y mayor que cero
- Guardar automáticamente los productos en JSON
- Recuperar los productos al iniciar el programa
- Manejar errores de lectura, escritura y formato JSON

## Persistencia de productos

Los productos se guardan automáticamente en:

```text
data/productos.json
```

Ejemplo del contenido del archivo:

```json
[
    {
        "codigo": "P001",
        "nombre": "Encebollado",
        "categoria": "Plato fuerte",
        "precio": 3.5
    }
]
```

Cuando se inicia el programa, `ArchivoServicio` lee la información mediante `json.load()`. Después, cada diccionario se convierte nuevamente en un objeto de la clase `Producto`.

El archivo se actualiza después de registrar, actualizar o eliminar un producto.

## Manejo de excepciones

El programa controla las siguientes excepciones:

- `FileNotFoundError`: cuando no existe `productos.json`
- `JSONDecodeError`: cuando el archivo no contiene un JSON válido
- `PermissionError`: cuando no existen permisos de lectura o escritura
- `KeyError`: cuando falta un dato obligatorio
- `ValueError`: cuando un valor no cumple las validaciones
- `OSError`: cuando ocurre otro problema relacionado con el archivo

Estos controles evitan que la aplicación se cierre inesperadamente y muestran mensajes comprensibles al usuario.

## Menú del sistema

```text
1. Registrar producto
2. Buscar producto
3. Actualizar producto
4. Eliminar producto
5. Listar productos
6. Registrar usuario
7. Listar usuarios
8. Mostrar categorías
9. Salir
```

## Requisitos

- Python 3.10 o superior
- Visual Studio Code o cualquier editor compatible
- No requiere instalar librerías externas

## Ejecución del proyecto

1. Abrir la carpeta principal del proyecto.
2. Abrir una terminal.
3. Ejecutar:

```bash
python main.py
```

4. Seleccionar una opción del menú y seguir las indicaciones.

## Pruebas realizadas

1. Se registró el producto `P001`.
2. Se comprobó que sus datos se guardaran en `productos.json`.
3. Se cerró y se volvió a ejecutar el programa.
4. Se verificó que el producto apareciera nuevamente.
5. Se actualizó el nombre a `Encebollado mixto` y el precio a `$4.25`.
6. Se reinició el programa y se comprobó que los cambios permanecieran.
7. Se eliminó el producto.
8. Se reinició el programa y se confirmó que ya no apareciera.

## Conclusión

Esta actividad permitió mejorar el sistema del restaurante mediante el uso de archivos JSON para conservar la información. El proyecto mantiene su organización modular y aplica validaciones, manejo de excepciones y reconstrucción de objetos. De esta manera, los productos permanecen disponibles aunque el programa se cierre y vuelva a ejecutarse.