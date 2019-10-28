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


def obtener_tipo(linea :str):
    sep = linea.find(':', 0)

    if sep == 0:
        return {tipo: 'LINEA'}

    clave = linea[:sep]

    print(clave)
    if clave in atributosUsuario['multilinea']:
        return {tipo: 'MULTILINEA'}


if __name__ == '__main__':
    contenido = open('usuario.cnt')

    for linea in contenido:
        tipo = obtener_tipo(linea)
        print(tipo)
