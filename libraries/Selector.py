from abc import abstractmethod, abstractproperty

class SelectorInterface:

    @abstractmethod
    def getData(self):
        pass

    @abstractmethod
    def selectData(self):
        pass




