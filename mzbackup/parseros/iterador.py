"""Este debe ser el último"""

class Iterador:
    """Este va a iterar mejor que ninguno"""
    def __init__(self):
        # Es un fichero abierto para nosotros
        self._contenido = None
        self._linea_actual = None
        self._linea_siguiente = None
        # linea_siguiente indica que esto se ha terminado. Todo debe terminar ya
        self.eof = False

    def _linea_inicia_objeto(self, linea):
        # TODO: Este no debería ser implementado, a la espera que se haga en la clase hijo
        if linea and linea.startswith("# name "):
            return len(linea.split(' ')) == 3 and linea.split(' ')[2].find('@', 0) > 0

        return False

    def inicio_objeto(self):
        veredicto = self._linea_inicia_objeto(self.linea_actual)
        return veredicto

    def _describe_final_objeto(self):
        linea_actual_vacia = self.linea_actual == "" 
        linea_siguiente_inicia = self._linea_inicia_objeto(self.linea_siguiente)
        return linea_actual_vacia and linea_siguiente_inicia 

    def fin_objeto(self):
        fin_objeto = self._describe_final_objeto()
        fin_fichero = self.eof
        return fin_objeto or fin_fichero 
    
    @property
    def linea_actual(self):
        """Le quita el salto de línea a self._linea_actual"""
        return self._linea_actual.strip()
    
    @property
    def linea_siguiente(self):
        """Le quita el salto de línea a self._linea_siguiente"""
        return self._linea_siguiente.strip()
    
    def configurar_contenido(self, contenido):
        self._contenido = contenido 
        self._linea_siguiente = self._contenido.readline()
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self._linea_actual = self._linea_siguiente
        self._linea_siguiente = self._contenido.readline()
        
        if self._linea_siguiente == "":
            self.eof = True
        
        if self._linea_actual == "":
            raise StopIteration
        
        return self._linea_actual.rstrip()