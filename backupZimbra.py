#!/usr/bin/python
# encoding: utf-8
import time
import os
from remoto import remoto
from listado import listar, borrar_usuarios, borrador
from threading import Thread, Semaphore

class backupeador(remoto, Thread):
    usuario = str()
    def __init__(self, directorio, semaforo = Semaphore(1)):
        '''Iniciamos la conexión ssh  como se especifica en la clase remoto'''
        remoto.__init__(self)
        Thread.__init__(self)
        self.semaforo = semaforo
        self.directorio = directorio
	
    def directorio_remoto(self):
        '''Creamos directorio remoto donde almacenar los fichero'''
        directorio = "/opt/zimbra/backup/" + self.directorio
        comando = "su - zimbra -c 'mkdir {cfile}'".format(cfile=directorio )
        status, mensaje	= self.ejecutor(comando)


    def crear_backup(self, user):
        ''' Creamos el backup en el servidor el backup ''' 
        archivo = "/opt/zimbra/backup/" + self.directorio + "/" + user.replace("@","AT") + ".tgz"
        comando = "su - zimbra -c '/opt/zimbra/bin/zmmailbox -z -m {cuser}  getRestURL -o {cfile} //?fmt=tgz'".format(cuser =user, cfile=archivo )
        status, mensaje	= self.ejecutor(comando)
	
    def obtener_backup(self, user):
        ''' Implementamos un cliente SFTP con la conexion que abrimos al instanciar la clase ''' 
        fichero = user.replace("@","AT")  + ".tgz"
        archivo = "/opt/zimbra/backup/" + self.directorio + "/" + fichero 
        self.scp(archivo, fichero)
        print "Obtenido el backup para " + user

    def run (self):
        semaforo.acquire()
        self.crear_backup(self.usuario)
        self.obtener_backup(self.usuario)
        semaforo.release()

def titulador(titulo):
    mensaje = "###############################################################################\n{title}".format
    print mensaje(title=titulo)

if __name__ == "__main__":
    # Creo el directorio donde guardo los ficheros
    dia = time.strftime("%d-%m-%y-%H%M%S")
    directorio = "mailbox-" + dia
    os.mkdir(directorio)
    os.chdir(directorio)
    #Procedimientos para modelar datos con 
    # métodos de modelado.py
    # Procedimientos para obtener datos con 
    # métodos de listado.py
    listador = listar()
    # Se obtiene la lista de dominios
    titulador("Obtenemos la lista de dominios")
    listador.obtener_dominio()
    # Se obtiene la lista de usuarios por cada dominio
    titulador("Obtenemos la lista de usuarios por cada dominio")
    listador.obtener_listado()
    dir = backupeador(directorio)
    dir.directorio_remoto()
    semaforo = Semaphore(9)
    for dom in listador.dominio:
        # Limpiamos el arreglo de usuarios
        usuarios = [x.rstrip() for x in listador.usuarios[dom]]
        borrar_usuarios(usuarios, dom)
        borrador(usuarios)
        for usuario in usuarios:
        # Ejecutado el procedimiento
            vaca = backupeador(directorio, semaforo)
            vaca.usuario = usuario
            vaca.start()
