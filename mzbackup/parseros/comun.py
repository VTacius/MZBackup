from logging import getLogger
from string import ascii_lowercase

log = getLogger('MZBackup')

def guardar_contenido(fichero, contenido):
    with open(fichero, 'a') as archivo:
        archivo.write("\n\n")
        archivo.write(contenido)

    return fichero


def guardar_multilinea(config_destino, usuario, contenido):
    archivos_creados = []
    for k, v in contenido.items():
        fichero = "{0}{1}.cmd".format(config_destino['directorio'], k)
        ingreso = "zmprov ma {0} {1} {2}".format(usuario, k, v) 
        archivos_creados.append(almacenar(fichero, ingreso))

    return archivos_creados 

class Recolector:

    def __init__(self, config_destino, parser, attrs):
        self.__linea_actual = None
        self.__linea_siguiente = None

        self.contenido = []
        self.fin_de_contenido = False

        self.parser = parser
        self.attrs = attrs
        self.config_destino = config_destino
        self.ficheros = []

    def _es_primera_linea(self, linea):
        pass

    def _es_ultima_linea(self, linea):
        pass
   
    def _guardar_procesal(config, identificador, contenido):
        pass

    def _guardar(self, config, identificador, contenido):
        archivos_creados = []
        if 'multilinea' in contenido:
            archivos_creados.extend(guardar_multilinea(config, identificador, contenido['multilinea']))
        
        if 'procesal' in contenido:
            archivos_creados.extend(self._guardar_procesal(config, identificador, contenido['procesal']))
        
        fichero = "{0}/{1}.cmd".format(config['directorio'], config['fichero'])
        archivos_creados.append(guardar_contenido(fichero, contenido['comando']))

        return archivos_creados

    def ultima_linea(self):
        self.contenido.append(self.__linea_actual)
        self.fin_de_contenido = True

        parser = self.parser(self.attrs)
        contenido = parser.procesar(self.contenido) 
        username = parser.usuario
        self.ficheros.extend(self._guardar(self.config_destino, username, contenido))

        return self.ficheros

    def agregar(self, linea):

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
            self.ficheros.extend(self._guardar(self.config_destino, username, contenido))
        else:
            self.contenido.append(self.__linea_actual)


class Parser:

    def __init__(self, atributos):
        self.usuario = ""
        # TODO: En orden de hacer esto más generico, allá donde dice usuario debe poner identificador
        self.identificador = ""
        self.attr = atributos

    def obtener_tipo(self, linea, multilinea):
        sep = linea.find(':', 0)

        clave = linea[:sep]

        if clave in self.attr['multilinea']:
            return {'tipo': 'MULTILINEA', 'sep': sep, 'mlactivo': True, 'mlatributo': clave}
    
        if clave in self.attr['procesal']:
            return {'tipo': 'PROCESAL', 'sep': sep, 'mlactivo': False, 'mlatributo': clave}

        for tipo, attrs in self.attr.items():
            if clave in attrs:
                return {'tipo': tipo.upper(), 'sep': sep, 'mlactivo': False, 'mlatributo': multilinea['mlatributo']}

        if clave.startswith('zimbra') and clave not in self.attr['deprecated']:
            return {'tipo': 'ZIMBRA', 'sep': sep, 'mlactivo': False, 'mlatributo': multilinea['mlatributo']}

        if multilinea['mlactivo']:
            return {'tipo': 'LINEA', 'mlactivo': True, 'mlatributo': multilinea['mlatributo']}

        log.debug("Error > {0} tendrá tokens por defecto".format(linea.strip()))
        return {'tipo': 'LINEA', 'mlactivo': False, 'mlatributo': multilinea['mlatributo']}

    def _crear_contenido_valido(self, tokens, linea):
        # TODO: Revisar si es un numero o una palabra, entonces no las entrecomillas
        sep = tokens['sep']
        clave = linea[:sep]
        valor = linea[sep + 2:]

        valores_no_alpha = sum([1 for x in [c for c in valor] if x not in tuple(ascii_lowercase)])
        valor = valor if valores_no_alpha == 0 else "'{0}'".format(valor)

        return " {0} {1}".format(clave, valor)

    def _crear_contenido_multilinea(self, tokens, linea):
        sep = tokens['sep']
        clave = tokens['mlatributo']
        valor = linea[sep + 2:] + " \\\n"

        return clave, valor
    
    def _crear_contenido_procesal(self, tokens, linea):
        pass

    def parsear_linea(self, contenido, tokens, linea):
        """ Procesa cada linea según el tipo (token) asignado """
        tipo = tokens['tipo']
        en_multilinea = tokens['mlactivo']
        if tipo == 'MULTILINEA':
            clave, valor = self._crear_contenido_multilinea(tokens, linea)
            contenido['multilinea'][clave] = valor
        elif tipo in ['POSIX', 'ZIMBRA']:
            contenido['comando'] += self._crear_contenido_valido(tokens, linea.strip())
        elif tipo == 'PROCESAL':
            clave, valor = self._crear_contenido_procesal(tokens, linea)
            contenido['procesal'][clave] = valor
        elif en_multilinea:
            clave = tokens['mlatributo']
            contenido['multilinea'][clave] += linea + " \\\n"
        else:
            if tipo != 'SISTEMA':
                log.debug("Contenido sin procesar > {0}".format(linea.strip()))

        return contenido

    def procesar(self, contenido):
        """ Realiza el procesamiento de todos los datos disponibles """
        titulo = self._titulador(contenido[0])

        # Iniciamos el procesamiento con un par de valores en sus predeterminados
        resultado = {'comando': titulo, 'multilinea': {}, 'procesal': {}}
        multilinea = {'mlactivo': False, 'mlatributo': ''}

        for linea in contenido[1:]:
            tokens = self.obtener_tipo(linea, multilinea)
            # Conforme vamos procesando, tanto multilinea y resultado van actualizandose
            # La idea es evitar la recursividad propiamente dicha, 
            #  pero aprovechar sus principios
            multilinea = {'mlactivo': tokens['mlactivo'], 'mlatributo': tokens['mlatributo']}
            resultado = self.parsear_linea(resultado, tokens, linea)

        return resultado

    def _titulador(self, linea):
        pass
