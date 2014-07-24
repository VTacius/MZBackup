#!/usr/bin/python
#encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Operaciones con listas de distribucion
'''
__author__ = "Alexander Ortiz"
__version__ = "0.8"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

from modulos.utilidades import guardar, ejecutar_comando
import os
import re as r
import time
from threading import Thread, Semaphore

class distribucion(Thread):
    listado = ()
    contenido = str()
    marcador  = "^#\sdistributionList"
    atributos = "^(cn|description|displayName|zimbraMailForwardingAddress|zimbraNotes|zimbraPrefReply):" 

    def __init__(self, semaforo=Semaphore(1), lista=str() ):
        Thread.__init__(self)
        self.semaforo = semaforo
        self.lista = lista
        self.archivo = "listas_distribucion.{ext}".format

    def listar_listas(self):
        comando = ['zmprov', 'gadl']
        self.listado = ejecutar_comando(comando)
        guardar(self.archivo(ext="lst"), self.listado, "l")

    def obtener(self, lista):
        comando = ['zmprov', 'gdl', lista]
        salida = ejecutar_comando(comando)
        self.almacenar(salida)
        guardar(self.archivo(ext="data"), salida, "l")

    def almacenar(self, datos):
        contenido = str()
        for linea in datos:
            contenido += self.__modelado(linea)
        guardar(self.archivo(ext="cmd"), contenido, "l")
        
    def __modelado(self, linea):
        sentencia = str()
        if r.match(self.marcador,linea):
            sentencia = "\n\nzmprov cdl " + linea.split(" ")[2] + " "
        elif r.match(self.atributos,linea):
            i = linea.find(" ")
            sentencia = linea[:i-1] + " \"" + linea[i+1:].rstrip("\n") + "\" "
        return sentencia
    
    def run(self):
        self.semaforo.acquire()
        self.obtener(self.lista)
        self.semaforo.release()
        print ("Terminado " + self.lista + " en " + self.getName())
