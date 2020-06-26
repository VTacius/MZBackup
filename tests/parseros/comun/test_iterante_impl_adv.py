from unittest import TestCase

CONTENIDO_UNO = """
INICIO
clave=: valor
key=: value

members
"""

CONTENIDO_DOS = """
INICIO
clave=: valor
key=: value
members: Usuario Principal

members
Usuario Principal
"""

CONTENIDO_TRES = """
INICIO
clave=: valor
key=: value
members: Usuario Principal

members
Usuario Principal

ERROR
Usuario Principal
"""


class TestIteranteImplementacionAvanzada(TestCase):
    @classmethod
    def setUpClass(cls):
        from mzbackup.parseros.comun.iterador import IteradorFichero
        class IterantePrueba(IteradorFichero):

            def _linea_inicia_objeto(self, linea):
                return linea == "INICIO"
            
            def _describe_final_objeto(self):
                return self.linea_actual == "" and self.linea_siguiente == "members"
        
        cls.Iterador = IterantePrueba 

    def test_contenido_unico(self):
        from mzbackup.mock import MockOpen
        fichero = MockOpen(CONTENIDO_UNO)

        iterante = self.Iterador()
        iterante.configurar_contenido(fichero)
        resultado = ["FINAL" for linea in iterante if iterante.fin_objeto()] 


        self.assertEqual(resultado, ["FINAL"])
    
    def test_finaliza_una_vez(self):
        from mzbackup.mock import MockOpen
        fichero = MockOpen(CONTENIDO_DOS)

        iterante = self.Iterador()
        iterante.configurar_contenido(fichero)
        resultado = ["FINAL" for linea in iterante if iterante.fin_objeto()] 


        self.assertEqual(resultado, ["FINAL"])
    
    def test_finaliza_solo_con_recolecion(self):
        from mzbackup.mock import MockOpen
        fichero = MockOpen(CONTENIDO_TRES)
        iterante = self.Iterador()
        iterante.configurar_contenido(fichero)
        resultado = ["FINAL" for linea in iterante if iterante.fin_objeto()] 


        self.assertEqual(resultado, ["FINAL"])