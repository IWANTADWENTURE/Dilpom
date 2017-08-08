from abc import abstractmethod, abstractproperty

class ConnectorInterface():

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def toDirectory(self):
        pass

    @abstractmethod
    def downloadFile(self):
        pass

    @abstractmethod
    def checkDownloadFile(self):
        pass

    @abstractmethod
    def getFiles(self):
        pass