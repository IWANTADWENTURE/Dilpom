import urllib.request;
import os, sys;
from datetime import datetime, timedelta
from ftplib import FTP

class FTPConnector():

    __host = "avisoftp.cnes.fr"
    __login = ""
    __password = ""
    __ftp = None

    def __init__(self):
        self.connect()

    def downloderFiles(self, filesList):
        for fileName in filesList:
            self.read_file_to_bytes(fileName)

    def read_file_to_bytes(self, file_name):
        self.__ftp.retrbinary("RETR %s" % file_name, open('ftp/satelite/'+file_name, 'wb').write)

    def connect(self, host=__host, login=__login, password=__password):
        self.__ftp = FTP(host)
        self.__ftp.login(login, password)

    def getFilesFromDir(self, firstDate, lastDate):
        self.__ftp.cwd('AVISO/pub/jason-2/igdr/cycle_319')
        listFileForDownload=[];
        for dirFile in self.__ftp.nlst():
            dateFileValue=datetime(int(dirFile.split('_')[4][0:4]), int(dirFile.split('_')[4][4:6]), int(dirFile.split('_')[4][6:8]), int(dirFile.split('_')[5][0:2]), int(dirFile.split('_')[5][2:4]), int(dirFile.split('_')[5][4:6]))
            if((dateFileValue>=firstDate)&(dateFileValue<=lastDate)):
                listFileForDownload.append(dirFile);#Условие проверки проработать
        self.downloderFiles(listFileForDownload);