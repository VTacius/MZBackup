"""Definición genérica del Iterador de Fichero"""
from abc import abstractmethod, ABC

class IteradorFichero(ABC):
    """Este va a iterar mejor que ninguno"""
    def __init__(self):
        # Es un fichero abierto para nosotros
        self._contenido = None
        # Remember, remember: Existen propiedades públicas para que ya no tienen el salto de línea
        #     Estas, precisamente, son más "raw"
        self._linea_actual = None
        self._linea_siguiente = None
        # El último readlines indica que esto se ha terminado, así que dejamos el aviso
        self.eof = False
        # Almacenamos la respuesta a ¿Estamos recolectando contenido de objetos en este momento?
        self.en_recolecion = False

    @abstractmethod
    def _linea_inicia_objeto(self, linea):
        """Formato de la linea que se considera inicio de objeto"""

    def inicio_objeto(self):
        """¿Representa linea_actual, en conjunto a su contexto, el inicio de un objeto a parsear?"""

        veredicto = self._linea_inicia_objeto(self.linea_actual)

        # Porque se aplica a todas y cada unas de las lineas sobre las que se itera
        self.en_recolecion = True if veredicto else self.en_recolecion

        return veredicto

    def _describe_final_objeto(self):
        """La forma en que evaluamos que este sea el fin de linea. Basta para COS y USUARIOS"""

        linea_actual_vacia = self.linea_actual == ""
        linea_siguiente_inicia = self._linea_inicia_objeto(self.linea_siguiente)

        return linea_actual_vacia and linea_siguiente_inicia

    def fin_objeto(self):
        """¿Representa linea_actual, en conjunto a su contexto, el final de un objeto a parsear?"""

        fin_objeto = self._describe_final_objeto()
        fin_fichero = self.eof

        # ¿Hemos terminado de recolectar contenido de un objeto?
        veredicto = fin_objeto or (fin_fichero and self.en_recolecion)

        # Porque se aplica todas las lineas sobre las cuales iteramos
        self.en_recolecion = False if veredicto else self.en_recolecion

        return veredicto

    @property
    def linea_actual(self):
        """Le quita el salto de línea a self._linea_actual"""
        return self._linea_actual.strip()

    @property
    def linea_siguiente(self):
        """Le quita el salto de línea a self._linea_siguiente"""
        return self._linea_siguiente.strip()

    def configurar_contenido(self, contenido):
        """Permite configurar el fichero sobre el cual iterar"""
        self._contenido = contenido
        self._linea_siguiente = self._contenido.readline()

    def __iter__(self):
        return self

    def __next__(self):
        # A la primera línea del archivo, linea_actual es None aún (El valor de linea_siguiente)
        # Es hasta la segunda linea del archivo que línea actual tiene algo, el valor de la primera
        #     linea que tenía linea_siguiente
        self._linea_actual = self._linea_siguiente
        self._linea_siguiente = self._contenido.readline()

        # Lo que significa que self._linea actual es la última del archivo
        if self._linea_siguiente == "":
            self.eof = True

        # ¿Cuándo acaba esto?
        # Cuando linea_actual adquiera la última línea (""), que poseía linea_siguiente
        if self._linea_actual == "":
            raise StopIteration

        return self._linea_actual.rstrip()
