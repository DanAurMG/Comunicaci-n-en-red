import socket
import time
import os

HOST = '127.0.0.1'
PORT = 12345

path=input()
file_path = path
with open(file_path, 'rb') as file:
    file_data = file.read()

# Conecta con el servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
time.sleep(1)

file_name = os.path.basename(file_path)
file_size = len(file_name).to_bytes(4, byteorder='big')
client_socket.sendall(file_size)
# Envía el nombre del archivo al servidor
client_socket.sendall(bytes(file_name, "utf-8"))

# Envía los datos del archivo al servidor
client_socket.send(file_data)

client_socket.close()
print("Archivo enviado al servidor")