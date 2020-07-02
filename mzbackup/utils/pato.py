"""Clases helpers para manipular rutas"""
from os.path import basename
from os.path import dirname
from os.path import split
from os.path import exists
from os import mkdir


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
        self.directorio = directorio
        self.archivo = archivo
        self.extension = extension

    def __as_dict__(self):
        base = self.base + "/" if len(self.base) > 0 else ""
        directorio = self.directorio + "/" if len(self.directorio) > 0 else ""
        archivo = self.archivo if len(self.archivo) > 0 else ""
        extension = "." + self.extension if len(self.extension) > 0 else ""
        return {'base': base, 'directorio': directorio, 'archivo': archivo, 'extension': extension}

    def __str__(self):
        config = self.__as_dict__()
        return "{}{}{}{}".format(config['base'], config['directorio'],
                                 config['archivo'], config['extension'])

    def ruta(self):
        """Devuelve la ruta a un fichero completa"""
        config = self.__as_dict__()
        return "{}{}".format(config['base'], config['directorio'])

    def nombre(self):
        """Devuelve el nombre del fichero"""
        config = self.__as_dict__()
        return "{}{}".format(config['archivo'], config['extension'])


class PatoRemoto(BasePato):
    """Pese a lo que sugiere su nombre, es una clase base con algunas de las funcionalidades
    base para otras posibles"""

    def __init__(self, objeto, marca, base, servidor_remoto):
        self.servidor_remoto = servidor_remoto
        base, directorio, archivo, extension = _analizar_ruta_nueva(objeto, marca, base)
        BasePato.__init__(self, base, directorio, archivo, extension)


class Pato(BasePato):
    """Establece funcionalidades adicionales para la manipulacion de rutas"""
    def __init__(self, objeto, marca, args):
        self.objeto = objeto
        self.marca = marca
        self.fichero = args['fichero']
        ruta = getattr(args['fichero'], 'name', None)
        self.debe_crearse = ruta is None

        # Por venir de Click, podemos asumir que habrá un valor por defecto
        base = args.get('base')

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
