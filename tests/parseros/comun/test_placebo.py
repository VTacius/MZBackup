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

class TestPlacebo(TestCase):

    def test_obtener_tipo(self):
        from mzbackup.parseros.placebo import Tipeador

        tipo = Tipeador(atributos)
        resultado = tipo.obtener_tipo("cn: Alexander Ortíz")

        esperado = {'tipo': "POSIX", 'mlactivo': False, 'sep': 2, 'mlatributo': '',
                    'clave': 'cn', 'valor': 'Alexander Ortíz'}

        self.assertDictEqual(esperado, resultado)

    def test_tipo_multilinea(self):
        from mzbackup.parseros.placebo import Tipeador

        tipo = Tipeador(atributos)
        resultado = tipo.obtener_tipo("zimbraMailSieveScript: allow")

        esperado = {'tipo': "MULTILINEA", 'mlactivo': True, 'sep': 21, 
                    'mlatributo': 'zimbraMailSieveScript', 'clave': 'zimbraMailSieveScript', 
                    'valor': 'allow'}

        self.assertDictEqual(esperado, resultado)

    def test_tipo_en_multilinea(self):
        from mzbackup.parseros.placebo import Tipeador

        tipo = Tipeador(atributos)
        tipo.obtener_tipo("zimbraMailSieveScript: allow")
        resultado = tipo.obtener_tipo("    filter {}")

        esperado = {'tipo': "LINEA", 'mlactivo': True, 'sep': -1, 
                    'mlatributo': 'zimbraMailSieveScript', 'clave': '', 
                    'valor': ''}

        self.assertDictEqual(esperado, resultado)

    def test_tipo_en_multilinea_termina(self):
        from mzbackup.parseros.placebo import Tipeador

        tipo = Tipeador(atributos)
        tipo.obtener_tipo("zimbraMailSieveScript: allow")
        tipo.obtener_tipo("    filter 'UNO' {}")
        tipo.obtener_tipo("    filter 'DOS' {}")
        resultado = tipo.obtener_tipo("zimbraFeaturePortalEnabled: FALSE")
        esperado = {'tipo': "ZIMBRA", 'mlactivo': False, 'sep': 26, 
                    'mlatributo': '', 'clave': 'zimbraFeaturePortalEnabled', 'valor': 'FALSE'}

        self.assertDictEqual(esperado, resultado)
