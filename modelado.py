#!/usr/bin/python
# encoding: utf-8
'''
Librería para formateado de datos de cada usuario en una comando zmprov de creación de usuario
y entradas ldif para modificar atributos de más de una línea
:author: Alexander Ortiz
:version: 1.0
'''
import re as r
import sys as s

class modelador():

    def __init__(self, usuario):
        # Marca los self.atributos que no deben ser tomados en cuenta
        self.atributos = "^(zimbraMailHost|zimbraMailTransport|zimbraFeatureNotebookEnabled|zimbraPrefCalendarReminderYMessenger|zimbraPrefReadingPaneEnabled|zimbraContactAutoCompleteEmailFields|zimbraPrefCalendarReminderSendEmail|zimbraPrefContactsInitialView|zimbraFeaturePeopleSearchEnabled|zimbraFeatureMailPollingIntervalPreferenceEnabled|zimbraPrefCalendarReminderDuration1|zimbraPrefCalendarReminderMobile|zimbraFeatureAdvancedSearchEnabled|zimbraFeatureWebSearchEnabled|zimbraPrefContactsExpandAppleContactGroups|zimbraPrefContactsDisableAutocompleteOnContactGroupMembers|zimbraFeatureShortcutAliasesEnabled|zimbraIMService|zimbraFeatureImportExportFolderEnabled|mail|zimbraCreateTimestamp|zimbraMailDeliveryAddress|objectClass|uid|userPassword|mail|zimbraId|zimbraMailAlias|zimbraLastLogonTimestamp|zimbraCOSId|$)"
        # Marca el inicio de línea  
        self.marcador  = "^#\sname"
        # Atributos cuyos valores tienen más de una línea
        self.especiales = "^(zimbraMailSieveScript|zimbraPrefMailSignature):"
        # Bandera que marca la localización de un valor especial
        self.especial = False
        self.comando = str()
        self.volcado = str()
        self.indice = 0
        self.attr = len(usuario)
        self.datos = usuario

    def guardar(self, archivo, datos):
        '''Almacena en la propiedades volcado y comando según vaya generando resultados '''
        if archivo == "ldif":
            self.volcado += datos
        if archivo == "fcmd":
            self.comando += datos

    def __cabecera(self, fcmd, line):
        '''Crea el inicio del comando zmprov '''
        usuario = line.split(" ")[2] 
        sentencia = "\n\nzmprov ca {user} 123456 ".format(user=usuario)
        self.guardar(fcmd, sentencia)
        return usuario

    def __attrComun(self, fcmd, line):
        '''Maneja los atributos más comunes '''
        i = line.find(" ")
        sentencia = line[:i-1] + " \"" + line[i+1:].rstrip("\n") + "\" "
        self.guardar(fcmd, sentencia)

    def __dneador(self, usuario):
        '''Crea el DN del usuario a ser usado en el fichero .ldif'''
        l = usuario.split('@')
        uid = "uid=" + l[0] + "," + "ou=people"
        base = ",".join(["dc=" + x for x in l[1].split('.')])
        dn = uid + "," + base
        return dn

    def __cabecera_especial(self, usuario, line):
        '''Crea la cabecera del archivo ldif '''
        i = line.find(" ")
        atributo = line[:i-1]
        ldif = "ldif"
        self.guardar(ldif, "\n" + "dn: " + self.__dneador(usuario) + "\n")
        self.guardar(ldif, "changetype: modify\n")
        self.guardar(ldif, "modify: " + atributo + "\n")
        self.guardar(ldif, line)
    
    def moldear(self):
        '''
    Itera a traves del arreglo usuario que ha sido pasado al momento de instanciar el objeto
    Usa los metodos privados según el caso que se vaya produciendo
        '''
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
                self.especial = False
            elif r.match(self.especiales, datos[self.indice]):
                self.especial = True
                self.__cabecera_especial(usuario, datos[self.indice])
                self.indice +=1
            elif not r.match(self.atributos,datos[self.indice]):
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
