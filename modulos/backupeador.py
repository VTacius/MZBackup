#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Clase backupeador para creación de backup del mailbox
'''
__author__ = "Alexander Ortiz"
__version__ = "0.9"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import os
from subprocess import Popen,PIPE,STDOUT
from modulos.utilidades import ejecutar_comando
from threading import Thread, Semaphore

class enviador(Thread):

    def __init__(self, origen, destino, semaforo):
        Thread.__init__(self)
        self.origen = origen
        self.destino = destino
        self.semaforo = semaforo

    def enviante(self, origen, destino):
        comando = ['scp', origen, 'root@10.10.20.102:' + destino]
        ejecutar_comando(comando)
    
    def run(self):
        self.semaforo.acquire()
        self.enviante(self.origen, self.destino)
        print (__name__ + " Terminado " + self.origen + " en " + self.getName())
        self.semaforo.release()

class backupeador(Thread):

    def __init__(self, usuario, semaforo):
        '''Traemos a cuenta algunas variables necesarias'''
        Thread.__init__(self)
        self.semaforo = semaforo
        self.directorio = os.getcwd()
        self.usuario = usuario
	
    def crear_backup(self, user):
        ''' Creamos el backup en el servidor el backup ''' 
        archivo = self.directorio + "/" + user.replace("@","AT") + ".tgz"
        exe = Popen(['zmmailbox', '-z', '-m', user, 'getRestURL', '-o', archivo, '/?fmt=tgz'], stdout=PIPE)
        stdout,stdin = exe.communicate()
	
    def run (self):
        self.semaforo.acquire()
        self.crear_backup(self.usuario)
        backup = self.usuario.replace("@","AT") + ".tgz"
        origen = self.directorio + "/" + backup
        destino = self.directorio + "/" + backup 
        self.semaforo.release()
        semaforo = Semaphore(2)
        enviante = enviador(origen, destino, semaforo)
        enviante.start()
        #print ("Terminado " + self.usuario + " en " + self.getName())

