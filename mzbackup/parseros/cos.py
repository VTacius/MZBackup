""" Implementación de Recolector y Parser para objeto COS"""
from logging import getLogger
from json import load, dump
from os import path

from mzbackup.parseros.comun import Parser
from mzbackup.parseros.comun import Recolector


log = getLogger('MZBackup')

atributos = {'posix': ['cn', 'description'],
             'sistema': ['mail', 'zimbraCreateTimestamp', 'zimbraMailDeliveryAddress',
                         'objectClass', 'uid', 'userPassword', 'zimbraId', 'zimbraMailAlias'],
             'procesal': ['zimbraId'],
             'modificante': 'mc',
             'deprecated': [],
             'multilinea': ['zimbraNotes']}


class RecolectorCos(Recolector):
    """Implementa un Recolector adecuado para COS"""
    def _es_primera_linea(self, linea):
        if linea and linea.startswith("# name "):
            return len(linea.split(' ')) == 3 and linea.split(' ')[2].find(' ', 0) == -1

        return False

    def _es_ultima_linea(self, linea):
        return linea == ''

    def _guardar_procesal(self, pato, identificador, contenido):
        # Recuerda que cada procesal requeriría una implementación diferente
        # Básicamente, habría un for - if
        archivos_creados = []
        if 'zimbraId' in contenido:
            pato.extension = "id"
            ruta = str(pato)
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
            archivos_creados = [ruta]

        return archivos_creados


class ParserCos(Parser):
    """Implementa un Parser adecuado para COS"""

    def _titulador(self, linea):
        contenido = linea.split(' ')
        identificador = contenido[2].strip()
        self.identificador = identificador
        return "zmprov cc {}".format(identificador)

    def _crear_contenido_procesal(self, tokens, linea):
        sep = tokens['sep']
        clave = linea[:sep]
        valor = linea[sep + 2:]

        # Recuerda que podría haber muchos atributos procesal que requerirían
        # otras tantas implementaciones
        # Por ahora, esta es un poco sencilla:
        # El ID es la nueva clave, el valor nuestro identificador global
        resultado = {valor: self.identificador}
        return clave, resultado
