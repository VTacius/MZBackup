#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.backupeador import backupeador
from modulos.configuracion import configuracion
from modulos.listado import listar
from modulos.utilidades import abrir_listado, situar_directorio, titulador, borrar_usuarios, borrar_patrones, ejecutar_comando, situar_remoto
from threading import Semaphore
import argparse
import os, sys

# Obtenemos valores de configuración para la aplicación desde mzbackup.ini
s_mailbox = int(configuracion("s_mailbox"))

if __name__ == "__main__":
    # Definimos como argumento -c con fichero cos.id
    parser = argparse.ArgumentParser(description='Backup de Buzones de correo')
    parser.add_argument('-l','--listado', help='Fichero dominio.lst dentro de un directorio {{dir-base}}/usuarios-{{fecha}}',required=True)
    args = parser.parse_args()
    listado_dominios = args.listado
    
    dominios = abrir_listado(listado_dominios)
    print(dominios)

    # Me situo en el directorio base de trabajo configurado en mzbackup.ini
    titulador("Empezamos operaciones situándonos en el directorio base")
    situar_directorio("mailbox")
    
    # Creamos directorio remoto donde almacenar los fichero
    titulador("Creamos el directorio remoto para enviar los datos")
    situar_remoto()
    
    # Se obtiene la lista de dominios
    titulador("Obtenemos la lista de dominios")
    listador = listar()
    listador.obtener_dominio()

    print(listador.dominios)
    
    # Se obtiene la lista de usuarios por cada dominio
    titulador("Obtenemos la lista de usuarios por cada dominio")
    listador.obtener_listado()

    sys.exit() 
    # Definido el número de hilos a usar
    semaforo = Semaphore(s_mailbox)
    titulador("Empieza los hilos para crear datos")
    for dom in listador.dominios:
        # Limpiamos el arreglo de usuarios
        borrar_usuarios(listador.usuarios[dom], dom)
        borrar_patrones(listador.usuarios[dom])
        for usuario in listador.usuarios[dom]:
        # Ejecutado el procedimiento
            vaca = backupeador(usuario, semaforo)
            vaca.start()
