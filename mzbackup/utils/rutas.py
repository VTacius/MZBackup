from os.path import isdir
from os.path import basename
from os.path import dirname
from os import mkdir
from os import access
from os import W_OK

from argparse import ArgumentTypeError


def directorio(value):
    if not isdir(value):
        raise ArgumentTypeError('%s no es un directorio' % value)
    if not access(value, W_OK):
        raise ArgumentTypeError('%s no es un directorio accesible para escritura' % value)

    return value


def diseccionar_ruta(ruta):
    fichero = basename(ruta)
    
    directorio = dirname(ruta)
    directorio = directorio if len(directorio) == 0 else directorio + "/"

    sep = fichero.rfind(".")
    sep = len(fichero) if sep == -1 else sep 

    fichero = fichero[:sep]
    return {'directorio':directorio, 'fichero': fichero}


def examinar_directorio(config):
    resultado = ()
    debe_crearse = False
    fichero_origen = getattr(config.fichero, 'name', None) 
    
    if fichero_origen:
        resultado = diseccionar_ruta(fichero_origen)
    else:
        debe_crearse = True
        fichero = getattr(config, 'objeto')
        directorio = getattr(config, 'base')
        resultado = {'directorio': directorio, 'fichero': fichero}
    
    return resultado, debe_crearse


def habilitar_directorio_local(debe_crearse, marca, config):
    resultado = config
    if debe_crearse:
        marca = datetime.now().strftime('%y-%m-%d-%H%M%S')
        directorio = "{}{}-{}".format(config['directorio'], config['fichero'], marca)
        mkdir(directorio, 0o750)
        
        resultado['directorio'] = directorio

    return resultado
