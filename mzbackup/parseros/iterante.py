"""Definición genérica del Iterante"""
from abc import abstractmethod, ABC
from mzbackup.utils.registro import get_logger

log = get_logger()


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
