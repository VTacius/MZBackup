#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab

from modulos.cosidear import cos
from modulos.utilidades import titulador, situar_directorio
from threading import Semaphore

if __name__ == "__main__":
    situar_directorio("cos")
    id = cos()
    titulador("Listamos COS")
    id.listar_Cos()
    semaforo = Semaphore(4)
    for elemento_cos in id.cos:
        ideador = cos(semaforo, elemento_cos)
        ideador.start()
    ideador.join()
    print ("Todos han terminado")
    titulador("Almacenamos los CosId")
    id.almacenar_Id()
