import os.path
import socket

# Configuración del cliente
HOST = 'localhost'  # Dirección IP del servidor
PORT = 65432        # Puerto para la comunicación

# Ruta de la imagen a enviar
imagen_a_enviar = 'image/placa3c.png'
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

sendServer(imagen_a_enviar)