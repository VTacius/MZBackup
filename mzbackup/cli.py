from mzbackup.parseros.cos import RecolectorCos, atributos as cos_attrs, ParserCos
from mzbackup.parseros.listas import RecolectorListas, atributos as lista_attrs, ParserLista
from mzbackup.parseros.usuarios import RecolectorUsuarios, atributos as usuario_attrs, ParserUsuario

from mzbackup.mzbackup import Ejecutor

from mzbackup.utils.pato import Pato
from mzbackup.utils.comandos import ejecutor
from mzbackup.utils.registro import configurar_log
from datetime import datetime
from logging import getLogger
import click


class ErrorSistemaLocal(Exception):
    pass


@click.group()
def main():
    """Migración/Backup de Usuarios y Cuentas en Zimbra"""


def opciones(funcion):
    funcion = click.option('--remoto', '-r', metavar="IP address", type=str, default="10.10.20.102", help="Servidor remoto al cual enviar el backup")(funcion)
    funcion = click.option("--base", "-b", metavar="directorio remoto", default="/opt/backup", help="Directorio base en SerEjecutorRemoto")(funcion)
    funcion = click.option("--envio", "-e", help="Habilita el envio a Servidor Remoto", is_flag=True)(funcion)
    funcion = click.option('--fichero', '-f', metavar="contenido", type=click.File("rb"))(funcion)
    funcion = click.option('--verbose', '-v', count=True)(funcion)
    funcion = click.option('--salida', '-s', type=click.Choice(['console', 'system'], case_sensitive=True), default="console")(funcion)

    return funcion


def enviar_remoto(debe_enviarse, pato, ficheros):
    log = getLogger('MZBackup')
    if not debe_enviarse:
        log.info("Operacion de Envío: No se habilito el envio de los ficheros al servidor remoto")
        return 0

    log.info("Operación de Envío: Creación de directorio remoto")
    ejecutor = Ejecutor("10.10.20.202:22")
    ejecutor.crear_directorio(pato.base, pato.directorio)
    for fichero in ficheros:
        log.debug("> Enviando {}".format(fichero))
        ejecutor.enviar_archivo(fichero, pato.ruta())


def habilitar_fichero_contenido(pato, comando):
    log = getLogger('MZBackup')

    if pato.debe_crearse:
        pato.extension = "data"
        log.debug("> Creando el fichero {}".format(pato))
        contenido, error = ejecutor(comando, str(pato))
        if error:
            raise ErrorSistemaLocal(error)
        archivo = open(str(pato))
    else:
        archivo = pato.fichero

    return archivo


def operacion_principal(pato, recolector, comando):
    log = getLogger('MZBackup')

    log.info('Operacion Principal: Habilitando directorios de salida')
    pato.habilitar_directorio_local()

    log.info('Operacion Principal: Habilitando ficheros con contenido')
    archivo = habilitar_fichero_contenido(pato, comando)

    log.info('Operacion Principal: Recolectando Información desde ficheros')
    ficheros_creados = [archivo.name]
    recolector.configurar_destino(pato)

    for linea in archivo:
        recolector.agregar(linea)
    else:
        ficheros_creados.extend(recolector.ultima_linea())

    return {*ficheros_creados}


@main.command()
@opciones
def cos(**args):
    """Backup de información de COS"""
    log = configurar_log(verbosidad=args['verbose'])
    log.info("Empiezan operaciones para backup de usuarios")

    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')

    try:
        pato = Pato('cos', marca, args)
        recolector = RecolectorCos(ParserCos, cos_attrs)
        ficheros_creados = operacion_principal(pato, recolector, "zmprov gac -v")
        enviar_remoto(args['envio'], pato, ficheros_creados)
    except Exception as e:
        log.error(e)
        exit(1)


@main.command()
@opciones
def listas(**args):
    """Backup de información de Listas de Distribución"""
    click.echo('Empezamos con listas')
    print(args)


@main.command()
@opciones
def usuarios(**args):
    """Backup de información de cuentas de usuarios"""
    click.echo('Empezamos con usuario')
    print(args)


if __name__ == "__main__":
    main()
