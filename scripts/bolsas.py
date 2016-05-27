#!/usr/bin/python

import sys
#import re
import string
import MySQLdb

if __name__ == '__main__':

    queue=str(sys.argv[1]).strip()
    texto=str(sys.argv[2]).strip()
    sys.stderr.write('Destino -----> %s\n'% (queue,));
    sys.stderr.flush()
    patron=['Bolsa','80','SMS','activada!']
    #patron=['hola','fernando','activada!']

    t=texto.split()
    sys.stderr.write('Mensaje Recibido -----> %s\n'% (t,));
    sys.stderr.flush()
    c=0
    for i in range(len(patron)):

        for j in range(len(t)):

            if patron[i].upper() == t[j].upper():
                c+=1

    if c>=2: #Match

        #if queue=='GSM1':
        db = MySQLdb.connect(host="localhost",user="root",passwd="vmo123",db="smsd")
        con=db.cursor()
        con.execute("update canales set credito = credito - 1600, cantidad = cantidad + 80 where queue='%s'" % queue)
        db.commit()
        db.close()

