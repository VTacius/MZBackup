import logging
from sys import stdout

TRACE_LEVEL_NUM = 5

LEVEL = {'CRITICAL': 50,
            'ERROR': 40,
            'INFO': 20,
            'DEBUG': 10,
            'TRACE': TRACE_LEVEL_NUM}


def trace(self, message, *args, **kws):
    """Nivel loggin personalizado. Más que nada, porque permite ser más {{dialectico}}"""
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(TRACE_LEVEL_NUM, message, args, **kws)


logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
logging.Logger.trace = trace


def configurar_log(salida='console', verbosidad=0):
    """Helper que facilita la configuración en la raíz de la aplicación"""
    verbosidad = verbosidad if verbosidad <= 4 else 4
    nivel = ['CRITICAL', 'ERROR', 'INFO', 'DEBUG', 'TRACE'][verbosidad]
    formato = logging.Formatter('%(module)s.%(funcName)s: %(message)s')

    if salida == 'syslog':
        handler = logging.handlers.SysLogHandler(address='/dev/log')
    else:
        handler = logging.StreamHandler(stdout)

    nivel_verbosidad = LEVEL.get(nivel)
    handler.setLevel(nivel_verbosidad)
    handler.setFormatter(formato)

    log = logging.getLogger('MZBackup')
    log.setLevel(nivel_verbosidad)
    log.addHandler(handler)

    return log
