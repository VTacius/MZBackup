from unittest import TestCase

CONTENIDO_UNO = """
INICIO
clave=: valor
key=: value

members
"""

class TestIteranteImplementacionAvanzada(TestCase):
    @classmethod
    def setUpClass(cls):
        from mzbackup.parseros.iterante import Iterante
        class IterantePrueba(Iterante):

            def _es_linea_inicio_contenido(self, linea):
                return linea == "INICIO"
            
            def _describe_fin_contenido(self):
                return self.linea_actual == "\n" and self.linea_siguiente == "members"
        
        cls.clase = IterantePrueba 

    def test_contenido_unico(self):
        from mzbackup.mock import MockOpen
        fichero = MockOpen(CONTENIDO_UNO)

        iterante = self.clase()
        iterante.configurar_contenido(fichero)
        resultado = ["FINAL" for linea in iterante if iterante.contenido_finaliza()] 


        self.assertEqual(resultado, ["FINAL"])