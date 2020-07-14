"""Operaciones base a componerse en el script principal"""
from mzbackup.utils.registro import get_logger
from mzbackup.mzbackup import Ejecutor

from mzbackup.parseros.comun.tipo import Tipo

from mzbackup.parseros.cos import RecolectorCos, atributos as cos_attrs, IteradorCos
from mzbackup.parseros.cos import EuropaCos

from mzbackup.parseros.usuarios import RecolectorUsuario, EuropaUsuario, IteradorUsuarios
from mzbackup.parseros.usuarios import atributos as usuarios_attrs

from mzbackup.parseros.listas import RecolectorListas, atributos as listas_attrs, IteradorListas
from mzbackup.parseros.listas import EuropaLista


log = get_logger()


def tipeador(objeto):
    """Devuelve clases y diccionario correspondientes a cada objeto"""
    if objeto == "cos":
        return cos_attrs, IteradorCos, RecolectorCos, EuropaCos
    if objeto == "listas":
        return listas_attrs, IteradorListas, RecolectorListas, EuropaLista
    if objeto == "usuarios":
        return usuarios_attrs, IteradorUsuarios, RecolectorUsuario, EuropaUsuario

    raise TypeError("Objeto no soportado")


def crear_recolector(objeto, pato, args):
    """Instancia un recolector adecuado, de acuerdo al tipo especificado"""
    attrs, Iterador, Recolector, Europa = tipeador(objeto)
    tipo = Tipo(attrs)
    iterador = Iterador()
    europa = Europa(pato, attrs.get("modificante", "DEFAULT"))
    recolector = Recolector(tipo, iterador, **args)
    recolector.configurar_destino(europa)

    return recolector


def crear_parser(objeto, comando, pato, args):
    """Crea un recolector desde comando"""
    recolector = crear_recolector(objeto, pato, args)

    log.info('Operacion Principal: Habilitando directorios de salida')
    pato.habilitar_directorio_local()

    log.info('Operacion Principal: Habilitando ficheros con contenido')
    pato.habilitar_fichero_contenido(comando)
    recolector.configurar_contenido(pato.fichero)

    return recolector

def enviar_remoto(debe_enviarse, pato, ficheros):
    """Se instrumentaliza el envío de ficheros al servidor remoto"""
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
