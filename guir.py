from customtkinter import CTk, CTkLabel, CTkComboBox, CTkTextbox, CTkButton, CTkCheckBox
import pcServer as pS
import threading
import vars
import socket
import raspServer as rS

idVehiculo = 0
ipactiva=0
valores=[]
Cars = ""

# HILOS
# Configuración del servidor
HOST = "localhost" # Dirección IP del servidor
PORT = 65432 # Puerto para la comunicación
PORT_MS = 65433
aliveWindow = 0
def check_window_closed():
    global aliveWindow
    aliveWindow = 1
    root.destroy()

def obtener_direccion_ip():
    # Obtiene la dirección IP de la máquina
    hostname = socket.gethostname()
    direccion_ip = socket.gethostbyname(hostname)
    IPDBtxt.delete("0.0", "end")
    IPDBtxt.insert("0.0", direccion_ip)

# -------------------------------- METODOS ----------------------------------------------
def actualizar_contenido():
    global Cars
    global valores
    global ipactiva

    try:
        if ipactiva == 1:
            pass
        else:
            pass
    except Exception as e:
        print(e)
    updateError()
    root.after(1000, actualizar_contenido)

def buscar_vehiculo(vehiculos, nombre):
    for vehiculo in vehiculos:
        if vehiculo[1] == nombre:
            return vehiculo
    return None

def updateError():
    errorlbl.configure(text=vars.Error)

def cleanError():
    errorlbl.configure(text="")

def startDB():
    global ipactiva
    if ipactiva == 0:
        ipactiva = 1
        btnServerDB.configure(text="Detener Servidor")
        pS.ip = IPDBtxt.get("0.0", "end-1c")
        print(ipactiva)
    else:
        ipactiva = 0
        btnServerDB.configure(text="Iniciar Servidor")
        print(ipactiva)
    

#Configuracion de la ventana
root = CTk()
root.geometry('500x500+540+100')
root.minsize(500,500)
root.maxsize(500,500)
root.title('ParkSys - Send Data')
root.grid_columnconfigure(0, weight=1)

IPDBlbl = CTkLabel(root,text="IP del Servidor",fg_color="transparent")
IPDBlbl.grid(column=0,columnspan=2,row=2)
IPDBtxt = CTkTextbox(root, height=10,corner_radius=10)
IPDBtxt.grid(column=0,row=3)
btnServerDB = CTkButton(root,text="Iniciar Servidor",command=startDB)
btnServerDB.grid(column=1,columnspan=2,row=3,padx=(0,50))
obtener_direccion_ip()

errorlbl = CTkLabel(root,text="",fg_color="transparent")
errorlbl.grid(column=0,columnspan=2,row=11,rowspan=2,pady=(50,0))


# Registrar la función on_closing para el evento de cierre de ventana
root.protocol("WM_DELETE_WINDOW", check_window_closed)

actualizar_contenido()
root.mainloop()