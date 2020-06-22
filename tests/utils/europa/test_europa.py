from unittest import TestCase
from unittest import mock

class Abrir():
    def __init__(self):
        self.contenido = []
    
    def write(self, contenido):
        self.contenido.append(contenido)
   
    def __repr___(self):
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

from mzbackup.utils.europa import AbstractEuropa
class EuropaMock(AbstractEuropa):
    """Al parecer, tengo que implementar para testar"""

    def _guardar_procesal(self, modificante, identificador, contenido):
        return []

class PatoMock():
    """Finjo una clase pato con la funcionalidad mínima requerida por el método guardar"""
    def __init__(self):
        self.archivo = "objeto"
        self.extension = "cmd"
    
    def __str__(self):
        return "{}.{}".format(self.archivo, self.extension)

class TestGuardar(TestCase):
    """El método Europa.guardar, que pone punto final a toda la operacion"""
    
    @mock.patch('mzbackup.parseros.recolector.open')
    def test_listado_ficheros(self, open):
        """Recuerda que, para evitar confusiones, lo mejor es que cada tipo configure a pato de
        acuerdo a sus necesidades.
        No se toma en cuenta procesal, por requerir una implementación en las subclases"""     
        
        pato = PatoMock()
        contenido = {'comando': "zmprov ca alortiz@salud.gob.sv", 'multilinea': {'atributo': 'valor', 'attr': 'Value'}}
        
        destino = EuropaMock(pato, "ma")
        
        destino.guardar("objeto", contenido)  
        
        self.assertEqual(destino.listar_archivos(), set(["objeto.cmd", "atributo.cmd", "attr.cmd"]))