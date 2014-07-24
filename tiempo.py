#!/usr/bin/python
# encoding: utf-8
from datetime import * 
import sys as s
import re as r
fichero = s.argv[1]

contenido = open(fichero, "r")

formato = "%b %d %H:%M:%S"

inicio = datetime.strptime('Jun 18 00:59:42', formato)
final = datetime.strptime('Jun 18 01:59:42', formato)

for i in contenido:
  fechado = "".join(r.findall('^\w+\s\d+\s\d+\:\d+\:\d+', i))
  fecha = datetime.strptime(fechado, formato)
  if fecha > inicio and fecha < final:
    print i.rstrip("\n")

