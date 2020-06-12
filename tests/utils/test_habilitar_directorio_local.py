from unittest import TestCase
from unittest import main
from unittest import mock


class TestCreacionDirectorio(TestCase):

    def test_habilitar_directorio_local(self):
        from mzbackup.utils.rutas import habilitar_directorio_local
        marca = "00/00/00"
        resultado = habilitar_directorio_local(False, marca, {'directorio': '/opt/backup/', 'fichero': 'burbuja'}) 
        self.assertEqual(resultado, {'directorio': '/opt/backup/', 'fichero': 'burbuja'})

    def test_habilitar_directorio_local_caso2(self):
        from mzbackup.utils.rutas import habilitar_directorio_local
        marca = "00/00/00"
        resultado = habilitar_directorio_local(False, marca, {'directorio': '/opt/backup/', 'fichero': 'burbuja'}) 
        self.assertEqual(resultado, {'directorio': '/opt/backup/', 'fichero': 'burbuja'})
  
    @mock.patch('mzbackup.utils.rutas.mkdir')
    def test_habilitar_directorio_local_caso3(self, mkdir):
        marca = "20-06-05-190000"
        from mzbackup.utils.rutas import habilitar_directorio_local
        resultado = habilitar_directorio_local(True, marca, {'directorio': '/opt/backup/', 'fichero': 'burbuja'}) 
        self.assertEqual(resultado, {'directorio': '/opt/backup/burbuja-20-06-05-190000', 'fichero': 'burbuja'})
