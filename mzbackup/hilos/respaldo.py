"""Worker para crear el respaldo del buzón para cada usuario"""

from queue import Queue
from threading import Thread
from logging import getLogger

from mzbackup.utils.comandos import ejecutor

log = getLogger('MZBackup')


class Respaldo(Thread):
    """Crea el respaldo para cada usuario en cola"""

    def __init__(self, pato, cola: Queue, cola_envio: Queue):
        Thread.__init__(self)
        self.pato = pato
        self.cola = cola
        self.cola_envio = cola_envio

    def run(self):
        """Código a ejecutar"""
        while True:
            usuario = self.cola.get()
            log.debug("Creando backup para %s" % usuario)
            archivo = "{0}/{1}.tgz".format(self.pato, usuario.replace("@", "AT"))
            comando = "zmmailbox -z -m {0} getRestURL -o {1} '/?fmt=tgz'".format(usuario, archivo)
            log.trace("Creando fichero %s para %s en %s" % (archivo, usuario, self.getName()))
            salida, error = ejecutor(comando)
            if self.cola_envio and error is None:
                self.cola_envio.put(archivo)

            self.cola.task_done()
