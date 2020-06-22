"""Se ocupa de almacenar cosas, como el almacén"""
from abc import abstractmethod, ABC
from mzbackup.utils.registro import get_logger
from mzbackup.utils.pato import Pato

log = get_logger()


def guardar_contenido(fichero, contenido):
    """Operación sencilla para crear a `fichero` con `contenido`"""
    with open(fichero, 'a') as archivo:
        archivo.write("\n\n")
        archivo.write(contenido)

    return fichero


class AbstractEuropa(ABC):
    """Base abstracta de Europa"""
    def __init__(self, pato: Pato, modificante):
        self.pato = pato
        self.archivos_creados = []
        self.modificante = modificante

    @abstractmethod
    def _guardar_procesal(self, modificante, identificador, contenido):
        """Debe implementarse"""

    def _guardar_multilinea(self, modificante, identificador, contenido):
        """Operación para guadar los comandos que configuran los atributos multilinea"""
        archivos_creados = []
        # Todos acá comparten la misma extension...
        self.pato.extension = "cmd"
        for clave, valor in contenido.items():
            # .. Y su nombre es la clave del item
            self.pato.archivo = clave
            valor = "\\\n".join(valor)
            ingreso = "zmprov {0} {1} {2} {3}".format(modificante, identificador, clave, valor)
            archivos_creados.append(guardar_contenido(str(self.pato), ingreso))
        return archivos_creados

    def guardar(self, identificador, contenido):
        """Guarda el contenido procesado al llegar a la última línea,
        tanto programaticamente en self.agregar(), como imperativamente, en self.ultima_linea()"""
        nombre_original = self.pato.archivo

        if 'multilinea' in contenido:
            corpus = contenido['multilinea']
            creados = self._guardar_multilinea(self.modificante, identificador, corpus)
            self.archivos_creados.extend(creados)

        if 'procesal' in contenido:
            corpus = contenido['procesal']
            self._guardar_procesal(self.modificante, identificador, corpus)

        self.pato.archivo = nombre_original
        self.pato.extension = "cmd"
        self.archivos_creados.append(guardar_contenido(str(self.pato), contenido['comando']))

    def listar_archivos(self):
        """Devuelve todos los ficheros creados durante el uso de la implementacion de Europa"""
        return {*self.archivos_creados}
