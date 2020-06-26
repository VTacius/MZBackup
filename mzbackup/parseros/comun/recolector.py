"""Ejecutor Final del parseado de ficheros"""

from abc import abstractmethod, ABC
from string import ascii_letters, digits
from mzbackup.parseros.comun.iterador import IteradorFichero

CONTENIDO = """# name vtacius@dominio.com
cn: Alexander Ortíz
zimbraPrefMailSignature: _________________________________________________________
Alexander Ortíz - Unidad de Redes y Seguridad Informática
Dirección de Tecnología
Companía Central

zimbraPrefMailSignatureStyle: internet

# name kpena@dominio.com
"""

def _crear_clave_valor(tokens, linea):
    """Separa a linea en clave y valor en el punto de separador"""
    sep = tokens['sep']
    clave = linea[:sep]
    valor = linea[sep + 2:]
    return clave, valor


def _crear_contenido_valido(tokens, linea):
    """Procesa un atributo - valor de cada línea, y lo entrecomilla de ser necesario"""
    clave, valor = _crear_clave_valor(tokens, linea)

    valores_no_ascii = filter(lambda x: x not in ascii_letters + digits, valor)
    necesita_espacios = len(list(valores_no_ascii)) > 0
    valor = "'{0}'".format(valor)if necesita_espacios else valor

    return " {0} {1}".format(clave, valor)

def _crear_contenido_multilinea(tokens, linea):
    """Procesa un atributo - valor de cada línea"""
    sep = tokens['sep']
    clave = tokens['mlatributo']
    valor = linea[sep + 2:]

    return clave, valor


class Recolector(ABC):
    """Verdadero instrumento de todo el proyecto"""
    def __init__(self, tipo, iterador):
        self.resultado = {'comando': "", 'multilinea': {}, 'procesal': {}}
        self.identificador = None
        self.iterador = iterador
        self.tipo = tipo

    @abstractmethod
    def _crear_contenido_procesal(self, tokens, linea):
        """Crea el contenido para atributos procesales"""
    
    def _parsear_linea(self, tokens, linea):
        """ Procesa cada linea según el tipo (token) asignado """
        tipo = tokens['tipo']
        if tipo == 'MULTILINEA':
            # TODO: Se supone que `tokens` ya contiene clave valor
            clave, valor = _crear_contenido_multilinea(tokens, linea)
            self.resultado['multilinea'][clave] = [valor]
        elif tipo in ['POSIX', 'ZIMBRA']:
            # TODO: Se supone que `tokens` ya contiene clave valor
            self.resultado['comando'] += _crear_contenido_valido(tokens, linea.strip())
        elif tipo == 'PROCESAL':
            # TODO: Se supone que `tokens` ya contiene clave valor
            clave, valor = self._crear_contenido_procesal(tokens, linea)
            self.resultado['procesal'][clave] = valor
        elif tipo == "LINEA":
            clave = tokens['mlatributo']
            self.resultado['multilinea'][clave].append(linea)

    @abstractmethod
    def _titulador(self, linea):
        """Crea el inicio del comando"""

    def _procesa_linea(self, linea):
        if self.iterador.inicio_objeto():
            titulo = self._titulador(linea)
            self.resultado['comando'] = titulo
        elif self.iterador.fin_objeto():
            # Antes de reiniciar, es necesario guardar esto
            print(self.resultado)
            self.resultado = {'comando': "", 'multilinea': {}, 'procesal': {}}
            self.tipo.fin_contenido()
        else:
            tokens = self.tipo.obtener_tipo(linea)
            self._parsear_linea(tokens, linea)

    def procesar_contenido(self):
        """Itera sobre el contenido y procesa cada línea"""
        for linea in self.iterador:
            self._procesa_linea(linea)

    def configurar_contenido(self, contenido):
        """Permite configurar el archivo sobre el cual se trabaja"""
        self.iterador.configurar_contenido(contenido)
