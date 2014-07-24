#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Clase backupeador y enviador para creación de backup del mailbox
'''
__author__ = "Alexander Ortiz"
__version__ = "0.9"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import os
from subprocess import Popen,PIPE,STDOUT
from modulos.utilidades import ejecutar_comando, enviante
from threading import Thread, Semaphore

remoto = "10.10.20.102"

class enviador(Thread):

    def __init__(self, origen, destino, semaforo):
        '''Traemos a cuenta algunas variables necesarias'''
        Thread.__init__(self)
        self.origen = origen
        self.destino = destino
        self.semaforo = semaforo
    
    def run(self):
        self.semaforo.acquire()
        enviante(self.origen, self.destino)
        self.semaforo.release()
        print (__name__ + " Terminado " + self.origen + " en " + self.getName())

class backupeador(Thread):

    def __init__(self, usuario, semaforo):
        '''Traemos a cuenta algunas variables necesarias'''
        Thread.__init__(self)
        self.semaforo = semaforo
        self.directorio = os.getcwd()
        self.usuario = usuario
	
    def crear_backup(self, user):
        ''' Creamos el backup en el servidor ''' 
        archivo = self.directorio + "/" + user.replace("@","AT") + ".tgz"
        comando ['zmmailbox', '-z', '-m', user, 'getRestURL', '-o', archivo, '/?fmt=tgz']
        ejecutar_comando(comando)
        return archivo
	
    def run (self):
        self.semaforo.acquire()
        backup = self.crear_backup(self.usuario)
        origen = self.directorio + "/" + backup
        destino = self.directorio + "/" + backup 
        # La idea es que una vez creado el fichero, podamos liberar el semaforo para que 
        # continue el envío con otros hilos
        self.semaforo.release()
        # Acá empieza el envío propiamente dicho
        semaforo = Semaphore(2)
        enviante = enviador(origen, destino, semaforo)
        enviante.start()
