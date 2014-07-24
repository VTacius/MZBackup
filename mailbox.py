#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from threading import Semaphore
from modulos.backupeador import backupeador
from modulos.listado import listar, borrar_usuarios, borrador
from modulos.utilidades import situar_directorio, titulador


if __name__ == "__main__":
    # Creo el directorio donde guardo los ficheros de prueba
    situar_directorio("mailbox")
    #Procedimientos para modelar datos con 
    # métodos de modelado.py
    # Procedimientos para obtener datos con 
    # métodos de listado.py
    listador = listar()
    # Se obtiene la lista de dominios
    titulador("Obtenemos la lista de dominios")
    listador.obtener_dominio()
    # Se obtiene la lista de usuarios por cada dominio
    titulador("Obtenemos la lista de usuarios por cada dominio")
    listador.obtener_listado()
    dir = backupeador()
    dir.directorio_remoto()
    semaforo = Semaphore(28)
    titulador("Obtenemos el buzón de cada usuario")
    for dom in listador.dominios:
        # Limpiamos el arreglo de usuarios
        usuarios = [x.rstrip() for x in listador.usuarios[dom] if len(x) > 0]
        borrar_usuarios(usuarios, dom)
        borrador(usuarios)
        for usuario in usuarios:
        # Ejecutado el procedimiento
            vaca = backupeador(semaforo)
            vaca.usuario = usuario
            vaca.start()
