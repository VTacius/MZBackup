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
    parser.add_argument('-l','--listado', help='Fichero dominio.lst dentro de un directorio {{dir-base}}/usuarios-{{fecha}}')
    args = parser.parse_args()
    listado_dominios = args.listado
    
    # Se obtiene la lista de dominios
    titulador("Obtenemos la lista de dominios")

    listador = listar()
    if listado_dominios:
        dominios = abrir_listado(listado_dominios) 
    else:
        listador.listar_dominios()
        dominios = listador.dominios

        # Se obtiene la lista de usuarios por cada dominio
        titulador("Obtenemos la lista de usuarios por cada dominio")
        listador.listar_usuarios().almacenar()

    
    print(dominios)

    # Me situo en el directorio base de trabajo configurado en mzbackup.ini
    titulador("Empezamos operaciones situándonos en el directorio base")
    situar_directorio("mailbox")
    
    # Creamos directorio remoto donde almacenar los fichero
    titulador("Creamos el directorio remoto para enviar los datos")
    situar_remoto()
    
    # Definido el número de hilos a usar
    semaforo = Semaphore(s_mailbox)
    # Recorremos el listado de dominios que se almacena en el atributo dominios de la clase listar()
    titulador("Empieza los hilos para crear datos")
    for dominio, lista_usuarios in listador.usuarios.iteritems():
        # Recorremos el diccionario del atributo usuarios, por cada indice dominio devuelve una lista de usuarios
        for usuario in lista_usuarios:
            # Ejecutado el procedimiento
            vaca = backupeador(usuario, semaforo)
            vaca.start()
