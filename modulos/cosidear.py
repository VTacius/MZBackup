#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Clase cos para creador de COS
'''
__author__ = "Alexander Ortiz"
__version__ = "0.9"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import json
import re
from modulos.utilidades import guardar, ejecutar_comando
from subprocess import STDOUT,PIPE, Popen
from threading import Thread, Semaphore

class cos(Thread):
    '''
    Maneja una entrada resultado de `zmprov gc COS`
    La convierte en una serie de comandos para crear la lista de distribución con todos los usuarios 
    que tenía en el servidor anterior
    '''

    id = str()
    cos = str()
    cosId = dict()
    nombre = str()
    # Configuramos 
    marca = "^#\sname"
    atributos = "^(zimbraFeatureNotebookEnabled|zimbraPrefCalendarReminderYMessenger|zimbraPrefReadingPaneEnabled|zimbraContactAutoCompleteEmailFields|zimbraPrefCalendarReminderSendEmail|zimbraPrefContactsInitialView|zimbraFeaturePeopleSearchEnabled|zimbraFeatureMailPollingIntervalPreferenceEnabled|zimbraPrefCalendarReminderDuration1|zimbraPrefCalendarReminderMobile|zimbraProxyCacheableContentTypes|zimbraFeatureAdvancedSearchEnabled|zimbraFeatureWebSearchEnabled|zimbraPrefContactsExpandAppleContactGroups|zimbraPrefContactsDisableAutocompleteOnContactGroupMembers|zimbraFeatureShortcutAliasesEnabled|zimbraIMService|zimbraFeatureImportExportFolderEnabled|zimbraMailHostPool|zimbraCreateTimestamp|$)"
    
    def __init__(self, semaforo = Semaphore(1), elemento_cos = str()):
        Thread.__init__(self)
        self.semaforo = semaforo
        self.elemento_cos = elemento_cos
        self.fichero = "cos.{ext}".format

    def listar_Cos (self):
        '''
        Esta lógica que no requiere multiprocesamiento deberia estar en listado.py
        '''
        comando = ['zmprov','-v','gac']
        self.cos = ejecutar_comando(comando)
        guardar(self.fichero(ext="lst"), self.cos, "l")

    def obtener(self):
        '''
        Obtiene todos los datos relacionados a cada COS
        '''
        comando = ['zmprov', 'gc', self.elemento_cos]
        salida = ejecutar_comando(comando)
        self.almacenar(salida)
        guardar(self.fichero(ext="data"), salida, "l")
    
    def almacenar(self, datos):
        '''
        Itera sobre el conjunto de datos de cada COS y modela cada linea que va encontrando gracias a self.__modelado
        '''
       contenido = str()
       for linea in datos:
           contenido += self.__modelado(linea)
       guardar(self.fichero(ext="cmd"), contenido, "l")
       self.cosId[self.id] = self.nombre

    def __modelado(self, contenido):
        '''
        Modela cada linea con los datos solicitados
        '''
        comando = str()
        if re.match(self.marca, contenido):
            self.nombre = contenido.split(" ")[2]
            comando = "\nzmprov cc " + self.nombre + " "
        elif re.match("^zimbraId:", contenido):
            self.id = contenido.split(" ")[1]
        elif not re.match(self.atributos, contenido):
            j = contenido.find(":")
            attr = contenido[:j] + ' "' + contenido[j+2:] + '" '
            comando += attr
        return comando

    def run(self):
        self.semaforo.acquire()
        self.obtener()
        self.semaforo.release()
        print ("Terminado " + self.elemento_cos + " en " + self.getName())
    
    def almacenar_Id(self):
        '''
        Almacena el diccionario cosId:cos que usaremos en el script usuario.py 
        para poder asignar el cosId en el nuevo servidor, dado que el cosId cambia 
        en el nuevo servidor, pero los datos del usuario almacenan el cosId
        '''
        datos = json.dumps(self.cosId)
        guardar(self.fichero(ext="id"), datos)
