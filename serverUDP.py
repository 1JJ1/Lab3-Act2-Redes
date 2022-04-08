import socket
from sqlite3 import connect
import sys
import os 
import hashlib
import time
from datetime import datetime

#from django.db import connection

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


num_conn = int(input('Bienvenido al servidor UDP. Por favor ingresar la cantidad de conexiones: '))

while (num_conn <= 0 and num_conn>25):
    num_conn = int(input('Por favor ingresar un número válido: '))


# Conectar socket al puerto con su IP respectiva.
server_address = ('192.168.37.133', 8888)
#server_address = ('localhost', 8888)
print('El %s esta esparando en el puerto %s' % server_address)
sock.bind(server_address)

#Archivo a enviar
file = input('Por favor ingrese el nombre del archivo a enviar. ej: Prueba_100MB.txt o Prueba_250MB.txt ')
while file not in ['Prueba_100MB.txt','Prueba_250MB.txt']:
    file = input('Por favor ingresar un nombre de archivo correcto: ')

archivoSize = os.path.getsize(file)

log = open("./logs/servidor-"+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+"log.txt", "w")
log.write('Fecha: '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+'\n')  
log.write('El nombre es: '+file+'\n') 
log.write('El tamaño del archivo es: '+str(archivoSize/1000000)+' MB'+'\n')
#TOdo: logs faltantes 

archivo = open(file, 'rb')
buf = archivo.read(1024) #Definimos el tamaño de lectura en 1024 Bytes.

while(buf):
    buf = archivo.read(1024)
 
for i in range(num_conn):
    
    f = open(file,'rb')
    l = f.read(1024)
  
    print ('El servidor esta a la espera de una conexión')
    # Esperando conexion. Deberia llegar iniciar conexion
    connection,client_addr = sock.recvfrom(32)
    print(connection.decode('utf-8'))
    start = time.time()
    log.write('Direccion del cliente: '+str(client_addr)+'\n')  
    try:
        print ('Conectado de', client_addr)
        
        sock.sendto(b'ok',client_addr)
        data,client_addr= sock.recvfrom(32)
        print(data.decode('utf-8'))
        sock.sendto(bytes(file, 'utf-8'),client_addr)
        data,client_addr = sock.recvfrom(32)

        print(data.decode('utf-8'))
        if(data.decode('utf-8')== "listo"):
            
            num_paq= 0
            while (l):
                sock.sendto(l,client_addr) 
                l= f.read(1024)
                num_paq+=1
                print('paquete:'+str(num_paq))
            

            sock.sendto(l,client_addr) 
            print('Conexión terminada exitosamente')
            log.write('Entrega del archivo: se envio el archivo '+'\n')  
            end = time.time()
            log.write('Tiempo transferencia con cliente: '+str(end-start)+'\n')  
        data,client_addr = sock.recvfrom(32)
            
            
    finally:
        print('termino')

log.close()
sock.close()

            

