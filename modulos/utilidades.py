#!/usr/bin/python
# encoding: utf-8
# vim: tabstop=4 : shiftwidth=4 : expandtab
'''
Funciones útiles de carácter general 
O de caracter especifico que no quise poner en otra parte porque me hacía ver fea las clases que de por si no son tan guapas que digamos
'''
__author__ = "Alexander Ortiz"
__version__ = "0.9"
__email__ = "alortiz@salud.gob.sv"
__status__ = "Production"

import json
import os
import re
import sys
import time
from subprocess import STDOUT,PIPE,Popen
from configuracion import configuracion

# Ejecutamos el fichero al inicio, con lo cual parece claramente garantiza que 
# leerá la configuración
remoto = configuracion("remoto")
dir_base = configuracion("dir_base")

def ejecutar_comando(comando):
    '''
    Ejecuta un comando en la consola mediante subprocess
    Detiene la ejecución si el comando no existe o si terminó con condición de error
    Devulve un array sin valores vacíos
    '''
    try:
        exe = Popen(comando, stdout=PIPE, stderr=PIPE)
        stdout, stderr = exe.communicate()
        if exe.returncode != 0:
            raise Exception('El comando ha terminado con una condición de error descrita a continuación:\n\t' + stdout + "\t" + stderr)
        else:
            salida = [ x for x in stdout.split("\n") if len(x) > 0 ]
        return salida
    except OSError as e:
        print("OS: " + str(e))
        sys.exit(1)
    except Exception as e:
        print("Error: " + str(e))
        sys.exit(1)

def ejecutar_remoto(comando):
    '''
    Por ahora, ejecutamos comando remotos con ssh, no queda otro si es que queremos avanzar por este momento
    '''
    orden = "'" + comando + "'"
    comando = ["ssh", "root@" + remoto, orden]
    ejecutar_comando(comando)
    
def enviante(origen, destino=str()):
    '''
    Por ahora, enviamos archivos con ssh, no queda de otra si es que queremos avanzar
    El destino es opcional, tomará el directorio actual, comportamiento útil para 
    los backup que listados que la mayoría de procesos crean.
    Por tanto, solo enviará ficheros regulares
    '''
    if origen == "*":
        # En este caso, usualmente será porque estamos enviando al mismo lugar
        localidad = os.getcwd()
        archivos = [x for x in os.listdir(localidad) if os.path.isfile(x)] 
        # Pero mejor lo probamos que no perdemos mucho
        destino = destino if len(destino)>0 else localidad
        for archivo in archivos:
            print("Enviando " + archivo + " hacia " + destino)
            comando = ['scp', archivo, 'root@' + remoto + ':' + destino]
            ejecutar_comando(comando)
    else:
        comando = ['scp', origen, 'root@' + remoto + ':' + destino]
        ejecutar_comando(comando)

def titulador(titulo):
    '''
    Saca a pantalla un mensaje con decorado, aparte los comodines se ven feos en los print
    dentro de las funciones, legibilidad le dicen unos
    '''
    mensaje = "###############################################################################\n{title}".format
    print mensaje(title=titulo)

def situar_remoto():
    '''
    Crea el directorio remoto igual al directorio actual
    Muy útil después de haber usado situar_directorio()
    '''
    directorio = os.getcwd()
    comando = "'/bin/mkdir " + directorio + "'"
    ejecutar_remoto(comando)

def situar_directorio(objeto, dirbase = ""):
    '''
    Crear un directorio local para el objeto dado, incluye una marca de tiempo. 
    Mueve las operaciones del script al directorio creado
    '''
    timestamp = time.strftime('%d-%m-%y-%H%M%S')
    dirbase = dir_base if not dirbase else dirbase 
    directorio = dirbase.rstrip("/") + "/" + objeto + "-" + timestamp
    try:
        os.mkdir(directorio)
        os.chdir(directorio)
    except IOError as e:
        print "IO: " + str(e)
        sys.exit(1)
    except OSError as e:
        print "OS: " + str(e)
        sys.exit(1)

def cadeneador(contenido, sep):
    '''
    Si el contenido no es una cadena, lo convierte en una
    Usa el separador especificado en sep
    '''
    if sep == "c":
        final = " "
    elif sep == "l":
        final = "\n"
    else:
        final = ""
    if isinstance(contenido, str):
        cadena = contenido
    else:
        cadena = str()
        for x in contenido:
            entrada = x + final
            cadena += entrada 
    return cadena

def guardar(archivo, contenido, separador = "z"):
    '''
    Guarda contenido en un fichero dado con métodos de os
    Usarlo en funciones Thread para crear un bloqueo del fichero
    Este procedimiento es claramente más lento, pero es necesario
    Soy el primero en reconocer que esta opción va demasiado lenta, cuesta un par de minutos (No una docena, pero si un par de minutos)
    '''
    fichero = os.open(archivo, os.O_RDWR|os.O_APPEND|os.O_CREAT)
    # Usamos la función cadeneador antes definida
    os.write(fichero, cadeneador(contenido, separador))
    os.close(fichero)

def abrir_json(archivo):
    '''
    Se encarga de abrir ficheros en formato json 
    y retorna un diccionario con su contenido
    '''
    try:
        with open(archivo, 'r') as json_fichero:
            diccionario = json.load(json_fichero)
    except IOError as e:
        print "IO: " + str(e)
        sys.exit(1)
    except OSError as e:
        print "OS: " + str(e)
        sys.exit(1)
    except ValueError as e:
        print "JSON: " + str(e)
        sys.exit(1)
    return diccionario


def borrar_usuarios (lista, dominio):
    '''
    Borrar los usuarios enumerado en la lista a de una lista dada
    y rompe el bucle al encontrarlo, pues en realidad solo hay uno de estos
    '''
    a = ['admin','galsync','spam']
    for e in a:
        cuenta = e + "@" + dominio	
        try:
            lista.remove(cuenta)
        except ValueError:
            pass
	
def borrar_patrones (listador):
    '''
    Borrar los usuarios de una lista, especificados en una expresión regular puesto
    que así son producidos por las versiones más nuevas de zimbra 
    y rompe el bucle al encontrarlo, pues en realidad solo hay uno de estos
    '''
    a = ['spam','ham','quarantine','virus-quarantine','galsync']    
    for i in a:
        patron = "^(" + i + ")\..+@(\w+\.*){3}$"
        for j in listador:
            if re.match(patron, j):
                listador.remove(j)
                break


def almacenar_diccionario(fichero, diccionario):
    '''
    Almacena el diccionario cosId:cos que usaremos en el script usuario.py 
    para poder asignar el cosId en el nuevo servidor, dado que el cosId cambia 
    en el nuevo servidor, pero los datos del usuario almacenan el cosId
    '''
    datos = json.dumps(diccionario)
    guardar(fichero, datos)
