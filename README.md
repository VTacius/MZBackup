## MZBackup: Migración y Backup de Zimbra 

MZBackup es un proyecto para la migraciónn/Backup de Zimbra con mediante los comandos nativos de administración de zimbra (zm*), envueltos en python al menos lo suficiente para capturar un par de errores y correr grandes listas en diferentes hilos.

### Uso:
#### Antes de su primer uso:
* Cambie la configuración del idioma en el fichero `~/.bash_profile`: Por defecto, zimbra cambia la configuración a "C", pese a lo que el sistema tenga configurado.  
Esto tiene un efecto adverso cuando tratamos con caracteres en español.
Al día de hoy no he tenido problemas respecto con este cambio de configuración:

Cambiar 
```bash
export LANG=C
export LC_ALL=C
```

Por un conjunto de caracteres adecuado a su idioma. Puede ver una lista de los conjuntos disponibles ejecutando en consola
```bash
$ locale -a
```

Así por ejemplo:
```bash
export LANG="es_SV.UTF-8"
export LC_ALL="es_SV.UTF-8"
```

* Configurar autenticación sin contraseña respecto al servidor remoto: Como usuario zimbra, copie las llaves públicas del servidor del al que va a realizar backup al que va a recibir el backup:  
También puede usar otro usuario, si es que la idea de usar root le molesta. Por un lado, las operaciones de restauración de backup se realizarán en el servidor destino de backup, por lo que en realidad no necesita tener control del usuario root de dicho equipo
```bash
su - zimbra
ssh-keygen -t rsa -b 4096 -C correo@dominio.com
ssh-copy-id root@<ip servidor remoto> 
```

* Si se encuentra en CentOS 6, será necesario instalar el módulo `argparse` para python 
```bash
$ rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/i386/python-argparse-1.2.1-2.el6.noarch.rpm
```

#### Configuración:
Cree el fichero `mzbackup.ini` para configurar la aplicación. Configure tomando en cuenta los siguientes paramétros

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
* El fichero de configuración queda de la siguiente forma:
```ini
[Global]
remoto = 10.30.20.200
dir_base = /opt/backup
s_backupeador = 2
s_usuarios = 35
s_mailbox = 28 
s_cos = 4
```

#### Ejecutando los script

* Sitúese en el servidor del que quiere realizar backup

* Todos los script se ejecutan como usuario zimbra

* El primer script que debe ejecutarse al menos una vez es `cos.py`, que guardará los cos de los usuarios y ayudará en la tarea de migración de los mismos `$ python MZBackup/cos.py`

#### Backup / Migración de datos sobre los usuarios
    $ python MZBackup/usuarios.py -c /opt/backup/cos-24-07-14-093319/cos.id

#### Backup / Migración de datos de listas de distribución
    $ python MZBackup/listas.py 

#### Backup / Migración de Buzones
    $ python MZBackup/mailbox.py
