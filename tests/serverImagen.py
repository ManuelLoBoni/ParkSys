import socket
import os
import time
import vars
import metodos

def getImage():
    global aliveWindow

    while True:
        try:
            # Crear un socket TCP/IP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((vars.HOST, vars.PORT))
                server_socket.listen()

                print("Esperando conexiones...")
                while True:
                    # Aceptar la conexión
                    conn, addr = server_socket.accept()
                    with conn:
                        print('Conexión establecida desde', addr)
                        
                        # Recibir datos de la imagen
                        image_data = b''
                        buffer_size = 1024
                        while True:
                            data = conn.recv(buffer_size)
                            if not data:
                                break
                            image_data += data
                        
                        # Verificar que se recibieron datos
                        if not image_data:
                            print("No se recibió ninguna imagen.")
                            continue
                        
                        # Verificar y crear el directorio si no existe
                        directory = 'image'
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        
                        image_path = os.path.join(directory, 'placa.jpg')
                        with open(image_path, 'wb') as f:
                            f.write(image_data)
                        print('Imagen recibida y guardada como "placa.jpg"')
                        vars.placa = metodos.ObtenerPlaca(metodos.image_path)
        
        except socket.error as sock_err:
            print(f"Error en el socket: {sock_err}")
            time.sleep(5)  # Espera 5 segundos antes de intentar reiniciar el socket
        except IOError as io_err:
            print(f"Error al guardar la imagen: {io_err}")
            time.sleep(5)  # Espera 5 segundos antes de intentar reiniciar el socket
        except Exception as e:
            print(f"Error inesperado: {e}")
            time.sleep(5)  # Espera 5 segundos antes de intentar reiniciar el socket
        finally:
            print("Reiniciando el socket...")

getImage()