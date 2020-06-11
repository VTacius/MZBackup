from paramiko.client import SSHClient

cliente = SSHClient()
cliente.load_system_host_keys()
cliente.connect('10.10.20.202')
stdin, stdout, stderr = cliente.exec_command('ls -l')
