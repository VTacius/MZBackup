"""Ejecutor Final del parseado de ficheros"""

from string import ascii_letters, digits
from mzbackup.parseros.iterante import Iterante

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


class IteranteUsuario(Iterante):
    """
    Implementación de un iterador para tipo USUARIO
    """

    def _es_linea_inicio_contenido(self, linea):
        """
        Describe el formato que una linea debe tener para considerarse inicio de contenido
        """
        print(linea)
        if linea and linea.startswith("# name "):
            veredicto = len(linea.split(' ')) == 3 and linea.split(' ')[2].find('@', 0) > 0
            print(veredicto)
            print(self._linea_siguiente)
            print(self._linea_siguiente)
            print(self._contenido_presente)
            print(self._contenido_presente)
            return veredicto

        return False

class Ejecutante:
    """Verdadero instrumento de todo el proyecto"""
    def __init__(self, tipo, iterador):
        self.resultado = {'comando': "", 'multilinea': {}, 'procesal': {}}
        self.identificador = None
        self.iterador = iterador
        self.tipo = tipo

    def _crear_contenido_procesal(self, tokens, linea):
        return _crear_clave_valor(tokens, linea)

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

    def _titulador(self, linea):
        linea = linea.split(' ')
        identificador = linea[2].strip()
        password = 'P@ssw0rd'
        titulo = "zmprov ca {0} {1}".format(identificador, password)
        self.identificador = identificador
        return titulo

    def _procesa_linea(self, linea):
        if self.iterador.contenido_inicia():
            titulo = self._titulador(linea)
            self.resultado['comando'] = titulo
        elif self.iterador.contenido_finaliza():
            # Antes de reiniciar, es necesario guardar esto
            print(self.resultado)
            self.resultado = {'comando': "", 'multilinea': {}, 'procesal': {}}
            self.tipo.fin_contenido()
        else:
            tokens = self.tipo.obtener_tipo(linea)
            #print(tokens)
            self._parsear_linea(tokens, linea)

    def procesar_contenido(self):
        """Itera sobre el contenido y procesa cada línea"""
        for linea in self.iterador:
            #print("En procesar: Esta es la linea %s" % linea)
            self._procesa_linea(linea)

    def configurar_contenido(self, contenido):
        """Permite configurar el archivo sobre el cual se trabaja"""
        self.iterador.configurar_contenido(contenido)
