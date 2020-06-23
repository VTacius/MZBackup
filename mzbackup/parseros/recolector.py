"""Definición genérica del Recolector"""
from abc import abstractmethod, ABC
from mzbackup.utils.registro import get_logger

log = get_logger()


class Recolector(ABC):
    """Recolector génerico que describe un comportamiento adecuado para iterar a tráves de cada
    una de las líneas en los ficheros con contenido"""

    def __init__(self, parser, attrs, datables=None):
        self._linea_actual = None
        self._linea_siguiente = None

        self.contenido = []
        self.fin_de_contenido = False

        self.attrs = attrs

        self.parser = parser
        self.destino = None
        self.datables = datables

    def configurar_destino(self, destino):
        """Permite configurar una objeto Europa después de iniciada la clase"""
        self.destino = destino

    @abstractmethod
    def _es_primera_linea(self, linea):
        pass

    @abstractmethod
    def _es_final_de_contenido(self, linea):
        pass

    def _es_ultima_linea(self, linea_actual, linea_siguiente):
        """Esta implementación es útil para COS y Usuarios"""
        es_ultima_linea = self._es_final_de_contenido(linea_actual)
        es_primera_linea = self._es_primera_linea(linea_siguiente)
        return es_ultima_linea and es_primera_linea

    def ultima_linea(self):
        """Se usa para señalar imperativamente la última línea"""
        self.contenido.append(self._linea_actual)
        self.fin_de_contenido = True

        parser = self.parser(self.attrs, self.datables)
        contenido = parser.procesar(self.contenido)
        identificador = parser.identificador
        ficheros_guardados = self.destino.guardar(identificador, contenido)

        return ficheros_guardados

    def agregar(self, linea):
        """Agrega cada línea para parseo. Define Primera y Última Linea"""
        self._linea_actual, self._linea_siguiente = self._linea_siguiente, linea.rstrip()

        if self._es_primera_linea(self._linea_actual):
            self.contenido = []
            self.contenido.append(self._linea_actual)
            self.fin_de_contenido = False
        elif self._es_ultima_linea(self._linea_actual, self._linea_siguiente):
            self.contenido.append(self._linea_actual)
            self.fin_de_contenido = True

            parser = self.parser(self.attrs, self.datables)
            contenido = parser.procesar(self.contenido)
            identificador = parser.identificador
            self.destino.guardar(identificador, contenido)
        else:
            # Según listas
            self.fin_de_contenido = False
            self.contenido.append(self._linea_actual)
