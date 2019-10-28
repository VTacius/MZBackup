from string import ascii_lowercase
from logging import getLogger
from MZBackup.parseros.comun import Parser
from MZBackup.parseros.comun import Recolector

log = getLogger('MZBackup')

# TODO: ¿zimbraMailHost como deprecated?
atributos = {
    'posix': ['cn', 'description', 'displayName'],
    'sistema': ['uid', 'objectClass', 'mail', 'zimbraCreateTimestamp', 'zimbraId', 'zimbraMailAlias'],
    'procesal': ['zimbraMailForwardingAddress'],
    'deprecated': ['zimbraMailHost'],
    'multilinea': ['zimbraNotes']
}


class RecolectorListas(Recolector):

    def _es_primera_linea(self, linea):
        if linea and linea.startswith("# distributionList"):
            return len(linea.split(' ')) == 4 and linea.split(' ')[3].find('=') > 0

        return False

    def _es_ultima_linea(self, linea: str):
        if linea and linea.startswith(tuple(ascii_lowercase)):
            if linea.find(" ") == -1 and (linea.find('@') > 0 or linea == "members"):
                return True

        return False


class ParserLista(Parser):

    def _titulador(self, contenido):
        # TODO: Si no funciona, podrías tirar una Excepción para contenido inválido
        contenido = contenido.split(" ")
        resultado = f"zmprov gdl {contenido[2]}"
        return resultado
