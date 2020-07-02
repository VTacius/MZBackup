"""Ejecución de comandos en el sistema"""
from subprocess import Popen, PIPE
from shlex import split


class SistemLocalError(Exception):
    """Error personalizado"""


def _ejecutar(comando, guardar):
    error = None
    with Popen(comando, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=False) as cursor:
        for linea in cursor.stdout:
            guardar(linea)

        error = cursor.stderr.readlines()

    if cursor.returncode != 0:
        error = "".join(error).rstrip()

    return error


class EjecutorLocal:
    """Ejecuta un comando en el sistema"""

    def __init__(self, comando):
        self.comando = split(comando)

    def obtener_resultado(self):
        """Obtiene una lista de str con el resultado del comando"""
        salida = []
        guardar = salida.append

        error = None
        try:
            error = _ejecutar(self.comando, guardar)
        except FileNotFoundError:
            error = "Comando no encontrado"

        if error:
            raise SistemLocalError(error)

        return salida

    def guardar_resultado(self, ruta_fichero_salida):
        """Devuelve un fichero, abierto, con el resultado del comando"""
        salida = open(str(ruta_fichero_salida), 'w+')
        guardar = salida.write

        error = None
        try:
            error = _ejecutar(self.comando, guardar)
        except FileNotFoundError:
            error = "Comando no encontrado"

        salida.close()
        if error:
            raise SistemLocalError(error)

        return open(str(ruta_fichero_salida))
