from unittest import TestCase
from unittest import mock


class TestHelpers(TestCase):

    def test_crear_clave_valor(self):
        """Separa en clave valor. Se usa tanto individual como en otras funciones"""
        from mzbackup.parseros.comun.helpers import _crear_clave_valor
        tokens = {'sep': 8}
        linea = "atributo: Valor asociado"
        resultado = _crear_clave_valor(tokens, linea)

        self.assertEqual(resultado, ('atributo', 'Valor asociado'))

    @mock.patch("mzbackup.parseros.comun.helpers._crear_clave_valor")
    def test_crear_contenido_valido(self, claveador):
        """A partir de clave-valor, crea contenido para agregar al comando tal"""

        from mzbackup.parseros.comun.helpers import _crear_contenido_valido

        claveador.return_value = ('atributo', 'Valor asociado')

        tokens = {'sep': 8}
        linea = "atributo: Valor asociado"
        resultado = _crear_contenido_valido(tokens, linea)

        self.assertEqual(resultado, " atributo 'Valor asociado'")

    @mock.patch("mzbackup.parseros.comun.helpers._crear_clave_valor")
    def test_crear_contenido_valido_caso2(self, claveador):
        """A partir de clave-valor, crea contenido para agregar al comando tal"""
        from mzbackup.parseros.comun.helpers import _crear_contenido_valido

        claveador.return_value = ('atributo', 'Valor')

        tokens = {'sep': 8}
        linea = "atributo: Valor"
        resultado = _crear_contenido_valido(tokens, linea)

        self.assertEqual(resultado, " atributo Valor")

    @mock.patch("mzbackup.parseros.comun.helpers._crear_clave_valor")
    def test_crear_contenido_valido_caso3(self, claveador):
        """A partir de clave-valor, crea contenido para agregar al comando tal"""
        from mzbackup.parseros.comun.helpers import _crear_contenido_valido

        claveador.return_value = ('atributo', 'Ñalor')

        tokens = {'sep': 8}
        linea = "atributo: Ñalor"
        resultado = _crear_contenido_valido(tokens, linea)

        self.assertEqual(resultado, " atributo 'Ñalor'")

    @mock.patch("mzbackup.parseros.comun.helpers._crear_clave_valor")
    def test_crear_contenido_valido_caso4(self, claveador):
        """A partir de clave-valor, crea contenido para agregar al comando tal"""
        from mzbackup.parseros.comun.helpers import _crear_contenido_valido

        claveador.return_value = ('atributo', 'Lugar "Nombre del Lugar"')

        tokens = {'sep': 8}
        linea = "atributo: Lugar \"Nombre del Lugar\""
        resultado = _crear_contenido_valido(tokens, linea)

        self.assertEqual(resultado, " atributo 'Lugar \"Nombre del Lugar\"'")


class TestParser(TestCase):

    @mock.patch("mzbackup.parseros.comun.helpers._crear_clave_valor")
    def test_crear_contenido_valido(self, claveador):
        from mzbackup.parseros.comun.helpers import _crear_contenido_valido

        claveador.return_value = ('atributo', 'valor')

        tokens = {'sep': 8}
        linea = "atributo: valor"
        resultado = _crear_contenido_valido(tokens, linea)
        self.assertEqual(" atributo valor", resultado)

    @mock.patch("mzbackup.parseros.comun.helpers._crear_clave_valor")
    def test_valuar_con_espacio(self, claveador):
        from mzbackup.parseros.comun.helpers import _crear_contenido_valido

        claveador.return_value = ('atributo', 'Este es mi contenido')

        tokens = {'sep': 8}
        resultado = _crear_contenido_valido(tokens, "atributo: Este es mi contenido")
        self.assertEqual(resultado, " atributo 'Este es mi contenido'")

    @mock.patch("mzbackup.parseros.comun.helpers._crear_clave_valor")
    def test_valuar_con_caracter(self, claveador):
        from mzbackup.parseros.comun.helpers import _crear_contenido_valido

        claveador.return_value = ('atributo', 'E$ta')

        tokens = {'sep': 8}
        resultado = _crear_contenido_valido(tokens, "atributo: E$ta")
        self.assertEqual(resultado, " atributo 'E$ta'")
