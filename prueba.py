from mzbackup.parseros.iterador import Iterador

if __name__ == "__main__":
    #contenido = open("contenido")
    #
    #print("\n\nContenido")
    #recolector = Iterador()
    #recolector.configurar_contenido(contenido)
    #
    #for linea in recolector:
    #    if recolector.eof:
    #        print("-- Ultima línea --") 
    #    else:
    #        print("###")
    #    print("actual: %s - siguiente: %s" % (recolector.linea_actual, recolector.linea_siguiente))
    #    print(">", linea)
    #
    contenido = open("contenido")
    #contenido = open("prueba/usuarios.data")
    #
    #print("\n\nContenido")
    recolector = Iterador()
    recolector.configurar_contenido(contenido)
    
    for linea in recolector:
        if recolector.inicio_objeto():
            print("** Primera Línea **") 
            print("\tactual: %s - siguiente: %s" % (recolector.linea_actual, recolector.linea_siguiente))
        if recolector.fin_objeto():
            print("-- Última Línea --") 
            print("\tactual: %s - siguiente: %s" % (recolector.linea_actual, recolector.linea_siguiente))
    #    else:
    #        print("actual: %s - siguiente: %s" % (recolector.linea_actual, recolector.linea_siguiente))
    #        print(">", linea)
    #
    #print(">\n>\nContenido Vacío")
    #contenido = open("contenido_vacio")
    #recolector.configurar_contenido(contenido)
    #for linea in recolector:
    #    if recolector.eof:
    #        print("-- Ultima línea --") 
    #    else:
    #        print("###")
    #    print("actual: %s - siguiente: %s" % (recolector.linea_actual.strip(), recolector.linea_siguiente.strip()))
    #    print(">", linea)
