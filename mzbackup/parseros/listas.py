""" Implementación de Recolector y Parser para objeto LISTAS"""
from logging import getLogger

from mzbackup.parseros.comun.recolector import Recolector
from mzbackup.parseros.comun.iterador import IteradorFichero
from mzbackup.utils.europa import Europa, guardar_contenido
from mzbackup.parseros.comun.helpers import _crear_clave_valor

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


class EuropaLista(Europa):
    """Implementación de las funcionalidades de guardado para objeto LISTA"""

    def _guardar_procesal(self, _modificante, identificador, contenido):
        # Recordar que pueden haber varios procesales que pueden requerir varias implementaciones
        if 'zimbraMailForwardingAddress' in contenido:
            self.pato.archivo = 'zimbraMailForwardingAddress'
            self.pato.extension = "cmd"
            valor = contenido['zimbraMailForwardingAddress']
            contenido = "zmprov adl {} {}".format(identificador, valor)
            archivo = guardar_contenido(str(self.pato), contenido)
            self.archivos_creados.append(archivo)


class IteradorListas(IteradorFichero):
    """Implementa un Iterador para un fichero con contenido de LISTAS"""

    def _linea_inicia_objeto(self, linea):
        if linea and linea.startswith("# distributionList"):
            return len(linea.split(' ')) == 4 and linea.split(' ')[3].find('=') > 0

        return False

    def _describe_final_objeto(self):
        linea_actual_vacia = self.linea_actual == ""
        linea_siguiente_members = self.linea_siguiente == "members"
        return linea_actual_vacia and linea_siguiente_members


class RecolectorListas(Recolector):
    """Implementa un Recolector adecuado para LISTA"""

    def _titulador(self, linea):
        linea = linea.split(' ')
        identificador = linea[2].strip()
        titulo = "zmprov cdl {0}".format(identificador)
        self.identificador = identificador
        return titulo

    def _crear_contenido_procesal(self, tokens, linea):
        return _crear_clave_valor(tokens, linea)
