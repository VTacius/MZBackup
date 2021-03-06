"""Operaciones base a componerse en el script principal"""
from mzbackup.utils.registro import get_logger
from mzbackup.utils.comandos import EjecutorLocal
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


def crear_fichero_contenido(pato_local, comando):
    """Crear el fichero con contenido proveniente de un comando, si es que no existe"""
    pato_local.extension = "data"
    log.debug("> Creando el fichero de datos %s", pato_local)

    ejecutor_local = EjecutorLocal(comando)
    archivo = ejecutor_local.guardar_resultado(pato_local)

    return archivo


class ParserFactory:
    """Crear un Parser de contenido COS"""

    @classmethod
    def desde_comando(cls, objeto, comando, pato, args):
        """Crea un recolector desde comando"""
        recolector = crear_recolector(objeto, pato, args)

        log.info('Operacion Principal: Habilitando directorios de salida')
        pato.habilitar_directorio_local()

        log.info('Operacion Principal: Habilitando ficheros con contenido')
        contenido = crear_fichero_contenido(pato, comando)
        recolector.configurar_contenido(contenido)

        return recolector

    @classmethod
    def desde_fichero(cls, objeto, contenido, pato, args):
        """Crea un recolector desde un fichero existente"""
        recolector = crear_recolector(objeto, pato, args)

        log.info('Operacion Principal: Habilitando ficheros con contenido')
        recolector.configurar_contenido(contenido)

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
