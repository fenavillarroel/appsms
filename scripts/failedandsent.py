#!/usr/bin/python

import sys,os
import subprocess
#import re
#import string
#import MySQLdb

if __name__ == '__main__':

    ids=str(sys.argv[1]).strip()
    tipo=str(sys.argv[2]).strip()
    fecha=str(sys.argv[3]).strip()
    #sys.stderr.write('Id sms: %s Tipo : %s Fecha  %s\n'% (ids,tipo,fecha));
    #sys.stderr.flush()

    #Enviamos el POST a la API failedandsent 

    formato='-H Content-Type: application/json -d {"idsms":%s,"tipo":"%s","fecha":"%s" } http://portal.opendata.cl:80/smscenter/default/failedandsent' % (ids,tipo,fecha) 

    #sys.stderr.write(formato)
    #sys.stderr.flush()

    try:

        maxm = subprocess.check_output('curl  %s' % (formato,))

    except:

       sys.exit(0)

    sys.exit(1)

