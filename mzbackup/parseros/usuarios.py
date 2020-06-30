""" Implementación de Recolector y Parser para objeto USUARIO"""
from logging import getLogger

from mzbackup.parseros.comun.recolector import Recolector
from mzbackup.parseros.comun.iterador import IteradorFichero
from mzbackup.utils.europa import Europa, guardar_contenido
from mzbackup.parseros.comun.helpers import _crear_clave_valor

log = getLogger('MZBackup')

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


class EuropaUsuario(Europa):
    """Implementación de las funcionalidades de guardado para objeto LISTA"""

    def _guardar_procesal(self, _modificante, identificador, contenido):
        if 'zimbraCOSId' in contenido:
            self.pato.archivo = 'zimbraCOSId'
            self.pato.extension = "cmd"
            valor = contenido['zimbraCOSId']
            contenido = "zmprov sac {} {}".format(identificador, valor)
            archivo = guardar_contenido(str(self.pato), contenido)
            self.archivos_creados.append(archivo)


class IteradorUsuarios(IteradorFichero):
    """Implementa un Iterador para un fichero con contenido de USUARIOS"""

    def _linea_inicia_objeto(self, linea):
        if linea and linea.startswith("# name "):
            return len(linea.split(' ')) == 3 and linea.split(' ')[2].find('@', 0) > 0

        return False


class RecolectorUsuario(Recolector):
    """Implementa un Recolector para un fichero con contenido de USUARIOS"""

    def __init__(self, tipo, iterador, datables):
        self.datables = datables
        Recolector.__init__(self, tipo, iterador)

    def _titulador(self, linea):
        linea = linea.split(' ')
        identificador = linea[2].strip()
        password = 'P@ssw0rd'
        titulo = "zmprov ca {0} {1}".format(identificador, password)
        self.identificador = identificador
        return titulo

    def _crear_contenido_procesal(self, tokens, linea):
        clave, valor = _crear_clave_valor(tokens, linea)

        if not ('zimbraCOSId' in self.datables and isinstance(self.datables, dict)):
            raise ParserError("Necesita un diccionario para datables['zimbraCOSId']")

        valor = self.datables['zimbraCOSId'].get(valor, None)
        return clave, valor


class ParserError(Exception):
    """Error personalizado para operaciones de Parseo"""
