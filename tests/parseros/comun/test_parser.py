from unittest import TestCase
from unittest import mock

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=0)

    
class Vacio:
    pass


from mzbackup.utils.europa import AbstractEuropa
class EuropaPrueba(AbstractEuropa):
    """Al parecer, tengo que implementar para testar"""

    def _guardar_procesal(self, modificante, identificador, contenido):
        return []

class PatoPrueba:
    def __init__(self):
        self.extension = ""
        self.archivo = ""

    def __str__(self):
        return "{}.{}".format(self.archivo, self.extension)

class Abrir():
    def __init__(self):
        self.contenido = []
    
    def write(self, contenido):
        self.contenido.append(contenido)
   
    def __as_dict___(self):
        return self.contenido

    @classmethod
    def ejecutar(cls, mock):
        return cls()


from mzbackup.parseros.parser import Parser
class ParserPrueba(Parser):
    
    def _titulador(self, linea):
        return linea

    def _crear_contenido_procesal(self, linea):
        return "clave", "valor"


class TestCrearContenidoMultilinea(TestCase):
    """Revisa la forma en que parseamos contenido multilínea"""
     
    def test_crear_contenido_multilinea(self):
        tokens = {'sep': 18, 'mlatributo': 'atributoMultilinea'}
        linea = "atributoMultilinea: Valor"
       
        parser = ParserPrueba({}, {})
        resultado = parser._crear_contenido_multilinea(tokens, linea)
        self.assertEqual(resultado, ('atributoMultilinea', 'Valor'))
        
    def test_parsear_contenido_multilinea(self):
        """Es bastante complejo y funcional respecto a como prueba el efectivo parseo de contenido
        multilinea"""
        from mzbackup.parseros.parser import Parser
        parser = ParserPrueba({}, {})
       
        procesables = [
                       {'linea': "attrMultilinea: Valor", 'tokens': {'tipo': 'MULTILINEA', 'sep': 14, 'mlatributo': 'attrMultilinea', 'mlactivo': True}}, 
                       {'linea': "    - Contenido valor", 'tokens': {'tipo': 'LINEA', 'sep': 14, 'mlatributo': 'attrMultilinea', 'mlactivo': True}},
                       {'linea': "    - Contenido final", 'tokens': {'tipo': 'LINEA', 'sep': 14, 'mlatributo': 'attrMultilinea', 'mlactivo': True}}
                      ]
        resultado = {'comando': "crear", 'multilinea': {}, 'procesal': {}}
        for tipo in procesables: 
            resultado = parser.parsear_linea(resultado, tipo['tokens'], tipo['linea'])

        self.assertEqual(resultado['multilinea'], {'attrMultilinea': ["Valor", "    - Contenido valor", "    - Contenido final"]})



class TestGuardarMultilinea(TestCase):
    """Este se fija solo en la implementación de los helpers, pero no profundiza en el contenido""" 
    
    @mock.patch("mzbackup.utils.europa.open")
    def test_ficheros_guardar_mulguardar_multilineartilinea(self, guardar):
        
        # En este caso, necesito controlar lo que pato devuelve
        pato = PatoPrueba()
        
        contenido = {'atributo': "Valor", 'attr': "Value"}

        destino = EuropaPrueba(pato, "ma") 
        resultado = destino._guardar_multilinea('ma', 'alortiz@salud.gob.sv', contenido)
        
        self.assertEqual(set(resultado), set(["atributo.cmd", "attr.cmd"]))
    
    @mock.patch("mzbackup.utils.europa.guardar_contenido")
    def test_ficheros_guardar_multilinea(self, guardar_contenido):
        """Mediante el mockeo de guardar_contenido, logro revisar que contenido se está produciendo""" 
        # En este otro caso, también necesito controlar lo que pato devuelve
        pato = Vacio()
        
        contenido = {'atributo': ["Valor"], 'attr': ["Value"]}
        guardar_contenido.side_effect = lambda x, y: y 

        destino = EuropaPrueba(pato, "ma") 
        resultado = destino._guardar_multilinea('ma', 'alortiz@salud.gob.sv', contenido)
        
        self.assertEqual(set(resultado), set(["zmprov ma alortiz@salud.gob.sv atributo Valor", "zmprov ma alortiz@salud.gob.sv attr Value"]))
