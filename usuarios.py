#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.listado import listar, obtener, borrar_usuarios, borrador
from modulos.utilidades import titulador, situar_directorio
from threading import Semaphore
import json
import os
import sys
import time

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print "Hace falta el directorio cos-{fecha} como parametro"
        sys.exit(1)
    dir_cos = sys.argv[1]
    cos_file = "/"+ dir_cos.rstrip("/") + "/cos.id"
    try:
        with open(cos_file) as json_file:
            cosId = json.load(json_file)
    except IOError as e:
        print "A: " + str(e)
        sys.exit(1)
    # Creo el directorio donde guardo los ficheros
    situar_directorio("usuarios")
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
    # Limpiamos el arreglo de dominio
    dominios = [x.rstrip("\n") for x in listador.dominios]
    semaforo = Semaphore(35)
    for dom in dominios:
        # Limpiamos el arreglo de usuarios
        usuarios = [x.rstrip() for x in listador.usuarios[dom]]
        borrar_usuarios(usuarios, dom)
        borrador(usuarios)	
        for usuario in usuarios:
        # Ejecutado el procedimiento
            saqueador = obtener(semaforo, usuario, dom, cosId)
            saqueador.start()
