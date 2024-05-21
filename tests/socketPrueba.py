import socket

# Configurar el servidor y el puerto
host = '192.168.240.51'  # Puedes cambiar esto por la IP de tu servidor
puerto = 12345

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket al servidor y puerto especificados
sock.bind((host, puerto))

# Escuchar conexiones entrantes (máximo 1 conexión)
sock.listen(1)

print(f"Servidor escuchando en {host}:{puerto}")

while True:
    try:
        # Esperar por una conexión
        conexion, direccion = sock.accept()
        print(f"Conexión entrante desde {direccion}")

        # Enviar datos al cliente (página web)
        mensaje = "Hola desde el servidor Python"
        conexion.sendall(mensaje.encode())

        # Cerrar la conexión
        conexion.close()
    except Exception as e:
        print(e)
    