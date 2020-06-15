from threading import Thread
from queue import Queue
from multiprocessing import Event

from mzbackup.utils.comandos import ejecutor
from random import randint


class Recolector(Thread):

    def __init__(self, cola: Queue):
        Thread.__init__(self)
        print("Me estoy inicializando")
        self.evento = Event()
        self.cola = cola

    def ejecutor(self, contenido):
        aleatorio = randint(1, 4)
        #resultado = ejecutor("sleep " + str(aleatorio))
        resultado = ejecutor("echo nada")
        print("Acabo de terminar")
        print(contenido)

        return resultado

    def run(self):
        while not self.evento.is_set() and not self.cola.empty():
            contenido = self.cola.get()
            self.ejecutor(contenido)
            self.cola.task_done()

    def cerrar(self):
        print("Cerrando estoy")
        self.evento.set()

## De acá, lo que falta es crear otro clase Thread que meta a la cola

if __name__ == "__main__":
    hilos = []
    contenido = Queue()
    trabajadores = []
    
    fichero = open("contenido.cnt")
    for linea in fichero:
        contenido.put(linea)
    
    for hilo in range(4):
        ejecutante = Recolector(contenido)
        ejecutante.setDaemon(True)
        ejecutante.start()
        trabajadores.append(ejecutante)
        hilos.append(hilo)

    for trabajador in trabajadores:
        trabajador.join()
    
    for trabajador in trabajadores:
        trabajador.cerrar()
