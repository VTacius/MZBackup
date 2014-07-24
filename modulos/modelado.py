#!/usr/bin/python
#encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Parseado de entrada LDAP del usuario en comando zmprov:
Cambia atributo:valor a opcion:valor
'''
__author__ = "Alexander Ortiz"
__version__ = "0.7"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import re as r
import sys as s

class modelador():
    def __init__(self, usuario, cosId):
        # Marca los self.atributos que no deben ser tomados en cuenta
        self.atributos = "^(zimbraMailHost|zimbraMailTransport|zimbraFeatureNotebookEnabled|zimbraPrefCalendarReminderYMessenger|zimbraPrefReadingPaneEnabled|zimbraContactAutoCompleteEmailFields|zimbraPrefCalendarReminderSendEmail|zimbraPrefContactsInitialView|zimbraFeaturePeopleSearchEnabled|zimbraFeatureMailPollingIntervalPreferenceEnabled|zimbraPrefCalendarReminderDuration1|zimbraPrefCalendarReminderMobile|zimbraFeatureAdvancedSearchEnabled|zimbraFeatureWebSearchEnabled|zimbraPrefContactsExpandAppleContactGroups|zimbraPrefContactsDisableAutocompleteOnContactGroupMembers|zimbraFeatureShortcutAliasesEnabled|zimbraIMService|zimbraFeatureImportExportFolderEnabled|mail|zimbraCreateTimestamp|zimbraMailDeliveryAddress|objectClass|uid|userPassword|mail|zimbraId|zimbraMailAlias|zimbraLastLogonTimestamp|zimbraCOSId|$)"
        # Marca el inicio de línea  
        self.marcador  = "^#\sname"
        # Atributos cuyos valores tienen más de una línea
        self.especiales = "^(zimbraMailSieveScript|zimbraPrefMailSignature|zimbraPrefMailSignatureHTML):"
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
        if archivo == "ldif":
            self.volcado += datos
        if archivo == "fcmd":
            self.comando += datos
        if archivo == "cosid":
            self.cosid += datos


    def __cabecera(self, fcmd, line):
        usuario = line.split(" ")[2] 
        sentencia = "\n\nzmprov ca {user} Un0.D0s.Tr3s ".format(user=usuario)
        self.guardar(fcmd, sentencia)
        return usuario

    def __attrComun(self, fcmd, line):
        i = line.find(" ")
        sentencia = line[:i-1] + " '" + line[i+1:].rstrip("\n") + "' "
        self.guardar(fcmd, sentencia)

    def __dneador(self, usuario):
        l = usuario.split('@')
        uid = "uid=" + l[0] + "," + "ou=people"
        base = ",".join(["dc=" + x for x in l[1].split('.')])
        dn = uid + "," + base
        return dn

    def __cabecera_especial(self, usuario, line):
        i = line.find(" ")
        atributo = line[:i-1]
        ldif = "ldif"
        self.guardar(ldif, "\n" + "dn: " + self.__dneador(usuario) + "\n")
        self.guardar(ldif, "changetype: modify\n")
        self.guardar(ldif, "modify: " + atributo + "\n")
        self.guardar(ldif, line)

    def __especiales(self, usuario, line):
        i = line.find(" ")
        atributo = line[:i-1]
        valor = line[i+1:]
        comando = "zmprov ma " + usuario + " "+ atributo + " '" + valor
        self.guardar("ldif", comando)

    def __cos_id(self, usuario, line):
        i = line.find(" ") + 1
        cosId = line[i:]
        cos = self.cosId[cosId]
        comando = "zmprov sac " + usuario + " " + cos
        self.guardar("cosid",comando + "\n")
        
    
    def moldear(self):
        datos = self.datos
        ldif = "ldif"
        fcmd = "fcmd"
        while self.indice < self.attr:
            if r.match(self.marcador,datos[self.indice]):
                usuario = self.__cabecera(fcmd, datos[self.indice])
                self.indice +=1
            elif self.especial:
                while not r.match("^zimbra[a-zA-Z]+:\s\w+", datos[self.indice]):
                    self.guardar(ldif, "  " + datos[self.indice] + "\n")
                    self.indice +=1
                self.guardar(ldif, "'\n\n")
                self.especial = False
            elif r.match(self.especiales, datos[self.indice]):
                self.especial = True
                self.__especiales(usuario, datos[self.indice])
                self.indice +=1
            elif r.match('^zimbraCOSId:', datos[self.indice]):
                self.__cos_id(usuario,  datos[self.indice])
                self.indice +=1
            elif not r.match(self.atributos, datos[self.indice]):
                self.__attrComun(fcmd, datos[self.indice])
                self.indice +=1
            else:
                self.indice +=1

if __name__ == "__main__":
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
