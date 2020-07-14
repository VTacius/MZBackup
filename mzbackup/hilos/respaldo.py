"""Worker para crear el respaldo del buzón para cada usuario"""

from queue import Queue
from threading import Thread

from mzbackup.utils.pato import PatoLocal
from mzbackup.utils.registro import get_logger
from mzbackup.utils.comandos import EjecutorLocal

log = get_logger()

class Respaldo(Thread):
    """Crea el respaldo para cada usuario en cola"""

    def __init__(self, pato: PatoLocal, cola: Queue, cola_envio: Queue):
        Thread.__init__(self)
        pato.extension = "tgz"
        self.pato = pato
        self.cola = cola
        self.cola_envio = cola_envio

    def run(self):
        """Código a ejecutar"""
        while True:
            usuario = self.cola.get()
            self.pato.archivo = usuario.replace('@', 'AT')

            log.debug("Creando backup para %s" % (usuario))
            comando = "zmmailbox -z -m {0} getRestURL -o {1} '/?fmt=tgz'".format(usuario, self.pato)
            log.trace("Creando fichero %s para %s en %s" % (self.pato, usuario, self.getName()))
            print(comando)
            ejecutor = EjecutorLocal(comando)
            salida = ejecutor.obtener_resultado()
            if self.cola_envio:
                self.cola_envio.put(str(self.pato))

            self.cola.task_done()
