import ftputil
import json
import requests
import pytz

from datetime import datetime

#parametros de configuracion
files_directory="/PT/LOAD"
ftp_base="fr.ftp.opendatasoft.com"
ftp_user="saba"
ftp_pass="HVKghgtcMTlRXStFL737vxvg"
params = (('pushkey', '805fff7d7f46e1a13b9445c5a6c637532d53aedfabede4b9941c0710'),) #push parameters
url_record_base="https://saba.opendatasoft.com/explore/dataset/pt_carga-aparcamientos/table/?q=nombre%3D" #falta el ide de parking tras la cadena

def CheckNotLoad(request):
    ### load config parameters from storage
    host= ftputil.FTPHost(ftp_base, ftp_user, ftp_pass)
    host.chdir(files_directory)
    listdirectory=host.listdir(host.curdir)
    for x in listdirectory:
        datos_fichero=host.lstat(x)
        print("el fichero "+str(x)+" tiene un tamaño de "+str(datos_fichero.st_size))
        if((datos_fichero.st_size)==0):
            parking=str(x).split('.')[0]
            url_record=url_record_base+parking
            print(url_record)
            print(parking)
            tempo=str(datetime.now())
            print(tempo)
            data = '{"causa":"Failed loading", "URL":"'+url_record+'","time":"'+tempo+'", "parking":"'+parking+'"}'
            print(data)
            response = requests.post('https://saba.opendatasoft.com/api/push/1.0/pt_alarmas/realtime/push/', params=params, data=data)
            print(response)
    return (str(listdirectory))
    
request=""
salida=CheckNotLoad(request)