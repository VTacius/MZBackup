#!/usr/bin/python
#encoding: utf-8
'''
Librería que implementa al módulo paramiko para mayor comodidad de las demás aplicaciones
:author: Alexander Ortiz
:version: 1.0
'''
import paramiko
import socket
import sys
class remoto ():
    def __init__(self):
		''' Inicia conexión ssh cada vez que se instancia'''
		###############################################################################	
		# Usamos las llaves privadas para acceder por medio de ellas al servidor
		# Y configuramos otros valores
		self.user_auth = "root"
		self.host = "10.10.20.2"
		self.port = 22
		self.nbytes = 100
		try:
			user_key = paramiko.RSAKey.from_private_key_file('/opt/zimbra/.ssh/id_rsa')
			host_key = paramiko.util.load_host_keys('/opt/zimbra/.ssh/known_hosts')
			paramiko.util.log_to_file('transacciones.log')
		except IOError as e:
			print "Error con la carga de ficheros de claves:\n\t" + str(e)
			sys.exit()
		except paramiko.SSHException as e:
			print "Error con la carga de ficheros de claves:\n\t" + str(e)
			sys.exit()
		
		###############################################################################	
		# Atrapamos los errores porque despues te tardas horas en hallar estas cosas
		try:
			self.trans = paramiko.Transport((self.host, self.port))
		except socket.error as e:
			print e
			sys.exit()
		
		try:
			self.trans.connect(username = self.user_auth, pkey = user_key)
		except paramiko.paramiko.SSHException as e:
			print e
			sys.exit()
		###############################################################################	
	
    def ejecutor(self, comando):
        '''
        Toma como parametro un comando a ejecutar en el servidor remoto
        Verifica excepciones
        Retorna valor de retorno y mensajes. 
        '''
		# Abrimos una self.sesion para trabajar en ella
        self.sesion = self.trans.open_channel("session")
        try:
        # Ejecutamos el comando que necesitamos
            self.sesion.exec_command(comando)
        except paramiko.SSHException as e:
            print "Error ejecutando comando " + str(e)
            sys.exit()
        
        # Cuando se reciba este valor, significa que el comando ya ha terminado de ejecutarse
        status = self.sesion.recv_exit_status()
        
        mensaje = str()
        while self.sesion.recv_ready():
            mensaje += (self.sesion.recv(self.nbytes))
        while self.sesion.recv_stderr_ready():
            mensaje += (self.sesion.recv_stderr(self.nbytes))
        return status, mensaje.split("\n")

    def scp(self, origen, destino):
        sftp = paramiko.SFTPClient.from_transport(self.trans)
        try:
            sftp.get(origen, destino)
        except paramiko.SSHException as e:
            print "SSH: Problemas obteniendo el fichero" + str(e)
            sys.exit()
        except IOError as e:
            print "IO: Problema obteniendo el fichero: " + str(e)
            sys.exit()
        sftp.close()

