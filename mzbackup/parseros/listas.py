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

    def _titulador(self, contenido):
        # TODO: Si no funciona, podrías tirar una Excepción para contenido inválido
        contenido = contenido.split(' ')
        identificador = contenido[2].strip()
        resultado = "zmprov cdl {0}".format(identificador)
        self.identificador = identificador
        return resultado

    def _crear_contenido_procesal(self, tokens, linea):
        # TODO: Una implementación real podría ser necesaria
        sep = tokens['sep']
        clave = linea[:sep]
        valor = linea[sep + 2:]
        return clave, valor
