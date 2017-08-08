from abc import abstractmethod, abstractproperty

class SelectorInterface(object):

    @abstractmethod
    def getFiles(self):
        pass

    @abstractmethod
    def selectData(self):
        pass