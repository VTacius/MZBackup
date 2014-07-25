#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.cosidear import cos
from modulos.listado import listar
from modulos.utilidades import titulador, situar_directorio, situar_remoto, enviante, almacenar_diccionario
from threading import Semaphore

if __name__ == "__main__":
    # Creo el directorio donde guardo los ficheros y se muevo a el
    titulador("Creado el directorio de trabajo")
    situar_directorio("cos")
    ##  Creamos directorio remoto donde almacenar los fichero
    titulador("Creamos el directorio remoto para enviar los datos")
    situar_remoto()
    # Acción de listado de COS
    titulador("Listamos COS")
    obtener_cos = listar()
    obtener_cos.listar_Cos()
    # Definido el número de hilos a usar
    semaforo = Semaphore(4)
    titulador("Empieza los hilos para crear datos")
    for elemento_cos in obtener_cos.cos:
        ideador = cos(semaforo, elemento_cos)
        ideador.start()
    ideador.join()
    titulador("Almacenamos los CosId")
    almacenar_diccionario("cos.id", ideador.cosId)
    # Enviamos los ficheros resultantes al servidor remoto
    titulador("Enviamos los ficheros resultantes")
    enviante('*')
