from PIL import Image



def reImage():# Abre la imagen
    imagen = Image.open("image/placa.jpg")
    # Obtén el tamaño original de la imagen
    ancho_original, alto_original = imagen.size

    # Calcula el nuevo tamaño (1/4 del tamaño original)
    nuevo_tamaño = (ancho_original // 4, alto_original // 4)

    # Redimensiona la imagen
    imagen_redimensionada = imagen.resize(nuevo_tamaño, Image.Resampling.LANCZOS)
    # Guarda la imagen redimensionada
    imagen_redimensionada.save("image/placa.jpg")

reImage()