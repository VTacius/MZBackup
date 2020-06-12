from logging import getLogger
from mzbackup.parseros.comun import Parser
from mzbackup.parseros.comun import Recolector

log = getLogger('MZBackup')

# TODO: ¿zimbraMailHost como deprecated?
atributos = dict(posix=['co', 'ou', 'street', 'ou', 'st', 'description', 'telephoneNumber', 'l', 'title',
                        'company', 'givenName', 'displayName', 'cn', 'sn', 'homePhone', 'mobile', 'initials',
                        'o', 'ou', 'st'],
                 sistema=['mail', 'zimbraCreateTimestamp', 'zimbraMailDeliveryAddress', 'objectClass',
                          'uid', 'userPassword', 'zimbraId', 'zimbraMailAlias', 'zimbraLastLogonTimestamp'],
                 procesal=['zimbraCOSId'],
                 deprecated=['zimbraMailHost', 'zimbraMailTransport', 'zimbraFeatureNotebookEnabled',
                             'zimbraPrefCalendarReminderYMessenger', 'zimbraPrefReadingPaneEnabled'
                             'zimbraContactAutoCompleteEmailFields', 'zimbraPrefCalendarReminderSendEmail',
                             'zimbraPrefContactsInitialView', 'zimbraFeaturePeopleSearchEnabled',
                             'zimbraFeatureMailPollingIntervalPreferenceEnabled',
                             'zimbraPrefCalendarReminderDuration1', 'zimbraPrefCalendarReminderMobile',
                             'zimbraFeatureAdvancedSearchEnabled', 'zimbraFeatureWebSearchEnabled',
                             'zimbraPrefContactsExpandAppleContactGroups',
                             'zimbraPrefContactsDisableAutocompleteOnContactGroupMembers',
                             'zimbraFeatureShortcutAliasesEnabled',
                             'zimbraIMService', 'zimbraFeatureImportExportFolderEnabled'],
                 multilinea=['zimbraMailSieveScript', 'zimbraPrefMailSignature', 'zimbraPrefMailSignatureHTML',
                             'zimbraMailOutgoingSieveScript', 'zimbraPrefOutOfOfficeReply',
                             'zimbraPrefOutOfOfficeExternalReply', 'zimbraNotes'])


class RecolectorUsuarios(Recolector):

    def _es_primera_linea(self, linea: str):
        if linea and linea.startswith("# name "):
            return len(linea.split(' ')) == 3 and linea.split(' ')[2].find('@', 0) > 0

    def _es_ultima_linea(self, linea: str):
        return linea == ''


class ParserUsuario(Parser):

    def _titulador(self, linea):
        contenido = linea.split(' ')
        usuario = contenido[2]
        self.usuario = contenido[2]
        password = 'P@ssw0rd'
        return "zmprov ca {0} {1}".format(usuario.strip(), password)

    def _crear_contenido_procesal(self, tokens, linea):
        # TODO: Una implementación real podría ser necesaria
        sep = tokens['sep']
        clave = linea[:sep]
        valor = linea[sep + 2:]
        return clave, valor
