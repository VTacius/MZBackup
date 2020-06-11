from subprocess import Popen, PIPE, STDOUT
from shlex import split
from time import sleep
from io import TextIOWrapper


def _ejecutar(comando, guardar):
    error = None
    with Popen(comando, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=False) as cursor:
        for linea in cursor.stdout:
            guardar(linea)

        error = cursor.stderr.readlines()

    if cursor.returncode != 0:
       error = "".join(error).rstrip()

    return error


def ejecutor(comando, salida = None):
    agregar = object()
    es_contenido = False 

    if salida is None:
        salida = []
        agregar = salida.append
        es_contenido = True
    elif isinstance(salida, str):
        salida = open(salida, 'w+')
        agregar = salida.write
    else:
        raise TypeError('Debe ser una cadena que especifique el nombre de fichero')

    try:
        error = _ejecutar(split(comando), agregar)
    except Exception as e:
        error = e

    if not es_contenido:
        salida.close()
        salida = []
    
    return salida, error
