#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.backupeador import backupeador
from modulos.listado import listar
from modulos.utilidades import situar_directorio, titulador, borrar_usuarios, borrar_patrones
from threading import Semaphore, Thread

import os
from subprocess import Popen,PIPE,STDOUT
import argparse

class backupeador(Thread):
    usuario = str()
    def __init__(self, semaforo = Semaphore(1)):
        '''Traemos a cuenta algunas variables necesarias'''
        Thread.__init__(self)
        self.semaforo = semaforo
        self.directorio = os.getcwd()
	
    def crear_backup(self, user):
        ''' Creamos el backup en el servidor el backup ''' 
        archivo = self.directorio + "/" + user.replace("@","AT") + ".tgz"
        exe = Popen(['zmmailbox', '-z', '-m', user, 'getRestURL', '-o', archivo, '/?fmt=tgz'], stdout=PIPE)
        stdout,stdin = exe.communicate()
	
    def run (self):
        self.semaforo.acquire()
        self.crear_backup(self.usuario)
        self.semaforo.release()
        print ("Terminado " + self.usuario + " en " + self.getName())

if __name__ == "__main__":
    # Creo el directorio donde guardo los ficheros
    titulador("Creado el directorio de trabajo")
    situar_directorio("mailbox", "/opt/extbackup")
    # Se obtiene la lista de dominios
    titulador("Obtenemos la lista de dominios")
    listador = listar()
    listador.obtener_dominio()
    # Se obtiene la lista de usuarios por cada dominio
    titulador("Obtenemos la lista de usuarios por cada dominio")
    listador.obtener_listado()
    # Definido el número de hilos a usar
    semaforo = Semaphore(28)
    titulador("Empieza los hilos para crear datos")
    dom = "salud.gob.sv"
    # Limpiamos el arreglo de usuarios
    for dom in listador.dominios:
        # Limpiamos el arreglo de usuarios
        borrar_usuarios(listador.usuarios[dom], dom)
        borrar_patrones(listador.usuarios[dom])
        for usuario in listador.usuarios[dom]:
        # Ejecutado el procedimiento
            vaca = backupeador(semaforo)
            vaca.usuario = usuario
            vaca.start()
