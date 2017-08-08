from libraries.Selector import SelectorInterface
import netCDF4;
import os, sys;
import numpy, math;
from libraries import satelite_FTP_Connector, model_FTP_Connector
from libraries import zipArchiveManager
from datetime import datetime,timedelta

class SateliteSelector(SelectorInterface):

    __list_ncvariables=None

    def __init__(self, ncvariables):
        self.__list_ncvariables=ncvariables

    def getData(self, enteredDate):
        firstDate = enteredDate - timedelta(
            hours=1)  # datetime.strptime('2017.02.03 10:00:00', '%Y.%m.%d %H:%M:%S')#"2017.03.02 23:15:00"#Верний порог времени
        lastDate = enteredDate + timedelta(
            hours=25)  # datetime.strptime('2017.02.13 08:15:00', '%Y.%m.%d %H:%M:%S')#"2017.03.03 02:15:00"#Нижний порог времени

        # Download archive with Satelite Data
        #ftp = satelite_FTP_Connector.SateliteFTPConnector(enteredDate, "avisoftp.cnes.fr")
        #ftp.getFiles() #Format date must be Year.Month.Day Hout:minute:second

        # Unpack downloaded archives
        #archive = zipArchiveManager.ZIPController()
        #archive.sortoutForUnpackSatelite();

        arrayOfSateliteData = [0] * len(self.__list_ncvariables)
        for nc in os.listdir('ftp/satelite/'):
            ncfile = netCDF4.Dataset('ftp/satelite/' + nc)
            lat = ncfile.variables['lat'][:];
            lon = ncfile.variables['lon'][:];
            time = ncfile.variables['time'][:];
            time_units = ncfile.variables['time'].units
            times = netCDF4.num2date(time, time_units)
            sel = (lon[:] > 27) & (lon[:] < 42) &\
                  (lat[:] > 40) & (lat[:] < 48) & \
                  (times[:] >= firstDate) & (times[:] <= lastDate)
            i = 0;
            while i < len(self.__list_ncvariables):
                arrayOfSateliteData[i] = numpy.hstack(
                    (arrayOfSateliteData[i], ncfile.variables[self.__list_ncvariables[i]][sel]));
                i += 1
            ncfile.close()
        return self.selectData(arrayOfSateliteData), time_units

    def selectData(self, arrSatDat):
        y = 0;
        while y < len(arrSatDat):
            arrSatDat[y] = numpy.delete(arrSatDat[y], 0);
            y += 1
        sel = [True] * len(arrSatDat[0])
        sel = sel & ((arrSatDat[3][:] >= 0.1)&(arrSatDat[3][:] <= 11))
        sel = sel & ((arrSatDat[4][:] >= 0) & (arrSatDat[4][:] <= 0.2))
        sel = sel & (arrSatDat[5][:]>=18)
        sel = sel & ((arrSatDat[6][:] >= (-0.5)) & (arrSatDat[6][:] <= 0.0))
        sel = sel & ((arrSatDat[7][:] >= (-0.2)) & (arrSatDat[7][:] <= 0.16))
        sel = sel & ((arrSatDat[8][:] >= (7)) & (arrSatDat[8][:] <= 30))
        sel = sel & ((arrSatDat[9][:] >= (0)) & (arrSatDat[9][:] <= 1))
        sel = sel & (arrSatDat[10][:] >= 18)
        sel = sel & ((arrSatDat[11][:] >= 0.5) & (arrSatDat[11][:] <= 28))
        y = 0;
        while y < len(arrSatDat):
            arrSatDat[y] = arrSatDat[y][sel]
            y += 1
        print(len(arrSatDat[0]))
        return arrSatDat;


    """"" sel = [True] * len(arrSatDat[0])
        sel = sel & (arrSatDat[3][:] >= 10)
        sel = sel & ((arrSatDat[4][:] >= 0) & (arrSatDat[4][:] <= 200))
        sel = sel & (((arrSatDat[5][:] - arrSatDat[6][:]) >= (-130000)) & \
              ((arrSatDat[5][:] - arrSatDat[6][:]) <= 100000))
        sel = sel & ((arrSatDat[7][:] >= (-400)) & (arrSatDat[7][:] <= 40))
        sel = sel & ((arrSatDat[8][:] >= (-500)) & (arrSatDat[8][:] <= 0))
        sel = sel & ((arrSatDat[9][:] >= (-5000)) & (arrSatDat[9][:] <= 5000))
        sel = sel & ((arrSatDat[10][:] >= (-1000)) & (arrSatDat[10][:] <= 1000))
        sel = sel & ((arrSatDat[11][:] >= (-150)) & (arrSatDat[11][:] <= 150))
        sel = sel & ((arrSatDat[12][:] >= 0) & (arrSatDat[12][:] <= 11000))
        sel = sel & ((arrSatDat[13][:] >= 7) & (arrSatDat[13][:] <= 30))
        sel = sel & ((arrSatDat[14][:] >= 0) & (arrSatDat[14][:] <= 30))
        sel = sel & ((arrSatDat[15][:] >= (-0.2)) & (arrSatDat[15][:] <= 0.64))
        sel = sel & ((arrSatDat[16][:] <= 1))
        sel = sel & ((arrSatDat[17][:] > 10))"""