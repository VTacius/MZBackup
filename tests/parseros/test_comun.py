from unittest import TestCase
from unittest import mock

from mzbackup.utils.registro import configurar_log

log = configurar_log(verbosidad=0)

class TestCrearContenidoMultilinea(TestCase):
    """Revisa la forma en que parseamos contenido multilínea"""
     
    def test_crear_contenido_multilinea(self):
        tokens = {'sep': 18, 'mlatributo': 'atributoMultilinea'}
        linea = "atributoMultilinea: Valor"
       
        from mzbackup.parseros.comun import Parser
        parser = Parser({})
        resultado = parser._crear_contenido_multilinea(tokens, linea)
        self.assertEqual(resultado, ('atributoMultilinea', 'Valor'))
        
    def test_parsear_contenido_multilinea(self):
        """Es bastante complejo y funcional respecto a como prueba el efectivo parseo de contenido
        multilinea"""
        from mzbackup.parseros.comun import Parser
        parser = Parser({})
       
        procesables = [
                       {'linea': "attrMultilinea: Valor", 'tokens': {'tipo': 'MULTILINEA', 'sep': 14, 'mlatributo': 'attrMultilinea', 'mlactivo': True}}, 
                       {'linea': "    - Contenido valor", 'tokens': {'tipo': 'LINEA', 'sep': 14, 'mlatributo': 'attrMultilinea', 'mlactivo': True}},
                       {'linea': "    - Contenido final", 'tokens': {'tipo': 'LINEA', 'sep': 14, 'mlatributo': 'attrMultilinea', 'mlactivo': True}}
                      ]
        resultado = {'comando': "crear", 'multilinea': {}, 'procesal': {}}
        for tipo in procesables: 
            resultado = parser.parsear_linea(resultado, tipo['tokens'], tipo['linea'])

        self.assertEqual(resultado['multilinea'], {'attrMultilinea': ["Valor", "    - Contenido valor", "    - Contenido final"]})
        

    
class Vacio:
    pass

class PatoMock():
    """Finjo una clase pato con la funcionalidad mínima requerida por el método guardar"""
    def __init__(self):
        self.archivo = "objeto"
        self.extension = "cmd"
    
    def __str__(self):
        return "{}.{}".format(self.archivo, self.extension)

class TestRecolectorGuardar(TestCase):
    """El método Recolector._guardar, que pone punto final a toda la operacion"""
    
    @mock.patch('mzbackup.parseros.comun.open')
    def test_listado_ficheros(self, open):
        """Recuerda que, para evitar confusiones, lo mejor es que cada tipo configure a pato de
        acuerdo a sus necesidades.
        No se toma en cuenta procesal, por requerir una implementación en las subclases"""     
        
        attrs = {'modificante': 'ma'}
        pato = PatoMock()
        contenido = {'comando': "zmprov ca alortiz@salud.gob.sv", 'multilinea': {'atributo': 'valor', 'attr': 'Value'}}
        
        from mzbackup.parseros.comun import Recolector  
        recolector = Recolector({}, attrs)
        archivos_creados = recolector._guardar(pato, "objeto", contenido)  
        self.assertEqual(set(archivos_creados), set(["objeto.cmd", "atributo.cmd", "attr.cmd"]))

class TestGuardarMultilinea(TestCase):
    """Este se fija solo en la implementación de los helpers, pero no profundiza en el contenido""" 
    @mock.patch('mzbackup.parseros.comun.open')
    def test_ficheros_guardar_multilinea(self, guardar):
        pato = Vacio()
        pato.ruta = lambda: "/var/backup"
        
        contenido = {'atributo': "Valor", 'attr': "Value"}
        
        from mzbackup.parseros.comun import guardar_multilinea
        ficheros_creados = guardar_multilinea(pato, 'ma', 'alortiz@salud.gob.sv', contenido)
        
        self.assertEqual(set(ficheros_creados), set(["/var/backup/atributo.cmd", "/var/backup/attr.cmd"]))
    
    @mock.patch('mzbackup.parseros.comun.guardar_contenido')
    def test_ficheros_guardar_multilinea(self, guardar_contenido):
        pato = Vacio()
        pato.ruta = lambda: "/var/backup"
        
        contenido = {'atributo': ["Valor"], 'attr': ["Value"]}
        guardar_contenido.side_effect = lambda x, y: y 
        
        from mzbackup.parseros.comun import guardar_multilinea
        ficheros_creados = guardar_multilinea(pato, 'ma', 'alortiz@salud.gob.sv', contenido)
        
        self.assertEqual(set(ficheros_creados), set(["zmprov ma alortiz@salud.gob.sv atributo Valor", "zmprov ma alortiz@salud.gob.sv attr Value"]))
        

class Abrir():
    def __init__(self):
        self.contenido = []
    
    def write(self, contenido):
        self.contenido.append(contenido)
   
    def __repr___(self):
        return self.contenido

    @classmethod
    def ejecutar(cls, mock):
        return cls()


class TestGuardar(TestCase):
    @mock.patch("mzbackup.parseros.comun.open")
    def test_guardar_contenido(self, open):
        """Siento que es un poco inútil si no puedo ver el contenido formado"""
        from mzbackup.parseros.comun import guardar_contenido
        open.return_value.__enter__ = Abrir.ejecutar
        a = guardar_contenido("direccion", "contenido\nnada\ntodo")
        self.assertEqual(a, "direccion")


class TestParser(TestCase):

    def test_crear_contenido_valido(self):
        from mzbackup.parseros.comun import Parser
        parser = Parser({})
        tokens = {'sep': 8}
        linea = "atributo: valor"
        resultado = parser._crear_contenido_valido(tokens, linea)
        self.assertEqual(" atributo valor", resultado)

    def test_valuar_con_espacio(self):
        from mzbackup.parseros.comun import Parser
        parser = Parser({})
        tokens = {'sep': 8}
        resultado = parser._crear_contenido_valido(tokens, "atributo: Este es mi contenido")
        self.assertEqual(resultado, " atributo 'Este es mi contenido'")

    def test_valuar_con_caracter(self):
        from mzbackup.parseros.comun import Parser
        parser = Parser({})
        tokens = {'sep': 8}
        resultado = parser._crear_contenido_valido(tokens, "atributo: E$ta")
        self.assertEqual(resultado, " atributo 'E$ta'")
