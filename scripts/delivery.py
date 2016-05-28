#!/usr/bin/python

import sys
#import re
import string
import MySQLdb

if __name__ == '__main__':

    id_sms=str(sys.argv[1]).strip()
    fecha=str(sys.argv[2]).strip()


    db = MySQLdb.connect(host="localhost",user="root",passwd="vmo123",db="smsd")
    con=db.cursor()
    con.execute("select id_outgoing from sms_log where id= %s" % (id_sms,))
    rws=con.fetchone()

    
    #Enviamos el POST a la API failedandsent·

    formato='-H Content-Type: application/json -d {"idsms":%s,"fecha":"%s" } http://apisms.opendata.cl:80/smscenter/default/delivery' \

                        % (rws[0],fecha)
    try:

        maxm = subprocess.check_output('curl  %s' % (formato,))

    except:

        return 0

    return 1

