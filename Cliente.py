import socket
import time
import matplotlib.pyplot as plt
import numpy as np

# Cambiamos la IP por la del dispositivo o la de la máquina virtual según queramos el que sea el servidor
#HOST = "192.168.1.93"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024
jugandoP = 0


print("Ingresa la IP destino")
HOST = input()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    #Establece la conexión con el servidor
    TCPClientSocket.connect((HOST, PORT))
    #Recibe e imprime el mensaje de bienvenida
    data = TCPClientSocket.recv(buffer_size)
    info = str(data)[2:(len(str(data)) - 1)]
    print(info)
    #Mandamos la dificultad que queremos al servidor
    print("Ingrese su elección de dificultad:")
    mensaje = input()
    TCPClientSocket.sendall(bytes(mensaje, "UTF-8"))
    #Recibimos el primer mensaje del servidor
    data = TCPClientSocket.recv(buffer_size)
    info = str(data)[2:(len(str(data)) - 1)]
    print(info)
    data = TCPClientSocket.recv(buffer_size)
    info = str(data)[2:(len(str(data)) - 1)]
    print(info)
    data = TCPClientSocket.recv(buffer_size)
    info = str(data)[2:(len(str(data)) - 1)]
    print(info)
    data = TCPClientSocket.recv(buffer_size)
    info = str(data)[2:(len(str(data)) - 1)]
    print(info)
    jugandoP = 1
    time.sleep(2)
    if(mensaje == "principiante" or mensaje == "Principiante"):
        # Creando el tablero
        print("Creando tablero nivel principiante")
        plt.figure(figsize=(5, 5))
        tablero = np.zeros((9, 9))
        plt.pcolor(tablero, edgecolors='k', linewidths=4)
        plt.savefig('TableroCP.png', dpi=300)
        while True:
            print("Haga su tiro en formato de número de dos números (xy), donde x representa la fila mientras que y representa la columna (números 0-9)")
            mensaje = input()
            TCPClientSocket.sendall(bytes(mensaje, "UTF-8"))
            data = TCPClientSocket.recv(buffer_size)
            info = str(data)[2:(len(str(data)) - 1)]
            print(info)
            if (info == "Okey"):
                tablero[int(mensaje[0]), int(mensaje[1])] = 1
                plt.pcolor(tablero, edgecolors='k', linewidths=4)
                plt.savefig('TableroCP.png', dpi=300)
                
            if (info == "Mina"):
                print("Has perdido")
                tablero[int(mensaje[0]), int(mensaje[1])] = 2
                plt.pcolor(tablero, edgecolors='k', linewidths=4)
                plt.savefig('TableroCP.png', dpi=300)
                data = TCPClientSocket.recv(buffer_size)
                info = str(data)[2:(len(str(data)) - 1)]
                print("Estuvo conectado: ", info, " segundos.")
                exit()
    #Procedimiento en caso de seleccionar avanzado
    if(mensaje == "avanzado" or mensaje == "Avanzado"):
        # Creando el tablero
        print("Creando tablero nivel avanzado")
        plt.figure(figsize=(5, 5))
        tablero = np.zeros((16, 16))
        plt.pcolor(tablero, edgecolors='k', linewidths=4)
        plt.savefig('TableroCA.png', dpi=300)
        while True:
            print("Haga su tiro en formato de dos números conformados por dos dígitos cada uno (xxyy), donde xx representa la fila mientras que yy representa la columna (números 0-15)")
            mensaje = input()
            TCPClientSocket.sendall(bytes(mensaje, "UTF-8"))
            data = TCPClientSocket.recv(buffer_size)
            info = str(data)[2:(len(str(data)) - 1)]
            print(info)
            
            if (info == "Okey"):
                tablero[int(mensaje[0:2]), int(mensaje[2:4])] = 2
                plt.pcolor(tablero, edgecolors='k', linewidths=4)
                plt.savefig('TableroCA.png', dpi=300)
                
            if (info == "Mina"):
                print("Has perdido")
                tablero[int(mensaje[0:2]), int(mensaje[2:4])] = 3
                plt.pcolor(tablero, edgecolors='k', linewidths=4)
                plt.savefig('TableroCA.png', dpi=300)
                data = TCPClientSocket.recv(buffer_size)
                info = str(data)[2:(len(str(data)) - 1)]
                print("Estuvo conectado: ", info, " segundos.")
                exit()
                
            if not data:
                print("No hubo datos :(")
                exit()
