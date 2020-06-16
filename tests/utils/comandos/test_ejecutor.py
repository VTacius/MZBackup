from unittest import TestCase
from unittest import mock


class TestEjecutor(TestCase):

    def test_error_argumento(self):
        from mzbackup.utils.comandos import ejecutor

        self.assertRaises(TypeError, ejecutor, "ls -l", {})


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

        def enter_popen(popen):
            return self.contenido

        Popen.return_value.__enter__ = enter_popen

        resultado = []
        metodo_almacenamiento = resultado.append
        _ejecutar("ls -l", metodo_almacenamiento)
        self.assertEqual(resultado, ["Contenido"])

    @mock.patch('mzbackup.utils.comandos.Popen')
    def test_devuelve_error(self, Popen):
        from mzbackup.utils.comandos import _ejecutar

        self.contenido.stderr.readlines = lambda: ["Error"]
        self.contenido.returncode = 1

        def enter_popen(popen):
            return self.contenido

        Popen.return_value.__enter__ = enter_popen

        resultado = []
        metodo_almacenamiento = resultado.append
        error = _ejecutar("ls -l", metodo_almacenamiento)
        self.assertEqual(error, "Error")
