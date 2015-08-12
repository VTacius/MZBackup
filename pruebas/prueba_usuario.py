#encoding: utf-8

from modulos.utilidades import ejecutar_comando, abrir_json
from modulos.usuareador import modelador
import argparse

import sys

# TODO: Hasta podrías trabajarlo de tal forma que si no se le proporciona archivo como parametro, 
# usa por defecto el más nuevo en que pueda encontrar en el directorio dir_base, y entonces si no lo encuentro
# ya luego avisa que necesita que se cree el fichero

if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='Lista de usuarios para un dominio dado')
    parser.add_argument('-l','--listado', help='Fichero con la lista de usuarios para un dominio dado', required=True)
    parser.add_argument('-c','--cos', help='Fichero JSON (cos.id)que contiene Cos:CosId', required=True)
    args = parser.parse_args()
    
    archivo_lista_usuarios = args.listado
    archivo_dict_cos = args.cos
    
    lista_usuarios = open(archivo_lista_usuarios, "r")

    dict_cos = abrir_json(archivo_dict_cos)
    
    for user in lista_usuarios:
        comando = ['zmprov', '-l', 'ga', user.strip()]
        salida = ejecutar_comando(comando)
        modelo = modelador(salida, dict_cos)
        modelo.moldear()
        print (modelo.volcado)

