from unittest import TestCase
from unittest import mock

from MZBackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)


class Recolector(TestCase):

    def test_es_primera_linea(self):
        from MZBackup.parseros.cos import RecolectorCos
        recolector = RecolectorCos({}, {})
        resultado = recolector._es_primera_linea("# name 750_NC")
        self.assertTrue(resultado)

    def test_no_es_primera_linea(self):
        from MZBackup.parseros.usuarios import RecolectorUsuarios
        recolector = RecolectorUsuarios({}, {})
        resultado = recolector._es_primera_linea("# nombre UsuariosDirectivos")
        self.assertFalse(resultado)

    @mock.patch('MZBackup.parseros.cos.ParserCos')
    def test_es_ultima_linea(self, parsermock):
        parser = parsermock
        parser.return_value.guardar.return_value = "contenido"

        from MZBackup.parseros.cos import RecolectorCos
        recolector = RecolectorCos(parser, {})
        recolector.agregar("")
        recolector.agregar("# name UsuariosEjecutivos")
        self.assertTrue(recolector.fin_de_contenido)


class RecolectorFuncional(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        archivo = open('data/cos/plural.data')
        cls.contenido = archivo.readlines()
        archivo.close()

    @mock.patch('MZBackup.parseros.cos.ParserCos')
    def test_lista_correctamente(self, parsermock):
        parser = parsermock
        parser.return_value.guardar.return_value = "contenido"

        from MZBackup.parseros.cos import RecolectorCos
        recolector = RecolectorCos(parser, {})

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
