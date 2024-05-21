import easyocr
from PIL import Image
import numpy as np
import re #Este es de Regex
import vars
import websockets
import asyncio
import json
from PIL import Image

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
    r"[A-Z]{3}-\d-[0-9]{3}-[A-Z]"
    r"[A-Z]-\d{3}-[A-Z]{3}",
]

def reImage():# Abre la imagen
    imagen = Image.open(image_path)
    # Obtén el tamaño original de la imagen
    ancho_original, alto_original = imagen.size
    # Calcula el nuevo tamaño (1/4 del tamaño original)
    nuevo_tamaño = (ancho_original // 4, alto_original // 4)
    # Redimensiona la imagen
    imagen_redimensionada = imagen.resize(nuevo_tamaño, Image.Resampling.LANCZOS)
    # Guarda la imagen redimensionada
    imagen_redimensionada.save(image_path)

def ObtenerPlaca(image_path):
    # Configurando variables
    reader = easyocr.Reader(['es'])
    txtsaver=[]
    extractxt = ''
    placa_obtenida = []
    placafinal = ""
    global patrones

    reImage()
    # Cargar la imagen para su analisis
    image = Image.open(image_path)
    # Convertir la parte central a un array numpy
    central_np = np.array(image)
    # Realizar OCR en la parte central
    result = reader.readtext(central_np)
    # Mostrar resultados
    for detection in result:
        text = detection[1]
        txtsaver.append(text)
    for i in range(len(txtsaver)):
        extractxt = extractxt +' '+ txtsaver[i]

    print("")
    print("Deteccion: " + extractxt)
    for patron in patrones:
        placa_obtenida = re.findall(patron, extractxt)
        if len(placa_obtenida) != 0:
            placafinal = placa_obtenida[0]
            return placafinal
        else:
            placafinal = "Error de detección."
            vars.Error = placafinal
    return None



# SOCKETS
async def sockpc(websocket):
    while True:
        datoRecibido = await websocket.recv()
        print(f"<<< {datoRecibido}")

        datoEnviado = json.dumps({"placa":vars.placa,"rfid":vars.rfid_txt})
        await websocket.send(datoEnviado)
        print(f">>> {datoEnviado}")

async def mainSock():
    print("Inicio WebSocket")
    async with websockets.serve(sockpc,vars.SWeb, 8765):
        await asyncio.Future()

def start_mainSock():
    asyncio.run(mainSock())