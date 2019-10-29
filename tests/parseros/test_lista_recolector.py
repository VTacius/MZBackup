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


class RecolectorFuncional(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        archivo = open('data/lista/plural.data')
        cls.contenido = archivo.readlines()
        archivo.close()

    @mock.patch('MZBackup.parseros.listas.ParserLista')
    def test_lista_correctamente(self, parsermock):
        parser = parsermock
        parser.return_value.guardar.return_value = "contenido"

        from MZBackup.parseros.listas import RecolectorListas
        recolector = RecolectorListas(parser, {})

        total = 0
        for linea in self.contenido:
            recolector.agregar(linea)
            if recolector.fin_de_contenido:
                total += 1
        else:
            recolector.ultima_linea()
            if recolector.fin_de_contenido:
                total += 1

        self.assertEqual(5, total)
