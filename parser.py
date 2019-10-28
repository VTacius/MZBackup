from MZBackup.parseros.cos import ParserCos, atributos as cos_attr
from MZBackup.parseros.listas import ParserLista, atributos as lista_attr
from MZBackup.parseros.usuarios import ParserUsuario, atributos as usuario_attr

from MZBackup.utils.registro import configurar_log

log = configurar_log(verbosidad=4)

if __name__ == '__main__':

    objeto = 'usuario'

    if objeto == 'cos':
        contenido = open('cos.cnt')
        parser = ParserCos(cos_attr)
        resultado = parser.procesar(contenido.readlines())
    elif objeto == 'lista':
        contenido = open('tests/data/lista.data')
        parser = ParserLista(lista_attr)
        resultado = parser.procesar(contenido.readlines())
    elif objeto == 'usuario':
        contenido = open('tests/data/usuario.data')
        parser = ParserUsuario(usuario_attr)
        resultado = parser.procesar(contenido.readlines())

    print('\n')
    print(resultado['comando'])
    for i, j in resultado['multilinea'].items():
        print(f"\n\n{i}")
        print(j)

