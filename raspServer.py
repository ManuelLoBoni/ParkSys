
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import os.path
import socket
import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

# Configuración del cliente
HOST = '192.168.123.147' # Dirección IP del servidor
PORT = 65432 # Puerto para la comunicación
PORT2 = 65433

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
        client_socket.connect((HOST, PORT2))

        # Envío del mensaje al servidor
        client_socket.sendall(message.encode())

    print('Mensaje enviado al servidor:', message)

# Configurando variables
picam2 = Picamera2()
picam2.start()

#Configurando Sensor Ultrasónico
GPIO.setmode(GPIO.BOARD)
TRIG_PIN = 16
ECHO_PIN = 18
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
    picam2.capture_file(imagen_a_enviar)
    print("Imagene tomada")
    # picam2.start_and_capture_file(imagen_a_enviar)

def rifas():
    while True:
        id, nombreCajon = reader.read()
        id_hex_tarjeta = format(id, 'X')  # Convertimos el ID a hexadecimal
        print(f"ID de la tarjeta: {id_hex_tarjeta}")
        print(f"Nombre del cajon: {nombreCajon}")
        sendText(id_hex_tarjeta)
        time.sleep(0.5)

threading.Thread(target=rifas).start()


try:
    while True:
        medida = medir_distancia()
        print(f"Distancia: {medida} cm")
        if(medida < 50):{
            tomarFoto(),
            sendServer(imagen_a_enviar)
        }
        time.sleep(1)
except Exception as e:
    print(e)
