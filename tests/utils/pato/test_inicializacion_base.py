from unittest import TestCase


class TestInicializacionBase(TestCase):

    def test_inicializar_base(self):
        from mzbackup.utils.pato import BasePato

        base = BasePato("/opt/zimbra", "cos-marca", "cos", "id")

        self.assertEqual(str(base), "/opt/zimbra/cos-marca/cos.id")
