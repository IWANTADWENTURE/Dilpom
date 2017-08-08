from zipfile import ZipFile;
import os, sys;

class ZIPController():
    def unpackerSatelite(self, archiveName):
        unpackedFile=ZipFile('ftp/satelite/'+archiveName, 'r');
        unpackedFile.extract(archiveName[:-3]+'nc','ftp/satelite/')

    def sortoutForUnpackSatelite(self):
        for zipFile in os.listdir('ftp/satelite/'):  # Пофайлово распаковываеться из архива.
            self.unpackerSatelite(zipFile)
            os.remove('ftp/satelite/'+zipFile)

    def sortoutForUnpackModel(self):
        for zipFile in os.listdir('ftp/model/'):  # Пофайлово распаковываеться из архива.
            self.unpackerModel(zipFile)
            os.remove('ftp/model/'+zipFile)

    def unpackerModel(self, archiveName):
        unpackedFile=ZipFile('ftp/model/'+archiveName, 'r');
        unpackedFile.extract(archiveName[:-4],'ftp/model/')