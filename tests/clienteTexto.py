import socket

# Configuración del cliente
HOST = 'localhost'  # Dirección IP del servidor
PORT = 65433        # Puerto para la comunicación

def sendText(message):
    # Conexión al servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))

        # Envío del mensaje al servidor
        client_socket.sendall(message.encode())

    print('Mensaje enviado al servidor:', message)

# Uso del método sendText
message_to_send = "Este es un mensaje desde el cliente al servidor."
sendText(message_to_send)
