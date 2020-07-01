"""Punto de entrada para MZBackup"""

from datetime import datetime
from sys import exit as salida
from json import loads

import traceback
import click


from mzbackup.parseros.comun.helpers import ParserError

from mzbackup.parseros.usuarios import RecolectorUsuarios, EuropaUsuario, ParserUsuario
from mzbackup.parseros.usuarios import atributos as usuarios_attrs

from mzbackup.parseros.cos import RecolectorCos, atributos as cos_attrs, ParserCos
from mzbackup.parseros.cos import EuropaCos

from mzbackup.parseros.listas import RecolectorListas, atributos as listas_attrs, ParserLista
from mzbackup.parseros.listas import EuropaLista

from mzbackup.mzbackup import Ejecutor

from mzbackup.utils.pato import Pato, PatoRemoto
from mzbackup.utils.comandos import ejecutor
from mzbackup.utils.registro import configurar_log
from mzbackup.utils.registro import get_logger


class SistemLocalError(Exception):
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


def enviar_remoto(debe_enviarse, pato, ficheros):
    """Se instrumentaliza el envío de ficheros al servidor remoto"""
    log = get_logger()
    if not debe_enviarse:
        log.info("Operacion de Envío: No se habilito el envio de los ficheros al servidor remoto")
        return 1

    log.info("Operación de Envío: Creación de directorio remoto")
    remoto = Ejecutor(pato.servidor_remoto)
    remoto.crear_directorio(pato.base, pato.directorio)

    log.info("Operación de Envío: Envío de ficheros")
    for fichero in ficheros:
        log.debug("> Enviando %s a %s", fichero, pato.ruta())
        remoto.enviar_archivo(fichero, pato.ruta())

    return 0


def habilitar_fichero_contenido(pato, comando):
    """Crear el fichero con contenido proveniente de un comando, si es que no existe"""
    log = get_logger()

    if pato.debe_crearse:
        pato.extension = "data"
        log.debug("> Creando el fichero %s", str(pato))
        _contenido, error = ejecutor(comando, str(pato))
        if error:
            raise SistemLocalError(error)
        archivo = open(str(pato))
    else:
        archivo = pato.fichero

    return archivo


def recolectar_ficheros(recolector, archivo, europa):
    """Toma cada fichero, recolecta cada línea, la parsea. Guarda todo en ficheros
    y retorno la lista de tales ficheros"""
    recolector.configurar_destino(europa)

    for linea in archivo:
        recolector.agregar(linea)

    recolector.ultima_linea()

    return recolector.destino.listar_archivos()


def operacion_principal(debe_enviarse, rutas, europa, recolector, comando):
    """Define las operaciones para la mayoría de subcomandos"""
    log = get_logger()
    pato = rutas['local']
    pato_remoto = rutas['remoto']

    log.info('Operacion Principal: Habilitando directorios de salida')
    pato.habilitar_directorio_local()

    log.info('Operacion Principal: Habilitando ficheros con contenido')
    archivo_datos = habilitar_fichero_contenido(pato, comando)

    log.info('Operacion Principal: Recolectando Información desde ficheros')
    ficheros_recolectados = recolectar_ficheros(recolector, archivo_datos, europa)
    archivos_creados = (archivo_datos.name, *ficheros_recolectados)

    enviar_remoto(debe_enviarse, pato_remoto, archivos_creados)

    return archivos_creados


@main.command()
@opciones
def cos(**args):
    """Backup de información de COS"""
    log = configurar_log(verbosidad=args['verbose'])
    log.info("Empiezan operaciones para backup de COS")

    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')
    nombre_objeto = 'cos'

    pato = {}
    pato['local'] = Pato(nombre_objeto, marca, args)
    pato['remoto'] = PatoRemoto(nombre_objeto, marca, args['base'], args['remoto'])

    comando = "zmprov gac -v"

    try:
        europa = EuropaCos(pato['local'], cos_attrs['modificante'])
        recolector = RecolectorCos(ParserCos, cos_attrs)
        operacion_principal(args['envio'], pato, europa, recolector, comando)
    except ParserError as mistake:
        log.error(mistake)
        salida(1)
    except SistemLocalError as mistake:
        log.error(mistake)
        traceback.print_exc()
        salida(1)


@main.command()
@opciones
def listas(**args):
    """Backup de información de LISTAS"""
    log = configurar_log(verbosidad=args['verbose'])
    log.info("Empiezan operaciones para backup de LISTAS")

    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')
    nombre_objeto = 'listas'

    pato = {}
    pato['local'] = Pato(nombre_objeto, marca, args)
    pato['remoto'] = PatoRemoto(nombre_objeto, marca, args['base'], args['remoto'])

    comando = "zmprov -l gadl -v"

    try:
        europa = EuropaLista(pato['local'], listas_attrs['modificante'])
        recolector = RecolectorListas(ParserLista, cos_attrs)
        operacion_principal(args['envio'], pato, europa, recolector, comando)
    except ParserError as mistake:
        log.error(mistake)
    except SistemLocalError as mistake:
        log.error(mistake)
        traceback.print_exc()
        salida(1)


def listar_dominios():
    """Consigue los dominios disponibles para el sistema"""
    comando = "zmprov gad"
    resultado, error = ejecutor(comando)
    if error:
        raise SistemLocalError(error)

    return [x.strip() for x in resultado]


@main.command()
@opciones
@click.option('--cos', '-c', type=click.File('r'), required=True)
def usuarios(**args):
    """Backup de información de USUARIOS"""
    log = configurar_log(verbosidad=args['verbose'])
    log.info("Empiezan operaciones para backup de USUARIOS")

    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')
    nombre_objeto = 'usuarios'

    pato = {}
    pato['local'] = Pato(nombre_objeto, marca, args)
    pato['remoto'] = PatoRemoto(nombre_objeto, marca, args['base'], args['remoto'])

    log.info("Se listan los dominios del sistema")
    dominios = listar_dominios()

    contenido = args['cos'].read()
    datables = {'zimbraCOSId': loads(contenido)}
    for dominio in dominios:
        comando = "zmprov -l gaa -v {}".format(dominio)
        pato['local'].archivo = dominio
        log.info("Se trabaja sobre la lista de usuarios %s", dominio)
        try:
            europa = EuropaUsuario(pato['local'], listas_attrs['modificante'])
            recolector = RecolectorUsuarios(ParserUsuario, usuarios_attrs, datables)
            operacion_principal(args['envio'], pato, europa, recolector, comando)
        except ParserError as mistake:
            log.error(mistake)
            salida(1)
        except SistemLocalError as mistake:
            log.error(mistake)
            traceback.print_exc()
            salida(1)


if __name__ == "__main__":
    main()
