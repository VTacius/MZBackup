"""Habilitar el logger MZBackup para el sistema. Incluye un nivel personalizado trace"""
from sys import stdout

import logging

TRACE_LEVEL_NUM = 5

LEVEL = {'CRITICAL': 50,
         'ERROR': 40,
         'INFO': 20,
         'DEBUG': 10,
         'TRACE': TRACE_LEVEL_NUM}

class ExtendedLogger(logging.Logger):
    """Añade un nivel trace"""
    def __init__(self, name):
        logging.Logger.__init__(self, name)

    def trace(self, message, *args, **kws):
        """Nivel loggin personalizado. Más que nada, porque permite ser más semántico"""
        if self.isEnabledFor(TRACE_LEVEL_NUM):
            self._log(TRACE_LEVEL_NUM, message, args, **kws)


logging.setLoggerClass(ExtendedLogger)
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")

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

def get_logger():
    """Devuelve un logger con la clase personalizada"""
    logging.setLoggerClass(ExtendedLogger)
    logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")

    return logging.getLogger('MZBackup')
