#!/usr/bin/python
#encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Obtiene listado de usuarios y funciones útiles relacionadas
'''
__author__ = "Alexander Ortiz"
__version__ = "0.8"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

from threading import Thread, Semaphore
from utilidades import guardar, ejecutar_comando

class listar ():
    '''
    Separé estos métodos en esta clase porque no pueden usar multiprocesamiento
    y son usados por otros script finales
    '''
    dominios = ()
    usuarios = {}
	
    def obtener_dominio (self):
        '''
        Obtiene todos los dominios que el servidor pueda requerir
        '''
        comando = [ 'zmprov', 'gad' ]
        self.dominios = ejecutar_comando(comando)
        guardar("dominios.lst", self.dominios, "l")

    def obtener_listado (self):
        '''
        Obtiene un listado de todos los usuarios de todos los dominios
        '''
        for dominio in self.dominios:
            comando = ['zmprov', '-l', 'gaa', dominio]
            self.usuarios[dominio] = ejecutar_comando(comando)
            guardar(dominio + ".lst", self.usuarios[dominio], "l")

