#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.cosidear import cos
from modulos.utilidades import titulador, situar_directorio
from threading import Semaphore

if __name__ == "__main__":
    # Creo el directorio donde guardo los ficheros
    titulador("Creado el directorio de trabajo")
    situar_directorio("cos")
    # Acción de listado de COS
    titulador("Listamos COS")
    id = cos()
    id.listar_Cos()
    # Definido el número de hilos a usar
    semaforo = Semaphore(4)
    titulador("Empieza los hilos para crear datos")
    for elemento_cos in id.cos:
        ideador = cos(semaforo, elemento_cos)
        ideador.start()
    ideador.join()
    titulador("Almacenamos los CosId")
    id.almacenar_Id()
