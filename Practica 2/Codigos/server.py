import socket
import selectors
import io
import re
import time
sel = selectors.DefaultSelector()

def accept(sock_a, mask):
    sock_conn, addr = sock_a.accept()  # Should be ready
    print('aceptado', sock_conn, ' de', addr)
    sock_conn.setblocking(False)
    sel.register(sock_conn, selectors.EVENT_READ | selectors.EVENT_WRITE, read_write)

def read_write(sock_c, mask):
    if mask & selectors.EVENT_READ:
        tam_archivo = sock_c.recv(4)
        tam_archivo = int.from_bytes(tam_archivo, byteorder='big')
        
        titulo = str(sock_c.recv(tam_archivo))[2:(len(str(sock_c.recv(tam_archivo))) - 1)]
        titulo = re.sub(".mp3'", "", titulo)
        
        cancion = sock_c.recv(1024)
        if cancion:
            recv_buffer = io.BytesIO()
            recv_buffer.write(cancion)
            while True:
                cancion = sock_c.recv(1024)
                if not cancion:
                    break
                recv_buffer.write(cancion)
            #Creamos un archivo donde almacenaremos los bytes recibidos
            with open(str(titulo) + '.mp3', 'wb') as f:
                f.write(recv_buffer.getvalue())
            sel.unregister(sock_c)
            sock_c.close() #Cerramos el socket luego de almacenar canción
        else: #No hubo datos
            print('cerrando', sock_c)
            sel.unregister(sock_c)
            sock_c.close() #Ceramos el socket
    if mask & selectors.EVENT_WRITE:
        print('Canción recibida y almacenada')
        

with socket.socket() as sock_accept:
    sock_accept.bind(('127.0.0.1', 12345))
    sock_accept.listen(100)
    sock_accept.setblocking(False)
    sel.register(sock_accept, selectors.EVENT_READ, accept)
    while True:
        print("Esperando evento...")
        events = sel.select()
        for key, mask in events:
            time.sleep(0.2)
            callback = key.data
            callback(key.fileobj, mask)
