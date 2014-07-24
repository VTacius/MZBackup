#!/usr/bin/python
#encoding: utf-8
import listado as l
import os
import time
from threading import Semaphore


def titulador(titulo):
    mensaje = "###############################################################################\n{title}".format
    print mensaje(title=titulo)

if __name__ == "__main__":
    # Creo el directorio donde guardo los ficheros
    dia = time.strftime("%d-%m-%y-%H%M%S")
    directorio = 'backup-' + dia
    os.mkdir(directorio)
    os.chdir(directorio)
    #Procedimientos para modelar datos con 
    # métodos de modelado.py
    # Procedimientos para obtener datos con 
    # métodos de listado.py
    listador = l.listar()
    # Se obtiene la lista de dominios
    titulador("Obtenemos la lista de dominios")
    listador.obtener_dominio()
    # Se obtiene la lista de usuarios por cada dominio
    titulador("Obtenemos la lista de usuarios por cada dominio")
    listador.obtener_listado()
    semaforo = Semaphore(50)
    for dom in listador.dominio:
        # Limpiamos el arreglo de usuarios
        usuarios = [x.rstrip() for x in listador.usuarios[dom]]
        l.borrar_usuarios(usuarios, dom)
        l.borrador(usuarios)	
        for usuario in usuarios:
        # Ejecutado el procedimiento
            saqueador = l.obtener(semaforo, usuario, dom)
            saqueador.start()
