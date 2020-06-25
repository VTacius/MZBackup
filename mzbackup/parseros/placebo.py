"""Parser de la aplicación"""
from mzbackup.parseros.iterante import Iterante


CONTENIDO_UNO = """zimbraPrefMailSignature:

Lorenzo Cerón Díaz
email: loceron2008@gmail.com, lceron@dominio.com

zimbraPrefMailSignatureStyle: internet
"""

CONTENIDO = """zimbraPrefMailSignature:

Lorenzo Cerón Díaz
email: loceron2008@gmail.com, lceron@dominio.com

cn: Lorenzo Cerón Díaz
"""

def tokenizador(linea):
    """Encuntra algunos valores en una línea dada"""
    sep = linea.find(":", 0)
    es_clave_valor = sep > 0
    clave = "" if not es_clave_valor else linea[:sep]
    valor = "" if not es_clave_valor else linea[sep+2:]

    return {'sep': sep, 'es_clave_valor': es_clave_valor,
            'clave': clave, 'valor': valor, 'linea': linea}


def tipeador(tipeado, multilinea_activo, mlattr, sep, **args):
    """Helper para ayudar a devolver tipos uniformes"""
    tipo = {'tipo': tipeado,
            'mlactivo': multilinea_activo,
            'sep': sep,
            'mlatributo': mlattr,
            'linea': args.get('linea', None)}
    return tipo


class Parser(Iterante):
    """Considera el tipo de cada línea para tratarla como es debido"""

    def __init__(self, attr):
        self._attr = attr
        # Se consideran únicamente los imprescindibles
        # El hecho es que es más probable que un atributo zimbra obligue a termina la multilinea
        self._es_atributo_posix = False
        self._es_atributo_sistema = False
        self._es_atributo_procesal = False
        self._es_atributo_deprecated = False
        self._es_atributo_multilinea = False
        Iterante.__init__(self)

    def _es_zimbra_valida(self, clave):
        self._es_atributo_posix = clave in self._attr['posix']
        self._es_atributo_sistema = clave in self._attr['sistema']
        self._es_atributo_procesal = clave in self._attr['procesal']
        self._es_atributo_deprecated = clave in self._attr['deprecated']
        self._es_atributo_multilinea = clave in self._attr['multilinea']

        if clave.startswith("zimbra"):
            return not (self._es_atributo_sistema or self._es_atributo_procesal or
                        self._es_atributo_deprecated or self._es_atributo_multilinea)

        return False

    def _asignar_tipo(self, linea, tipo_anterior):
        tokens = tokenizador(linea)
        es_zimbra = self._es_zimbra_valida(tokens['clave'])
        tipo = tipeador('DEFAULT', False, '', **tokens)
        if self._es_atributo_multilinea:
            tipo = tipeador('MULTILINEA', True, tokens['clave'], **tokens)
        elif self._es_atributo_procesal:
            tipo = tipeador('PROCESAL', False, '', **tokens)
        elif self._es_atributo_posix:
            tipo = tipeador('POSIX', False, '', **tokens)
        elif es_zimbra:
            tipo = tipeador('ZIMBRA', False, '', **tokens)
        elif tipo_anterior['mlactivo']:
            tipo = tipeador('LINEA', True, tipo_anterior['mlatributo'], **tokens)
        else:
            print("No reconozco la línea %s" % linea)

        return tipo
