## MZBackup: Migración y Backup de Zimbra 

MZBackup es un proyecto para la migración/Backup de Zimbra con mediante los comandos nativos de administración de zimbra (zm*), envueltos en python al menos lo suficiente para capturar un par de errores y correr grandes listas en diferentes hilos.

### Uso:
#### Antes de su primer uso:
* Instalar el módulo `argparse` para python `rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/i386/python-argparse-1.2.1-2.el6.noarch.rpm`

* Copiar las llaves públicas del servidor que esta por copiar `ssh-copy-id root@<ip servidor remoto>`

* Cambiar la dirección del servidor backup en `modulos/backupeador.py` y `modulos/utilidades.py`

* El primer script que debe ejecutarse al menos una vez es `cos.py`, que guardará los cos de los usuarios y ayudará en la tarea de migración de los mismos `$ python MZBackup/cos.py`

#### Backup / Migración de datos sobre los usuarios
    $ python MZBackup/usuarios.py -c /opt/backup/cos-24-07-14-093319/cos.id

#### Backup / Migración de datos de listas de distribución
    $ python MZBackup/listas.py 

#### Backup / Migración de Buzones
    $ python MZBackup/mailbox.py

