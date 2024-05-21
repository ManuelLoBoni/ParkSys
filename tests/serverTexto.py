import vars
import socket
import time

def getText():
    global aliveWindow

    while True:
        try:
            # Crear un socket TCP/IP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((vars.HOST, vars.PORT_MS))
                server_socket.listen()

                while True:
                    print("Esperando conexiones...")
                    # Aceptar la conexión
                    conn, addr = server_socket.accept()

                    with conn:
                        print('Conexión establecida desde', addr)
                        
                        # Recibir el mensaje del cliente
                        message = conn.recv(1024).decode()
                        if message:
                            print('Mensaje recibido del cliente:', message)
                            vars.rfid_txt = message
                        else:
                            print('No se recibió ningún mensaje del cliente.')
        
        except socket.error as sock_err:
            print(f"Error en el socket: {sock_err}")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar
        
        except Exception as e:
            print(f"Error inesperado: {e}")
            time.sleep(5)  # Esperar 5 segundos antes de reintentar

        finally:
            print("Reiniciando el servidor de texto...")

# Llamada a la función getText para iniciar el servidor
getText()
