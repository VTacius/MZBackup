from unittest import TestCase
from unittest import skip
from mzbackup.parseros.iterante import Foreador

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

CONTENIDO_CUATRO = """
INICIO
clave=: valor
key=: value

members
"""

class MockOpen:
    def __init__(self, contenido):
        self.contenido = contenido.strip().split("\n")
        self.tamanio = len(self.contenido)
        self.iterador = 0

    def readline(self):
        resultado = ""
        if self.tamanio > self.iterador:
            resultado = self.contenido[self.iterador] + '\n'
            self.iterador += 1
        
        return resultado

class IterantePrueba(Foreador):
    
    def _inicia_contenido(self):
        # TODO: Volvemos a la necesidad de implementar un método que señale como es una primera linea
        #    así, podría dejar esto por aca casi que tengo
        return self.linea_actual == "INICIO"
    
    def _finaliza_contenido(self):
        # Necesito el atributo "puro" self._linea_siguiente, el dirá la verdad
        # TODO: Algo asi como linea_actual_en_fin_de_contenido y linea_siguiente_en_fin_de_contenido
        return (self.linea_actual == "\n" and self.linea_siguiente == "INICIO") or self.fin_de_fichero


class TestIteranteImplementacion(TestCase):

    def test_contenido_unico(self):
        
        fichero = MockOpen(CONTENIDO_UNO)
        
        iterante = IterantePrueba()
        iterante.configurar_contenido(fichero)
        resultado = ["FINAL" for linea in iterante if iterante._finaliza_contenido()] 


        self.assertEqual(resultado, ["FINAL"])
    
    def test_separa_contenido(self):
        """Aunque el contenido no parece estar completo, se hace final de contenido por el final 
        de archivo"""
        
        fichero = MockOpen(CONTENIDO_DOS)
        
        iterante = IterantePrueba()
        iterante.configurar_contenido(fichero)

        resultado = ["FINAL" for linea in iterante if iterante._finaliza_contenido()] 


        self.assertEqual(resultado, ["FINAL", "FINAL"])
    
    def test_separa_contenido_tres(self):
        
        fichero = MockOpen(CONTENIDO_TRES)
        
        iterante = IterantePrueba()
        iterante.configurar_contenido(fichero)

        resultado = ["FINAL" for linea in iterante if iterante._finaliza_contenido()] 


        self.assertEqual(resultado, ["FINAL", "FINAL"])