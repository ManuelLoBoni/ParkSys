import os
import socket
import time

# Configuración del cliente
HOST = '192.168.1.159'  # Dirección IP del servidor
PORT = 65432        # Puerto para la comunicación

# Ruta de la imagen a enviar
imagen_a_enviar = 'image/placa1.jpg'

def sendServer(image):
    # Verificar si la imagen existe
    if os.path.exists(image):
        try:
            # Conexión al servidor
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))

                # Abrir y enviar la imagen
                with open(image, 'rb') as f:
                    data = f.read(1024)
                    while data:
                        client_socket.sendall(data)
                        data = f.read(1024)

            print('Imagen enviada')
        except socket.error as sock_err:
            print(f"Error en la conexión o envío de datos: {sock_err}")
        except Exception as e:
            print(f"Error inesperado: {e}")
    else:
        print('La imagen no existe.')

while True:
    sendServer(imagen_a_enviar)
    time.sleep(1)