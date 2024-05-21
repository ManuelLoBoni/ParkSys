import socket
import time

# Configuración del cliente
HOST = 'localhost'  # Dirección IP del servidor
PORT = 65433        # Puerto para la comunicación

def sendText(message):
    while True:
        try:
            # Conexión al servidor
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))

                # Envío del mensaje al servidor
                client_socket.sendall(message.encode())

            print('Mensaje enviado al servidor:', message)
            break  # Salir del bucle si se envía el mensaje correctamente

        except socket.error as sock_err:
            print(f"Error en el socket: {sock_err}")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar

        except Exception as e:
            print(f"Error inesperado: {e}")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar

# Uso del método sendText
message_to_send = "Este es un mensaje desde el cliente al servidor."

while True:
    sendText(message_to_send)
    time.sleep(1)