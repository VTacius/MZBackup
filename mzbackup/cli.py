from mzbackup.parseros.cos import RecolectorCos, atributos as cos_attrs, ParserCos
from mzbackup.parseros.listas import RecolectorListas, atributos as lista_attrs, ParserLista
from mzbackup.parseros.usuarios import RecolectorUsuarios, atributos as usuario_attrs, ParserUsuario

from mzbackup.utils.rutas import examinar_directorio, habilitar_directorio_local
from mzbackup.utils.comandos import ejecutor
from datetime import datetime
import click


class ErrorSistemaLocal(Exception):
    pass


@click.group()
def main():
    """Migración/Backup de Usuarios y Cuentas en Zimbra"""


def opciones(funcion):
    funcion = click.option('--remoto', '-r', metavar="IP address", type=str, default="10.10.20.102", help="Servidor remoto al cual enviar el backup")(funcion)
    funcion = click.option("--base", "-b", metavar="directorio remoto", default="/home/vtacius/", help="Directorio base en Servidor Remoto")(funcion)
    funcion = click.option("--envio", "-e", help="Habilita el envio a Servidor Remoto", is_flag=True)(funcion)
    funcion = click.option('--fichero', '-f', metavar="contenido", type=click.File("rb"))(funcion)

    return funcion


@main.command()
@opciones
def usuarios(**args):
    """Backup de información de cuentas de usuarios"""
    click.echo('Empezamos con usaurio')
    print(args)


def habilitar_fichero_contenido(debe_crearse, comando, args, config_destino):
    if debe_crearse:
        fichero = "{}/{}.data".format(config_destino['directorio'], config_destino['fichero'])
        contenido, error = ejecutor(comando, fichero)
        if error:
            raise ErrorSistemaLocal(error)
        archivo = open(fichero)
    else:
        archivo = args.fichero

    return archivo


def operacion_principal(args, objeto, Recolector, Parser, attrs, comando):
    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')

    config_destino_remoto, debe_crearse = examinar_directorio(objeto, args)
    config_destino_remoto = habilitar_directorio_local(debe_crearse, marca, config_destino_remoto)

    recolector = Recolector(config_destino_remoto, Parser, attrs)

    archivo = habilitar_fichero_contenido(debe_crearse, comando, args, config_destino_remoto)

    ficheros_creados = []
    for linea in archivo:
        recolector.agregar(linea)
    else:
        ficheros_creados.extend(recolector.ultima_linea())

    return {*ficheros_creados}


def enviar_remoto(ficheros):
    for f in ficheros:
        print("Voy a enviar a {}".format(f))


@main.command()
@opciones
def cos(**args):
    """Backup de información de COS"""
    try:
        #ficheros = operacion_principal(args, "cos", RecolectorCos, ParserCos, cos_attrs, "zmprov gac -v")
        ficheros = operacion_principal(args, "cos", RecolectorCos, ParserCos, cos_attrs, "cat /home/vtacius/public_html/MZBackup/mzbackup/cos.datica")
        if args['envio']:
            enviar_remoto(ficheros)
    except ErrorSistemaLocal as e:
        print(type(e), e)
        exit()


@main.command()
@opciones
def listas(**args):
    """Backup de información de Listas de Distribución"""
    click.echo('Empezamos con listas')
    print(args)


if __name__ == "__main__":
    main()