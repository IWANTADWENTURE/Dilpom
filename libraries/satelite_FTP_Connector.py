from libraries import Connector
from datetime import datetime, timedelta
import FTP

class SateliteFTPConnector(Connector):

    __ftp=None
    __host=None
    __login=None
    __password=None
    __path=None
    __enteredDate=None
    __beginOfTime=None
    __endOfTime=None

    def __init__(self, enteredDate, host='', login='', password='', path='ftp/satelite'):
        self.__host=host
        self.__login=login
        self.__password=password
        self.__path=path
        self.__enteredDate=enteredDate
        self.__beginOfTime=enteredDate-timedelta(hours=1)#datetime.strptime('2017.02.03 10:00:00', '%Y.%m.%d %H:%M:%S')#"2017.03.02 23:15:00"#Верний порог времени
        self.__endOfTime=enteredDate+timedelta(hours=25)#datetime.strptime('2017.02.13 08:15:00', '%Y.%m.%d %H:%M:%S')#"2017.03.03 02:15:00"#Нижний порог времени

    def connect(self):
        self.__ftp=FTP(self.__host)
        self.__ftp.login(self.__login, self.__password)

    def disconnect(self):
        self.__ftp.quit()

    def downloadFile(self, fileName):
        self.read_file_to_bytes(fileName, self.__path)

    def checkDownloadFile(self):
        pass

    def getFiles(self, path='AVISO/pub/jason-2/igdr/'):
        self.connect()
        self.__ftp.cwd(path)
        for cycle in self.__ftp.nlst():
            self.__ftp.cwd(cycle + "/")
            for dirFile in self.__ftp.nlst():
                dateFileValue = datetime(int(dirFile.split('_')[4][0:4]), int(dirFile.split('_')[4][4:6]),
                                         int(dirFile.split('_')[4][6:8]), int(dirFile.split('_')[5][0:2]),
                                         int(dirFile.split('_')[5][2:4]), int(dirFile.split('_')[5][4:6]))
                if ((dateFileValue >= self.__beginOfTime) & (dateFileValue <= self.__endOfTime)):
                    self.downloadFile(dirFile, 'ftp/satelite/');
            self.__ftp.cwd('..')

