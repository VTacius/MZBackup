from os.path import basename
from os.path import dirname
from os.path import split
from os import mkdir


class Pato:

    def __init__(self, objeto, marca, args):
        self.fichero = args['fichero']
        ruta = getattr(args['fichero'], 'name', None)
        self.debe_crearse = ruta is None
        self.marca = marca
        self.objeto = objeto

        # Por venir de Click, podemos asumir que habrá un valor por defecto
        base = args.get('base')

        if self.debe_crearse:
            base, directorio, archivo, extension = self._analizar_ruta_nueva(objeto, marca, base)
        else:
            base, directorio, archivo, extension = self._analizar_ruta_existente(ruta)

        self.base = base
        self.directorio = directorio
        self.archivo = archivo
        self.extension = extension

    def _analizar_ruta_nueva(self, objeto, marca, base):
        directorio = "{}-{}".format(objeto, marca)
        nombre = objeto
        return base, directorio, nombre, ""

    def _analizar_ruta_existente(self, ruta):
        fichero = basename(ruta)

        sep = fichero.rfind(".")

        if sep > 0:
            nombre = fichero[:sep]
            extension = fichero[sep+1:]
        else:
            nombre = fichero
            extension = ""

        base, directorio = split(dirname(ruta))

        return base, directorio, nombre, extension

    def habilitar_directorio_local(self):
        if self.debe_crearse:
            config = self.__dict__()
            directorio = "{}{}".format(config['base'], config['directorio'])
            mkdir(directorio, 0o750)

    def ruta(self):
        config = self.__dict__()
        return "{}{}".format(config['base'], config['directorio'])

    def nombre(self):
        config = self.__dict__()
        return "{}{}".format(config['archivo'], config['extension'])

    def __dict__(self):
        base = self.base + "/" if len(self.base) > 0 else ""
        directorio = self.directorio + "/" if len(self.directorio) > 0 else ""
        archivo = self.archivo if len(self.archivo) > 0 else ""
        extension = "." + self.extension if len(self.extension) > 0 else ""
        return {'base': base, 'directorio': directorio, 'archivo': archivo, 'extension': extension}

    def __str__(self):
        config = self.__dict__()
        return "{}{}{}{}".format(config['base'], config['directorio'], config['archivo'], config['extension'])
