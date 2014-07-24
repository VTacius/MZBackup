#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Clase cos para creador de COS
'''
__author__ = "Alexander Ortiz"
__version__ = "0.7"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import json
import re
from subprocess import STDOUT,PIPE, Popen
from modulos.utilidades import guardar
from threading import Thread, Semaphore

class cos(Thread):
    cos = str()
    cosId = dict()
    
    def __init__(self, semaforo = Semaphore(1), elemento_cos = str()):
        Thread.__init__(self)
        self.semaforo = semaforo
        # Configuramos 
        self.marca = "^#\sname"
        self.atributos = "^(zimbraFeatureNotebookEnabled|zimbraPrefCalendarReminderYMessenger|zimbraPrefReadingPaneEnabled|zimbraContactAutoCompleteEmailFields|zimbraPrefCalendarReminderSendEmail|zimbraPrefContactsInitialView|zimbraFeaturePeopleSearchEnabled|zimbraFeatureMailPollingIntervalPreferenceEnabled|zimbraPrefCalendarReminderDuration1|zimbraPrefCalendarReminderMobile|zimbraProxyCacheableContentTypes|zimbraFeatureAdvancedSearchEnabled|zimbraFeatureWebSearchEnabled|zimbraPrefContactsExpandAppleContactGroups|zimbraPrefContactsDisableAutocompleteOnContactGroupMembers|zimbraFeatureShortcutAliasesEnabled|zimbraIMService|zimbraFeatureImportExportFolderEnabled|zimbraMailHostPool|zimbraCreateTimestamp|$)"
        # Los pedimos al inicializar
        self.lista = "cos.lst"
        self.cmd = "cos.cmd"
        self.data = "cos.data"
        self.fid = "cos.id"
        self.elemento_cos = elemento_cos

    def listar_Cos (self):
        exe = Popen(['zmprov','-v','gac'], stdout=PIPE)
        stdout, stdin = exe.communicate()
        self.cos = [x for x in stdout.split("\n") if len(x)>0]
        guardar(self.lista, stdout)

    def __modelado(self, contenido):
        lineas = contenido.split("\n")
        comando = str() 
        for i in lineas:
            if re.match(self.marca, i):
                nombre = i.split(" ")[2]
                comando = "\nzmprov cc " + nombre + " "
            elif re.match("^zimbraId:", i):
                id = i.split(" ")[1]
            elif not re.match(self.atributos, i):
                j = i.find(":")
                attr = i[:j] + ' "' + i[j+2:] + '" '
                comando += attr
        guardar(self.cmd, comando)
        self.cosId[id] = nombre
        
    def run(self):
        self.semaforo.acquire()
        exe = Popen(['zmprov', 'gc', self.elemento_cos], stdout=PIPE)
        stdout,stdin = exe.communicate()
        self.__modelado(stdout)
        guardar(self.data, stdout)
        self.semaforo.release()
        print ("Terminado " + self.elemento_cos + " en " + self.getName())
    
    def almacenar_Id(self):
        datos = json.dumps(self.cosId)
        guardar(self.fid, datos)
