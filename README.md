## MZBackup: Migración y Backup de Zimbra 

MZBackup es un proyecto para la migraciónn/Backup de Zimbra con mediante los comandos nativos de administración de zimbra (zm*), envueltos en python al menos lo suficiente para capturar un par de errores y correr grandes listas en diferentes hilos.

### Uso:
#### Antes de su primer uso:
* Sitúese en el servidor del que quiere realizar backup

* Si se encuentra en CentOS 6, será necesario instalar el módulo `argparse` para python 
```bash
$ rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/i386/python-argparse-1.2.1-2.el6.noarch.rpm
```

* Cree el fichero `mzbackup.ini` para configurar la aplicación.
Los valores a configurar son:
 * `remoto`: Servidor que ha de recibir el backup
 * `dir_base`: Directorio base donde la aplicación realiza todas las operaciones. Cuide de crearlos manualmente en ambos servidores
```bash
mkdir /opt/backup
chmod 750 /opt/backup/
chown zimbra:root /opt/backup/
```
 * `s_backupeador`: Número de hilos para enviar mediante red los archivos de backup
 * `s_usuarios`: Hilos en los que se obtiene y formatea información de los usuarios. Más allá de los 35 no se nota una mejoría significativa en el tiempo empleado
 * `s_mailbox`: Cantidad de hilos que implica el trabajo en paralelo que. Más allá de los 28 no se nota mejoría en el tiempo empleado
 * `s_cos`: Números de hilos en los que se obtiene y formatea información de COS (Class of Service). No creo que un número alto sea necesario, entre otras cosas porque usualmente nunca son muchos. (Usualmente, claro)

```ini
[Global]
remoto = 10.30.20.200
dir_base = /opt/backup
s_backupeador = 2
s_usuarios = 35
s_mailbox = 28 
s_cos = 4
```

* Configurar autenticación sin contraseña respecto al servidor remoto: Como usuario zimbra, copie las llaves públicas del servidor del al que va a realizar backup al que va a recibir el backup: 
También puede usar otro usuario, si es que la idea de usar root le molesta. Por un lado, las operaciones de restauración de backup se realizarán en el servidor destino de backup, por lo que en realidad no necesita tener control del usuario root de dicho equipo
```bash
su - zimbra
ssh-keygen -t rsa -b 4096 -C correo@dominio.com
ssh-copy-id root@<ip servidor remoto> 
```
* Todos los script se ejecutan como usuario zimbra

* El primer script que debe ejecutarse al menos una vez es `cos.py`, que guardará los cos de los usuarios y ayudará en la tarea de migración de los mismos `$ python MZBackup/cos.py`

#### Backup / Migración de datos sobre los usuarios
    $ python MZBackup/usuarios.py -c /opt/backup/cos-24-07-14-093319/cos.id

#### Backup / Migración de datos de listas de distribución
    $ python MZBackup/listas.py 

#### Backup / Migración de Buzones
    $ python MZBackup/mailbox.py
