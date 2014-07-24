#!/usr/bin/python
#encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Obtiene listado de usuarios y funciones útiles relacionadas
'''
__author__ = "Alexander Ortiz"
__version__ = "0.8"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

from threading import Thread, Semaphore
from utilidades import guardar, ejecutar_comando

class listar ():
    dominios = ()
    usuarios = {}
	
    def obtener_dominio (self):
        comando = [ 'zmprov', 'gad' ]
        self.dominios = ejecutar_comando(comando)
        guardar("dominios.lst", self.dominios, "l")

    def obtener_listado (self):
        for dominio in self.dominios:
            comando = ['zmprov', '-l', 'gaa', dominio]
            self.usuarios[dominio] = ejecutar_comando(comando)
            guardar(dominio + ".lst", self.usuarios[dominio], "l")

if __name__ == "__main__":
    '''
    Probablemente esta implementación no sirve
    Y sería muy buena idea que la arreglaras
    '''
    semaforo = Semaphore(14)
    listador = listar()
    print("Se obtiene la lista de dominios")	
    listador.obtener_dominio()
    print("Se obtiene la lista de usuarios por cada dominio")	
    listador.obtener_listado()
    # Limpiamos el arreglo de dominio
    dominios = [x.rstrip("\n") for x in listador.dominios]
    for dom in dominios:
        # Limpiamos el arreglo de usuarios
        print("Limpiando el arreglo de usuarios")	
        usuarios = [x.rstrip() for x in listador.usuarios[dom]]
        borrar_usuarios(usuarios,dom)
        borrador(usuarios)	
        print("###############################################################################")
        for usuario in usuarios:
        # Ejecutado el procedimiento
            saqueador = obtener(semaforo, usuario, dom)
            saqueador.start()

