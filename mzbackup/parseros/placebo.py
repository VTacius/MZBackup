"""Analizador de tipo para linea"""


def tokenizador(linea):
    """Encuentra algunos valores en una línea dada"""
    sep = linea.find(":")
    es_clave_valor = sep > 0
    clave = "" if not es_clave_valor else linea[:sep]
    valor = "" if not es_clave_valor else linea[sep+2:]

    return {'sep': sep, 'es_clave_valor': es_clave_valor,
            'clave': clave, 'valor': valor, 'linea': linea}


def tipeador(tipeado="DEFAULT", multilinea_activo=False, mlattr="", sep=-1, **args):
    """Helper para ayudar a devolver tipos uniformes"""
    tipo = {'tipo': tipeado,
            'mlactivo': multilinea_activo,
            'sep': sep,
            'mlatributo': mlattr,
            'clave': args.get('clave', None),
            'valor': args.get('valor', None)}
    return tipo


class Tipeador:
    """Considera el tipo de cada línea para tratarla como es debido"""

    def __init__(self, attrs):
        # Le asignamos un tipo por defecto si no hubo línea anterior
        self.tipo_anterior = tipeador()
        self.clave = None
        self._attrs = attrs
        # De los atributos Posix se consideran únicamente los imprescindibles
        # El hecho es que es más probable que un atributo zimbra obligue a termina la multilinea
        self._es_atributo_sistema = False
        self._es_atributo_deprecated = False

    def _es_atributo_multilinea(self):
        return self.clave in self._attrs['multilinea']

    def _es_atributo_procesal(self):
        return self.clave in self._attrs['procesal']

    def _es_atributo_posix(self):
        return self.clave in self._attrs['posix']

    def _es_atributo_zimbra(self):
        if self.clave.startswith("zimbra"):
            return not (self._es_atributo_sistema or self._es_atributo_deprecated)

        return False

    def _es_atributo_linea(self):
        if self.tipo_anterior['mlactivo']:
            return not (self._es_atributo_sistema or self._es_atributo_deprecated)

        return False

    def obtener_tipo(self, linea):
        """Devuelve un tipo basado en los tokens de la línea actual y de la línea anterior"""
        tokens = tokenizador(linea)
        self.clave = tokens['clave']
        self._es_atributo_sistema = self.clave in self._attrs['sistema']
        self._es_atributo_deprecated = self.clave in self._attrs['deprecated']

        tipo = tipeador('DEFAULT', False, '', **tokens)

        if self._es_atributo_multilinea():
            tipo = tipeador('MULTILINEA', True, self.clave, **tokens)
        elif self._es_atributo_procesal():
            tipo = tipeador('PROCESAL', **tokens)
        elif self._es_atributo_posix():
            tipo = tipeador('POSIX', **tokens)
        elif self._es_atributo_zimbra():
            tipo = tipeador('ZIMBRA', **tokens)
        elif self._es_atributo_linea():
            tipo = tipeador('LINEA', True, self.tipo_anterior['mlatributo'], **tokens)
        else:
            if not (self._es_atributo_deprecated or self._es_atributo_sistema):
                print("No reconozco la línea %s" % linea)

        # Guardamos el tipo actual como tipo anterior
        self.tipo_anterior = tipo

        return tipo

    def fin_contenido(self):
        """Borra tipo anterior para que no cause problemas con el parseo de una nuevo contenido"""
        self.tipo_anterior = {}
