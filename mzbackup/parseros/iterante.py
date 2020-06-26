"""Definición genérica del Iterante"""
from abc import abstractmethod, ABC
from mzbackup.utils.registro import get_logger

log = get_logger()

class Iterante(ABC):
    """
    Itera de forma especial sobre el contenido, a fin de proporcionar
    linea_actual y linea_siguiente
    """

    def __init__(self):
        self._contenido = None
        self.linea_actual = None
        # Linea siguiente esta oculta para crear un get donde le quitemos el salto de línea
        self._linea_siguiente = None
        self.fin_de_fichero = False
        # ¿Hubo un inicio de contenido en este momento?
        self._contenido_presente = False
        self._contenido_finalizado = False

    @abstractmethod
    def _es_linea_inicio_contenido(self, linea):
        """
        Señala el formato que debe tener una linea para considerarse el inicio de contenido
        """

    def contenido_inicia(self):
        """
        En casi todo los objetos, el inicio de contenido se marca por el hecho que una línea
        tenga un formato específico
        """
        #print("Por acá, revisando si contenido inicia con %s" % self.linea_actual)
        veredicto = self._es_linea_inicio_contenido(self.linea_actual)
        # TODO: Se cual sea el problema con la captura de salida, el problema acá es que 
        # linea_actual tiene el salto de línea aún. Eso fue todo
        self._contenido_presente = veredicto
        #print("Veredicto: %s" % veredicto)
        return veredicto

    def _describe_fin_contenido(self):
        return self.linea_actual == "\n" and self._es_linea_inicio_contenido(self.linea_siguiente)

    def contenido_finaliza(self):
        """
        El contenido llegó a su final
        """
        veredicto = self._describe_fin_contenido() or self.fin_de_fichero
        veredicto = veredicto and self._contenido_presente
        self._contenido_presente = not veredicto
        return veredicto

    @property
    def linea_siguiente(self):
        """Le quita el salto de línea a self._linea_siguiente"""
        return self._linea_siguiente.strip()

    def configurar_contenido(self, fichero_contenido):
        """Configura el fichero con los datos, y hace la primera iteración sobre los mismos"""
        self._contenido = fichero_contenido
        self._linea_siguiente = self._contenido.readline()

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
            self.fin_de_fichero = True

        if self.linea_actual == "":
            raise StopIteration()

        return self.linea_actual.strip()
