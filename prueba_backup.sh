#!/bin/bash
if [ -d backup ]; then rm -rf backup && mkdir backup; else mkdir backup; fi
if [ $# -eq 1 ]
then 
  for i in `cat $1`
  do
    # TGZ es el único de los formatos que guarda metadata, necesaria para que recrear los buzones
    zmmailbox -z -m $i getRestURL -o backup/"$i".tgz "/?fmt=tgz" && \
    echo -e "\t\tSe obtiene el backup para usuario $i\n"
    # Es necesario enviar las claves publicas hacia el servidor destino para poder enviarlas sin contrasenia.
    scp backup/"$i".tgz root@10.10.20.102:/opt/zimbra/backup && \
    echo -e "\t\tEnviado backup de $i\n"
  done
else
  echo "Estoy saliendo"
  exit
fi
