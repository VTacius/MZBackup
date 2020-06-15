#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.backupeador import Respaldante, Enviante
from modulos.configuracion import configuracion
from modulos.listado import listar
from modulos.utilidades import abrir_listado, situar_directorio, titulador, situar_remoto

from argparse import ArgumentParser
from Queue import Queue
from shutil import copy
from threading import Semaphore
from os.path import dirname

# Obtenemos valores de configuración para la aplicación desde mzbackup.ini
s_mailbox = int(configuracion("s_mailbox"))
s_envio = int(configuracion("s_envio"))

if __name__ == "__main__":
    # Definimos como argumento -c con fichero
    parser = ArgumentParser(description='Backup de Buzones de correo')
    parser.add_argument('-l', '--listado', help='Fichero dominio.lst dentro de un directorio {{dir-base}}/usuarios-{{fecha}}')
    parser.add_argument('-e', '--envio', action='store_true', help='Envio el fichero de backup al servidor remoto')
    parser.add_argument('-u', '--usuarios', help='Lista de usuarios a los cuales ha de realizarse backup')
    
    # Tomamos el valor de las opciones pasadas al fichero
    args = parser.parse_args()
    listado_dominios = args.listado
    listado_usuarios = args.usuarios
    ejecutar_envio = args.envio
    
    # Me situo en el directorio base de trabajo configurado en mzbackup.ini
    titulador("Empezamos operaciones situándonos en el directorio base")
    situar_directorio("mailbox")
    
    # Creamos directorio remoto donde almacenar los fichero
    if ejecutar_envio:
        titulador("Creamos el directorio remoto para enviar los datos")
        situar_remoto()

    # Sinceramente creo que de otras partes de este proyecto se agradecería tener esta funcionalidad en un métodos exportable
    # Declaramos una matriz que cuyo claves serán dominios y el contenido serán listas de usuarios
    matriz_usuarios = {}
    if listado_usuarios:
        titulador("Obtenemos la lista de usuarios")
        lista_usuarios = abrir_listado(listado_usuarios)
        titulador("Obtenemos backup de cada usuario")
        for correo in lista_usuarios:
            dominio = correo.split('@')[1]
            if not dominio in matriz_usuarios:
                matriz_usuarios[dominio] = []
            matriz_usuarios[dominio].append(correo)
    elif listado_dominios:
        titulador("Obtenemos la lista de dominios")
        lista_dominios = abrir_listado(listado_dominios)
        copy(listado_dominios, '.')
        titulador("Obtenemos la lista de usuarios por cada dominio")
        directorio = dirname(listado_dominios)
        for dominio in lista_dominios:
            lista_usuarios = "{0}/{1}.lst".format(directorio, dominio)
            copy(lista_usuarios, '.')
            matriz_usuarios[dominio] = abrir_listado(lista_usuarios)
    else:
        listador = listar()
        titulador("Obtenemos la lista de dominios")
        listador.listar_dominios().almacenar()
        titulador("Obtenemos la lista de usuarios por cada dominio")
        listador.listar_usuarios().almacenar()
        matriz_usuarios = listador.usuarios

    # Creamos semáforos y colas para usar dentro de las clases multi-threading
    cola = Queue() if ejecutar_envio else None
    # Definido el número de hilos a usar según la configuración de la clave s_mailbox en mzbackup.ini
    semaforo_respaldo = Semaphore(s_mailbox)
    # Definido el número de hilos a usar según la configuración de la clave s_envio en mzbackup.ini
    semaforo_envio = Semaphore(s_envio)

    for dominio, lista_usuarios in matriz_usuarios.iteritems():
        for usuario in lista_usuarios:
            respaldo = Respaldante(semaforo_respaldo, cola, usuario)
            respaldo.start()
            if ejecutar_envio:
                envio = Enviante(semaforo_envio, cola)
                envio.setDaemon(True)
                envio.start()
    respaldo.join()
    if ejecutar_envio:
        cola.join()
