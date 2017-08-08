import urllib.request;
import os, sys;
from datetime import datetime, timedelta
from ftplib import FTP
import os

class FTPConnector():

    __hostSatelite = "avisoftp.cnes.fr"
    __hostModel = "innovation.org.ru"
    __loginSatelite = ""
    __loginModel = "diplom"
    __passwordSatelite = ""
    __passwordModel = "QNLN9p?7b"
    __ftpSatelite = None
    __ftpModel = None

    #def __init__(self):
        #self.connect()

    def downloderFiles(self, filesList):
        for fileName in filesList:
            self.read_file_to_bytes(fileName)
        #self.checkDownloadFiles(filesList)

    def downFiles(self, fileName, path):
        self.read_file_to_bytes(fileName, path)
        #self.checkDownloadFiles(filesList)

    def read_file_to_bytes(self, file_name, path):
        self.__ftp.retrbinary("RETR %s" % file_name, open(path+file_name, 'wb').write)

    def connectToFTP(self, host, login, password):
        self.__ftp = FTP(host)
        self.__ftp.login(login, password)

    def getFilesWithSateliteData(self, firstDate, lastDate):
        self.connectToFTP(self.__hostSatelite, self.__loginSatelite, self.__passwordSatelite)
        self.__ftp.cwd('AVISO/pub/jason-2/igdr/')
        listFileForDownload=[];
        for cycle in self.__ftp.nlst():
            self.__ftp.cwd(cycle+"/")
            for dirFile in self.__ftp.nlst():
                dateFileValue=datetime(int(dirFile.split('_')[4][0:4]), int(dirFile.split('_')[4][4:6]), int(dirFile.split('_')[4][6:8]), int(dirFile.split('_')[5][0:2]), int(dirFile.split('_')[5][2:4]), int(dirFile.split('_')[5][4:6]))
                if((dateFileValue>=firstDate)&(dateFileValue<=lastDate)):
                    self.downFiles(dirFile, 'ftp/satelite/');
            self.__ftp.cwd('..')

    def getFilesWithModelData(self, enteredDate):
        self.connectToFTP(self.__hostModel, self.__loginModel, self.__passwordModel)
        self.__ftp.cwd('wave/model/2017/')
        i=0;
        while i<6:
            if(((enteredDate.day-i)>0)& (enteredDate.day-i<31)):
                self.__ftp.cwd(enteredDate.year.__str__()+
                           (('0'+enteredDate.month.__str__())if (enteredDate.month<10) else enteredDate.month.__str__())+
                           (('0'+(enteredDate.day-i).__str__())if (enteredDate.day-i<10) else (enteredDate.day-i).__str__()))
                for dirFile in self.__ftp.nlst():
                    dateFileValue = datetime(int(dirFile.split('_')[0][0:4]), int(dirFile.split('_')[0][4:6]),
                                             int(dirFile.split('_')[0][6:8]))
                    if (dateFileValue==enteredDate):
                        self.downFiles(dirFile, 'ftp/model/');
                self.__ftp.cwd('..')
            i+=1

    def checkDownloadFiles(self,filesList):
        if(self.__ftp.pwd()=='AVISO/pub/jason-2/igdr/cycle_317/'):
            listFileFromFtpDir = self.__ftp.nlst()
            for nameFile in filesList:
                if (os.path.getsize('ftp/satelite/' + nameFile) != self.__ftp.size(nameFile)):
                    os.remove('ftp/satelite/' + nameFile)
                    self.read_file_to_bytes(nameFile)
        self.__ftp.cwd('AVISO/pub/jason-2/igdr/cycle_317/')
"""""
def getFilesWithSateliteData(self, firstDate, lastDate):
        self.__ftp.cwd('AVISO/pub/jason-2/igdr')
        listFileForDownload=[];
        for cycle in self.__ftp.nlst():
            self.__ftp.cwd(cycle)
            for dirFile in self.__ftp.nlst():
                dateFileValue=datetime(int(dirFile.split('_')[4][0:4]), int(dirFile.split('_')[4][4:6]), int(dirFile.split('_')[4][6:8]), int(dirFile.split('_')[5][0:2]), int(dirFile.split('_')[5][2:4]), int(dirFile.split('_')[5][4:6]))
                if((dateFileValue>=firstDate)&(dateFileValue<=lastDate)):
                    listFileForDownload.append(dirFile);
            # self.__ftp.cwd('..')
            self.downloderFiles(listFileForDownload);

    def getFilesWithSateliteData(self, firstDate, lastDate):
        self.__ftp.cwd('AVISO/pub/jason-2/igdr/cycle_317/')
        listFileForDownload=[];
        for dirFile in self.__ftp.nlst():
            dateFileValue=datetime(int(dirFile.split('_')[4][0:4]), int(dirFile.split('_')[4][4:6]), int(dirFile.split('_')[4][6:8]), int(dirFile.split('_')[5][0:2]), int(dirFile.split('_')[5][2:4]), int(dirFile.split('_')[5][4:6]))
            if((dateFileValue>=firstDate)&(dateFileValue<=lastDate)):
                listFileForDownload.append(dirFile);#Условие проверки проработать
        self.downloderFiles(listFileForDownload);
"""""