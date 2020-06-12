from utils.rutas import examinar_directorio, habilitar_directorio_local
from datetime import datetime
import click

@click.group()
def main():
    """Migración/Backup de Usuarios y Cuentas en Zimbra"""

@main.command()
@click.option('--remoto', '-r', metavar="IP address", type=str, default="10.10.20.102", help="Servidor remoto al cual enviar el backup")
@click.option("--base", "-b", help="Directorio base en Servidor Remoto")
@click.option("--envio", "-e", help="Habilita el envio a Servidor Remoto", is_flag=True)
@click.option('--fichero', '-f', metavar="contenido", type=click.File("rb"))
def usuarios(**args):
    """Backup de información de cuentas de usuarios"""
    click.echo('Empezamos con usaurio')
    print(args)


def habilitar_fichero_origen(debe_crearse, comando, args, config_destino):
    if debe_crearse:
        fichero = "{}/{}.data".format(config_destino['directorio'], config_destino['fichero'])
        contenido, error = ejecutor(comando, fichero)
        archivo = open(fichero)
    else:
        archivo = args.fichero

    return archivo

@main.command()
@click.option('--remoto', '-r', metavar="IP address", type=str, default="10.10.20.102", help="Servidor remoto al cual enviar el backup")
@click.option("--base", "-b", help="Directorio base en Servidor Remoto", default="/opt/")
@click.option("--envio", "-e", help="Habilita el envio a Servidor Remoto", is_flag=True)
@click.option('--fichero', '-f', metavar="contenido", type=click.File("rb"))
def cos(**args):
    """Backup de información de COS"""
    
    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')
    click.echo('Empezamos con cos')
    config_destino, debe_crearse = examinar_directorio("cos", args)
    config_destino = habilitar_directorio_local(debe_crearse, marca, config_destino)
    
    archivo = habilitar_fichero_origen(debe_crearse, comando, args, config_destino)
    
    recolector = RecolectorCos(config_destino, ParserCos, cos_attrs)
    comando = "zmprov gac -v"
    
    resultado = []
    for linea in archivo:
        recolector.agregar(linea)
    else:
        resultado.extend(recolector.ultima_linea())

@main.command()
@click.option('--remoto', '-r', metavar="IP address", type=str, default="10.10.20.102", help="Servidor remoto al cual enviar el backup")
@click.option("--base", "-b", help="Directorio base en Servidor Remoto")
@click.option("--envio", "-e", help="Habilita el envio a Servidor Remoto", is_flag=True)
@click.option('--fichero', '-f', metavar="contenido", type=click.File("rb"))
def listas(**args):
    """Backup de información de Listas de Distribución"""
    click.echo('Empezamos con listas')
    print(args)

if __name__ == "__main__":
    main()
