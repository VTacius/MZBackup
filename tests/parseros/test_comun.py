from unittest import TestCase
from unittest import skip

from MZBackup.utils.registro import configurar_log

log = configurar_log(verbosidad=0)


class Parser(TestCase):

    def test_crear_contenido_valido(self):
        from MZBackup.parseros.comun import Parser
        parser = Parser({})
        tokens = {'sep': 8}
        linea = "atributo: valor"
        resultado = parser._crear_contenido_valido(tokens, linea)
        self.assertEqual(" atributo valor", resultado)

    def test_valuar_con_espacio(self):
        from MZBackup.parseros.comun import Parser
        parser = Parser({})
        tokens = {'sep': 8}
        resultado = parser._crear_contenido_valido(tokens, "atributo: Este es mi contenido")
        self.assertEqual(resultado, " atributo 'Este es mi contenido'")

    def test_valuar_con_caracter(self):
        from MZBackup.parseros.comun import Parser
        parser = Parser({})
        tokens = {'sep': 8}
        resultado = parser._crear_contenido_valido(tokens, "atributo: E$ta")
        self.assertEqual(resultado, " atributo 'E$ta'")
