#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.listado import listar
from modulos.usuareador import obtener
from modulos.utilidades import titulador, situar_directorio, abrir_json, borrar_usuarios, borrar_patrones, situar_remoto, enviante
from threading import Semaphore
import argparse

if __name__ == "__main__":
    # Definimos como argumento -c con fichero cos.id
    parser = argparse.ArgumentParser(description='Backup de la definición de usuarios en Zimbra')
    parser.add_argument('-c','--cos', help='Fichero JSON (cos.id)que contiene Cos:CosId',required=True)
    args = parser.parse_args()
    cos_file = args.cos
    cosId = abrir_json(cos_file)
    # Creo el directorio donde guardo los ficheros
    titulador("Creado el directorio de trabajo")
    situar_directorio("usuarios")
    ##  Creamos directorio remoto donde almacenar los fichero
    titulador("Creamos el directorio remoto para enviar los datos")
    situar_remoto()
    # Se obtiene la lista de dominios
    titulador("Obtenemos la lista de dominios")
    listador = listar()
    listador.obtener_dominio()
    # Se obtiene la lista de usuarios por cada dominio
    titulador("Obtenemos la lista de usuarios por cada dominio")
    listador.obtener_listado()
    # Definido el número de hilos a usar
    semaforo = Semaphore(35)
    titulador("Empieza los hilos para crear datos")
    for dom in listador.dominios:
        # Limpiamos el arreglo de usuarios
        borrar_usuarios(listador.usuarios[dom], dom)
        borrar_patrones(listador.usuarios[dom])	
        for usuario in listador.usuarios[dom]:
            # Ejecutado el procedimiento
            saqueador = obtener(semaforo, usuario, dom, cosId)
            saqueador.start()
    saqueador.join()
    titulador("Enviamos los ficheros resultantes")
    enviante('*')
