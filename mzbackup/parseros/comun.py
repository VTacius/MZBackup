"""Definiciones Genéricas de Recolector y Parser, con las funcionalidades más básicas"""
from mzbackup.utils.registro import get_logger
from string import ascii_lowercase

log = get_logger()


def guardar_contenido(fichero, contenido):
    """Operación sencilla para crear a `fichero` con `contenido`"""
    with open(fichero, 'a') as archivo:
        archivo.write("\n\n")
        archivo.write(contenido)
    return fichero


def guardar_multilinea(pato, modificante, identificador, contenido):
    """Operación para guadar los comandos que configuran los atributos multilinea"""
    archivos_creados = []
    # Todos acá comparten la misma extension...
    pato.extension = "cmd"
    for clave, valor in contenido.items():
        # .. Y su nombre es la clave del item
        pato.archivo = clave
        valor = "\\\n".join(valor)
        ingreso = "zmprov {0} {1} {2} {3}".format(modificante, identificador, clave, valor)
        archivos_creados.append(guardar_contenido(str(pato), ingreso))

    return archivos_creados


class Recolector:
    """Recolector génerico que describe un comportamiento adecuado para iterar a tráves de cada
    una de las líneas en los ficheros con contenido"""

    def __init__(self, parser, attrs):
        self._linea_actual = None
        self._linea_siguiente = None

        self.contenido = []
        self.fin_de_contenido = False

        self.parser = parser
        self.attrs = attrs
        self.config_destino = {'directorio': "./", 'fichero': "objeto"}
        self.ficheros = []

    def configurar_destino(self, config_destino):
        """Permite configurar una objeto Pato después de iniciada la clase"""
        self.config_destino = config_destino

    def _es_primera_linea(self, linea):
        pass

    def _es_ultima_linea(self, linea):
        pass

    def _guardar_procesal(self, pato, identificador, contenido):
        return []

    def _guardar(self, pato, identificador, contenido):
        """Guarda el contenido procesado al llegar a la última línea,
        tanto programaticamente en self.agregar(), como imperativamente, en self.ultima_linea()"""
        nombre_original = pato.archivo
        archivos_creados = []

        if 'multilinea' in contenido:
            modificante = self.attrs['modificante']
            creados = guardar_multilinea(pato, modificante, identificador, contenido['multilinea'])
            archivos_creados.extend(creados)

        if 'procesal' in contenido:
            creados = self._guardar_procesal(pato, identificador, contenido['procesal'])
            archivos_creados.extend(creados)

        pato.archivo = nombre_original
        pato.extension = "cmd"
        archivos_creados.append(guardar_contenido(str(pato), contenido['comando']))

        return archivos_creados

    def ultima_linea(self):
        """Se usa para señalar imperativamente la última línea"""
        self.contenido.append(self._linea_actual)
        self.fin_de_contenido = True

        parser = self.parser(self.attrs)
        contenido = parser.procesar(self.contenido)
        identificador = parser.identificador
        self.ficheros.extend(self._guardar(self.config_destino, identificador, contenido))

        return self.ficheros

    def agregar(self, linea):
        """Agrega cada línea para parseo. Define Primera y Última Linea"""
        self._linea_actual, self._linea_siguiente = self._linea_siguiente, linea.rstrip()

        if self._es_primera_linea(self._linea_actual):
            self.contenido = []
            self.contenido.append(self._linea_actual)
            self.fin_de_contenido = False
        elif self._es_ultima_linea(self._linea_actual) and self._es_primera_linea(self._linea_siguiente):
            self.contenido.append(self._linea_actual)
            self.fin_de_contenido = True

            parser = self.parser(self.attrs)
            contenido = parser.procesar(self.contenido)
            identificador = parser.identificador
            self.ficheros.extend(self._guardar(self.config_destino, identificador, contenido))
        else:
            self.contenido.append(self._linea_actual)


class Parser:
    """Parser génericos con las operaciones básicas para procesar el contenido recolectado"""
    def __init__(self, atributos):
        self.identificador = ""
        self.attr = atributos

    def obtener_tipo(self, linea, multilinea):
        """Asigna un tipo (tokens) a cada linea"""
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

        log.trace("Error > {0} tendrá tokens por defecto".format(linea.strip()))
        return {'tipo': 'LINEA', 'mlactivo': False, 'mlatributo': multilinea['mlatributo']}

    def _crear_contenido_valido(self, tokens, linea):
        """Procesa un atributo - valor de cada línea, y lo entrecomilla de ser necesario"""
        sep = tokens['sep']
        clave = linea[:sep]
        valor = linea[sep + 2:]

        valores_no_alpha = sum([1 for x in [c for c in valor] if x not in tuple(ascii_lowercase)])
        valor = valor if valores_no_alpha == 0 else "'{0}'".format(valor)

        return " {0} {1}".format(clave, valor)

    def _crear_contenido_multilinea(self, tokens, linea):
        """Procesa un atributo - valor de cada línea"""
        sep = tokens['sep']
        clave = tokens['mlatributo']
        valor = linea[sep + 2:]

        return clave, valor

    def _crear_contenido_procesal(self, tokens, linea):
        pass

    def parsear_linea(self, contenido, tokens, linea):
        """ Procesa cada linea según el tipo (token) asignado """
        tipo = tokens['tipo']
        en_multilinea = tokens['mlactivo']
        if tipo == 'MULTILINEA':
            clave, valor = self._crear_contenido_multilinea(tokens, linea)
            contenido['multilinea'][clave] = [valor]
        elif tipo in ['POSIX', 'ZIMBRA']:
            contenido['comando'] += self._crear_contenido_valido(tokens, linea.strip())
        elif tipo == 'PROCESAL':
            clave, valor = self._crear_contenido_procesal(tokens, linea)
            contenido['procesal'][clave] = valor
        elif en_multilinea:
            clave = tokens['mlatributo']
            contenido['multilinea'][clave].append(linea)
        else:
            if tipo != 'SISTEMA':
                log.trace("Contenido sin procesar > {0}".format(linea.strip()))

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
