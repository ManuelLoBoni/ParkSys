
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import os.path
import socket
import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# Configuración del cliente
HOST = 'localhost' # Dirección IP del servidor
PORT = 65432 # Puerto para la comunicación
PORT = 65433
reader = SimpleMFRC522()

# Ruta de la imagen a enviar
imagen_a_enviar = 'image/placa.jpg'

def sendServer(image):
    # Verificar si la imagen existe
    if os.path.exists(image):
        # Conexión al servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))

            # Abrir y enviar la imagen
            with open(imagen_a_enviar, 'rb') as f:
                data = f.read(1024)
                while data:
                    client_socket.sendall(data)
                    data = f.read(1024)

            print('Imagen enviada')
    else:
        print('La imagen no existe.')

def sendText(message):
    # Conexión al servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        # Envío del mensaje al servidor
        client_socket.sendall(message.encode())

    print('Mensaje enviado al servidor:', message)

# Configurando variables
picam2 = Picamera2()

#Configurando Sensor Ultrasónico
GPIO.setmode(GPIO.BCM)
TRIG_PIN = 23
ECHO_PIN = 24
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
    
# Medir Distancia Sensor Ultrasónico
def medir_distancia():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def tomarFoto():
    global imagen_a_enviar
    picam2.start_and_capture_file(imagen_a_enviar)

def previewCamera():
    picam2.preview_configuration()

threading.Thread(target=previewCamera).start()



while True:
    medida = medir_distancia()
    if medida > 100:
        tomarFoto()
        sendServer(imagen_a_enviar)

    id, nombreCajon = reader.read()
    id_hex_tarjeta = format(id, 'X')  # Convertimos el ID a hexadecimal
    print(f"ID de la tarjeta: {id_hex_tarjeta}")
    print(f"Nombre del cajon: {nombreCajon}")