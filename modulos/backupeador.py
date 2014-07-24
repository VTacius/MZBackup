#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Clase backupeador para creación de backup del mailbox
'''
__author__ = "Alexander Ortiz"
__version__ = "0.7"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import os
from modulos.remoto import remoto, scp
from subprocess import Popen,PIPE,STDOUT
from threading import Thread, Semaphore

class backupeador(Thread):
    usuario = str()
    def __init__(self, semaforo = Semaphore(1)):
        '''Traemos a cuenta algunas variables necesarias'''
        Thread.__init__(self)
        self.semaforo = semaforo
        self.directorio = os.getcwd()
	
    def directorio_remoto(self):
        '''Creamos directorio remoto donde almacenar los fichero'''
        directorio = self.directorio
        print "Creamos los directorio local y remoto en " + directorio
        comando = "su - zimbra -c 'mkdir {cfile}'".format(cfile=directorio )
        ejecutor = remoto()
        status, mensaje	= ejecutor.ejecutor(comando)

    def crear_backup(self, user):
        ''' Creamos el backup en el servidor el backup ''' 
        archivo = self.directorio + "/" + user.replace("@","AT") + ".tgz"
        exe = Popen(['zmmailbox', '-z', '-m', user, 'getRestURL', '-o', archivo, '/?fmt=tgz'], stdout=PIPE)
        stdout,stdin = exe.communicate()
	
    def obtener_backup(self, user):
        ''' Implementamos un cliente SFTP con la conexion que abrimos al instanciar la clase ''' 
        backup = user.replace("@","AT") + ".tgz"
        archivo = self.directorio + "/" + backup
        fichero = self.directorio + "/" + backup 
        scp(archivo, fichero)

    def run (self):
        self.semaforo.acquire()
        self.crear_backup(self.usuario)
        self.obtener_backup(self.usuario)
        self.semaforo.release()
        print ("Terminado " + self.usuario + " en " + self.getName())
