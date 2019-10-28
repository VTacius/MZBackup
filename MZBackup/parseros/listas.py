from string import ascii_lowercase
from logging import getLogger

atributosListas = {
    'posix': ['cn', 'description', 'displayName'],
    'sistema': ['uid', 'objectClass', 'mail', 'zimbraCreateTimestamp', 'zimbraId'],
    'procesal': ['zimbraMailForwardingAddress'],
    'deprecated': [],
    'multilinea': ['zimbraNotes']
}

log = getLogger('MZBackup')


class RecolectorListas:

    def __init__(self, parser, attrs):
        self.__linea_actual = None
        self.__linea_siguiente = None

        self.contenido = []
        self.fin_de_contenido = False

        self.parser = parser
        self.attrs = attrs

    def _es_primera_linea(self, linea):
        if linea and linea.find("# distributionList", 0) == -1:
            return False
        # TODO: Esta comprobación podría ser más sencilla
        try:
            contenido = linea.split(" ")
            return contenido[3].find("=") > 0
        except IndexError:
            return False
        except AttributeError:
            return False

    def _es_ultima_linea(self, linea: str):
        if linea and linea.startswith(tuple(ascii_lowercase)):
            if linea.find(" ") == -1 and (linea.find('@') > 0 or linea == "members"):
                return True

        return False

    def ultima_linea(self):
        self.contenido.append(self.__linea_actual)
        self.fin_de_contenido = True
        parser = self.parser(self.contenido, self.attrs)
        parser.procesar()
        print(parser.guardar())

    def agregar(self, linea: str):

        self.__linea_actual, self.__linea_siguiente = self.__linea_siguiente, linea.rstrip()

        if self._es_primera_linea(self.__linea_actual):
            self.contenido = []
            self.contenido.append(self.__linea_actual)
            self.fin_de_contenido = False
        elif self._es_ultima_linea(self.__linea_actual) and self._es_primera_linea(self.__linea_siguiente):
            self.contenido.append(self.__linea_actual)
            self.fin_de_contenido = True

            parser = self.parser(self.contenido, self.attrs)
            parser.procesar()
            print(parser.guardar())
        else:
            self.contenido.append(self.__linea_actual)


class ParserLista:

    def __init__(self, contenido, attr):
        self.contenido = contenido
        self.resultado = ""
        self.attr = attr

        self.atributos_zimbra_invalidos = attr['sistema'] + attr['procesal'] + attr['deprecated'] + attr['multilinea']

        self.actual_atributo_multilinea = ""
        self.recolectando_multilinea = False
        self.contenido_multilinea = {}

    def _titulador(self, contenido):
        # TODO: Si no funciona, podrías tirar una Excepción para contenido inválido
        contenido = contenido.split(" ")
        resultado = f"zmprov gdl {contenido[2]}"
        return resultado

    def _valuar(self, valor):
        # TODO: ¿Habrá que considerar escapar los '' en el valor original
        valores_no_alpha = sum([1 for x in [c for c in valor] if x not in tuple(ascii_lowercase)])
        return valor if valores_no_alpha == 0 else f"'{valor}'"

    def _es_contenido_valido(self, linea):
        sep = linea.find(":", 0)
        # TODO: Deberías reconsiderar una reescritura de esto
        if sep > 0:
            atributo = linea[:sep]
            es_posix = atributo in self.attr['posix'] and atributo not in self.attr['sistema']
            parece_zimbra = atributo.find('zimbra', 0) > 0
            zimbra_valido = atributo not in self.atributos_zimbra_invalidos
            return es_posix or (parece_zimbra and zimbra_valido)
        else:
            return False

    def _es_multilinea(self, linea):
        sep = linea.find(":", 0)
        # TODO: Esto esta sujeto para una rescritura también
        if sep > 0:
            atributo = linea[:sep]
            return atributo in self.attr['multilinea']
        else:
            return False

    def _es_procesal(self, linea):
        sep = linea.find(":", 0)
        # TODO: Esto esta sujeto para una rescritura también
        if sep > 0:
            atributo = linea[:sep]
            return atributo in self.attr['procesal']
        else:
            return False

    def _agregar_a_contenido(self, linea: str):
        if self.recolectando_multilinea:
            if self._es_contenido_valido(linea):
                log.debug('> Contenido Normal (DM): ' + linea)
                clave, valor = linea.split(":")[:2]
                procesal = f" {clave} {self._valuar(valor.strip())}"
                self.resultado += procesal
                self.recolectando_multilinea = False
            elif self._es_procesal(linea):
                log.debug('> Procesal: (DM)' + linea)
                self.recolectando_multilinea = False
            elif linea.strip() == "members":
                log.debug("> Members: " + linea.strip())
                self.recolectando_multilinea = False
            else:
                log.debug("> Contenido Multilinea: " + linea.strip())
                self.contenido_multilinea[self.actual_atributo_multilinea] = linea.strip()
        elif self._es_contenido_valido(linea):
            clave, valor = linea.split(":")[:2]
            procesal = f" {clave} {self._valuar(valor.strip())}"
            log.debug('> Contenido Normal: ' + procesal)
            self.resultado += procesal
        elif self._es_procesal(linea):
            clave, valor = linea.split(":")
            log.debug('> Procesal: ' + clave)
        elif self._es_multilinea(linea):
            clave, valor = linea.split(":")
            # TODO: ¿Si ya existe? ¿Hay contenido que haga necesario esto?
            log.debug('> Contenido Multilinea - Primer: ' + clave)
            self.contenido_multilinea[clave] = valor
            self.actual_atributo_multilinea = clave
            self.recolectando_multilinea = True
        else:
            log.debug('> Contenido sin procesar: ' + linea.strip())

    def procesar(self):
        self.resultado = self._titulador(self.contenido[0])
        for linea in self.contenido[1:]:
            self._agregar_a_contenido(linea)

    def guardar(self):
        return self.resultado
