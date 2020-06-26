class MockOpen:
    """Mock a open"""
    
    def __init__(self, contenido):
        self.contenido = contenido.rstrip().split("\n")
        self.tamanio = len(self.contenido)
        self.iterador = 0

    def readline(self):
        """Este es el metódo a usar para obtener contenido"""
        resultado = ""
        if self.tamanio > self.iterador:
            resultado = self.contenido[self.iterador] + '\n'
            self.iterador += 1
        
        return resultado
