from mzbackup.parseros.ejecutante import atributos
from mzbackup.parseros.ejecutante import Ejecutante
from mzbackup.parseros.ejecutante import IteranteUsuario
from mzbackup.parseros.placebo import Tipeador
if __name__ == "__main__":

    tipo = Tipeador(atributos)

    resultado = {'comando': "", 'multilinea': {}, 'procesal': {}}
    contenido = open('prueba/contenido.data')
    #contenido = open('prueba/usuarios.data')

    recolector = IteranteUsuario()

    ejecutor = Ejecutante(tipo, recolector)
    ejecutor.configurar_contenido(contenido)
    ejecutor.procesar_contenido()