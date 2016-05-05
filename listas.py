#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.ldistribuidor import distribucion
from modulos.utilidades import situar_directorio, titulador, enviante
from modulos.configuracion import configuracion
from threading import Semaphore
from modulos.configuracion import configuracion
import argparse

s_listas = int(configuracion("s_listas"))

if __name__ == "__main__":
    # Definimos que el envío sea opcional de ficheros a un lugar remoto sea opcional
    parser = argparse.ArgumentParser(description='Backup de la definición de Listas de Distribución  en Zimbra')
    parser.add_argument('-e', '--envio', action='store_true', help='Envio de ficheros .cos al servidor remoto')

    # Tomamos las opciones pasadas al fichero
    args = parser.parse_args()
    ejecutar_envio = args.envio
    
    # Creo el directorio donde guardo los ficheros
    titulador("Empezamos operaciones situándonos en el directorio base")
    situar_directorio("listas")
    
    ##  Creamos directorio remoto donde almacenar los fichero
    if ejecutar_envio:
        titulador("Creamos el directorio remoto para enviar los datos")
        situar_remoto()
    
    # Acción de listado de listas de distribucion
    titulador("Listamos listas de distribución")
    listar = distribucion()
    listar.listar_listas()
    
    # Definido el número de hilos a usar
    semaforo = Semaphore(s_listas)
    titulador("Empieza los hilos para crear datos")
    for lista in listar.listado:
        ld = distribucion(semaforo, lista)
        ld.start()
    ld.join()
    
    # Enviamos los ficheros resultantes al servidor remoto
    if ejecutar_envio:
        titulador("Enviamos los ficheros resultantes")
        enviante('*')
