"""Definición genérica del Iterante"""
from abc import abstractmethod, ABC
from mzbackup.utils.registro import get_logger

log = get_logger()

class Foreador(ABC):
    """Esta es la nueva generación"""

    def __init__(self):
        self._contenido  = None
        self.linea_actual = None
        # Linea siguiente esta oculta para crear un get donde le quitemos el salto de línea
        self._linea_siguiente = None
        self.fin_de_fichero = False

    @abstractmethod
    def _inicia_contenido(self):
        """Da la posibilidad que cada objeto defina como es su Linea de Inicio
        Por ahora, basta con definir como debe ser un línea"""

    @abstractmethod
    def _finaliza_contenido(self):
        """Es la implementación por defecto para la última línea que separa el contenido
        COS y Usuarios hacen uso de ella"""
    
    @property
    def linea_siguiente(self):
        return self._linea_siguiente.strip()
    
    def __iter__(self):
        return self

    def __next__(self):
        linea = self._contenido.readline()
        # A la primera línea del archivo, linea_actual es None aún (El valor de linea_siguiente)
        # Es hasta la segunda linea del archivo que línea actual tiene algo, el valor de la primera
        #     linea que tenía linea_siguiente
        self.linea_actual, self._linea_siguiente = self._linea_siguiente, linea

        # ¿Cuándo acaba esto? 
        # Cuando linea_actual adquiera la última línea, que poseía linea_siguiente
        if self._linea_siguiente == "":
            print("El fin esta cerca")
            print("comienza ")
            print(self.linea_actual)
            print("termina")
            self.fin_de_fichero = True
        
        if self.linea_actual == "":
            raise StopIteration()
        
        return self.linea_actual.strip()
    
    def configurar_contenido(self, fichero_contenido):
        self._contenido = fichero_contenido
        self._linea_siguiente = self._contenido.readline()

class Iterante(ABC):
    """Iterante génerico que describe un comportamiento adecuado para iterar a tráves de cada
    una de las líneas en los ficheros con contenido
    Guarda una Línea actual y Línea siguiente, con lo que cual es más fácil analizar
    el contexto, lo que nos permite decidir con que tipo de línea tratammos"""

    def __init__(self):
        self._linea_actual = None
        self._linea_siguiente = None

        self.fin_de_contenido = False
        self.destino = None

    @abstractmethod
    def _es_primera_linea(self, linea):
        """Da la posibilidad que cada objeto defina como es su Linea de Inicio"""

    @abstractmethod
    def _es_final_de_contenido(self, linea):
        """Da la posibilidad que cada objeto defina como es su Linea de Fin de Contenido"""

    @abstractmethod
    def _procesamiento(self, linea, tipo_pasado):
        pass

    def _es_ultima_linea(self, linea_actual, linea_siguiente):
        """Es la implementación por defecto para la última línea que separa el contenido
        COS y Usuarios hacen uso de ella"""
        es_ultima_linea = self._es_final_de_contenido(linea_actual)
        es_primera_linea = self._es_primera_linea(linea_siguiente)
        return es_ultima_linea and es_primera_linea

    def configurar_destino(self, destino):
        """Permite configurar una objeto Europa después de iniciada la clase"""
        self.destino = destino

    def _agregar(self, linea, tipo_pasado):
        """Agrega cada línea de un archivo o contenido para su análisis"""
        # Este es el tipo mínimo que podemos tener, porque si no tiene tipo
        tipo = {'mlactivo': False}

        # ¿Es esta la primera línea del archivo?
        es_inicio = self._linea_siguiente is None

        self._linea_actual, self._linea_siguiente = self._linea_siguiente, linea.rstrip()

        # Con esto, nos aseguramos que esta línea sea la primera linea del archivos.
        if not es_inicio:
            tipo = self._procesamiento(self._linea_actual, tipo_pasado)

        return tipo
