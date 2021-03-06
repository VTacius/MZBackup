"""Punto de entrada para MZBackup"""

from collections import namedtuple
from datetime import datetime
from sys import exit as salida
from json import loads

import traceback
import click

from mzbackup.utils.pato import Pato, PatoRemoto
from mzbackup.utils.comandos import EjecutorLocal
from mzbackup.utils.registro import configurar_log
from mzbackup.utils.registro import get_logger

from mzbackup.instrumentos import enviar_remoto
from mzbackup.instrumentos import ParserFactory
from mzbackup.parseros.comun.helpers import ParserError
from mzbackup.utils.comandos import SistemLocalError

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


ComponentesNombre = namedtuple(
    "ComponentesNombre", ["timestamp", "base_fichero", "directorio_base"])

def operacion_principal(nombre, tipo_objeto, comando, args, datos):
    """ Instrumentaliza todo el trabajo en un sólo lugar"""
    log = get_logger()
    debe_enviarse = args['envio']
    fichero = args['fichero']

    pato = Pato(nombre.base_fichero, nombre.timestamp, args)
    pato_remoto = PatoRemoto(nombre.base_fichero, nombre.timestamp, nombre.directorio_base,
                             args['remoto'])

    try:
        recolector = object
        if pato.debe_crearse:
            recolector = ParserFactory.desde_comando(tipo_objeto, comando, pato, datos)
        else:
            recolector = ParserFactory.desde_fichero(tipo_objeto, fichero, pato, datos)

        log.info('Operacion Principal: Recolectando Información desde ficheros')
        recolector.procesar_contenido()
        ficheros_creados = recolector.listar_archivos()
        # TODO: ¿Dónde esta el fichero con los datos?
        enviar_remoto(debe_enviarse, pato_remoto, ficheros_creados)
    except ParserError as mistake:
        log.error(mistake)
        salida(1)
    except SistemLocalError as mistake:
        log.error(mistake)
        traceback.print_exc()
        salida(1)
    return 1


@main.command()
@opciones
def cos(**args):
    """Backup de información de COS"""
    log = configurar_log(verbosidad=args['verbose'])
    log.info("Empiezan operaciones para backup de COS")

    nombre_objeto = 'cos'
    comando = "zmprov gac -v"
    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')
    nombre = ComponentesNombre(marca, nombre_objeto, args['base'])

    operacion_principal(nombre, nombre_objeto, comando, args, {})


@main.command()
@opciones
def listas(**args):
    """Backup de información de LISTAS"""
    log = configurar_log(verbosidad=args['verbose'])
    log.info("Empiezan operaciones para backup de LISTAS")

    nombre_objeto = 'listas'
    comando = "zmprov -l gadl -v"
    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')
    nombre = ComponentesNombre(marca, nombre_objeto, args['base'])

    operacion_principal(nombre, nombre_objeto, comando, args, {})


def listar_dominios():
    """Consigue los dominios disponibles para el sistema"""
    comando = "zmprov gad"
    ejecutor_local = EjecutorLocal(comando)
    resultado = ejecutor_local.obtener_resultado()
    return [x.strip() for x in resultado]


@main.command()
@opciones
@click.option('--cos', '-c', type=click.File('r'), required=True)
def usuarios(**args):
    """Backup de información de USUARIOS"""
    log = configurar_log(verbosidad=args['verbose'])
    log.info("Empiezan operaciones para backup de USUARIOS")

    nombre_objeto = 'usuarios'
    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')

    log.info("Se listan los dominios del sistema")
    dominios = listar_dominios()

    log.info("Conseguidos los COSID")
    contenido = args['cos'].read()
    datables = {'zimbraCOSId': loads(contenido)}
    datos = {'datables': datables}

    for dominio in dominios:
        nombre = ComponentesNombre(marca, dominio, args['base'])
        comando = "zmprov -l gaa -v {}".format(dominio)
        operacion_principal(nombre, nombre_objeto, comando, args, datos)


if __name__ == "__main__":
    main()
