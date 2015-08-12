#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Funciones para leer la configuracion
Como varios otros ficheros la necesitaban, decidí separalo en un archivo separado
'''
__author__ = "Alexander Ortiz"
__version__ = "0.5"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import ConfigParser
import sys
import os

# Leyendo del archivo de configuracion
parser = ConfigParser.SafeConfigParser()
base = os.getcwd()
fichero = base + "/mzbackup.ini"
seccion = 'Global'

def configuracion(clave):
    '''
    Leer de un fichero .ini algunas variables propias del usuario
    '''
    # Revisamos que el fichero exista
    if not os.path.isfile(fichero):
        print('El fichero de configuración mzbackup.ini no existe')
        sys.exit()
    
    # Retornamos tal parametros si es que es posible parsear el fichero
    parser.read(fichero)
    secciones = parser.sections()
    if len(secciones)>0:
        return parser.get(seccion,clave)
    else:
        print "Revise la estructura del fichero mzbackup.ini"
        sys.exit()
