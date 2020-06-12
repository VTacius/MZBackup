from argparse import ArgumentParser
from argparse import FileType
from datetime import datetime

from mzbackup.parseros.cos import RecolectorCos, atributos as cos_attrs, ParserCos
from mzbackup.parseros.listas import RecolectorListas, atributos as lista_attrs, ParserLista
from mzbackup.parseros.usuarios import RecolectorUsuarios, atributos as usuario_attrs, ParserUsuario

from mzbackup.utils.registro import configurar_log

from mzbackup.utils.rutas import directorio, examinar_directorio, habilitar_directorio_local

from mzbackup.utils.comandos import ejecutor

log = configurar_log(verbosidad=1)

def habilitar_fichero_origen(debe_crearse, comando, args, config_destino):
    if debe_crearse:
        fichero = "{}/{}.data".format(config_destino['directorio'], config_destino['fichero'])
        contenido, error = ejecutor(comando, fichero)
        archivo = open(fichero)
    else:
        archivo = args.fichero

    return archivo

## TODO: Habilitar servidor remoto
## TODO: Envio a servidor remoto

def main():
    parser = ArgumentParser(description="Migración/Backup de Usuarios y Cuentas en Zimbra")
    parser.add_argument('objeto', choices=['cos', 'listas', 'usuarios'])
    parser.add_argument('--fichero', '-f', type=FileType('r'))
    parser.add_argument('--base', '-b', type=directorio)

    args = parser.parse_args()
    objeto = args.objeto

    marca = datetime.now().strftime('%y-%m-%d-%H%M%S')
    recolector = object()
    
    config_destino, debe_crearse = examinar_directorio(args)
    config_destino = habilitar_directorio_local(debe_crearse, marca, config_destino)

    if objeto == 'cos':
        recolector = RecolectorCos(config_destino, ParserCos, cos_attrs)
        comando = "zmprov gac -v"
    elif objeto == 'listas':
        recolector = RecolectorListas(config_destino, ParserLista, lista_attrs)
        comando = "zmprov gadl -v"
    elif objeto == "usuarios":
        recolector = RecolectorUsuarios(config_destino, ParserUsuario, usuario_attrs)
        comando = "zmprov gaa -l salud.gob.sv -v"

    archivo = habilitar_fichero_origen(debe_crearse, comando, args, config_destino)
    
    for linea in archivo:
        recolector.agregar(linea)
    else:
        recolector.ultima_linea()

if __name__ == '__main__':
    main()
