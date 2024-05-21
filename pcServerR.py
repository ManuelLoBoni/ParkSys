import easyocr
from PIL import Image
import numpy as np
import re #Este es de Regex
import vars
import websockets
import asyncio
import json
import socket
import os
import time

image_path = 'image/placa.jpg'

# Configurando variables
patrones = [
    r"([A-Z]{3}-\d{2}-\d{2})",
    r"([A-Z]{3}-\d{3}-\d)",
    r"([A-Z]{2}-\d{2}-\d{3})",
    r"([A-Z]{3}-\d{3}-[A-Z])",
    r"([A-Z]{3}-\d{2}-\d{2})",
    r"([A-Z]{3}-\d{3}-\d)",
    r"([A-Z]{2}-\d{2}-\d{3})",
    r"([A-Z]{3}-\d{3}-[A-Z])",
    r"[A-Z]{3}-\d[A-Z]{3}",
    r"[A-Z]{2}-\d{3}-[A-Z]{2}",
    r"[A-Z]{2}-\d{2}-[A-Z]{3}",
    r"[A-Z]{2}-\d{3}-[A-Z]\d",
    r"[A-Z]{4}-\d{2}-[A-Z]{2}",
    r"[A-Z]{3}-\d{4}-[A-Z]",
    r"[A-Z]{3}-\d-[0-9]{3}-[A-Z]",
    r"[A-Z]-\d{3}-[A-Z]{3}",
]

def reImage(image_path):
    try:
        # Asegurar que el directorio existe
        directory = os.path.dirname(image_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        if not os.path.exists(image_path):
            print(f"Error: El archivo {image_path} no existe.")
            return False
        
        # Abre la imagen
        imagen = Image.open(image_path)
        # Obtén el tamaño original de la imagen
        ancho_original, alto_original = imagen.size
        # Calcula el nuevo tamaño (1/4 del tamaño original)
        nuevo_tamaño = (ancho_original // 4, alto_original // 4)
        # Redimensiona la imagen
        imagen_redimensionada = imagen.resize(nuevo_tamaño, Image.Resampling.LANCZOS)
        # Guarda la imagen redimensionada
        imagen_redimensionada.save(image_path)
        return True
    except Exception as e:
        print(f"Error al redimensionar la imagen: {e}")
        return False

def ObtenerPlaca(image_path):
    if not reImage(image_path):
        return "Error al redimensionar la imagen."
    
    try:
        # Configurando variables
        reader = easyocr.Reader(['es'])
        txtsaver = []
        extractxt = ''
        placa_obtenida = []
        global patrones

        # Cargar la imagen para su análisis
        image = Image.open(image_path)
        # Realizar OCR en la imagen
        result = reader.readtext(image)
        
        # Mostrar resultados
        for detection in result:
            text = detection[1]
            txtsaver.append(text)
        
        for i in range(len(txtsaver)):
            extractxt += ' ' + txtsaver[i]

        print("")
        print("Detección: " + extractxt)
        for patron in patrones:
            placa_obtenida = re.findall(patron, extractxt)
            if placa_obtenida:
                placafinal = placa_obtenida[0]
                print("Placa:")
                print(placafinal)
                return placafinal
        
        return "Error de detección. No se encontró una placa válida."
    
    except FileNotFoundError:
        return f"Error: El archivo {image_path} no se encontró."
    except Exception as e:
        return f"Error inesperado durante el OCR: {e}"

# SOCKETS
def getImage():
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
                        vars.placa = ObtenerPlaca(image_path)
        
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

def getText():
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

# WEBSOCKETS
async def sockpc(websocket, path):
    # Variables globales para almacenar los valores previos
    prev_placa = None
    prev_rfid = None

    while True:
        try:
            datoRecibido = await websocket.recv()

            current_placa = vars.placa
            current_rfid = vars.rfid_txt
            datoEnviado = json.dumps({"placa": current_placa, "rfid": current_rfid})

            # Enviar siempre los datos
            await websocket.send(datoEnviado)

            # Imprimir solo si los valores son diferentes
            if current_placa != prev_placa or current_rfid != prev_rfid:
                print(f"<<< {datoRecibido}")
                print(f">>> {datoEnviado}")

                # Actualizar los valores previos
                prev_placa = current_placa
                prev_rfid = current_rfid
        
        except websockets.ConnectionClosed:
            print("Conexión cerrada")
            break

        except Exception as e:
            print(f"Error inesperado: {e}")
            break

async def mainSock():
    print("Inicio WebSocket")
    async with websockets.serve(sockpc, vars.SWeb, 8765):
        await asyncio.Future()  # Mantener el servidor en funcionamiento

def start_mainSock():
    asyncio.run(mainSock())