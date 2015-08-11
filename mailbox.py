#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.backupeador import backupeador
from modulos.listado import listar
from modulos.utilidades import situar_directorio, titulador, borrar_usuarios, borrar_patrones, ejecutar_comando, situar_remoto
from threading import Semaphore
import os

if __name__ == "__main__":
    # Creo el directorio donde guardo los ficheros y se muevo a el
    titulador("Creado el directorio de trabajo")
    situar_directorio("mailbox")
    
    # Creamos directorio remoto donde almacenar los fichero
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
    semaforo = Semaphore(28)
    titulador("Empieza los hilos para crear datos")
    for dom in listador.dominios:
        # Limpiamos el arreglo de usuarios
        borrar_usuarios(listador.usuarios[dom], dom)
        borrar_patrones(listador.usuarios[dom])
        for usuario in listador.usuarios[dom]:
        # Ejecutado el procedimiento
            vaca = backupeador(usuario, semaforo)
            vaca.start()
