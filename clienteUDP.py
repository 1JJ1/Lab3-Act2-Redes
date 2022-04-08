from http import server
import socket
import sys
import os
import threading
from datetime import datetime
import time


num_client = int(input('Cuantos clientes desea crear? '))
while (num_client <= 0 and num_client>25 ):
    num_client = int(input('Por favor ingresar un número válido: '))

class Main:    
    def __init__(self):
        self.lock = threading.Lock()
    def funct(self, nombre):
        self.lock.acquire()
        log = open("./logs/"+nombre+' '+datetime.today().strftime('%Y-%m-%d-%H-%M-%S')+"log.txt", "w")
        self.lock.release()

        # Crear a UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Conectar socket al puerto donde se esta escuchando. IP de maquina virtual Ubuntu.
        server_addr = ('192.168.37.133', 8888)
        #server_addr = ('localhost', 8888)
        print( 'connecting to %s port %s' % server_addr)
        sock.connect(server_addr)
        file = open("./ArchivosRecibidos/"+nombre+"-prueba-"+str(num_client)+".txt", "w")
        
        try:
            self.lock.acquire()
            mensaje = b'Iniciar conexion...'
            print ( 'enviando "%s"' % mensaje)
            sock.sendto(mensaje,server_addr)
        
            confirmacion,server_addr = sock.recvfrom(32)
            if(confirmacion.decode('utf-8') == "ok"):
                print('servidor mando ok')
                sock.sendto(b'Cual es el nombre del archivo?',server_addr)
                nA,server_addr = sock.recvfrom(32)
                nombreArchivo = nA.decode('utf-8') 
                log.write('El nombre es: '+nombreArchivo+'\n')
                sock.sendto(b'listo',server_addr)
                num_paq=0
                start = time.time()
                err = False
                while (True):      
                    data,server_addr = sock.recvfrom(1024)
                    
                    if data:
                        try:
                            file.write(data.decode('utf-8') + os.linesep)
                            num_paq+=1
                            print('paquete: '+str(num_paq))
                            
                        except:
                            err = True
                            print('Ocurrio un error') 
                            sock.sendto(b'Hubo un error al recibir el archivo',server_addr)
                            break
                        
                    else:
                        print ('Final de lectura del archivo')
                        sock.sendto(b'Archivo recibido',server_addr)
                        break
                end = time.time()
                tam = os.path.getsize("./ArchivosRecibidos/"+nombre+"-prueba-"+str(num_client)+".txt")
                

                file.close()
                log.write('El nombre del cliente es: '+nombre+'\n')
                log.write('El tamaño del archivo es: '+str(tam/1000000)+' MB'+'\n')
                
                if err == False:
                    print("Archivo leido")
                    log.write('Entrega del archivo'+'\n')
                else:
                    log.write('Error entrega archivo'+'\n')

                log.write('Tiempo de transferencia: '+str(end-start)+ ' segs'+'\n') 
                log.write('Valor total en bytes recibidos: '+str(tam)+'\n')     
                log.write('Cantidad de paquetes recibidos: '+str(num_paq)+'\n') 
                         
        finally:
            
            print ('Cerrar socket')
            
            self.lock.release() 
            print ('Fin del programa')
            log.close()
        sock.close()
           
def targ(c, nombre):
        c.funct(nombre)
        
hilo=Main()
for num_cliente in range(num_client):
    cliente = threading.Thread(name="Cliente%s" %(num_cliente+1),
                               target=targ,
                               args=(hilo,"Cliente%s" %(num_cliente+1))
                              )
    cliente.start()
