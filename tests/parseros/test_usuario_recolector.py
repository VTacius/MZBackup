from unittest import TestCase
from unittest import mock

from MZBackup.utils.registro import configurar_log

log = configurar_log(verbosidad=0)


class Recolector(TestCase):

    def test_es_primera_linea(self):
        from MZBackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios({}, {})
        resultado = recolector._es_primera_linea("# name vtacius@dominio.com")
        self.assertTrue(resultado)

    def test_no_es_primera_linea(self):
        from MZBackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios({}, {})
        resultado = recolector._es_primera_linea("#name vtacius@dominio.com")
        self.assertFalse(resultado)

    @mock.patch('MZBackup.parseros.usuarios.ParserUsuario')
    def test_es_ultima_linea(self, parsermock):
        parser = parsermock
        parser.return_value.guardar.return_value = "contenido"

        from MZBackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios(parser, {})
        recolector.agregar("")
        recolector.agregar("# name usuario@dominio.com")
        self.assertTrue(recolector.fin_de_contenido)


class RecolectorFuncional(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        archivo = open('data/usuario/plural.data')
        cls.contenido = archivo.readlines()
        archivo.close()

    @mock.patch('MZBackup.parseros.usuarios.ParserUsuario')
    def test_lista_correctamente(self, parsermock):
        parser = parsermock
        parser.return_value.guardar.return_value = "contenido"

        from MZBackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios(parser, {})

        total = 0
        for linea in self.contenido:
            recolector.agregar(linea)
            if recolector.fin_de_contenido:
                total += 1
        else:
            recolector.ultima_linea()
            if recolector.fin_de_contenido:
                total += 1

        self.assertEqual(10, total)
