#!/usr/bin/python
#encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Obtiene listado de usuarios y funciones útiles relacionadas
TODO: Básicamente, si aún necesitas que esto sea útil y funcione, será necesario que lo cambies bastante para que funcione mejor
'''
__author__ = "Alexander Ortiz"
__version__ = "1.0"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

from utilidades import guardar, ejecutar_comando, abrir_listado
import re
from os import path

class listar ():
    '''
    Separé estos métodos en esta clase porque no pueden usar multiprocesamiento
    y son usados por otros script finales
    '''
    def __init__ (self):
        self.nombre_fichero = str()
        self.contenido = object()
        self.dominios = object()
        self.usuarios = object()
        self.re_verifica_usuarios_sistema = re.compile('(admin|spam|ham|quarantine|virus-quarantine|galsync)(\..+)*@(\w+\.*){3}')

    def listar_cos (self):
        '''
        Obtiene todos los COS configurados en el servidor
        '''
        comando = ['zmprov','-v','gac']
        self.contenido = ejecutar_comando(comando)
        self.nombre_fichero = 'cos.lst'
        return self

    def listar_dominios (self):
        '''
        Obtiene todos los dominios que se hayan configurado en el servidor
        '''
        comando = [ 'zmprov', 'gad' ]
        self.contenido = ejecutar_comando(comando)
        self.dominios = self.contenido
        self.nombre_fichero = 'dominios.lst'
        return self

    def __listar_usuarios_dominio (self, dominio):
        '''
        Obtiene un listado de usuarios para dominio dado
        mediante el comando zimbra zmprov -l gaa, y limpia de aquellos usuarios del sistema cuyo backup es innecesario
        '''
        comando = ['zmprov', '-l', 'gaa', dominio]
        contenido = ejecutar_comando(comando)
        listado = [usuario for usuario in contenido if not self.__verfica_usuarios_sistema(usuario)]
        return listado

    def listar_usuarios (self, dominio = ""):
        '''
        Método público para obtener usuarios: 
        Si se especifica un directorio con listado de dominios, revisa si en el mismo directorio existen los listados 
        y los convertirá en un listado mediante abrir_listado
        Si se especifica un dominio como cadena, saca la lista de usuarios para ese dominio específico mediante __listar_usuarios_dominio
        Por defecto, crea una lista de usuarios por cada dominio configurado en self.dominios
        '''
        if dominio and path.isfile(dominio):
            self.contenido = dict()
            directorio = path.dirname(dominio)
            for fichero in abrir_listado(dominio):
                listado = directorio + "/" + fichero + ".lst"
                self.contenido[fichero] = abrir_listado(listado)
        elif isinstance(dominio, str) and dominio:
            self.contenido = dict()
            self.contenido[dominio] = self.__listar_usuarios_dominio(dominio)
        else:
            # CentOS 6 usa python 2.6
            self.contenido = dict((dominio, self.__listar_usuarios_dominio(dominio)) for dominio in self.dominios)
        
        self.usuarios = self.contenido
        return self
            
    def almacenar(self):
        '''
        Al invocarse, trabaja con el contenido actual de la propiedad contenido
        Funciona mediante utilidades.guardar, que acepta listas y contenido plano, así que nos toca revisar nada más si 
        es un diccionario para iterar sobre él
        '''
        if isinstance(self.contenido, dict):
            for dominio, usuarios in self.contenido.iteritems():
                guardar(dominio + ".lst", usuarios, "l")
        else:
            guardar(self.nombre_fichero, self.contenido, "l")

    def __verfica_usuarios_sistema(self, entrada):
        return self.re_verifica_usuarios_sistema.match(entrada)
	
