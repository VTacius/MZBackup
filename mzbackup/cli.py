"""Punto de entrada para MZBackup"""
import traceback
from datetime import datetime

import click

from mzbackup.parseros.cos import RecolectorCos, atributos as cos_attrs, ParserCos

from mzbackup.parseros.cos import EuropaCos

from mzbackup.mzbackup import Ejecutor

from mzbackup.utils.pato import Pato, PatoRemoto
from mzbackup.utils.comandos import ejecutor
from mzbackup.utils.registro import configurar_log
from mzbackup.utils.registro import get_logger

class ErrorSistemaLocal(Exception):
    """Error personalizado"""


@click.group()
def main():
    """Migración/Backup de Usuarios y Cuentas en Zimbra"""


def opciones(funcion):
    """Decorador que agrupa un conjunto de decoradores comunes a algunos subcomandos"""
    funcion = click.option('--remoto', '-r', metavar="IP:PORT",
                           type=str, default="10.10.20.202:22",
                           help="Servidor remoto al cual enviar el backup")(funcion)
    funcion = click.option("--base", "-b", metavar="directorio remoto",
                           default="/opt/backup",
                           help="Directorio base en SerEjecutorRemoto")(funcion)
    funcion = click.option("--envio", "-e",
                           help="Habilita el envio a Servidor Remoto", is_flag=True)(funcion)
    funcion = click.option('--fichero', '-f',
                           metavar="contenido", type=click.File("r"))(funcion)
    funcion = click.option('--verbose', '-v', count=True)(funcion)
    funcion = click.option('--salida', '-s',
                           type=click.Choice(['console', 'system'], case_sensitive=True),
                           default="console")(funcion)

    return funcion


def enviar_remoto(debe_enviarse, servidor_remoto, pato, ficheros):
    """Se instrumentaliza el envío de ficheros al servidor remoto"""
    log = get_logger()
    if not debe_enviarse:
        log.info("Operacion de Envío: No se habilito el envio de los ficheros al servidor remoto")
        return 1

    log.info("Operación de Envío: Creación de directorio remoto")
    remoto = Ejecutor(servidor_remoto)
    remoto.crear_directorio(pato.base, pato.directorio)
    for fichero in ficheros:
        log.debug("> Enviando %s a %s" % (fichero, pato.ruta()))
        remoto.enviar_archivo(fichero, pato.ruta())

    return 0

def habilitar_fichero_contenido(pato, comando):
    """Crear el fichero con contenido proveniente de un comando, si es que no existe"""
    log = get_logger()

    if pato.debe_crearse:
        pato.extension = "data"
        log.debug("> Creando el fichero %s" % str(pato))
        _contenido, error = ejecutor(comando, str(pato))
        if error:
            raise ErrorSistemaLocal(error)
        archivo = open(str(pato))
    else:
        archivo = pato.fichero

    return archivo


def operacion_principal(pato, europa, recolector: RecolectorCos, comando):
    """Define las operaciones para la mayoría de subcomandos"""
    log = get_logger()

    log.info('Operacion Principal: Habilitando directorios de salida')
    pato.habilitar_directorio_local()

    log.info('Operacion Principal: Habilitando ficheros con contenido')
    archivo = habilitar_fichero_contenido(pato, comando)

    log.info('Operacion Principal: Recolectando Información desde ficheros')
    #ficheros_creados = [archivo.name]
    recolector.configurar_destino(europa)

    for linea in archivo:
        recolector.agregar(linea)
    
    recolector.ultima_linea()

    return {*recolector.destino.listar_archivos()}


@main.command()
@opciones
def cos(**args):
    """Backup de información de COS"""
    log = configurar_log(verbosidad=args['verbose'])
    log.info("Empiezan operaciones para backup de COS")

    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')

    try:
        pato = Pato('cos', marca, args)
        pato_remoto = PatoRemoto('cos', marca, args['base'])
        europa = EuropaCos(pato, cos_attrs['modificante'])
        recolector = RecolectorCos(ParserCos, cos_attrs)
        ficheros_creados = operacion_principal(pato, europa, recolector, "zmprov gac -v")
        enviar_remoto(args['envio'], args['remoto'], pato_remoto, ficheros_creados)
    except Exception as mistake:
        log.error(mistake)
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
