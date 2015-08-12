#!/usr/bin/python
#encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Parseado de entrada LDAP del usuario en comando zmprov:
Cambia atributo:valor a opcion:valor
'''
__author__ = "Alexander Ortiz"
__version__ = "0.2"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import re as r
import sys as s
from threading import Thread, Semaphore
from utilidades import ejecutar_comando, guardar

class modelador():
    '''
    Maneja una entrada resultado de zmprov -l ga user@dominio.com
    La convierte en una serie de comandos para dejar al usuario tal como estaba en el servidor anterior
    '''
    def __init__(self, usuario, cosId):
        # Marca los self.atributos que no deben ser tomados en cuenta porque se consideran obsoletos
        self.atributos = r.compile('^(zimbraMailHost|zimbraMailTransport|zimbraFeatureNotebookEnabled|zimbraPrefCalendarReminderYMessenger|zimbraPrefReadingPaneEnabled|zimbraContactAutoCompleteEmailFields|zimbraPrefCalendarReminderSendEmail|zimbraPrefContactsInitialView|zimbraFeaturePeopleSearchEnabled|zimbraFeatureMailPollingIntervalPreferenceEnabled|zimbraPrefCalendarReminderDuration1|zimbraPrefCalendarReminderMobile|zimbraFeatureAdvancedSearchEnabled|zimbraFeatureWebSearchEnabled|zimbraPrefContactsExpandAppleContactGroups|zimbraPrefContactsDisableAutocompleteOnContactGroupMembers|zimbraFeatureShortcutAliasesEnabled|zimbraIMService|zimbraFeatureImportExportFolderEnabled|mail|zimbraCreateTimestamp|zimbraMailDeliveryAddress|objectClass|uid|userPassword|mail|zimbraId|zimbraMailAlias|zimbraLastLogonTimestamp|zimbraCOSId|$)')
        # Marca el inicio de línea  
        self.marcador  = r.compile('^#\sname')
        # Marca todos los atributos zimbra, util para salir del ciclo que los atributos en self.especiales empiezan
        self.marcador_atributo = r.compile('^zimbra[a-zA-Z]+:\s\w+')
        # Marca el atributo zimbraCOSId, con el que se hacen operaciones específicas
        self.marcador_cos = r.compile('^zimbraCOSId:')
        # Atributos cuyos valores tienen más de una línea
        self.especiales = r.compile('^(zimbraMailSieveScript|zimbraPrefMailSignature|zimbraPrefMailSignatureHTML):')
        # Bandera que marca la localización de un valor especial
        self.especial = False
        # Atributos para almacenar los resultados de la iteracion
        self.comando = str()
        self.volcado = str()
        self.cosid = str()
        self.indice = 0
        self.attr = len(usuario)
        self.datos = usuario
        self.cosId = cosId

    def guardar(self, archivo, datos):
        '''
        Guarda virtualmente el contenido según el modelador los va encontrando, 
        colocandolo en el atributo necesario
        '''
        if archivo == "ldif":
            self.volcado += datos
        if archivo == "fcmd":
            self.comando += datos
        if archivo == "cosid":
            self.cosid += datos

    def __cabecera(self, fcmd, line):
        '''
        Inicia el comando cuando self.marcador es encontrado dentro del contenido dado
        Da una contraseña por defecto Un0.D0s.Tr3s 
        '''
        usuario = line.split(" ")[2] 
        sentencia = "\n\nzmprov ca {user} Un0.D0s.Tr3s ".format(user=usuario)
        self.guardar(fcmd, sentencia)
        return usuario

    def __attrComun(self, fcmd, line):
        '''
        Maneja los atributos más comunes que no coinciden con self.atributos
        Como self.atributos son atributos marcados como obsoletos desde versiones anteriores,
        se supone que cualquier atributo que llegue a esta opción por defecto es un atributo válido
        que necesitamos usar dentro del comando
        Convierte atributos:valor en opcion_valor
        '''
        i = line.find(" ")
        sentencia = line[:i-1] + " '" + line[i+1:].rstrip("\n") + "' "
        self.guardar(fcmd, sentencia)

    def __especiales(self, usuario, line):
        '''
        Al coincidir con self.especiales, contruye los comandos para volver a configurarlos
        '''
        print(line)
        i = line.find(" ")
        atributo = line[:i-1]
        valor = line[i+1:]
        comando = "zmprov ma {0} {1} '{2}\n".format(usuario, atributo, valor)
        self.guardar("ldif", comando)

    def __cos_id(self, usuario, line):
        '''
        Al coincidir con ^zimbraCOSId:, crea el comando necesario para asignar el COS
        del usuario en el nuevo servidor
        '''
        i = line.find(" ") + 1
        cosId = line[i:]
        cos = self.cosId[cosId]
        comando = "zmprov sac " + usuario + " " + cos + "\n"
        self.guardar("cosid", comando)
        
    
    def moldear(self):
        '''
        Este es el MÉTODO.
        Lo encontrará en los otros script como __modelado
        Este es publico porque la clase modelador es auxiliar para la clase obtener
        '''
        datos = self.datos
        ldif = "ldif"
        fcmd = "fcmd"
        while self.indice < self.attr:
            if self.marcador.match(datos[self.indice]):
                usuario = self.__cabecera(fcmd, datos[self.indice])
                self.indice +=1
            elif self.especial:
                # TODO: Si el siguiente atributo a uno de los especiales es por ejemplo uno posix, se incluira dentro del valor del atributo especial
                while not self.marcador_atributo.match(datos[self.indice]):
                    self.guardar(ldif, datos[self.indice] + "\n")
                    self.indice +=1
                self.guardar(ldif, "'\n\n")
                self.especial = False
            elif self.especiales.match(datos[self.indice]):
                print(datos[self.indice])
                self.especial = True
                self.__especiales(usuario, datos[self.indice])
                self.indice +=1
            elif self.marcador_cos.match(datos[self.indice]):
                self.__cos_id(usuario,  datos[self.indice])
                self.indice +=1
            elif not self.atributos.match(datos[self.indice]):
                self.__attrComun(fcmd, datos[self.indice])
                self.indice +=1
            else:
                self.indice +=1

class obtener(Thread):
    '''
    Se limita a envolver el comando nativo de administración zimbra 'zmprov -l ga usuario@dominio.com'
    en una clase que hereda de Thread y maneja el uso de hilos
    '''
    def __init__ (self, semaforo, user, dominio, cosId):
        Thread.__init__(self)
        self.semaforo = semaforo
        self.user = user
        self.dominio = dominio
        self.cosId = cosId

    def obtener_datos (self, user, dominio):
        '''
        Usara modelador para para obtener los datos del usuarios obtenido, y después lo guarda
        '''
        # Sacas el contenido a una variable
        # usas el guardar_fichero en run
        comando = ['zmprov', '-l', 'ga', user]
        salida = ejecutar_comando(comando)
        guardar(dominio + ".data", salida)
        # Para esto usamos la clase modelado
        modelo = modelador(salida, self.cosId)
        modelo.moldear()
        # Modelado los datos, almacenamos fisicamente los atributos 'modelo.comando', modelo.volcado', 'modelo.cosid'
        # que contiene los comandos para crear/modificar a los usuarios en el nuevo servidor
        guardar(dominio + ".cmd", modelo.comando, "l")
        guardar(dominio + ".ldif", modelo.volcado, "l")
        guardar(dominio + ".cos", modelo.cosid, "z")

    def run (self):
        self.semaforo.acquire()
        self.obtener_datos(self.user, self.dominio)
        self.semaforo.release()
        print ("Terminado " + self.user + " en " + self.getName())

if __name__ == "__main__":
    '''
    Probablemente esta implementación no sirve
    Y sería muy buena idea que la arreglaras
    '''
    if not len(s.argv)>1:
        print "Falta el fichero con los datos en bruto de los usuarios"
        s.exit(1)
    
    entrada = s.argv[1]
    salida = entrada.replace("data","cmd")
    especial = entrada.replace("data","ldif")
    # Abrimos el fichero de salida con cuidado
    try:
        ## Si lo abres en la función, que significa una apertura por pasada,
        ## se vuelve increíblemente lento
        fcmd  = open(salida, "w")
        ldif  = open(especial, "w")
        datos = open(entrada, "r")
    except IOError as error:
        print error
        s.exit(1)
    '''
Las siguientes líneas tienen por objeto obtener una entrada completa de cada usuario. 
Se toma en cuenta el inicio del tipo '# name ... ' para marcar cada nueva entrada
Supongo que existe mejores formas
        '''
    a = ""
    user = ""
    for line in datos:
        if r.match("^#\sname", line):
            user_line = line.split(" ")[2].rstrip('\n')
            datos = a.split("\n")
            moldear(ldif, fcmd, datos)
            if not user_line == user:
                a = line
                user = user_line
            else:
                a += line
        else:
            a += line
  # Obligamos a que formatee al último usuario en un archivo
  # Por la forma en que lo estamos iterando
    datos = a.split("\n")
    moldear(ldif, fcmd, datos)
