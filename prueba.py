from mzbackup.parseros.usuarios import atributos
from mzbackup.parseros.usuarios import IteradorUsuarios
from mzbackup.parseros.usuarios import RecolectorUsuario
from mzbackup.parseros.listas import IteradorListas
from mzbackup.parseros.comun.tipo import Tipo

if __name__ == "__main__":
    contenido = open("contenido")
    iterador = IteradorUsuarios()
    tipo = Tipo(atributos)
    ejecutor = RecolectorUsuario(tipo, iterador, {}) 
    ejecutor.configurar_contenido(contenido)
    ejecutor.procesar_contenido()
    
    #for linea in recolector:
    #    if recolector.inicio_objeto():
    #        print("** Primera Línea **") 
    #        print("\tactual: %s - siguiente: %s" % (recolector.linea_actual, recolector.linea_siguiente))
    #    if recolector.fin_objeto():
    #        print("-- Última Línea --") 
    #        print("¿Estoy recolectando? %s - ¿Soy fin de fichero? %s" % (self.en_recolecion, self.eof)
    #        print("\tactual: %s - siguiente: %s" % (recolector.linea_actual, recolector.linea_siguiente))
    #    else:
    #        print("actual: %s - siguiente: %s" % (recolector.linea_actual, recolector.linea_siguiente))
    #        print(">", linea)
    #
    

    contenido = open("contenido_members")
    recolector = IteradorListas()
    recolector.configurar_contenido(contenido)
    
    #for linea in recolector:
    #    if recolector.inicio_objeto():
    #        print("** Primera Línea **") 
    #        print("\tactual: %s - siguiente: %s" % (recolector.linea_actual, recolector.linea_siguiente))
    #    if recolector.fin_objeto():
    #        print("-- Última Línea --") 
    #        print("\tactual: %s - siguiente: %s" % (recolector.linea_actual, recolector.linea_siguiente))
    #    else:
    #        print("actual: %s - siguiente: %s" % (recolector.linea_actual, recolector.linea_siguiente))
    #        print(">", linea)
    #
