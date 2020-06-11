from unittest import TestCase
from unittest import main
from unittest import mock


class TestCreacionDirectorio(TestCase):

    def test_habilitar_directorio_local(self):
        from mzbackup.utils.rutas import habilitar_directorio_local
        resultado = habilitar_directorio_local(False, {'directorio': '/opt/backup/', 'fichero': 'burbuja'}) 
        self.assertEqual(resultado, {'directorio': '/opt/backup/', 'fichero': 'burbuja'})

    def test_habilitar_directorio_local_caso2(self):
        from mzbackup.utils.rutas import habilitar_directorio_local
        resultado = habilitar_directorio_local(False, {'directorio': '/opt/backup/', 'fichero': 'burbuja'}) 
        self.assertEqual(resultado, {'directorio': '/opt/backup/', 'fichero': 'burbuja'})
  
    @mock.patch('mzbackup.utils.rutas.datetime')
    @mock.patch('mzbackup.utils.rutas.mkdir')
    def test_habilitar_directorio_local_caso3(self, mkdir, datetime):
        datetime.now.return_value.strftime.return_value = "20-06-05-190000"
        from mzbackup.utils.rutas import habilitar_directorio_local
        resultado = habilitar_directorio_local(True, {'directorio': '/opt/backup/', 'fichero': 'burbuja'}) 
        self.assertEqual(resultado, {'directorio': '/opt/backup/burbuja-20-06-05-190000', 'fichero': 'burbuja'})
