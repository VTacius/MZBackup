## MZBackup: Migración y Backup de Zimbra 
MZBackup es un proyecto para la migraciónn/Backup de Zimbra con mediante los comandos nativos de administración de zimbra (zm), envueltos en python al menos lo suficiente para capturar un par de errores y correr grandes listas en diferentes hilos.

### Uso:
#### Antes de su primer uso:
* Cambie la configuración del idioma en el fichero `~/.bash_profile`: Por defecto, zimbra cambia la configuración a "C", pese a lo que el sistema tenga configurado.  Esto tiene un efecto adverso cuando tratamos con caracteres en español.  Al día de hoy no he tenido problemas respecto con este cambio de configuración: Cambiar
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
* Configurar autenticación sin contraseña respecto al servidor remoto: Como usuario zimbra, copie las llaves públicas del servidor del al que va a realizar backup al que va a recibir el backup:  También puede usar otro usuario, si es que la idea de usar root le molesta. Por un lado, las operaciones de restauración de backup se realizarán en el servidor destino de backup, por lo que en realidad no necesita tener control del usuario root de dicho equipo
```bash
su - zimbra ssh-keygen -t rsa -b 4096 -C correo@dominio.com
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
* `s_listas`: Número de hilos para obtener y modelar información sobre listas de distribución y los usuarios que pertenecen a ellas
* `s_envio`: Cantidad de ficheros que envía por medio de SSH al servidor Remoto. Realmente no es útil configurar más que eso, al menos según lo que sabemos hasta el momento
* `s_cos`: Números de hilos en los que se obtiene y formatea información de COS (Class of Service). No creo que un número alto sea necesario, entre otras cosas porque usualmente nunca son muchos. (Usualmente, claro)

* El fichero de configuración queda de la siguiente forma:
```ini
[Global]
remoto = 10.30.20.200
dir_base = /opt/backup
s_backupeador = 2
s_usuarios = 35
s_mailbox = 28
s_listas = 14
s_envio = 2
s_cos = 4
```

#### Ejecutando los script

* Sitúese en el servidor del que quiere realizar backup

* Todos los script se ejecutan como usuario zimbra

* El primer script que debe ejecutarse al menos una vez es `cos.py`, que guardará los COS configurados en el servidor, y ayudará otros script a hacer la correspondencia entre COS-id y COS
```bash 
$ python MZBackup/cos.py
```
* Por defecto, el backup para todos los módulos se realiza de forma local en el servidor. Si además de ello se requiere enviar al servidor remoto, usar la opción `--envio` que esta presente para todos los módulos
```bash
$ python MZBackup/cos.py --envio
```
#### Backup / Migración de datos sobre los usuarios
Es totalmente necesaria la opción `--cos` para asociar el ficheros cos.id más reciente
```bash
    $ python MZBackup/usuarios.py -c /opt/backup/cos-24-07-14-093319/cos.id
```
Puede usarse una lista de usuarios sobre los cuales realizar el backup de definición. Incluso pueden pertenecer a varios dominios
```bash
    $ python MZBackup/usuarios.py -c /opt/backup/cos-24-07-14-093319/cos.id -l /opt/backup/backup-retirados/lista-11072016.lst 
```
#### Backup / Migración de datos de listas de distribución

    $ python MZBackup/listas.py

#### Backup / Migración de Buzones
 
    $ python MZBackup/mailbox.py

### Desarrollo
#### Instalacion
```sh
python setup install
```

#### Linting
```sh
pylama
```

#### Testing
Llamando a pytest como módulo agrega el actual path al SYSPATH (La cosa más genial del mundo si me lo preguntan)
```sh
python -m pytest -v tests/
```

