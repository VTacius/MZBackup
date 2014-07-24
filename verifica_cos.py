import json
def coidi(fichero):
  with open(fichero) as json_file:
    cos = json.load(json_file)
    for j,i in cos.iteritems():
      print(j + "\t" + i + " \t" + fichero)

lista = ("/opt/backup/cos-17-07-14-122430/cos.id", "/opt/backup/cos-17-07-14-142805/cos.id", "/opt/backup/cos-17-07-14-151739/cos.id", "/opt/backup/cos-17-07-14-154942/cos.id", "/opt/backup/cos-17-07-14-133733/cos.id", "/opt/backup/cos-17-07-14-151618/cos.id", "/opt/backup/cos-17-07-14-151929/cos.id", "/opt/backup/cos-17-07-14-160912/cos.id", "/opt/backup/cos-17-07-14-161246/cos.id", "/opt/backup/cos-17-07-14-161405/cos.id")
for fichero in lista:
  coidi(fichero)
