#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Clase backupeador y enviador para creación de backup del mailbox
'''
__author__ = "Alexander Ortiz"
__version__ = "1.1"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

from modulos.utilidades import ejecutar_comando, enviante 
from os import getcwd
from Queue import Queue
from threading import Thread

class Enviante(Thread):
    """Envia el respaldo del usuario al servidor destinado para backup"""
 
    def __init__(self, semaforo,  cola):
        Thread.__init__(self)
        self.cola = cola
        self.semaforo = semaforo
 
    def run(self):
        while True:
            self.semaforo.acquire() 
            # Obtiene ruta de ficheros de backup en la cola
            backup = self.cola.get()
            print("Enviando " + backup)
 
            # Envia el fichero backup
            enviante(backup, backup)
 
            # Enviamos una señal sobre que nuestro trabajo ha sido realizado con exito
            self.cola.task_done()
            self.semaforo.release()
            print ("Finalizado envío para " + backup)
 
class Respaldante(Thread):
    """Creo el respaldo del usuario"""

    def __init__(self, semaforo, cola, usuario):
        Thread.__init__(self)
        self.semaforo = semaforo
        self.cola = cola
        self.usuario = usuario
        self.directorio = getcwd()
    
    def run(self):
        self.semaforo.acquire()
        print "Creo respaldo para " + self.usuario
        backup = self.crear_backup(self.usuario)
        if self.cola:
            self.cola.put(backup)
        print "Terminado backup para " + self.usuario
        self.semaforo.release()
    
    def crear_backup(self, user):
        ''' 
        Hacemos un backup para el usuario dado
        ''' 
        archivo = "{0}/{1}.tgz".format(self.directorio, user.replace("@","AT"))
        comando = ['zmmailbox', '-z', '-m', user, 'getRestURL', '-o', archivo, '/?fmt=tgz']
        ejecutar_comando(comando)
        return archivo


