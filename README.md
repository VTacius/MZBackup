## MZBackup: Migración y Backup de Zimbra 

MZBackup es un proyecto para la migración/Backup de Zimbra con mediante los comandos nativos de administración de zimbra (zm*), envueltos en python al menos lo suficiente para capturar un par de errores y correr grandes listas en diferentes hilos.

### Uso:
#### Antes de su primer uso:
* Sitúese en el servidor del que quiere realizar backup

* Si se encuentra en CentOS 6, ser� necesario instalar el módulo `argparse` para python `rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/i386/python-argparse-1.2.1-2.el6.noarch.rpm`

* Cree el fichero `modulos/mzbackup.ini` para configurar la aplicación.
Los valores a configurar son:
** `remoto`: servidor que ha de recibir el backup

```ini
[Global]
remoto = 10.10.20.2
```


* Configurar autenticaci�n sin contrase�a respecto al servidor remoto: Copie las llaves públicas d servidor del que va a realizar backup al que va a recibir el backup:

    $ ssh-copy-id root@<ip servidor remoto> 

* Cambiar la dirección del servidor backup en `modulos/backupeador.py` y `modulos/utilidades.py`

* El primer script que debe ejecutarse al menos una vez es `cos.py`, que guardará los cos de los usuarios y ayudará en la tarea de migración de los mismos `$ python MZBackup/cos.py`

#### Backup / Migración de datos sobre los usuarios
    $ python MZBackup/usuarios.py -c /opt/backup/cos-24-07-14-093319/cos.id

#### Backup / Migración de datos de listas de distribución
    $ python MZBackup/listas.py 

#### Backup / Migración de Buzones
    $ python MZBackup/mailbox.py

