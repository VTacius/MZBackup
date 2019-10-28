from argparse import ArgumentParser
from argparse import FileType

from parseros.usuarios import RecolectorUsuarios, atributosUsuario, ParserUsuario
from parseros.listas import RecolectorListas, atributosListas, ParserLista
from utils.registro import configurar_log

log = configurar_log(verbosidad=4)

if __name__ == '__main__':
    parser = ArgumentParser(description="Migración/Backup de Usuarios y Cuentas en Zimbra")
    parser.add_argument('objeto', choices=['usuarios', 'listas'])
    parser.add_argument('--fichero', '-f', type=FileType('r'), required=True)

    args = parser.parse_args()

    archivo = args.fichero
    objeto = args.objeto

    if objeto == "usuarios":
        recolector = RecolectorUsuarios(ParserUsuario, atributosUsuario)
    else:
        recolector = RecolectorListas(ParserLista, atributosListas)

    for linea in archivo:
        recolector.agregar(linea)
    else:
        recolector.ultima_linea()
