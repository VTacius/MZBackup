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
    '''
    Maneja una entrada resultado de zmprov gdl `lista@dominio.com`
    La convierte en una serie de comandos para crear la lista de distribución con todos los usuarios 
    que tenía en el servidor anterior
    '''
    
    listado = ()
    contenido = str()
    marcador  = r.compile('^#\sdistributionList')
    atributos = r.compile('^(cn|description|displayName|zimbraMailForwardingAddress|zimbraNotes|zimbraPrefReply):')

    def __init__(self, semaforo=Semaphore(5), lista=str()):
        Thread.__init__(self)
        self.archivo = "listas_distribucion.{ext}".format
        self.semaforo = semaforo
        self.lista = lista

    def listar_listas(self):
        '''
        Esta lógica que no requiere multiprocesamiento deberia estar en listado.py
        '''
        comando = ['zmprov', 'gadl']
        self.listado = ejecutar_comando(comando)
        guardar(self.archivo(ext="lst"), self.listado, "l")

    def obtener(self, lista):
        '''
        Obtiene todos los datos relacionados a cada lista de distribucion 
        '''
        comando = ['zmprov', 'gdl', lista]
        salida = ejecutar_comando(comando)
        self.almacenar(salida)
        guardar(self.archivo(ext="data"), salida, "l")

    def almacenar(self, datos):
        '''
        Itera sobre el conjunto de datos de cada lista de distribución y modela cada linea que va encontrando gracias a self.__modelado
        '''
        contenido = str()
        for linea in datos:
            contenido += self.__modelado(linea)
        guardar(self.archivo(ext="cmd"), contenido, "l")
        
    def __modelado(self, linea):
        '''
        Modela cada linea con los datos solicitados
        '''
        sentencia = str()
        if self.marcador.match(linea):
            sentencia = "\n\nzmprov cdl " + linea.split(" ")[2] + " "
        elif self.atributos.match(linea):
            i = linea.find(" ")
            sentencia = linea[:i-1] + " \"" + linea[i+1:].rstrip("\n") + "\" "
        return sentencia
    
    def run(self):
        self.semaforo.acquire()
        self.obtener(self.lista)
        self.semaforo.release()
        print ("Terminado " + self.lista + " en " + self.getName())
