#!/usr/bin/python
# encoding: utf-8
'''
Librería para listado y obtención de datos de los usuarios almacenados en zimbra por medio de ssh
:author: Alexander Ortiz
:version: 1.0
'''

import os
import paramiko
import re
import sys
from modelado import modelador as m
from remoto import remoto
from subprocess import Popen,PIPE,STDOUT
from threading import Thread, Semaphore

class listar (remoto):
    dominios = []
    usuarios = {}
    
    def guardar_fichero (self, archivo, datos):
        fichero = open(archivo, "w")
        fichero.write("\n".join(datos))
        fichero.flush()

    def obtener_dominio (self):
        comando = "su - zimbra -c 'zmprov gad'"
        status, self.dominio = self.ejecutor(comando)
        self.guardar_fichero ("dominios.lst", self.dominio)

    def obtener_listado (self):
        for dominio in self.dominio:
            comando = "su - zimbra -c 'zmprov -l gaa " + dominio + "'"
            status, self.usuarios[dominio] = self.ejecutor(comando)
            self.guardar_fichero (dominio + ".lst", self.usuarios[dominio])

class obtener(remoto, Thread):

    def guardar_fichero (self, archivo, datos):
    	fd = os.open(archivo, os.O_RDWR|os.O_APPEND|os.O_CREAT)
    	os.write(fd, datos)
    	os.close(fd)

    def obtener_datos (self, user, dominio):
        # Sacas el contenido a una variable
        # usas el guardar_fichero en run
        # Lo cierto es que no guarda como esperaba
        if len(user)>0:
            comando = "su - zimbra -c 'zmprov -l ga " + user + "'"
            status, resultado = self.ejecutor(comando)
            datos = "".join(resultado)
            self.guardar_fichero(dominio + ".data", datos)
            # Todo el script modelado.py se acaba de reducir a esto
            modelador = m(resultado)
            modelador.moldear()
            self.guardar_fichero(dominio + ".cmd", modelador.comando)
            self.guardar_fichero(dominio + ".ldif", modelador.volcado)

    def __init__ (self, semaforo, user, dominio):
        remoto.__init__(self)
        Thread.__init__(self)
        self.semaforo = semaforo
        self.user = user
        self.dominio = dominio

    def run (self):
        self.semaforo.acquire()
        self.obtener_datos(self.user, self.dominio)
        self.semaforo.release()
        print ("Terminado " + self.user + " en " + self.getName())

def borrar_usuarios (lista, dominio):
	a = ['admin','galsync','spam', '']
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
    '''
    Esta implementación no esta funcionando por el momento
    Refierase al archivo main.py para ver como trabaja
    '''
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

