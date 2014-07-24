# encoding: utf-8
from subprocess import STDOUT,PIPE,Popen
import sys
def comando(comando):
    try:
        exe = Popen(comando, stdout=PIPE, stderr=PIPE)
        stdout, stderr = exe.communicate()
        if exe.returncode != 0:
            raise Exception('El comando ha terminado con una condición de error descrita a continuación:\n' + stdout)   
        else:
            salida = [ x for x in stdout.split("\n") if len(x) > 0 ]
        return salida
    except OSError as e:
        print("OS: " + str(e))
        sys.exit(1)
    except Exception as e:
        print("Error: " + str(e))
        sys.exit(1)

print "Estamos fuera del comando"
salida = comando(['zmprov','gaud'])
print salida
print "Hemos terminado, de hecho"
