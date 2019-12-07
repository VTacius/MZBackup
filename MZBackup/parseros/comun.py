from logging import getLogger
from string import ascii_lowercase

log = getLogger('MZBackup')

def almacenar(fichero, contenido):
    with open(fichero, 'a') as archivo:
        archivo.write("\n\n")
        archivo.write(contenido)

def guardar(usuario, contenido):
    if 'multilinea' in contenido:
        for k, v in contenido['multilinea'].items():
            almacenar(k + ".cmd", f'zmprov ma {usuario} {k} {v}')
    
    almacenar('usuario.cmd', contenido['comando'])

class Recolector:

    def __init__(self, parser, attrs):
        self.__linea_actual = None
        self.__linea_siguiente = None

        self.contenido = []
        self.fin_de_contenido = False

        self.parser = parser
        self.attrs = attrs

    def _es_primera_linea(self, linea):
        pass

    def _es_ultima_linea(self, linea: str):
        pass

    def ultima_linea(self):
        self.contenido.append(self.__linea_actual)
        self.fin_de_contenido = True

        parser = self.parser(self.attrs)
        contenido = parser.procesar(self.contenido) 
        username = parser.usuario
        guardar(username, contenido)

    def agregar(self, linea: str):

        self.__linea_actual, self.__linea_siguiente = self.__linea_siguiente, linea.rstrip()

        if self._es_primera_linea(self.__linea_actual):
            self.contenido = []
            self.contenido.append(self.__linea_actual)
            self.fin_de_contenido = False
        elif self._es_ultima_linea(self.__linea_actual) and self._es_primera_linea(self.__linea_siguiente):
            self.contenido.append(self.__linea_actual)
            self.fin_de_contenido = True

            parser = self.parser(self.attrs)
            contenido = parser.procesar(self.contenido) 
            username = parser.usuario
            guardar(username, contenido)
        else:
            self.contenido.append(self.__linea_actual)


class Parser:

    def __init__(self, atributos):
        self.usuario = ""
        self.attr = atributos

    def obtener_tipo(self, linea, multilinea):
        sep = linea.find(':', 0)

        clave = linea[:sep]

        if clave in self.attr['multilinea']:
            return {'tipo': 'MULTILINEA', 'sep': sep, 'mlactivo': True, 'mlatributo': clave}

        for tipo, attrs in self.attr.items():
            if clave in attrs:
                return {'tipo': tipo.upper(), 'sep': sep, 'mlactivo': False, 'mlatributo': multilinea['mlatributo']}

        if clave.startswith('zimbra') and clave not in self.attr['deprecated']:
            return {'tipo': 'ZIMBRA', 'sep': sep, 'mlactivo': False, 'mlatributo': multilinea['mlatributo']}

        if multilinea['mlactivo']:
            return {'tipo': 'LINEA', 'mlactivo': True, 'mlatributo': multilinea['mlatributo']}

        log.debug(f'Error > {linea.strip()} tendrá tokens por defecto')
        return {'tipo': 'LINEA', 'mlactivo': False, 'mlatributo': multilinea['mlatributo']}

    def _crear_contenido_valido(self, tokens, linea):
        # TODO: Revisar si es un numero o una palabra, entonces no las entrecomillas
        sep = tokens['sep']
        clave = linea[:sep]
        valor = linea[sep + 2:]

        valores_no_alpha = sum([1 for x in [c for c in valor] if x not in tuple(ascii_lowercase)])
        valor = valor if valores_no_alpha == 0 else f"'{valor}'"

        return f" {clave} {valor}"

    def _crear_contenido_multilinea(self, tokens, linea):
        sep = tokens['sep']
        clave = tokens['mlatributo']
        valor = linea[sep + 2:] + " \\\n"

        return clave, valor

    def _procesar(self, tokens, linea):
        pass

    def parsear_linea(self, contenido, tokens, linea):
        clave = tokens['tipo']
        en_multilinea = tokens['mlactivo']
        if clave == 'MULTILINEA':
            clave, valor = self._crear_contenido_multilinea(tokens, linea)
            contenido['multilinea'][clave] = valor
        elif clave in ['POSIX', 'ZIMBRA']:
            contenido['comando'] += self._crear_contenido_valido(tokens, linea.strip())
        elif clave == 'PROCESAL':
            self._procesar(tokens, linea)
        elif en_multilinea:
            clave = tokens['mlatributo']
            contenido['multilinea'][clave] += linea + " \\\n"
        else:
            if clave != 'SISTEMA':
                log.debug(f'Contenido sin procesar > {linea.strip()}')

        return contenido

    def procesar(self, contenido):
        titulo = self._titulador(contenido[0])

        resultado = {'comando': titulo, 'multilinea': {}}
        multilinea = {'mlactivo': False, 'mlatributo': ''}

        for linea in contenido[1:]:
            tokens = self.obtener_tipo(linea, multilinea)
            multilinea = {'mlactivo': tokens['mlactivo'], 'mlatributo': tokens['mlatributo']}
            resultado = self.parsear_linea(resultado, tokens, linea)

        return resultado

    def _titulador(self, linea):
        pass
