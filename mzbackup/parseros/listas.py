""" Implementación de Recolector y Parser para objeto LISTAS"""
from logging import getLogger

from mzbackup.parseros.comun import Parser
from mzbackup.parseros.comun import Recolector

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


class RecolectorListas(Recolector):
    """Implementa un Recolector adecuado para LISTA"""
    def _es_primera_linea(self, linea):
        if linea and (linea.startswith("# distributionList") or linea == "members"):
            return len(linea.split(' ')) == 4 and linea.split(' ')[3].find('=') > 0

        return False

    def _es_ultima_linea(self, linea: str):
        return linea == ""

    def _guardar_procesal(self, pato, identificador, contenido):
        # Recordar que pueden haber varios procesales que pueden requerir varias implementaciones
        archivos_creados = []
        if 'zimbraMailForwardingAddress' in contenido:
            valor = contenido['zimbraMailForwardingAddress']
            contenido = "zmprov adlm {} {}".format(identificador, valor)
            pato.archivo = 'zimbraMailForwardingAddress'
            pato.extension = "cmd"
            fichero = open(str(pato), 'a')
            fichero.write(contenido)
            fichero.write("\n\n")
            archivos_creados.append(str(pato))
        return archivos_creados

    def agregar(self, linea):

        self._linea_actual, self._linea_siguiente = self._linea_siguiente, linea.rstrip()

        if self._es_primera_linea(self._linea_actual):
            self.contenido = []
            self.contenido.append(self._linea_actual)
            self.fin_de_contenido = False
        elif self._es_ultima_linea(self._linea_actual) and self._linea_siguiente == "members":
            self.contenido.append(self._linea_actual)
            self.fin_de_contenido = True

            parser = self.parser(self.attrs)
            contenido = parser.procesar(self.contenido)
            identificador = parser.identificador
            self.ficheros.extend(self._guardar(self.config_destino, identificador, contenido))
        else:
            self.fin_de_contenido = False
            self.contenido.append(self._linea_actual)

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
