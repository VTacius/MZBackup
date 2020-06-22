""" Implementación de Recolector y Parser para objeto LISTAS"""
from logging import getLogger

from mzbackup.parseros.parser import Parser
from mzbackup.parseros.recolector import Recolector
from mzbackup.utils.europa import AbstractEuropa

log = getLogger('MZBackup')

# REVISAR: ¿zimbraMailHost como deprecated?
atributos = {
    'posix': ['cn', 'description', 'displayName'],
    'sistema': ['uid', 'objectClass', 'mail',
                'zimbraCreateTimestamp', 'zimbraId', 'zimbraMailAlias'],
    'procesal': ['zimbraMailForwardingAddress'],
    'modificante': 'mdl',
    'deprecated': ['zimbraMailHost'],
    'multilinea': ['zimbraNotes']
}

class EuropaLista(AbstractEuropa):
    """Implementación de las funcionalidades de guardado para objeto LISTA"""
    def _guardar_procesal(self, _modificante, identificador, contenido):
        # Recordar que pueden haber varios procesales que pueden requerir varias implementaciones
        if 'zimbraMailForwardingAddress' in contenido:
            valor = contenido['zimbraMailForwardingAddress']
            contenido = "zmprov adl {} {}".format(identificador, valor)
            self.pato.archivo = 'zimbraMailForwardingAddress'
            self.pato.extension = "cmd"
            fichero = open(str(self.pato), 'a')
            fichero.write(contenido)
            fichero.write("\n\n")
            self.archivos_creados.append(str(self.pato))


class RecolectorListas(Recolector):
    """Implementa un Recolector adecuado para LISTA"""
    def _es_primera_linea(self, linea):
        if linea and (linea.startswith("# distributionList") or linea == "members"):
            return len(linea.split(' ')) == 4 and linea.split(' ')[3].find('=') > 0

        return False

    def _es_final_de_contenido(self, linea: str):
        return linea == ""

    def _es_ultima_linea(self, linea_actual, linea_siguiente):
        """Esta implementación es útil para COS y Usuarios"""
        es_ultima_linea = self._es_final_de_contenido(linea_actual)
        es_linea_members = linea_siguiente == "members"
        return es_ultima_linea and es_linea_members


class ParserLista(Parser):
    """Implementa un Parser adecuado para LISTA"""

    def _titulador(self, linea):
        linea = linea.split(' ')
        identificador = linea[2].strip()
        titulo = "zmprov cdl {0}".format(identificador)
        self.identificador = identificador
        return titulo
