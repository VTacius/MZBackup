import logging
from sys import stdout


def configurar_log(salida='console', verbosidad=0):
    verbosidad = verbosidad if verbosidad <= 3 else 3
    nivel = ['CRITICAL', 'ERROR', 'INFO', 'DEBUG'][verbosidad]
    formato = logging.Formatter('%(module)s.%(funcName)s: %(message)s')

    if salida == 'syslog':
        handler = logging.handlers.SysLogHandler(address='/dev/log')
    else:
        handler = logging.StreamHandler(stdout)

    nivel_verbosidad = getattr(logging, nivel)
    handler.setLevel(nivel_verbosidad)
    handler.setFormatter(formato)

    log = logging.getLogger('MZBackup')
    log.setLevel(nivel_verbosidad)
    log.addHandler(handler)

    return log
