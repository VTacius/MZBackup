#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.listado import listar
from modulos.usuareador import obtener
from modulos.utilidades import titulador, situar_directorio, abrir_json, situar_remoto, enviante, abrir_listado
from modulos.configuracion import configuracion
from threading import Semaphore
import argparse

# Obtenemos valores de configuración para la aplicación desde mzbackup.ini
s_usuarios = int(configuracion("s_usuarios"))

if __name__ == "__main__":
    # Definimos como argumento -c con fichero cos.id
    parser = argparse.ArgumentParser(description='Backup de la definición de usuarios en Zimbra')
    parser.add_argument('-c','--cos', help='Fichero JSON (cos.id)que contiene Cos:CosId', required=True)
    parser.add_argument('-e', '--envio', help='Envio de ficheros .cos al servidor remoto', action='store_true')
    parser.add_argument('-l', '--listado-usuarios', help='Lista específica de usuarios sobre los cuales realizar backup')
    
    # Tomamos las opciones que fueron pasadas como argumentos al fichero
    args = parser.parse_args()
    cos_file = args.cos
    cosId = abrir_json(cos_file)
    ejecutar_envio = args.envio
    listado_usuarios = args.listado_usuarios

    # Me situo en el directorio base de trabajo configurado en mzbackup.ini
    titulador("Empezamos operaciones situándonos en el directorio base")
    situar_directorio("usuarios")
   
    # Definido el número de hilos a usar según la configuración de la clave s_usuario en mzbackup.ini
    semaforo = Semaphore(s_usuarios)

    '''
    Hacemos backup de definición de datos sobre un listado específico de usuarios
    '''

    if listado_usuarios:
        lista_usuarios = abrir_listado(listado_usuarios)
        for usuario in lista_usuarios:
            dominio = usuario.split('@')[1]
            saqueador = obtener(semaforo, usuario, dominio, cosId)
            saqueador.start()
        saqueador.join()
    else:
        ##  Creamos directorio remoto donde almacenar los fichero
        if ejecutar_envio:
            titulador("Creamos el directorio remoto para enviar los datos")
            situar_remoto()
        
        # Se obtiene la lista de dominios
        titulador("Obtenemos la lista de dominios")
        listador = listar()
        listador.listar_dominios().almacenar()
        
        # Se obtiene la lista de usuarios por cada dominio
        titulador("Obtenemos la lista de usuarios por cada dominio")
        listador.listar_usuarios().almacenar()
        
        # Recorremos el listado de dominios que se almacena en el atributo dominios de la clase listar()
        titulador("Empieza los hilos para crear datos")
        for dominio, lista_usuarios in listador.usuarios.iteritems():
            # Recorremos el diccionario del atributo usuarios, por cada indice dominio devuelve una lista de usuarios
            for usuario in lista_usuarios:
                # Ejecutado el procedimiento
                saqueador = obtener(semaforo, usuario, dominio, cosId)
                saqueador.start()
        saqueador.join()
    
    # El envío de ficheros es independiente de si el listado origen es un fichero 
    # o creado en tiempo de ejecución
    # Enviamos los ficheros resultantes al servidor remoto
    if ejecutar_envio:
        titulador("Enviamos los ficheros resultantes")
        enviante('*')
