"""Ejecutor Final del parseado de ficheros"""

from string import ascii_letters, digits
from mzbackup.parseros.placebo import Parser

atributos = {'posix': ['co', 'ou', 'street', 'ou', 'st', 'description', 'telephoneNumber', 'l',
                       'title', 'company', 'givenName', 'displayName', 'cn', 'sn', 'homePhone',
                       'mobile', 'initials', 'o', 'ou', 'st'],
             'sistema': ['mail', 'zimbraCreateTimestamp', 'zimbraMailDeliveryAddress',
                         'objectClass', 'uid', 'userPassword', 'zimbraId', 'zimbraMailAlias',
                         'zimbraLastLogonTimestamp'],
             'procesal': ['zimbraCOSId'],
             'modificante': 'ma',
             'deprecated': ['zimbraMailHost', 'zimbraMailTransport',
                            'zimbraFeatureNotebookEnabled', 'zimbraPrefCalendarReminderYMessenger',
                            'zimbraPrefReadingPaneEnabled', 'zimbraContactAutoCompleteEmailFields',
                            'zimbraPrefCalendarReminderSendEmail', 'zimbraPrefContactsInitialView',
                            'zimbraFeaturePeopleSearchEnabled',
                            'zimbraFeatureMailPollingIntervalPreferenceEnabled',
                            'zimbraPrefCalendarReminderDuration1',
                            'zimbraPrefCalendarReminderMobile',
                            'zimbraFeatureAdvancedSearchEnabled',
                            'zimbraFeatureWebSearchEnabled',
                            'zimbraPrefContactsExpandAppleContactGroups',
                            'zimbraPrefContactsDisableAutocompleteOnContactGroupMembers',
                            'zimbraFeatureShortcutAliasesEnabled', 'zimbraIMService',
                            'zimbraFeatureImportExportFolderEnabled'],
             'multilinea': ['zimbraMailSieveScript', 'zimbraPrefMailSignature',
                            'zimbraPrefMailSignatureHTML', 'zimbraMailOutgoingSieveScript',
                            'zimbraPrefOutOfOfficeReply', 'zimbraPrefOutOfOfficeExternalReply',
                            'zimbraNotes']}

CONTENIDO = """# name vtacius@dominio.com
cn: Alexander Ortíz
zimbraPrefMailSignature: _________________________________________________________
Alexander Ortíz - Unidad de Redes y Seguridad Informática
Dirección de Tecnología
Companía Central

zimbraPrefMailSignatureStyle: internet

# name kpena@dominio.com
"""

def _crear_clave_valor(tokens, linea):
    """Separa a linea en clave y valor en el punto de separador"""
    sep = tokens['sep']
    clave = linea[:sep]
    valor = linea[sep + 2:]
    return clave, valor


def _crear_contenido_valido(tokens, linea):
    """Procesa un atributo - valor de cada línea, y lo entrecomilla de ser necesario"""
    clave, valor = _crear_clave_valor(tokens, linea)

    valores_no_ascii = filter(lambda x: x not in ascii_letters + digits, valor)
    necesita_espacios = len(list(valores_no_ascii)) > 0
    valor = "'{0}'".format(valor)if necesita_espacios else valor

    return " {0} {1}".format(clave, valor)

def _crear_contenido_multilinea(tokens, linea):
    """Procesa un atributo - valor de cada línea"""
    sep = tokens['sep']
    clave = tokens['mlatributo']
    valor = linea[sep + 2:]

    return clave, valor

class Ejecutante(Parser):
    """Verdadero instrumento de todo el proyecto"""
    def __init__(self, attr, forzar_ultima_linea=True):
        self.contenido = None
        self.resultado = {'comando': "", 'multilinea': {}, 'procesal': {}}
        self.identificador = None
        self._forzar_ultima_linea = forzar_ultima_linea
        Parser.__init__(self, attr)

    # ¿Es acá dónde debería estar?
    def _crear_contenido_procesal(self, tokens, linea):
        return _crear_clave_valor(tokens, linea)

    # Las tres siguientes son implementaciones reales
    def _titulador(self, linea):
        linea = linea.split(' ')
        identificador = linea[2].strip()
        password = 'P@ssw0rd'
        titulo = "zmprov ca {0} {1}".format(identificador, password)
        self.identificador = identificador
        return titulo

    def _es_primera_linea(self, linea: str):
        if linea and linea.startswith("# name "):
            return len(linea.split(' ')) == 3 and linea.split(' ')[2].find('@', 0) > 0

        return False

    def _es_final_de_contenido(self, linea: str):
        return linea == ''

    def crear_contenido(self):
        """Pues eso, que crea el contenido a conveniencia"""
        self.contenido = CONTENIDO.split("\n")

    def _parsear_linea(self, tokens, linea):
        """ Procesa cada linea según el tipo (token) asignado """
        tipo = tokens['tipo']
        if tipo == 'MULTILINEA':
            clave, valor = _crear_contenido_multilinea(tokens, linea)
            self.resultado['multilinea'][clave] = [valor]
        elif tipo in ['POSIX', 'ZIMBRA']:
            self.resultado['comando'] += _crear_contenido_valido(tokens, linea.strip())
        elif tipo == 'PROCESAL':
            clave, valor = self._crear_contenido_procesal(tokens, linea)
            self.resultado['procesal'][clave] = valor
        elif tipo == "LINEA":
            clave = tokens['mlatributo']
            self.resultado['multilinea'][clave].append(linea)

    def _ejecutar_ultima_linea(self):
        for clave, valor in self.resultado.items():
            print("\t%s:" % clave)
            print("%s" % valor)

    def _procesamiento(self, linea, tipo_pasado):
        if self._es_primera_linea(linea):
            titulo = self._titulador(linea)
            self.resultado['comando'] = titulo
        elif self._es_ultima_linea(self._linea_actual, self._linea_siguiente):
            print("Acá termina contenido")
            self._ejecutar_ultima_linea()
            self.resultado = {'comando': "", 'multilinea': {}, 'procesal': {}}
        else:
            tipo_pasado = self._asignar_tipo(linea, tipo_pasado)
            self._parsear_linea(tipo_pasado, linea)

        return tipo_pasado

    def ejecutar(self):
        """La ejecución propiamente dicha"""
        # Inicializamos tipo
        # El tipo por defecto
        tipo_pasado = {'tipo': 'DEFAULT', 'sep': 0, 'mlactivo': False, 'mlatributo': ''}
        for contenido in self.contenido:
            tipo_pasado = self._agregar(contenido, tipo_pasado)

        if self._forzar_ultima_linea:
            self._ejecutar_ultima_linea()

if __name__ == "__main__":
    recolector = Ejecutante(atributos)
    recolector.crear_contenido()
    recolector.ejecutar()
    #recolector.guardar()
