from unittest import TestCase
from unittest import mock

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class MockEuropa:
    def guardar(self, identificador, contenido):
        pass


class Recolector(TestCase):

    def test_es_primera_linea(self):
        from mzbackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas({}, {})
        resultado = recolector._es_primera_linea("# distributionList lista@dominio.com memberCount=11")
        self.assertTrue(resultado)

    def test_es_primera_linea_caso2(self):
        from mzbackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas({}, {})
        resultado = recolector._es_primera_linea("# distributionList lista@dominio.com")
        self.assertFalse(resultado)

    #def test_es_primera_linea_caso3(self):
    #    from mzbackup.parseros.listas import RecolectorListas
    #    recolector = RecolectorListas({}, {})
    #    recolector.agregar("pflores@conasan.gob.sv")
    #    recolector.agregar("# distributionList lista@dominio.com")
    #    recolector.agregar("# distributionList lista@dominio.com")
    #    recolector.agregar("objectClass: zimbraDistributionList")
    #    self.assertEqual(recolector.contenido, [None, "# distributionList lista@dominio.com"])

    #def test_es_primera_linea_caso4(self):
    #    from mzbackup.parseros.listas import RecolectorListas
    #    recolector = RecolectorListas({}, {})
    #    recolector.agregar("members")
    #    recolector.agregar("# distributionList lista@dominio.com")
    #    recolector.agregar("objectClass: zimbraDistributionList")
    #    self.assertEqual(recolector.contenido, [None, "# distributionList lista@dominio.com"])

    @mock.patch('mzbackup.parseros.listas.ParserLista')
    def test_es_ultima_linea(self, parser):
        europa = MockEuropa()
        
        from mzbackup.parseros.listas import RecolectorListas
        
        recolector = RecolectorListas(parser, {})
        recolector.configurar_destino(europa)
        recolector.agregar("onovoa@hnm.gob.sv")
        recolector.agregar("")
        recolector.agregar("members")

        self.assertTrue(recolector.fin_de_contenido)

    @mock.patch('mzbackup.parseros.listas.ParserLista')
    def test_es_ultima_linea_sin_miembros(self, parser):
        europa = MockEuropa()
        
        from mzbackup.parseros.listas import RecolectorListas
        
        recolector = RecolectorListas(parser, {})
        recolector.configurar_destino(europa)
        recolector.agregar("")
        recolector.agregar("members")

        self.assertTrue(recolector.fin_de_contenido)

    @mock.patch('mzbackup.parseros.listas.ParserLista')
    def test_es_ultima_linea_multilinea(self, parser):
        europa = MockEuropa()
        
        from mzbackup.parseros.listas import RecolectorListas
        
        recolector = RecolectorListas(parser, {})
        recolector.configurar_destino(europa)
        recolector.agregar("zimbraNotes: Yasmin del Carmen Jaime de Diaz")
        recolector.agregar("")
        recolector.agregar("members")

        self.assertTrue(recolector.fin_de_contenido)

    @mock.patch('mzbackup.parseros.listas.ParserLista')
    def test_no_es_ultima_linea(self, parser):
        europa = MockEuropa()
        
        from mzbackup.parseros.listas import RecolectorListas
        
        recolector = RecolectorListas(parser, {})
        recolector.configurar_destino(europa)
        recolector.agregar("")
        recolector.agregar("members")
        self.assertTrue(recolector.fin_de_contenido)


class RecolectorFuncional(TestCase):

    @classmethod
    def setUpClass(cls):
        archivo = open('tests/data/lista/plural.data')
        cls.contenido = archivo.readlines()
        archivo.close()

    @mock.patch('mzbackup.parseros.listas.ParserLista')
    def test_lista_correctamente(self, parser):
        europa = MockEuropa()
        
        from mzbackup.parseros.listas import RecolectorListas
        
        recolector = RecolectorListas(parser, {})
        recolector.configurar_destino(europa)
        
        total = 0
        for linea in self.contenido:
            recolector.agregar(linea)
            if recolector.fin_de_contenido:
                total += 1

        self.assertEqual(5, total)
