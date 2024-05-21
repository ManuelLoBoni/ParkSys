import easyocr
import re
import os
from PIL import Image

image_path = 'image/placa.jpg'

# Configurando patrones de regex
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

# Uso de la función ObtenerPlaca
placa = ObtenerPlaca(image_path)
print("Placa detectada:", placa)
