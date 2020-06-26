from unittest import TestCase

CONTENIDO_UNO = """
INICIO
clave=: valor
key=: value
"""

CONTENIDO_DOS = """
INICIO
clave=: valor
key=: value

INICIO
"""

CONTENIDO_TRES = """
INICIO
clave=: valor
key=: value

INICIO
clave=: valor
key=: value
"""

class TestIteranteImplementacionBasica(TestCase):
    @classmethod
    def setUpClass(cls):
        from mzbackup.parseros.iterante import Iterante
        
        class IterantePrueba(Iterante):

            def _es_linea_inicio_contenido(self, linea):
                return linea == "INICIO"

        cls.clase = IterantePrueba 
    
    def test_contenido_unico(self):
        """El iterador reconoce que fin de fichero también es fin de contenido"""
        from mzbackup.mock import MockOpen
        fichero = MockOpen(CONTENIDO_UNO)
        
        iterante = self.clase()
        iterante.configurar_contenido(fichero)
        resultado = ["FINAL" for linea in iterante if iterante.contenido_finaliza()] 

        self.assertEqual(resultado, ["FINAL"])
    
    def test_separa_contenido(self):
        """Iterador muestra muestra contenido completo"""  
        from mzbackup.mock import MockOpen
        
        fichero = MockOpen(CONTENIDO_DOS)
        
        iterante = self.clase()
        iterante.configurar_contenido(fichero)
        resultado = ["FINAL" for linea in iterante if iterante.contenido_finaliza()] 

        # Aunque reconoce 
        self.assertEqual(resultado, ["FINAL"])
    
    def test_separa_contenido_tres(self):
        """Iterador reconoce un fin de contenido y fin de fichero, sin solapar"""
        from mzbackup.mock import MockOpen
        fichero = MockOpen(CONTENIDO_TRES)
        
        iterante = self.clase()
        iterante.configurar_contenido(fichero)
        resultado = ["FINAL" for linea in iterante if iterante.contenido_finaliza()] 


        self.assertEqual(resultado, ["FINAL", "FINAL"])
