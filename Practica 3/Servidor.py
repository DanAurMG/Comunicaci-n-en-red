import socket
import time
import threading
import numpy as np

#HOST = "172.100.85.114"
HOST = "127.0.0.1"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024

def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=juego, args=[client_conn, client_addr])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("Hilos activos:", threading.active_count())
    print("Enumerar", threading.enumerate())
    print("Tamaño y lista de conexiones: ", len(listaconexiones))
    print(listaconexiones)


def juego(Client_conn, Client_addr):
    try:
        cur_thread = threading.current_thread()
        print("Conectado a", Client_addr)
        inicio = time.time()
        print("Nuevo cliente detectado")
        # Mensaje de bienvenida
        Client_conn.sendall(b"Vamos a jugar buscaminas, puedes elegir entre dificultad: principiante o avanzado")
        print("Esperando a recibir dificultad... ")
        data = Client_conn.recv(buffer_size)
        if not data:
            print("No hubo datos :(")

        info = str(data)[2:(len(str(data)) - 1)]
        print(info)
        while True:

            # Recibimos la dificultad que mande el cliente
            if (info == "principiante" or info == "Principiante"):
                print("El cliente quiere jugar principiante")
                Client_conn.sendall(
                    b"Vamos a jugar buscaminas en nivel principiante")
                Client_conn.sendall(
                    b"Permiteme crear el tablero de 9 x 9 y colocar las 10 bombas...")

                # Creando el tablero
                print("Creando tablero nivel principiante")
                tablero = np.zeros((9, 9))
                minas = np.zeros(9)
                for i in range(0, 10):
                    # for j in range (10):
                    #     print("-\t")
                    # print("\n")
                    fila = np.random.randint(0, 9)
                    col = np.random.randint(0, 9)
                    tablero[fila, col] = 1
                    minas[col] = fila
                    print("Mina colocada en: ", fila, col)
                
                print(tablero)

                time.sleep(3)
                Client_conn.sendall(b"Tablero creado")
                time.sleep(3)
                Client_conn.sendall(
                        b"Bombas colocadas... Estamos listo, has tu primer tiro, si te atreves...")
                    # Aqui creamos la matriz y obtenemos la ubicación de las bombas para principiante
                    # Si ya estamos jugando entrará jugar en principiante
                while True:
                    time.sleep(3)
                    print("Esperando el siguiente tiro...")
                    data = Client_conn.recv(buffer_size)
                    info = str(data)[2:(len(str(data)) - 1)]
                    print(info)
                    if not data:
                        print("No hubo datos :(")
                    if (tablero[int(info[0]), int(info[1])]):
                        Client_conn.sendall(b"Mina")
                        print("El cliente pisó una mina")
                        fin = time.time()
                        despedida = "Estuvo conectado " + str(fin-inicio) + " segundos."
                        print(despedida)
                        Client_conn.sendall(bytes(str(fin-inicio),  "UTF-8"))
                        break
                    else:
                        tablero[int(info[0]), int(info[1])] = "8"
                        print(tablero)               
    
                        Client_conn.sendall(b"Okey")
                                                        
            elif(info == "avanzado" or info == "Avanzado"):
                print("El cliente quiere jugar avanzado")
                Client_conn.sendall(b"Vamos a jugar avanzado pues")
                Client_conn.sendall(b"Permiteme crear el tablero de 16 x 16 y colocar las 40 bombas")
                    
                #Aqui creamos la matriz y obtenemos la ubicación de las bombas para principiante   
                #Creando el tablero
                print("Creando tablero nivel avanzado")
                tablero = np.zeros((16,16))
                minas = np.zeros(40)
                for i in range(0 , 40):
                    fila = np.random.randint(0,15)
                    col = np.random.randint(0,15)
                    tablero[fila,col] = 1
                    minas[col] = fila
                    print("Mina colocada en: ", fila, col)
                
                print(tablero)
                    
                time.sleep(3)
                Client_conn.sendall(b"Tablero creado")
                time.sleep(3)
                Client_conn.sendall(b"Bombas colocadas... Estamos listo, has tu primer tiro, si te atreves...")                    
                #Aqui creamos la matriz y obtenemos la ubicación de las bombas para principiante
                #Si ya estamos jugando entrará jugar en principiante
                while True:  
                    time.sleep(3)                 
                    print("Esperando el siguiente tiro...")
                    data = Client_conn.recv(buffer_size)                    
                    info = str(data)[2:(len(str(data)) - 1)]
                    print(info)
                    if not data:
                        print("No hubo datos :(")
                    if(tablero[int(info[0:2]), int(info[2:4])]):
                        Client_conn.sendall(b"Mina")
                        print("El cliente pisó una mina")
                        fin = time.time()
                        despedida = "Estuvo conectado " + str(fin-inicio) + " segundos."
                        print(despedida)
                        Client_conn.sendall(bytes(despedida,  "UTF-8"))
                        break
                    else:
                        tablero[int(info[0:2]), int(info[2:4])] = "8"
                        print(tablero)
    
    
                        Client_conn.sendall(b"Okey")
            #Tiempo muerto entre conexión y conexión
            time.sleep(2) 
            break 
    except Exception as e:
        print(e)
    finally:
        Client_conn.close()

listaConexiones = []
numConn = input("Ingresa el numero de jugadores simultaneos:\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")
    
    servirPorSiempre(TCPServerSocket, listaConexiones)