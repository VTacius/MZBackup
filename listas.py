#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

import os
import re as r
import time
from subprocess import STDOUT,PIPE,Popen
from threading import Thread, Semaphore
from modulos.utilidades import titulador, situar_directorio, guardar

class distribucion(Thread):
    listado = ()
    contenido = str()
    marcador  = "^#\sdistributionList"
    atributos = "^(cn|description|displayName|zimbraMailForwardingAddress|zimbraNotes|zimbraPrefReply):" 

    def __init__(self, semaforo=Semaphore(1), lista=str() ):
        Thread.__init__(self)
        self.semaforo = semaforo
        self.lista = lista
        self.marca = "listas_distribucion" 

    def listar(self):
        exe = Popen(['zmprov', 'gadl'], stdout=PIPE)
        stdout, stdin = exe.communicate()
        self.listado = [ x for x in stdout.split("\n") if len(x) > 0 ]
        archivo = self.marca + ".lst" 
        guardar(archivo, stdout)

    def obtener(self, lista):
        exe = Popen(['zmprov', 'gdl', lista], stdout=PIPE)
        stdout,stdin = exe.communicate()
        self.almacenar(stdout.split("\n"))
        archivo = self.marca + ".data" 
        guardar(archivo, stdout + "\n")

    def almacenar(self, datos):
        contenido = str()
        for linea in datos:
            contenido += self.formateo(linea)
        archivo = self.marca+ ".cmd"
        guardar(archivo, contenido)
        
    def formateo(self, linea):
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


if __name__ == "__main__":
    situar_directorio("listas")
    titulador("Listamos lista de distribución")
    listar = distribucion()
    listar.listar()
    semaforo = Semaphore(14)
    titulador("Empieza los hilos para crear datos")
    for lista in listar.listado:
        ld = distribucion(semaforo, lista)
        ld.start()

