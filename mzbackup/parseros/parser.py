"""Definiciones Genéricas de Recolector y Parser, con las funcionalidades más básicas"""
from string import ascii_lowercase

from mzbackup.utils.registro import get_logger

log = get_logger()

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
