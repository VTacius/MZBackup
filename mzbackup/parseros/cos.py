""" Implementación de Recolector y Parser para objeto COS"""
from logging import getLogger
from json import load, dump
from os import path

from mzbackup.parseros.comun.recolector import Recolector
from mzbackup.parseros.comun.iterador import IteradorFichero
from mzbackup.parseros.comun.helpers import ParserError, _crear_clave_valor
from mzbackup.utils.europa import Europa

log = getLogger('MZBackup')

atributos = {'posix': ['cn', 'description'],
             'sistema': ['mail', 'zimbraCreateTimestamp', 'zimbraMailDeliveryAddress',
                         'objectClass', 'uid', 'userPassword', 'zimbraId', 'zimbraMailAlias'],
             'procesal': ['zimbraId'],
             'modificante': 'mc',
             'deprecated': [],
             'multilinea': ['zimbraNotes']}


class EuropaCos(Europa):
    """Establece métodos de guardado para objeto COS"""

    def _guardar_procesal(self, _modificante, identificador, contenido):
        # Recuerda que cada procesal requeriría una implementación diferente
        # Básicamente, habría un for - if
        if 'zimbraId' in contenido:
            self.pato.extension = "id"
            ruta = str(self.pato)
            esquema = {}
            resultado = {}
            # Parece que se comporta bien, aún cuando el fichero ya existe.
            # No parece haber la necesidad de borrarlo implicitamente
            if path.exists(ruta):
                with open(ruta, 'r') as fichero:
                    esquema = load(fichero)
                    resultado = {**esquema, **contenido['zimbraId']}
            else:
                resultado = {**contenido['zimbraId']}

            with open(ruta, 'w+') as fichero:
                dump(resultado, fichero, indent=4)

            # Recuerda que es posible que más archivos sean creados
            self.archivos_creados.append(ruta)


class IteradorCos(IteradorFichero):
    """Implementa un Iterador para un fichero con contenido de COS"""

    def _linea_inicia_objeto(self, linea):
        if linea and linea.startswith("# name "):
            return len(linea.split(' ')) == 3 and linea.split(' ')[2].find(' ', 0) == -1

        return False


class RecolectorCos(Recolector):
    """Implementa un Parser adecuado para COS"""

    def _titulador(self, linea):
        if linea is None:
            raise ParserError("Revise el formato del fichero con los datos de entrada")

        linea = linea.split(' ')
        identificador = linea[2].strip()
        titulo = "zmprov cc {}".format(identificador)
        self.identificador = identificador
        return titulo

    def _crear_contenido_procesal(self, tokens, linea):
        clave, valor = _crear_clave_valor(tokens, linea)
        # Recuerda que podría haber muchos atributos procesal que requerirían
        # otras tantas implementaciones
        # Por ahora, esta es un poco sencilla:
        # El ID es la nueva clave, el valor nuestro identificador global
        resultado = {valor: self.identificador}
        return clave, resultado
