from unittest import TestCase
from unittest import mock

class PatoMock:
    def __init__(self):
        self.extension = ""
        self.archivo = ""

    def __str__(self):
        return "{}.{}".format(self.archivo, self.extension)

class TestCosEuropa(TestCase):
    """Prueba la definición de Europa para tipos COS"""

    @mock.patch("mzbackup.parseros.cos.dump") 
    @mock.patch("mzbackup.parseros.cos.load")
    @mock.patch("mzbackup.parseros.cos.open")
    @mock.patch("mzbackup.parseros.cos.path")
    def test_guardar_procesal(self, path, open, load, dump):
        pato = PatoMock()
        pato.archivo = 'zimbraId'
        path.exist.return_value = True
        contenido = {'zimbraId': {"000-000": "nombreCos"}}
        
        load.return_value = {"clave": "valor"}
        
        from mzbackup.parseros.cos import EuropaCos
        europa = EuropaCos(pato, "cdl")
        europa._guardar_procesal("No usado", "cos", contenido)

        self.assertEqual(europa.listar_archivos(), set(['zimbraId.id']))
        

    @mock.patch('builtins.print')
    @mock.patch("mzbackup.parseros.cos.dump") 
    @mock.patch("mzbackup.parseros.cos.load")
    @mock.patch("mzbackup.parseros.cos.open")
    @mock.patch("mzbackup.parseros.cos.path")
    def test_guardar_procesal_contenido(self, path, open, load, dump, mock_print):
        """Reviso que este uniendo el contenido actual al contenido del fichero, si este existe"""
        pato = PatoMock()
        pato.archivo = 'zimbraId'
        path.exist.return_value = True
        contenido = {'zimbraId': {"000-002": "nombreCos"}}
        
        load.return_value = {"000-001": "nombreCos"}
        dump.side_effect = lambda *args, **kwargs: print(args[0])
        
        from mzbackup.parseros.cos import EuropaCos
        europa = EuropaCos(pato, "cdl")
        europa._guardar_procesal("No usado", "cos", contenido)

        mock_print.assert_called_with({'000-001': 'nombreCos', '000-002': 'nombreCos'})
         