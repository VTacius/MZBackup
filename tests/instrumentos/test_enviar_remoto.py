from unittest import TestCase
from unittest import mock

class TestEnviarRemoto(TestCase):

    @classmethod
    def setUpClass(cls):

        class PatoPrueba:
            def __init__(self, base, directorio, servidor_remoto):
                self.base = base
                self.directorio = directorio
                self.servidor_remoto = servidor_remoto

            def ruta(self):
                return "/backup/"

        cls.Pato = PatoPrueba

    @mock.patch("mzbackup.instrumentos.Ejecutor")
    def test_envio_remoto(self, Ejecutor):
        from mzbackup.instrumentos import enviar_remoto
        pato = self.Pato("/", 'backup/', "128.0.0.1")
        esperado = ['INFO:MZBackup:Operación de Envío: Creación de directorio remoto',
                    'INFO:MZBackup:Operación de Envío: Envío de ficheros']
        with self.assertLogs('MZBackup', level='INFO') as log:
            enviar_remoto(True, pato, ['uno.tgz'])

            self.assertEqual(log.output, esperado)

    @mock.patch("mzbackup.instrumentos.Ejecutor")
    def test_envio_remoto_debug(self, Ejecutor):
        from mzbackup.instrumentos import enviar_remoto
        pato = self.Pato("/", 'backup/', "128.0.0.1")
        esperado = ['INFO:MZBackup:Operación de Envío: Creación de directorio remoto',
                    'INFO:MZBackup:Operación de Envío: Envío de ficheros',
                    'DEBUG:MZBackup:> Enviando uno.tgz a /backup/']
        with self.assertLogs('MZBackup', level='DEBUG') as log:
            enviar_remoto(True, pato, ['uno.tgz'])

            self.assertEqual(log.output, esperado)

    def test_enviar_remoto_desactivado(self):
       from mzbackup.instrumentos import enviar_remoto

       with self.assertLogs('MZBackup', level='INFO') as log:
           enviar_remoto(False, {}, {})
           self.assertEqual(log.output, ['INFO:MZBackup:Operacion de Envío: No se habilito el envio de los ficheros al servidor remoto'])