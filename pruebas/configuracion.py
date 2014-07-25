# encoding: utf-8
import ConfigParser
import sys
parser = ConfigParser.SafeConfigParser()
fichero = "mzbackup.ini"
seccion = 'Global'

def configuracion(clave):
    parser.read(fichero)
    secciones = parser.sections()
    if len(secciones)>0:
        return parser.get(seccion,clave)
    else:
        print "Problemas con el fichero mzbackup.ini"
        sys.exit()

remoto = configuracion("remoto")
print remoto
