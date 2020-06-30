"""Un montón de funciones que sirven al mundo completo"""
from string import ascii_letters, digits


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
