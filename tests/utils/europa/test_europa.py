from unittest import TestCase
from unittest import mock


class Abrir():
    def __init__(self):
        self.contenido = []

    def write(self, contenido):
        self.contenido.append(contenido)

    def __as_dict___(self):
        return self.contenido

    @classmethod
    def ejecutar(cls, mock):
        return cls()


class TestGuardarContenido(TestCase):

    @mock.patch("mzbackup.utils.europa.open")
    def test_guardar_contenido(self, open):
        """Siento que es un poco inútil si no puedo ver el contenido formado"""

        from mzbackup.utils.europa import guardar_contenido

        open.return_value.__enter__ = Abrir.ejecutar
        a = guardar_contenido("direccion", "contenido\nnada\ntodo")
        self.assertEqual(a, "direccion")


class TestGuardar(TestCase):

    @classmethod
    def setUpClass(cls):
        from mzbackup.utils.europa import Europa

        class EuropaPrueba(Europa):
            """Al parecer, tengo que implementar para testar"""

            def _guardar_procesal(self, modificante, identificador, contenido):
                return []

        class PatoPrueba():
            """Finjo una clase pato con la funcionalidad mínima requerida por el método guardar"""
            def __init__(self):
                self.archivo = "objeto"
                self.extension = "cmd"

            def __str__(self):
                return "{}.{}".format(self.archivo, self.extension)

            """El método Europa.guardar, que pone punto final a toda la operacion"""

        cls.Europa = EuropaPrueba
        cls.Pato = PatoPrueba

    def test_listado_ficheros(self):
        """Recuerda que, para evitar confusiones, lo mejor es que cada tipo configure a pato de
        acuerdo a sus necesidades.
        No se toma en cuenta procesal, por requerir una implementación en las subclases"""

        pato = self.Pato()
        contenido = {'comando': "zmprov ca alortiz@salud.gob.sv",
                     'multilinea': {'atributo': 'valor', 'attr': 'Value'}}

        destino = self.Europa(pato, "ma")

        destino.guardar("objeto", contenido)

        self.assertEqual(destino.listar_archivos(), set(["objeto.cmd", "atributo.cmd", "attr.cmd"]))
