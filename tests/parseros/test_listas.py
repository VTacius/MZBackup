from unittest import TestCase
from unittest import mock

from MZBackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class Recolector(TestCase):
    def test_es_primera_linea(self):
        from MZBackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas({}, {})
        resultado = recolector._es_primera_linea("# distributionList lista@dominio.com memberCount=11")
        self.assertTrue(resultado)

    def test_no_es_primera_linea(self):
        from MZBackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas({}, {})
        resultado = recolector._es_primera_linea("# distributionList lista@dominio.com")
        self.assertFalse(resultado)

    @mock.patch('MZBackup.parseros.listas.ParserLista')
    def test_es_ultima_linea(self, parsermock):
        parser = parsermock
        parser.return_value.guardar.return_value = "contenido"

        from MZBackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas(parser, {})
        recolector.agregar("onovoa@hnm.gob.sv")
        recolector.agregar("# distributionList jefaturas@dominio.com memberCount=37")

        self.assertTrue(recolector.fin_de_contenido)

    @mock.patch('MZBackup.parseros.listas.ParserLista')
    def test_es_ultima_linea_sin_miembros(self, parsermock):
        parser = parsermock
        parser.return_value.guardar.return_value = "contenido"

        from MZBackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas(parser, {})
        recolector.agregar("members")
        recolector.agregar("# distributionList jefaturas@dominio.com memberCount=37")

        self.assertTrue(recolector.fin_de_contenido)

    def test_no_es_ultima_linea(self):
        from MZBackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas({}, {})
        recolector.agregar("mail: onovoa@hnm.gob.sv")
        recolector.agregar("# distributionList jefaturas@dominio.com memberCount=37")
        self.assertFalse(recolector.fin_de_contenido)


class MetodosAuxiliaresParsero(TestCase):

    def test_titulador(self):
        from MZBackup.parseros.listas import ParserLista
        parser = ParserLista({})
        titulo = parser._titulador("# distributionList lista@dominio.com memberCount=6")
        self.assertEqual(titulo, "zmprov gdl lista@dominio.com")


class Parsero(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        archivo = open("data/lista.data")
        cls.contenido = archivo.readlines()
        archivo.close()

        archivo = open("data/lista.cmd")
        cls.respuesta = archivo.read().rstrip()
        archivo.close()

    def test_parsear_contenido(self):
        from MZBackup.parseros.listas import ParserLista
        from MZBackup.parseros.listas import atributos

        parser = ParserLista(atributos)
        resultado = parser.procesar(self.contenido)
        self.assertEqual(resultado['comando'], self.respuesta)
