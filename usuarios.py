#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.listado import listar
from modulos.usuareador import obtener
from modulos.utilidades import titulador, situar_directorio, abrir_json, borrar_usuarios, borrar_patrones, situar_remoto, enviante
from modulos.configuracion import configuracion
from threading import Semaphore
import argparse

# Obtenemos valores de configuración para la aplicación desde mzbackup.ini
s_usuarios = int(configuracion("s_usuarios"))

if __name__ == "__main__":
    # Definimos como argumento -c con fichero cos.id
    parser = argparse.ArgumentParser(description='Backup de la definición de usuarios en Zimbra')
    parser.add_argument('-c','--cos', help='Fichero JSON (cos.id)que contiene Cos:CosId',required=True)
    args = parser.parse_args()
    cos_file = args.cos
    cosId = abrir_json(cos_file)

    # Me situo en el directorio base de trabajo configurado en mzbackup.ini
    titulador("Empezamos operaciones situándonos en el directorio base")
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
    
    # Definido el número de hilos a usar según la configuración de la clave s_usuario en mzbackup.ini
    semaforo = Semaphore(s_usuarios)
    titulador("Empieza los hilos para crear datos")
    # Recorremos el listado de dominios que se almacena en el atributo dominios de la clase listar()
    for dom in listador.dominios:
        # Limpiamos el arreglo de usuarios de usuarios de los que no usaremos backup
        borrar_usuarios(listador.usuarios[dom], dom)
        borrar_patrones(listador.usuarios[dom])	
        # Recorremos el diccionario del atributo usuarios, por cada indice dominio devuelve una lista de usuarios
        for usuario in listador.usuarios[dom]:
            # Ejecutado el procedimiento
            saqueador = obtener(semaforo, usuario, dom, cosId)
            saqueador.start()
    saqueador.join()
    
    # Enviamos los ficheros resultantes al servidor remoto
    titulador("Enviamos los ficheros resultantes")
    enviante('*')
