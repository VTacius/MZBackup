from string import ascii_lowercase
from logging import getLogger

atributosUsuario = dict(posix=['co', 'ou', 'street', 'ou', 'st', 'description', 'telephoneNumber', 'l', 'title',
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
                        multilinea=['mail', 'zimbraCreateTimestamp', 'zimbraMailDeliveryAddress', 'objectClass',
                                    'uid', 'userPassword', 'zimbraId', 'zimbraMailAlias', 'zimbraLastLogonTimestamp'])

log = getLogger('MZBackup')


class RecolectorUsuarios:

    def __init__(self, parser, attrs):
        self.__linea_actual = None
        self.__linea_siguiente = None

        self.contenido = []
        self.fin_de_contenido = False

        self.parser = parser
        self.attrs = attrs

    def _es_primera_linea(self, linea):
        if linea and linea.startswith("# name "):
            correo = linea.split(' ')[2]
            return correo.find('@', 0) > 0

        return False

    def _es_ultima_linea(self, linea: str):
        return linea == ""

    def ultima_linea(self):
        self.contenido.append(self.__linea_actual)
        self.fin_de_contenido = True
        parser = self.parser(self.contenido, self.attrs)
        parser.procesar()
        print(parser.guardar())

    def agregar(self, linea: str):

        self.__linea_actual, self.__linea_siguiente = self.__linea_siguiente, linea.rstrip()

        if self._es_primera_linea(self.__linea_actual):
            self.contenido = []
            self.contenido.append(self.__linea_actual)
            self.fin_de_contenido = False
        elif self._es_ultima_linea(self.__linea_actual) and self._es_primera_linea(self.__linea_siguiente):
            self.contenido.append(self.__linea_actual)
            self.fin_de_contenido = True

            parser = self.parser(self.contenido, self.attrs)
            parser.procesar()
            print(parser.guardar())
        else:
            self.contenido.append(self.__linea_actual)


class ParserUsuario:
    pass
