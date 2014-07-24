#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.ldistribuidor import distribucion
from modulos.utilidades import situar_directorio, titulador
from threading import Semaphore

if __name__ == "__main__":
    # Creo el directorio donde guardo los ficheros
    titulador("Creado el directorio de trabajo")
    situar_directorio("listas")
    # Acción de listado de listas de distribucion
    titulador("Listamos listas de distribución")
    listar = distribucion()
    listar.listar_listas()
    # Definido el número de hilos a usar
    semaforo = Semaphore(14)
    titulador("Empieza los hilos para crear datos")
    for lista in listar.listado:
        ld = distribucion(semaforo, lista)
        ld.start()
