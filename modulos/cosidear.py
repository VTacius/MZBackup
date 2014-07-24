#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Clase cos para creador de COS
'''
__author__ = "Alexander Ortiz"
__version__ = "0.8"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import json
import re
from modulos.utilidades import guardar, ejecutar_comando
from subprocess import STDOUT,PIPE, Popen
from threading import Thread, Semaphore

class cos(Thread):
    cos = str()
    cosId = dict()
    nombre = str()
    id = str()
    # Configuramos 
    marca = "^#\sname"
    atributos = "^(zimbraFeatureNotebookEnabled|zimbraPrefCalendarReminderYMessenger|zimbraPrefReadingPaneEnabled|zimbraContactAutoCompleteEmailFields|zimbraPrefCalendarReminderSendEmail|zimbraPrefContactsInitialView|zimbraFeaturePeopleSearchEnabled|zimbraFeatureMailPollingIntervalPreferenceEnabled|zimbraPrefCalendarReminderDuration1|zimbraPrefCalendarReminderMobile|zimbraProxyCacheableContentTypes|zimbraFeatureAdvancedSearchEnabled|zimbraFeatureWebSearchEnabled|zimbraPrefContactsExpandAppleContactGroups|zimbraPrefContactsDisableAutocompleteOnContactGroupMembers|zimbraFeatureShortcutAliasesEnabled|zimbraIMService|zimbraFeatureImportExportFolderEnabled|zimbraMailHostPool|zimbraCreateTimestamp|$)"
    
    def __init__(self, semaforo = Semaphore(1), elemento_cos = str()):
        Thread.__init__(self)
        self.semaforo = semaforo
        self.elemento_cos = elemento_cos
        self.fichero = "cos.{ext}".format

    def listar_Cos (self):
        comando = ['zmprov','-v','gac']
        self.cos = ejecutar_comando(comando)
        guardar(self.fichero(ext="lst"), self.cos, "l")

    def obtener(self):
        comando = ['zmprov', 'gc', self.elemento_cos]
        salida = ejecutar_comando(comando)
        self.almacenar(salida)
        guardar(self.fichero(ext="data"), salida, "l")
    
    def almacenar(self, datos):
       contenido = str()
       for linea in datos:
           contenido += self.__modelado(linea)
       guardar(self.fichero(ext="cmd"), contenido, "l")
       self.cosId[self.id] = self.nombre

    def __modelado(self, contenido):
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
        datos = json.dumps(self.cosId)
        guardar(self.fichero(ext="id"), datos)
