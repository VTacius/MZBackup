""" Implementación de Recolector y Parser para objeto USUARIO"""
from logging import getLogger

from mzbackup.parseros.parser import Parser
from mzbackup.parseros.recolector import Recolector

log = getLogger('MZBackup')

# REVISAR: ¿zimbraMailHost como deprecated?
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


class RecolectorUsuarios(Recolector):
    """Implementa un Recolector adecuado para USUARIO"""

    def _es_primera_linea(self, linea: str):
        if linea and linea.startswith("# name "):
            return len(linea.split(' ')) == 3 and linea.split(' ')[2].find('@', 0) > 0

        return False

    def _es_final_de_contenido(self, linea: str):
        return linea == ''


class ParserUsuario(Parser):
    """Implementa un Parser adecuado para USUARIO"""

    def _titulador(self, linea):
        linea = linea.split(' ')
        identificador = linea[2].strip()
        password = 'P@ssw0rd'
        titulo = "zmprov ca {0} {1}".format(identificador, password)
        return titulo
