import urllib.request;
import os, sys;
from datetime import datetime, timedelta
from ftplib import FTP

class FTPConnector():

    __host = "avisoftp.cnes.fr"
    __login = ""
    __password = ""
    __ftp = None

    def ftpDownloader(self, firstDate, lastDate,):
        os.makedirs('/ftp/satelite', mode=0o777, exist_ok=True);
        destination = 'ftp/satelite/JA2_IPN_2PdP319_001_20170223_063707_20170223_073320.zip'
        url = 'ftp://avisoftp.cnes.fr/AVISO/pub/jason-2/igdr/cycle_319/JA2_IPN_2PdP319_001_20170223_063707_20170223_073320.zip'
        urllib.request.urlretrieve(url, destination)

    def read_file_to_bytes(self, file_name, output):
        self.__ftp.retrbinary("RETR %s" % file_name, output.write)

    def __init__(self):
        self.connect()

    def connect(self, host=__host, login=__login, password=__password):
        self.__ftp = FTP(host)
        self.__ftp.login(login, password)

    def getFilesFromDir(self, firstDate, lastDate):
        self.__ftp.cwd('AVISO/pub/jason-2/igdr/cycle_319')
        listFileForDownload=[];
        for dirFile in self.__ftp.nlst():
            dateFileValue=datetime(int(dirFile.split('_')[4][0:4]), int(dirFile.split('_')[4][4:6]), int(dirFile.split('_')[4][6:8]))
            if(dateFileValue>datetime.strptime(firstDate, '%Y.%m.%d')):
                listFileForDownload.append(dirFile);
        print(listFileForDownload);
    def printer(self):
        self.__ftp.cwd('AVISO/pub/jason-2/igdr/cycle_319')
        print(self.__ftp.nlst())

    #def linkCreater(self):


