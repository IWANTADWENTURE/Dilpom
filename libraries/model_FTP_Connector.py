from libraries.Connector import ConnectorInterface
from datetime import datetime, timedelta
from ftplib import FTP

class ModelFTPConnector(ConnectorInterface):

    __ftp=None
    __host=None
    __login=None
    __password=None
    __path=None
    __enteredDate=None
    __numOfProgn=None

    def __init__(self, enteredDate, numOfProgn, host='', login='', password='', pathForFiles='ftp/model'):
        self.__host=host
        self.__login=login
        self.__password=password
        self.__path=pathForFiles
        self.__enteredDate=enteredDate
        self.__numOfProgn=numOfProgn

    def connect(self):
        self.__ftp=FTP(self.__host)
        self.__ftp.login(self.__login, self.__password)

    def disconnect(self):
        self.__ftp.quit()

    def downloadFile(self, fileName):
        self.read_file_to_bytes(fileName, self.__path)

    def checkDownloadFile(self):
        pass

    def getFiles(self, path='wave/model/2017/'):
        self.connect()
        self.__ftp.cwd(path)
        i=0;
        while i<self.__numOfProgn:
            if(((self.__enteredDate.day-i)>0)& (self.__enteredDate.day-i<31)):
                try:
                    self.__ftp.cwd(self.__enteredDate.year.__str__()+
                               (('0'+self.__enteredDate.month.__str__())if (self.__enteredDate.month<10) else self.__enteredDate.month.__str__())+
                               (('0'+(self.__enteredDate.day-i).__str__())if (self.__enteredDate.day-i<10) else (self.__enteredDate.day-i).__str__()))
                    for dirFile in self.__ftp.nlst():
                        dateFileValue = datetime(int(dirFile.split('_')[0][0:4]), int(dirFile.split('_')[0][4:6]),
                                                 int(dirFile.split('_')[0][6:8]))
                        if (dateFileValue==self.__enteredDate):
                            self.downFiles(dirFile, 'ftp/model/');
                    self.__ftp.cwd('..')
                except:
                    pass
            i+=1
