from unittest import TestCase
from unittest import mock


class TestTipeador(TestCase):

    def test_tipo_no_definido(self):
        from mzbackup.instrumentos import tipeador

        self.assertRaises(TypeError, tipeador, 'inexistente')


class TestCrearRecolector(TestCase):

    @mock.patch("mzbackup.utils.pato.Pato")
    def test_creacion_asigna_contenido(self, Pato):
        from mzbackup.instrumentos import crear_recolector
        from mzbackup.utils.europa import Europa
        pato = Pato()
        resultado = crear_recolector("cos", pato, {})

        self.assertIsInstance(resultado.europa, Europa)
    
    @mock.patch("mzbackup.utils.pato.Pato")
    def test_creacion_asigna_datables(self, Pato):
        from mzbackup.instrumentos import crear_recolector
        from mzbackup.utils.europa import Europa
        pato = Pato()
        args = {'datables': "contenido"}
        resultado = crear_recolector("usuarios", pato, args)
        self.assertEqual(resultado.datables, "contenido")




class TestCrearFicheroContenido(TestCase):

    @mock.patch("mzbackup.instrumentos.EjecutorLocal")
    @mock.patch("mzbackup.utils.pato.Pato")
    def test_crear_fichero_contenido(self, Pato, ejecutor):
        from mzbackup.instrumentos import crear_fichero_contenido
        pato = Pato()
        ejecutor.return_value.guardar_resultado = lambda pato: "fichero"
        resultado = crear_fichero_contenido(pato, "inexistente -v")

        self.assertEqual("fichero", resultado)
