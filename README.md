# ParkSys - Servidor Python

Este es el repositorio del código de la parte del servidor en Python de ParkSys. Este proyecto utiliza librerías especializadas para la detección de texto en imágenes, con el objetivo de detectar placas vehiculares, la proximidad de vehículos y un detector de tarjetas de identificación.

## Materiales

- Raspberry Pi
- Sensor Ultrasónico
- Cámara para Raspberry Pi
- Sensor RFID

## Funcionamiento del Sistema

El sistema está diseñado para ayudar en la gestión de lugares en un estacionamiento público, identificando clientes por placa vehicular o tarjeta RFID. El funcionamiento es el siguiente:

1. **Detección de Proximidad**: Cuando llega un automóvil, la Raspberry Pi utiliza un sensor ultrasónico para medir la distancia del vehículo y actuar como disparador de la cámara. La distancia programada es ajustable, y puede variar entre 20 cm y 100 cm según las pruebas.

2. **Captura de Imagen**: Una vez tomada la foto, esta se envía desde la aplicación en la Raspberry Pi a la aplicación en la computadora mediante un socket.

3. **Procesamiento de Imagen**: La computadora, que ejecuta un programa de recepción de imágenes hecho en Python, procesa la imagen para encontrar el texto. Si se detecta texto, este se envía al servidor web de la Raspberry Pi utilizando websockets.

4. **Gestión Web**: El resto del proceso es manejado por la [página web](https://github.com/JhonCODEOWO/ParkSys).

## Consideraciones

La Raspberry solo funciona para manejar los sensores.
El procesamiento se hace en una computadora normal y debido al alto uso de cpu se necesita una tarjeta grafica compatible con los modelos de EasyOCR.

Como esta organizado:
- **gui-remake**: Es la GUI de la PC, contiene los métodos para recibir la imagen, texto e hilos para ejecutar los sockets en paralelo.
- **pcServerR**: Contiene los métodos para cambiar el tamaño de la imagen, para obtener la placa y para el websocket.
- **raspServer**: Contiene métodos para enviar imágenes (fotos tomadas) y texto a través de sockets.
- **guir**: Interfaz tentativa para seleccionar IP desde Raspberry.
- La carpeta de **tests** es donde están archivos para pruebas unitarias de sockets.
- Recordar revisar requirements y hacer un entorno virtual.
