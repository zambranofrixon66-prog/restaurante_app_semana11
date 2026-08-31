Restaurante App - Semana 11

Estudiante: Frixon Jeancarlos Zambrano Ortiz
Asignatura: Programación Orientada a Objetos
Semana: 11

1. Descripción del Sistema

Evolución de la aplicación modular de restaurante implementada en Python bajo el paradigma de Programación Orientada a Objetos (POO). El sistema incorpora relaciones entre entidades (Usuario, Producto y Venta), control de inventario (stock) y persistencia de datos en archivos JSON mediante un servicio centralizado de almacenamiento.

2. Estructura Modular del Proyecto

restaurante_app_semana11/
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

3. Responsabilidad de las Clases

Producto

Representa los productos del restaurante. Almacena código, nombre, precio y stock. También permite verificar y reducir el stock después de una venta.

Usuario

Representa a los usuarios registrados. Almacena identificación, nombre y correo electrónico.

Venta

Representa una venta realizada. Relaciona un usuario con un producto y registra la cantidad vendida.

ArchivoServicio

Se encarga de guardar y cargar la información de los archivos JSON.

Restaurante

Administra las colecciones de productos, usuarios y ventas. También realiza búsquedas, registros, ventas y consultas.

4. Funcionalidades Principales

Registrar Producto: Permite ingresar código, nombre, precio y stock inicial con validaciones.

Listar Productos: Muestra el listado de productos con sus existencias actualizadas.

Registrar Usuario: Guarda la identificación, nombre y correo del usuario.

Listar Usuarios: Muestra todos los usuarios almacenados.

Realizar Venta: Verifica la existencia del usuario, el producto y el stock disponible, descuenta la cantidad vendida y registra la venta.

Consultar Ventas por Usuario: Muestra el historial de compras asociadas a una identificación.

Persistencia Automática: Carga los datos desde archivos JSON al iniciar y guarda los cambios realizados durante la ejecución.

5. Persistencia JSON y Manejo de Rutas

Los datos se almacenan en la carpeta datos/.

Se utilizan los archivos productos.json, usuarios.json y ventas.json.

Se emplea la biblioteca estándar json para guardar y recuperar la información.

Las rutas se manejan mediante os.path.

El guardado se realiza con codificación UTF-8 e indentación de 4 espacios.

Los objetos se convierten en diccionarios mediante to_dict() y se reconstruyen mediante from_dict().

6. Manejo de Excepciones

FileNotFoundError: Si un archivo JSON no existe, el sistema retorna una lista vacía sin interrumpir la ejecución.

json.JSONDecodeError: Se controla cuando un archivo JSON está vacío o contiene información inválida.

PermissionError: Maneja problemas de permisos de lectura o escritura.

ValueError: Controla valores inválidos en cantidades, precios, stock y campos obligatorios.

KeyError: Captura claves faltantes al reconstruir objetos desde los archivos JSON.

7. Instrucciones de Ejecución

Abrir la carpeta principal del proyecto en Visual Studio Code.

Abrir una terminal en el directorio principal.

Ejecutar el comando:

python main.py

Seleccionar una opción del menú y seguir las indicaciones.

8. Pruebas Realizadas

Registro de producto: Se comprobó el registro de productos con código, nombre, precio y stock.

Registro de usuario: Se verificó el almacenamiento de identificación, nombre y correo.

Bloqueo de duplicados: Se comprobó que no se permitan productos o usuarios repetidos.

Venta con stock suficiente: Se verificó que la venta se registre y que el stock disminuya correctamente.

Venta con stock insuficiente: Se comprobó que el sistema rechace la operación sin modificar el inventario.

Consulta por usuario: Se verificó que se muestre correctamente el historial de ventas del usuario.

Persistencia JSON: Se comprobó que productos, usuarios y ventas se guarden en sus respectivos archivos.

Persistencia al reiniciar: Se cerró y volvió a ejecutar el programa para comprobar que los datos permanecieran almacenados.

9. Conclusión

La actividad permitió ampliar el sistema del restaurante mediante la incorporación del control de stock, el registro de ventas y la persistencia de productos, usuarios y ventas en archivos JSON. Además, se aplicaron relaciones entre objetos, validaciones y manejo de excepciones dentro de una estructura modular basada en Programación Orientada a Objetos.