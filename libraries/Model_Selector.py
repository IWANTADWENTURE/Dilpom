from libraries.Selector import SelectorInterface
import netCDF4;
import os, sys;
import numpy, math;
from libraries import satelite_FTP_Connector, model_FTP_Connector
from libraries import zipArchiveManager
from datetime import datetime,timedelta

class ModelSelector(SelectorInterface):

    def getData(self, arrSatDat, enteredDate, numOfProgn, time_units):
        # Download archive with Model Data
        #ftp = model_FTP_Connector.ModelFTPConnector(enteredDate, numOfProgn, "innovation.org.ru", "diplom", "QNLN9p?7b")
        #ftp.getFiles() #Format date must be Year.Month.Day Hout:minute:second

        # Unpack downloaded archives
        #archive = zipArchiveManager.ZIPController()
        #archive.sortoutForUnpackModel();
        y = 0;
        arrUnDat = [0] * 5
        for nc in os.listdir('ftp/model/'):
            print(nc)
            arrayOfModelData = [0] * 4
            ncfile = netCDF4.Dataset('ftp/model/' + nc)
            lat = ncfile.variables['lat'][:];
            lon = ncfile.variables['lon'][:];
            time = ncfile.variables['time'][:];
            mod_time_units = ncfile.variables['time'].units;
            i = 0;
            while i < len(arrSatDat[0]):
                itime = math.floor(abs(arrSatDat[0][i] - netCDF4.date2num(
                    netCDF4.num2date(time[0], mod_time_units), time_units)) /
                                   (netCDF4.date2num(netCDF4.num2date(time[1], ncfile.variables['time'].units),
                                                     time_units) -
                                    netCDF4.date2num(netCDF4.num2date(time[0], ncfile.variables['time'].units),
                                                     time_units)))
                if ((itime >= 0) & (itime+1 < 24)):
                    if ((abs(arrSatDat[0][i]
                                 - netCDF4.date2num(netCDF4.num2date(time[itime + 1], mod_time_units), time_units))) <
                            (abs(arrSatDat[0][i]
                                     - netCDF4.date2num(netCDF4.num2date(time[itime], mod_time_units), time_units)))):
                        itime += 1;
                ilt = math.floor(((arrSatDat[1][i] - lat[0]) / (lat[1] - lat[0])))
                if ((ilt >= 0) & (ilt+1 < 132)):
                    if ((abs(arrSatDat[1][i] - lat[ilt + 1])) < (abs(arrSatDat[1][i] - lat[ilt]))):
                        ilt += 1;
                iln = math.floor(((arrSatDat[2][i] - lon[0]) / (lon[1] - lon[0])))
                if ((iln >= 0) & (iln+1 <238)):
                    if ((abs(arrSatDat[2][i] - lon[iln + 1])) < (abs(arrSatDat[2][i] - lon[iln]))):
                        iln += 1;
                arrayOfModelData[0] = numpy.hstack((arrayOfModelData[0], time[itime]));
                arrayOfModelData[1] = numpy.hstack((arrayOfModelData[1], lat[ilt]));
                arrayOfModelData[2] = numpy.hstack((arrayOfModelData[2], lon[iln]));
                arrayOfModelData[3] = numpy.hstack((arrayOfModelData[3], ncfile.variables['hsig'][itime][ilt][iln]));
                i += 1
            arrUnDat[y] = arrayOfModelData;
            y += 1;
            ncfile.close()
        y = 0;
        while y < len(arrUnDat):
            arrUnDat[y][0] = numpy.delete(arrUnDat[y][0], 0);
            arrUnDat[y][1] = numpy.delete(arrUnDat[y][1], 0);
            arrUnDat[y][2] = numpy.delete(arrUnDat[y][2], 0);
            arrUnDat[y][3] = numpy.delete(arrUnDat[y][3], 0);
            y += 1
        while y < len(arrUnDat):
            y += 1

        return arrUnDat, mod_time_units
