""" Implementación de Recolector y Parser para objeto USUARIO"""
from logging import getLogger

from mzbackup.parseros.parser import Parser, ParserError, _crear_clave_valor
from mzbackup.parseros.recolector import Recolector
from mzbackup.utils.europa import AbstractEuropa, guardar_contenido

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


class EuropaUsuario(AbstractEuropa):
    """Implementación de las funcionalidades de guardado para objeto LISTA"""

    def _guardar_procesal(self, _modificante, identificador, contenido):
        if 'zimbraCOSId' in contenido:
            self.pato.archivo = 'zimbraCOSId'
            self.pato.extension = "cmd"
            contenido = "zmprov sac {} {}".format(identificador, contenido['zimbraCOSId'])
            archivo = guardar_contenido(str(self.pato), contenido)
            self.archivos_creados.append(archivo)


class RecolectorUsuarios(Recolector):
    """Implementa un Recolector adecuado para USUARIO"""

    def _es_primera_linea(self, linea: str):
        if linea and linea.startswith("# name "):
            return len(linea.split(' ')) == 3 and linea.split(' ')[2].find('@', 0) > 0

        return False


class ParserUsuario(Parser):
    """Implementa un Parser adecuado para USUARIO"""

    def _titulador(self, linea):
        if linea is None:
            raise ParserError("Revise el formato del fichero con los datos de entrada")
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
