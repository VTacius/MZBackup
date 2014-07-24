#!/usr/bin/python
#encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Obtiene listado de usuarios y funciones útiles relacionadas
'''
__author__ = "Alexander Ortiz"
__version__ = "0.7"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import os
import re
import time, random
from modelado import modelador
from subprocess import Popen,PIPE,STDOUT
from threading import Thread, Semaphore
from utilidades import guardar

class listar ():
    dominios = ()
    usuarios = {}
	
    def guardar_fichero (self, archivo, datos):
        fichero = open(archivo, "w")
        for i in datos:
            fichero.write(i + "\n")
            fichero.flush()

    def obtener_dominio (self):
        exe = Popen([ 'zmprov', 'gad' ], stdout=PIPE)
        stdout,stdin = exe.communicate()
        self.dominios=stdout.split("\n")
        self.dominios.remove("")
        self.guardar_fichero ("dominios.lst", self.dominios)

    def obtener_listado (self):
        for dominio in self.dominios:
            exe = Popen(['zmprov', '-l', 'gaa', dominio], stdout=PIPE)
            stdout, stdin = exe.communicate()
            self.usuarios[dominio] = stdout.split("\n")
            self.guardar_fichero (dominio + ".lst", self.usuarios[dominio])

class obtener(Thread):
    def __init__ (self, semaforo, user, dominio, cosId):
        Thread.__init__(self)
        self.semaforo = semaforo
        self.user = user
        self.dominio = dominio
        self.cosId = cosId

    def obtener_datos (self, user, dominio):
        # Sacas el contenido a una variable
        # usas el guardar_fichero en run
        # Lo cierto es que no guarda como esperaba
        if len(user)>0:
            exe = Popen(['zmprov', '-l', 'ga', user], stdout=PIPE)
            stdout,stdin = exe.communicate()
            guardar(dominio + ".data", stdout)
            # Todo el script modelado.py se acaba de reducir a esto
            modelo = modelador(stdout.split("\n"), self.cosId)
            modelo.moldear()
            guardar(dominio + ".cmd", modelo.comando)
            guardar(dominio + ".ldif", modelo.volcado)
            guardar(dominio + ".cos", modelo.cosid)

    def run (self):
        self.semaforo.acquire()
        self.obtener_datos(self.user, self.dominio)
        self.semaforo.release()
        print ("Terminado " + self.user + " en " + self.getName())

def borrar_usuarios (lista, dominio):
	a = ['admin','galsync','spam']
	for e in a:
		cuenta = e + "@" + dominio	
		try:
			lista.remove(cuenta)
		except ValueError:
			pass
	
def borrador (listador):
   a = ['spam','ham','quarantine','virus-quarantine','galsync']
   for i in a:
      patron = "^(" + i + ")\..+@(\w+\.*){3}$"
      for j in listador:
         if re.match(patron, j):
            listador.remove(j)
            break

if __name__ == "__main__":
	semaforo = Semaphore(14)
	listador = listar()
	print("""
###############################################################################
Se obtiene la lista de dominios
	""")	
	listador.obtener_dominio()
	print("""
###############################################################################
Se obtiene la lista de usuarios por cada dominio
	""")	
	listador.obtener_listado()
	# Limpiamos el arreglo de dominio
	dominios = [x.rstrip("\n") for x in listador.dominios]
	for dom in dominios:
		# Limpiamos el arreglo de usuarios
		print("""
###############################################################################
Limpiando el arreglo de usuarios
		""")	
		usuarios = [x.rstrip() for x in listador.usuarios[dom]]
		borrar_usuarios(usuarios,dom)
		borrador(usuarios)	
		print("""
###############################################################################
###############################################################################
		""")
	   	for usuario in usuarios:
		# Ejecutado el procedimiento
			saqueador = obtener(semaforo, usuario, dom)
			saqueador.start()

