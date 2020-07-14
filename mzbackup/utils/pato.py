"""Clases helpers para manipular rutas"""
from os.path import basename
from os.path import dirname
from os.path import split
from os.path import exists
from os import mkdir

from mzbackup.utils.comandos import EjecutorLocal
from mzbackup.utils.registro import get_logger
log = get_logger()


def _analizar_ruta_nueva(objeto, marca, base):
    directorio = "{}-{}".format(objeto, marca)
    nombre = objeto
    return base, directorio, nombre, ""


def _analizar_ruta_existente(ruta):
    fichero = basename(ruta)

    sep = fichero.rfind(".")

    nombre = fichero if sep < 0 else fichero[:sep]
    extension = "" if sep < 0 else fichero[sep+1:]

    base, directorio = split(dirname(ruta))

    return base, directorio, nombre, extension


class BasePato:
    """Establece los atributos bases y sus representaciones"""
    def __init__(self, base, directorio, archivo, extension):
        self.base = base
        self._directorio = directorio
        self._archivo = archivo
        self._extension = extension

    @property
    def extension(self):
        """La extensión que ha de tener el archivo"""
        if len(self._extension) > 0:
            return "." + self._extension
        return ""

    @extension.setter
    def extension(self, extension):
        self._extension = extension

    @property
    def archivo(self):
        """El nombre del archivo"""
        if len(self._archivo) > 0:
            return self._archivo
        return ""

    @archivo.setter
    def archivo(self, archivo):
        self._archivo = archivo

    @property
    def directorio(self):
        """El directorio según tipo y fecha"""
        if len(self._directorio) > 0:
            return self._directorio.rstrip("/") + "/"
        return ""

    @directorio.setter
    def directorio(self, directorio):
        self._directorio = directorio

    @property
    def base(self):
        """El directorio base sobre el que se construyen los directorios por tipo y fecha"""
        if len(self._base) > 0:
            return self._base.rstrip("/") + "/"
        return ""

    @base.setter
    def base(self, base):
        self._base = base

    def __as_dict__(self):
        return {'base': self.base, 'directorio': self.directorio,
                'archivo': self.archivo, 'extension': self.extension}

    def __str__(self):
        config = self.__as_dict__()
        return "{}{}{}{}".format(config['base'], config['directorio'],
                                 config['archivo'], config['extension'])

    def ruta(self):
        """Devuelve la ruta a un fichero completa"""
        return "{}{}".format(self.base, self.directorio)

    def nombre(self):
        """Devuelve el nombre del fichero"""
        return "{}{}".format(self.archivo, self.extension)


class PatoRemoto(BasePato):
    """Pese a lo que sugiere su nombre, es una clase base con algunas de las funcionalidades
    base para otras posibles"""

    def __init__(self, pato_local, servidor_remoto):
        self.servidor_remoto = servidor_remoto
        base, directorio, archivo, extension = _analizar_ruta_existente(str(pato_local))
        BasePato.__init__(self, base, directorio, archivo, extension)


class Pato(BasePato):
    """Establece funcionalidades adicionales para la manipulacion de rutas"""
    def __init__(self, objeto, marca, fichero, base):
        ruta = getattr(fichero, 'name', None)
        self.fichero = fichero
        self.debe_crearse = ruta is None

        if self.debe_crearse:
            base, directorio, archivo, extension = _analizar_ruta_nueva(objeto, marca, base)
        else:
            base, directorio, archivo, extension = _analizar_ruta_existente(ruta)

        BasePato.__init__(self, base, directorio, archivo, extension)

    def habilitar_directorio_local(self):
        """Crea de ser necesario el directorio `base` para nuestro archivo"""
        config = self.__as_dict__()
        directorio = "{}{}".format(config['base'], config['directorio'])
        # Es que a veces, podríamos trabajar sobre un mismo directorio
        if not exists(directorio):
            mkdir(directorio, 0o750)

    def habilitar_fichero_contenido(self, comando):
        """Crear el fichero con contenido proveniente de un comando, si es que no existe"""
        self.extension = "data"
        log.debug("> Creando el fichero de datos %s", self.__str__())

        if self.debe_crearse:
            ejecutor_local = EjecutorLocal(comando)
            self.fichero = ejecutor_local.guardar_resultado(self.__str__())


class PatoFactory:
    """Helper para crear la clase Pato"""

    @classmethod
    def remoto_de_local(cls, pato_local, servidor_remoto):
        """Crea un PatoRemoto a partir de los datos de PatoLocal"""
        return PatoRemoto(pato_local, servidor_remoto)
