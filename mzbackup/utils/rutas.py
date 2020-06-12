from os.path import isdir
from os.path import basename
from os.path import dirname
from os import mkdir



def diseccionar_ruta(ruta):
    fichero = basename(ruta)
    
    directorio = dirname(ruta)
    directorio = directorio if len(directorio) == 0 else directorio + "/"

    sep = fichero.rfind(".")
    sep = len(fichero) if sep == -1 else sep 

    fichero = fichero[:sep]
    return {'directorio':directorio, 'fichero': fichero}


def examinar_directorio(objeto, config):
    """Si las opciones del cli dan un fichero válido, no será necesario crear el fichero"""
    
    resultado = ()
    fichero_origen = getattr(config['fichero'], 'name', None) 
    debe_crearse = fichero_origen == None
    
    if not debe_crearse:
        resultado = diseccionar_ruta(fichero_origen)
    else:
        # Espera que el objeto config tenga una base por defecto
        directorio = config.get('base')
        resultado = {'directorio': directorio, 'fichero': objeto}
    
    return resultado, debe_crearse


def habilitar_directorio_local(debe_crearse, marca, config):
    resultado = config
    print(config)
    if debe_crearse:
        directorio = "{}/{}-{}".format(config['directorio'], config['fichero'], marca)
        mkdir(directorio, 0o750)
        
        resultado['directorio'] = directorio

    return resultado
