from zipfile import ZipFile;
import os, sys;

class ZIPController():

    def unpacker(self, archiveName):
        unpackedFile=ZipFile('ftp/satelite/'+archiveName, 'r');
        #print(archiveName[:-3]+'nc')
        #print(unpackedFile.testzip())
        #unpackedFile.extractall('ftp/satelite/'+archiveName[:-3]+'nc')
        unpackedFile.extract(archiveName[:-3]+'nc','ftp/satelite/')
        #return unpackedFile.read(archiveName[:-3] + 'nc')

    def sortoutForUnpack(self):
        for zipFile in os.listdir('ftp/satelite/'):  # Пофайлово распаковываеться из архива.
            self.unpacker(zipFile)
            os.remove('ftp/satelite/'+zipFile)
        #print(os.listdir('ftp/satelite/'));