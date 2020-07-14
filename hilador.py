from datetime import datetime
from queue import Queue
from mzbackup.utils.pato import PatoFactory
from mzbackup.instrumentos import listar_dominios
from mzbackup.hilos.respaldo import Respaldo

from mzbackup.utils.registro import configurar_log

if __name__ == "__main__":
    # Estos deben recibirse desde Click
    base = "/opt/backup"

    #log = configurar_log(10)
    #log.info("Listando dominios")
    #dominios = listar_dominios()

    # Estas es la operación, por dominio, que ha de realizarse
    timestamp = datetime.now().strftime('%y-%m-%d-%H%M%S')
    pato = PatoFactory.local_de_componentes("backup", timestamp, base)
    pato.extension = "lst"
    
    pato.habilitar_directorio_local()
    
    ## Esto se hace por cada dominio.
    dominio = "salud.gob.sv"
    pato.archivo = dominio
    pato.habilitar_fichero_contenido("zmprov -l gaa {0}".format(dominio))
    fichero_contenido = str(pato)

    # Empezamos con la cuestión multihilo
    cola_envios = Queue()
    cola_usuarios = Queue()
    listado_respaldantes = []
    for hilo in range(4):
        respaldo = Respaldo(pato, cola_usuarios, cola_envios)
        respaldo.setDaemon(True)
        respaldo.start()
        listado_respaldantes.append(respaldo)

    contenido = open(fichero_contenido) 
    for usuario in contenido:
        cola_usuarios.put(usuario.rstrip())

    for respaldante in listado_respaldantes:
        respaldo.join()