from queue import Queue
from threading import Thread

from mzbackup.utils.comandos import ejecutor
from mzbackup.hilos.respaldo import Respaldo
from mzbackup.utils.registro import configurar_log

## De acá, lo que falta es crear otro clase Thread que meta a la cola

if __name__ == "__main__":
    verbosidad = 4
    max_hilos_respaldo = 5
    dominio = "salud.gob.sv"
    pato = "/opt/backup"
    
    log = configurar_log(verbosidad=verbosidad)
    listado_usuarios = Queue()
    trabajadores = []
   
    contenido, error = ejecutor("zmprov -l gaa {}".format(dominio))
    for usuario in contenido:
       listado_usuarios.put(usuario.strip())

    for hilo in range(4):
        ejecutante = Respaldo(pato, listado_usuarios, None)
        #ejecutante.setDaemon(True)
        ejecutante.start()
        trabajadores.append(ejecutante)

    for trabajador in trabajadores:
        trabajador.join()
