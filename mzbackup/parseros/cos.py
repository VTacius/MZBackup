from logging import getLogger
from mzbackup.parseros.comun import Parser
from mzbackup.parseros.comun import Recolector

log = getLogger('MZBackup')

atributos = {'posix': ['cn', 'description'],
             'sistema': ['mail', 'zimbraCreateTimestamp', 'zimbraMailDeliveryAddress', 'objectClass',
                         'uid', 'userPassword', 'zimbraId', 'zimbraMailAlias'],
             'procesal': ['zimbraId'],
             'deprecated': [],
             'multilinea': ['zimbraNotes']}


class RecolectorCos(Recolector):
    def _es_primera_linea(self, linea):
        if linea and linea.startswith("# name "):
            return len(linea.split(' ')) == 3 and linea.split(' ')[2].find(' ', 0) == -1

    def _es_ultima_linea(self, linea):
        return linea == ''


class ParserCos(Parser):

    def _titulador(self, linea):
        contenido = linea.split(' ')
        usuario = contenido[2]
        return "zmprov cc {}".format(usuario.strip())
