from unittest import TestCase


class TestHelperTokenizador(TestCase):

    def test_tokenizador(self):
        from mzbackup.parseros.comun.tipo import tokenizador
        linea = "c: valor"
        resultado = tokenizador(linea)

        esperado = {'sep': 1, 'es_clave_valor': True, 'clave': 'c', 'valor': 'valor',
                    'linea': linea}

        self.assertDictEqual(esperado, resultado)

    def test_no_es_clave_valor(self):
        from mzbackup.parseros.comun.tipo import tokenizador
        linea = "Comentario externo que de algo servira"
        resultado = tokenizador(linea)

        esperado = {'sep': -1, 'es_clave_valor': False, 'clave': '', 'valor': '',
                    'linea': linea}

        self.assertDictEqual(esperado, resultado)

    def test_no_valor_vacio(self):
        from mzbackup.parseros.comun.tipo import tokenizador
        linea = "c:"
        resultado = tokenizador(linea)

        esperado = {'sep': 1, 'es_clave_valor': True, 'clave': 'c', 'valor': '',
                    'linea': linea}

        self.assertDictEqual(esperado, resultado)


class TestHelperTipeador(TestCase):

    def test_tipeador(self):
        from mzbackup.parseros.comun.tipo import tipeador
        linea = "key: value"
        tokens = {'sep': 3, 'es_clave_valor': True, 'clave': 'key', 'valor': 'value',
                  'linea': linea}

        resultado = tipeador("ZIMBRA", **tokens)

        esperado = {'tipo': "ZIMBRA", 'mlactivo': False, 'sep': 3, 'mlatributo': '',
                    'clave': 'key', 'valor': 'value'}

        self.assertDictEqual(esperado, resultado)

    def test_tipeador_multilinea(self):
        from mzbackup.parseros.comun.tipo import tipeador
        linea = "keyMulti: value"
        tokens = {'sep': 9, 'es_clave_valor': True, 'clave': 'keyMulti', 'valor': 'value',
                  'linea': linea}

        resultado = tipeador('MULTILINEA', True, tokens['clave'], **tokens)

        esperado = {'tipo': "MULTILINEA", 'mlactivo': True, 'sep': 9, 'mlatributo': 'keyMulti',
                    'clave': '', 'valor': 'value'}

        self.assertDictEqual(esperado, resultado)

    def test_tipeador_en_multilinea(self):
        from mzbackup.parseros.comun.tipo import tipeador
        linea = "Lugar donde trabaja. (Algo que sea parte de una firma"
        tokens = {'sep': -1, 'es_clave_valor': False, 'clave': '', 'valor': '',
                  'linea': linea}

        mlatributo = "keyMulti"
        resultado = tipeador('LINEA', True, mlatributo, **tokens)

        esperado = {'tipo': "LINEA", 'mlactivo': True, 'sep': -1, 'mlatributo': mlatributo,
                    'clave': '', 'valor': ''}

        self.assertDictEqual(esperado, resultado)

    def test_tipeador_en_default(self):
        from mzbackup.parseros.comun.tipo import tipeador

        resultado = tipeador()

        esperado = {'tipo': "DEFAULT", 'mlactivo': False, 'sep': -1, 'mlatributo': '',
                    'clave': None, 'valor': None}

        self.assertDictEqual(esperado, resultado)
