import json
def coidi(fichero):
  with open(fichero) as json_file:
    cos = json.load(json_file)
    for j,i in cos.iteritems():
      print(j + "\t" + i + " \t" + fichero)

lista = ("/opt/backup/cos-23-07-14-153132/cos.id","/opt/backup/cos-24-07-14-090410/cos.id","/opt/backup/cos-24-07-14-093319/cos.id","/opt/backup/cos-24-07-14-152440/cos.id","/opt/backup/cos-24-07-14-170347/cos.id", "/opt/backup/cos-24-07-14-171039/cos.id")

for fichero in lista:
  coidi(fichero)

