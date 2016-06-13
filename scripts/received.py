#!/usr/bin/python

import json
import urllib2
import requests
import sys
#import re
import string
import MySQLdb

if __name__ == '__main__':

    id_sms=str(sys.argv[1]).strip()
    fecha=str(sys.argv[2]).strip()
    text=str(sys.argv[3]).strip()

    t=text.split()
    sys.stderr.write("=======>>>>> id_sms %s Texto '%s\n'" % (id_sms,t));
    sys.stderr.flush()
    try:
        n=t[4][3:]
    except:
        n='0'
    db = MySQLdb.connect(host="localhost",user="root",passwd="vmo123",db="smsd")
    con=db.cursor()
    con.execute("select id_outgoing from sms_log where receiver= '%s' order by id desc limit 1" % (n,))
    rws=con.fetchone()
    sys.stderr.write("=======>>>>> Id sms: %s  Fecha  '%s\n'" % (rws[0],fecha));
    sys.stderr.flush()

    #formato='-H Content-Type: application/json -d {"idsms":%s,"fecha":"%s" } http://portal.opendata.cl:80/smscenter/default/delivery'  % (rws[0],fecha)
    payload={}
    payload['idsms']=rws[0]
    payload['fecha']=fecha
    url='http://portal.opendata.cl/smscenter/default/delivery'
    headers={'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.ok:
        print 'OK'
    else:
        print response
