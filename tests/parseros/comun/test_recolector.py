from unittest import TestCase
from unittest import mock

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=0)


class Vacio:
    pass


class PatoPrueba:
    def __init__(self):
        self.extension = ""
        self.archivo = ""

    def __str__(self):
        return "{}.{}".format(self.archivo, self.extension)


class TestCrearContenidoMultilinea(TestCase):
    """Revisa la forma en que parseamos contenido multilínea"""

    @classmethod
    def setUpClass(cls):
        from mzbackup.parseros.comun.recolector import Recolector

        class RecolectorPrueba(Recolector):
            def _crear_contenido_procesal(self, _tokens, _linea):
                pass

            def _titulador(self, linea):
                return linea
        cls.Recolector = RecolectorPrueba

    def test_crear_contenido_multilinea(self):
        from mzbackup.parseros.comun.recolector import _crear_contenido_multilinea
        tokens = {'sep': 18, 'mlatributo': 'atributoMultilinea'}
        linea = "atributoMultilinea: Valor"

        resultado = _crear_contenido_multilinea(tokens, linea)
        self.assertEqual(resultado, ('atributoMultilinea', 'Valor'))

    def test_parsear_contenido_multilinea(self):
        """Es bastante complejo y funcional respecto a como prueba el efectivo parseo de contenido
        multilinea"""
        parser = self.Recolector({}, {})

        procesables = [
                       {'linea': "attrMultilinea: Valor", 'tokens': {'tipo': 'MULTILINEA',
                        'sep': 14, 'mlatributo': 'attrMultilinea', 'mlactivo': True}},
                       {'linea': "    - Contenido valor", 'tokens': {'tipo': 'LINEA',
                        'sep': 14, 'mlatributo': 'attrMultilinea', 'mlactivo': True}},
                       {'linea': "    - Contenido final", 'tokens': {'tipo': 'LINEA',
                        'sep': 14, 'mlatributo': 'attrMultilinea', 'mlactivo': True}}
                      ]

        for tipo in procesables:
            parser._parsear_linea(tipo['tokens'], tipo['linea'])

        valorMultilinea = ["Valor", "    - Contenido valor", "    - Contenido final"]
        self.assertEqual(parser.resultado['multilinea'], {'attrMultilinea': valorMultilinea})


class TestGuardarMultilinea(TestCase):
    """Este se fija solo en la implementación de los helpers, pero no profundiza en el contenido"""
    @classmethod
    def setUpClass(cls):
        from mzbackup.utils.europa import Europa

        class EuropaPrueba(Europa):
            """Al parecer, tengo que implementar para testar"""

            def _guardar_procesal(self, modificante, identificador, contenido):
                return []
        cls.Europa = EuropaPrueba

    @mock.patch("mzbackup.utils.europa.open")
    def test_ficheros_guardar_mulguardar_multilineartilinea(self, guardar):

        # En este caso, necesito controlar lo que pato devuelve
        pato = PatoPrueba()

        contenido = {'atributo': "Valor", 'attr': "Value"}

        destino = self.Europa(pato, "ma")
        resultado = destino._guardar_multilinea('ma', 'alortiz@salud.gob.sv', contenido)

        self.assertEqual(set(resultado), set(["atributo.cmd", "attr.cmd"]))

    @mock.patch("mzbackup.utils.europa.guardar_contenido")
    def test_ficheros_guardar_multilinea(self, guardar_contenido):
        """Mediante mockeo de guardar_contenido, logro revisar que contenido se está produciendo"""
        # En este otro caso, también necesito controlar lo que pato devuelve
        pato = Vacio()

        contenido = {'atributo': ["Valor"], 'attr': ["Value"]}
        guardar_contenido.side_effect = lambda x, y: y

        destino = self.Europa(pato, "ma")
        resultado = destino._guardar_multilinea('ma', 'alortiz@salud.gob.sv', contenido)

        esperado = set(["zmprov ma alortiz@salud.gob.sv atributo Valor",
                        "zmprov ma alortiz@salud.gob.sv attr Value"])
        self.assertEqual(set(resultado), esperado)
