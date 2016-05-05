#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.cosidear import cos
from modulos.configuracion import configuracion
from modulos.listado import listar
from modulos.utilidades import titulador, situar_directorio, situar_remoto, enviante, almacenar_diccionario
from threading import Semaphore
import argparse

# Obtenemos valores de configuración para la aplicación desde mzbackup.ini
s_cos = int(configuracion("s_cos"))

if __name__ == "__main__":
    # Definimos que el envío sea opcional de ficheros a un lugar remoto sea opcional
    parser = argparse.ArgumentParser(description='Backup de la definición de COS en Zimbra')
    parser.add_argument('-e', '--envio', action='store_true', help='Envio de ficheros .cos al servidor remoto')

    # Tomamos las opciones pasadas al fichero
    args = parser.parse_args()
    ejecutar_envio = args.envio

    # Me situo en el directorio base de trabajo configurado en mzbackup.ini
    titulador("Empezamos operaciones situándonos en el directorio base")
    situar_directorio("cos")

    ##  Creamos directorio remoto donde almacenar los fichero
    if ejecutar_envio:
        titulador("Creamos el directorio remoto para enviar los datos")
        situar_remoto()

    # Acción de listado de COS
    titulador("Listamos COS")
    obtener_cos = listar()
    obtener_cos.listar_cos()

    # Definido el número de hilos a usar
    semaforo = Semaphore(s_cos)
    titulador("Empieza los hilos para crear datos")
    for elemento_cos in obtener_cos.cos:
        ideador = cos(semaforo, elemento_cos)
        ideador.start()
    ideador.join()

    # Guardamos un fichero json con los cos que después hemos de usar con los usuarios
    titulador("Almacenamos los CosId")
    almacenar_diccionario("cos.id", ideador.cosId)

    # Enviamos los ficheros resultantes al servidor remoto
    if ejecutar_envio:
        titulador("Enviamos los ficheros resultantes al servidor remoto")
        enviante('*')
