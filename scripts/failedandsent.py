#!/usr/bin/python

import json
import sys
import requests

if __name__ == '__main__':

    ids=str(sys.argv[1]).strip()
    tipo=str(sys.argv[2]).strip()
    fecha=str(sys.argv[3]).strip()
    sys.stderr.write('Id sms: %s Tipo : %s Fecha  %s\n'% (ids,tipo,fecha));
    sys.stderr.flush()

    #Enviamos el POST a la API failedandsent 
    payload={}
    payload['idsms']=ids
    payload['tipo']=tipo
    payload['fecha']=fecha
    url='http://portal.opendata.cl/smscenter/default/failedandsent'
    headers={'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.ok:
        print 'Ok'
    else:
        print response



