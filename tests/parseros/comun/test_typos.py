from unittest import TestCase

class TestTiposLista(TestCase):

    def test_es_primera_linea_caso3(self):
        from mzbackup.parseros.comun.tipo import Tipo
        from mzbackup.parseros.listas import atributos
        contenido = [
            "cn: # Unidad de Soporte Informático de la DTIC",
            "displayName: # Unidad de Soporte Informático de la DTIC",
            "mail: usi_dtic@salud.gob.sv",
            "objectClass: zimbraDistributionList",
            "uid: usi_dtic",
            "zimbraMailForwardingAddress: rgarcia@salud.gob.sv",
        ]
            
        tipeador = Tipo(atributos)
        resultado = [tipeador.obtener_tipo(tipo).get('tipo') for tipo in contenido]
        
        self.assertEqual(resultado, ["POSIX", "POSIX", "DEFAULT", "DEFAULT", "DEFAULT", "PROCESAL"])
