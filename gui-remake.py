from customtkinter import CTk, CTkLabel, CTkComboBox, CTkTextbox, CTkButton, CTkCheckBox
import pcServerR as pS
import threading
import vars
import socket

idVehiculo = 0
valores=[]
Cars = ""


aliveWindow = 0
def check_window_closed():
    global aliveWindow
    aliveWindow = 1
    root.destroy()

def obtener_direccion_ip():
    # Obtiene la dirección IP de la máquina
    hostname = socket.gethostname()
    direccion_ip = socket.gethostbyname(hostname)
    IPtxt.delete("0.0", "end")
    IPtxt.insert("0.0", direccion_ip)
    IPWebTxt.delete("0.0", "end")
    IPWebTxt.insert("0.0", direccion_ip)

def getImage():
    global aliveWindow
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
                    data = conn.recv(1024)  # Recibir datos (tamaño del buffer)
                    with open('image/placa.jpg', 'wb') as f:
                        while data:
                            f.write(data)
                            data = conn.recv(1024)
                    print('Imagen recibida y guardada como "placa.jpg"')
                vars.placa = pS.ObtenerPlaca(pS.image_path)
                placatxt.delete("0.0", "end")
                placatxt.insert("0.0",vars.placa)
                print(aliveWindow)
                if aliveWindow:
                    return False

    except Exception as e:
        print(f"Error al recibir la imagen: {e}")
        return "N"  # Si hay un error al recibir la imagen

def getText():
    global aliveWindow
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
                    print('Mensaje recibido del cliente:', message)
                vars.rfid_txt = message
                updateRFID()
                print(aliveWindow)
                if aliveWindow:
                    return False

    except Exception as e:
        print(f"Error al recibir el mensaje: {e}")

def updatePlacaTxt():
    placatxt.delete("0.0", "end")
    placatxt.insert("0.0",vars.placa)

def updateRFID():
    rfidtxt.delete("0.0", "end")
    rfidtxt.insert("0.0", vars.rfid_txt)

# -------------------------------- METODOS ----------------------------------------------
def updateError():
    errorlbl.configure(text=vars.Error)

def cleanError():
    errorlbl.configure(text="")

# HILOS
hiloImagen = threading.Thread(target=getImage)
hiloTexto = threading.Thread(target=getText)
hiloweb = threading.Thread(target=pS.start_mainSock)

def startServer():
    cleanError()
    vars.HOST = IPtxt.get("0.0", "end-1c")
    hiloImagen.start()
    hiloTexto.start()
    btnServer.configure(state="disabled")

def startDB():
    cleanError()
    vars.SWeb = IPWebTxt.get("0.0", "end-1c")
    hiloweb.start()
    btnServerWeb.configure(state="disabled")
    

#Configuracion de la ventana
root = CTk()
root.geometry('500x500+540+100')
root.minsize(500,500)
root.maxsize(500,500)
root.title('ParkSys - Send Data')
root.grid_columnconfigure(0, weight=1)


IPlbl = CTkLabel(root,text="IP Raspberry",fg_color="transparent")
IPlbl.grid(column=0,columnspan=2,row=0)
IPtxt = CTkTextbox(root, height=10,corner_radius=10)
IPtxt.grid(column=0,row=1)
btnServer = CTkButton(root,text="Iniciar Servidor",command=startServer)
btnServer.grid(column=1,row=1,padx=(0,50))

IPDBlbl = CTkLabel(root,text="IP Web",fg_color="transparent")
IPDBlbl.grid(column=0,columnspan=2,row=2)
IPWebTxt = CTkTextbox(root, height=10,corner_radius=10)
IPWebTxt.grid(column=0,row=3)
btnServerWeb = CTkButton(root,text="Iniciar BD",command=startDB)
btnServerWeb.grid(column=1,columnspan=2,row=3,padx=(0,50))
obtener_direccion_ip()


placalbl = CTkLabel(root,text="Placa:",fg_color="transparent")
placalbl.grid(column=0,columnspan=2,row=6)
placatxt = CTkTextbox(root,height=10,corner_radius=10)
placatxt.grid(column=0,columnspan=2,row=7)

rfidlbl = CTkLabel(root,text="Identificación:",fg_color="transparent")
rfidlbl.grid(column=0,columnspan=2,row=8,pady=(20,0))
rfidtxt = CTkTextbox(root,height=10,corner_radius=10)
rfidtxt.grid(column=0,columnspan=2,row=9,rowspan=2,padx=20)

errorlbl = CTkLabel(root,text="",fg_color="transparent")
errorlbl.grid(column=0,columnspan=2,row=11,rowspan=2,pady=(50,0))

# Registrar la función on_closing para el evento de cierre de ventana
root.protocol("WM_DELETE_WINDOW", check_window_closed)

root.mainloop()