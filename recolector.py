from argparse import ArgumentParser
from argparse import FileType

from MZBackup.parseros.cos import RecolectorCos, atributos as cos_attrs, ParserCos
from MZBackup.parseros.listas import RecolectorListas, atributos as lista_attrs, ParserLista
from MZBackup.parseros.usuarios import RecolectorUsuarios, atributos as usuario_attrs, ParserUsuario

from MZBackup.utils.registro import configurar_log

log = configurar_log(verbosidad=1)

if __name__ == '__main__':
    parser = ArgumentParser(description="Migración/Backup de Usuarios y Cuentas en Zimbra")
    parser.add_argument('objeto', choices=['usuarios', 'listas'])
    parser.add_argument('--fichero', '-f', type=FileType('r'), required=True)

    args = parser.parse_args()
    archivo = args.fichero
    objeto = args.objeto

    if objeto == 'cos':
        recolector = RecolectorCos(ParserCos, cos_attrs)
    elif objeto == 'lista':
        recolector = RecolectorListas(ParserLista, lista_attrs)
    elif objeto == "usuarios":
        recolector = RecolectorUsuarios(ParserUsuario, usuario_attrs)

    for linea in archivo:
        recolector.agregar(linea)
    else:
        recolector.ultima_linea()
