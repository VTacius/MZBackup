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

    
    def __init__(self, semaforo = Semaphore(5), elemento_cos = str()):
        # Iniciamos los valores que hemos de llenar
        self.id = str()
        self.cos = str()
        self.cosId = dict()
        self.nombre = str()
        # Compilamos las expresiones regulares a usar
        self.marca = re.compile('^#\sname')
        self.zimbraId = re.compile('^zimbraId:')
        self.atributos = re.compile('^(zimbraFeatureNotebookEnabled|zimbraPrefCalendarReminderYMessenger|zimbraPrefReadingPaneEnabled|zimbraContactAutoCompleteEmailFields|zimbraPrefCalendarReminderSendEmail|zimbraPrefContactsInitialView|zimbraFeaturePeopleSearchEnabled|zimbraFeatureMailPollingIntervalPreferenceEnabled|zimbraPrefCalendarReminderDuration1|zimbraPrefCalendarReminderMobile|zimbraProxyCacheableContentTypes|zimbraFeatureAdvancedSearchEnabled|zimbraFeatureWebSearchEnabled|zimbraPrefContactsExpandAppleContactGroups|zimbraPrefContactsDisableAutocompleteOnContactGroupMembers|zimbraFeatureShortcutAliasesEnabled|zimbraIMService|zimbraFeatureImportExportFolderEnabled|zimbraMailHostPool|zimbraCreateTimestamp|$)')

        Thread.__init__(self)
        self.semaforo = semaforo
        self.elemento_cos = elemento_cos
        self.fichero = "cos.{ext}".format

    def obtener_datos(self):
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
        if self.marca.match(contenido):
            self.nombre = contenido.split(" ")[2]
            comando = "\nzmprov cc " + self.nombre + " "
        elif self.marca.match(contenido):
            self.id = contenido.split(" ")[1]
        elif not self.atributos.match(contenido):
            j = contenido.find(":")
            attr = contenido[:j] + ' "' + contenido[j+2:] + '" '
            comando += attr
        return comando

    def run(self):
        self.semaforo.acquire()
        self.obtener_datos()
        self.semaforo.release()
        print ("Terminado " + self.elemento_cos + " en " + self.getName())
    
