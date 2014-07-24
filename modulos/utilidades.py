#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Funciones útiles de carácter general
'''
__author__ = "Alexander Ortiz"
__version__ = "0.7"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import os
import sys
import time

def titulador(titulo):
    '''
    Saca a pantalla un mensaje con decorado, aparte los comodines se ven feos en los print
    '''
    mensaje = "###############################################################################\n{title}".format
    print mensaje(title=titulo)

def situar_directorio(objeto):
    '''
    Crear un directorio local para el objeto dado, incluye una marca de tiempo. 
    Mueve las operaciones del script al directorio creado
    '''
    dirbase = "/opt/backup" 
    timestamp = time.strftime('%d-%m-%y-%H%M%S')
    directorio = dirbase.rstrip("/") + "/" + objeto + "-" + timestamp
    try:
        os.mkdir(directorio)
        os.chdir(directorio)
    except IOError as e:
        print "IO: " + str(e)
        sys.exit(1)
    except OSError as e:
        print "OS: " + str(e)
        sys.exit(1)

def guardar(archivo, contenido):
    '''
    Función que guarda contenido en un fichero dado con métodos de os
    Usarlo en funciones Thread para crear un bloqueo del fichero
    Este procedimiento es claramente más lento, pero es necesario
    '''
    fichero = os.open(archivo, os.O_RDWR|os.O_APPEND|os.O_CREAT)
    os.write(fichero, contenido)
    os.close(fichero)

