from unittest import TestCase
from unittest import mock
from unittest.mock import Mock, mock_open, patch, MagicMock


class TestEjecutor(TestCase):
    @classmethod
    def setUpClass(cls):
        class Vacio:
            pass

        cls.contenido = Vacio()
        cls.contenido.stdout = []
        cls.contenido.stderr = Vacio()
        cls.contenido.stderr.readlines = lambda: None
        cls.contenido.returncode = 0

    @mock.patch('mzbackup.utils.comandos._ejecutar')
    def test_error_ejecucion(self, ejecutar):
        from mzbackup.utils.comandos import EjecutorLocal
        from mzbackup.utils.comandos import SistemLocalError
        ejecutar.side_effect = FileNotFoundError
        ejecutor = EjecutorLocal("comando_no_existente")

        self.assertRaises(SistemLocalError, ejecutor.obtener_resultado)

    @mock.patch('mzbackup.utils.comandos.Popen')
    def test_retorna_lista(self, Popen):
        from mzbackup.utils.comandos import EjecutorLocal
        self.contenido.stdout = ["LINEA 01", "LINEA 02"]
        Popen.return_value.__enter__ = Mock(return_value=self.contenido)

        ejecutor = EjecutorLocal("comando")
        resultado = ejecutor.obtener_resultado()

        self.assertEqual(resultado, ["LINEA 01", "LINEA 02"])

    @mock.patch('mzbackup.utils.comandos.Popen')
    def test_retorna_fichero(self, Popen):
        from mzbackup.utils.comandos import EjecutorLocal

        self.contenido.stdout = ["LINEA 01", "LINEA 02"]
        Popen.return_value.__enter__ = Mock(return_value=self.contenido)

        ejecutor = EjecutorLocal("comando")
        contenido = mock_open()
        with patch("builtins.open", contenido, create=True):
            resultado = ejecutor.guardar_resultado("inexistente")
            self.assertIsInstance(resultado, MagicMock)


class TestEjecutorAuxiliar(TestCase):
    @classmethod
    def setUpClass(cls):
        class Vacio:
            pass

        cls.contenido = Vacio()
        cls.contenido.stdout = []
        cls.contenido.stderr = Vacio()
        cls.contenido.stderr.readlines = lambda: None
        cls.contenido.returncode = 0

    @mock.patch('mzbackup.utils.comandos.Popen')
    def test_guardar_segun_requerimiento(self, Popen):
        from mzbackup.utils.comandos import _ejecutar

        self.contenido.stdout = ["Contenido"]

        Popen.return_value.__enter__ = Mock(return_value=self.contenido)

        resultado = []
        metodo_almacenamiento = resultado.append
        _ejecutar("ls -l", metodo_almacenamiento)
        self.assertEqual(resultado, ["Contenido"])

    @mock.patch('mzbackup.utils.comandos.Popen')
    def test_devuelve_error(self, Popen):
        from mzbackup.utils.comandos import _ejecutar

        self.contenido.stderr.readlines = lambda: ["Error"]
        self.contenido.returncode = 1

        Popen.return_value.__enter__ = Mock(return_value=self.contenido)

        resultado = []
        metodo_almacenamiento = resultado.append
        error = _ejecutar("ls -l", metodo_almacenamiento)
        self.assertEqual(error, "Error")
