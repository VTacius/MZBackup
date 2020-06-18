"""Ejecución de comandos en el sistema"""
from subprocess import Popen, PIPE
from shlex import split


def _ejecutar(comando, guardar):
    error = None
    with Popen(comando, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=False) as cursor:
        for linea in cursor.stdout:
            guardar(linea)

        error = cursor.stderr.readlines()

    if cursor.returncode != 0:
        error = "".join(error).rstrip()

    return error


def ejecutor(comando, salida=None):
    """Prepara el objeto de salida de un comando"""
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
    except Exception as misktake:
        error = misktake

    if not es_contenido:
        salida.close()
        salida = []

    return salida, error
