from unittest import TestCase
atributos = {'posix': ['cn', 'ou', 'ou'],
             'sistema': ['mail', 'uid', 'userPassword'],
             'procesal': ['zimbraCOSId'],
             'deprecated': ['zimbraMailHost', 'zimbraMailTransport'],
             'multilinea': ['zimbraMailSieveScript', 'zimbraPrefMailSignature']}


CONTENIDO_UNO = """
zimbraPrefMailSignature:

Lorenzo Cerón Díaz
email: loceron2008@gmail.com, lceron@dominio.com

zimbraPrefMailSignatureStyle: internet
"""

CONTENIDO = """
zimbraPrefMailSignature:

Lorenzo Cerón Díaz
email: loceron2008@gmail.com, lceron@dominio.com

cn: Lorenzo Cerón Díaz
"""


class TestTipo(TestCase):

    def test_obtener_tipo(self):
        from mzbackup.parseros.comun.tipo import Tipo

        tipo = Tipo(atributos)
        resultado = tipo.obtener_tipo("cn: Alexander Ortíz")

        esperado = {'tipo': "POSIX", 'mlactivo': False, 'sep': 2, 'mlatributo': '',
                    'clave': 'cn', 'valor': 'Alexander Ortíz'}

        self.assertDictEqual(esperado, resultado)

    def test_tipo_multilinea(self):
        from mzbackup.parseros.comun.tipo import Tipo

        tipo = Tipo(atributos)
        linea = 'zimbraMailSieveScript: require ["fileinto", "reject", "tag", "flag"];'
        resultado = tipo.obtener_tipo(linea)

        esperado = {'tipo': "MULTILINEA", 'mlactivo': True, 'sep': 21,
                    'mlatributo': 'zimbraMailSieveScript', 'clave': '',
                    'valor': 'require ["fileinto", "reject", "tag", "flag"];'}

        self.assertDictEqual(esperado, resultado)

    def test_tipo_en_multilinea(self):
        from mzbackup.parseros.comun.tipo import Tipo

        tipo = Tipo(atributos)
        tipo.obtener_tipo("zimbraMailSieveScript: allow")
        resultado = tipo.obtener_tipo("    filter {}")

        esperado = {'tipo': "LINEA", 'mlactivo': True, 'sep': -1,
                    'mlatributo': 'zimbraMailSieveScript', 'clave': '',
                    'valor': ''}

        self.assertDictEqual(esperado, resultado)

    def test_tipo_en_multilinea_termina(self):
        from mzbackup.parseros.comun.tipo import Tipo

        tipo = Tipo(atributos)
        tipo.obtener_tipo('zimbraMailSieveScript: require ["fileinto", "reject", "tag", "flag"];')
        tipo.obtener_tipo("")
        tipo.obtener_tipo('# Flujo de actividad')
        tipo.obtener_tipo('disabled_if anyof (bulk,')
        tipo.obtener_tipo('  list) {')
        tipo.obtener_tipo('    fileinto "Flujo de actividad";')
        tipo.obtener_tipo('}')

        esperado = {'tipo': "ZIMBRA", 'mlactivo': False, 'sep': 28,
                    'mlatributo': '', 'clave': 'zimbraMailSignatureMaxLength', 'valor': '10240'}

        resultado = tipo.obtener_tipo("zimbraMailSignatureMaxLength: 10240")
        self.assertDictEqual(esperado, resultado)

