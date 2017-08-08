import netCDF4;
import os, sys;
import numpy;
from datetime import datetime,timedelta;

class SelectionController():

    __list_ncvariables = ['time', 'lat', 'lon', 'range_numval_ku', 'range_rms_ku', 'alt', 'range_ku', 'iono_corr_alt_ku',
                        'sea_state_bias_ku', 'ocean_tide_sol1', 'solid_earth_tide', 'pole_tide', 'swh_ku', 'sig0_ku',
                        'wind_speed_alt', 'off_nadir_angle_wf_ku', 'sig0_rms_ku', 'sig0_numval_ku'];

    def getSateliteData(self, enteredDate):
        firstDate = enteredDate - timedelta(
            hours=1)  # datetime.strptime('2017.02.03 10:00:00', '%Y.%m.%d %H:%M:%S')#"2017.03.02 23:15:00"#Верний порог времени
        lastDate = enteredDate + timedelta(
            hours=25)  # datetime.strptime('2017.02.13 08:15:00', '%Y.%m.%d %H:%M:%S')#"2017.03.03 02:15:00"#Нижний порог времени

        # Download archive with Satelite Data
        # ftp = ftpManager.FTPConnector()
        # ftp.getFilesWithSateliteData(firstDate, lastDate) #Format date must be Year.Month.Day Hout:minute:second

        # Unpack downloaded archives
        # archive = zipArchiveManager.ZIPController()
        # archive.sortoutForUnpackSatelite();

        arrayOfSateliteData = [0] * len(self.__list_ncvariables)
        for nc in os.listdir('ftp/satelite/'):
            ncfile = netCDF4.Dataset('ftp/satelite/' + nc)
            print(nc)
            lat = ncfile.variables['lat'][:];
            lon = ncfile.variables['lon'][:];
            time = ncfile.variables['time'][:];
            time_units = ncfile.variables['time'].units
            times = netCDF4.num2date(time, time_units)
            sel = (lat[:] > 40) & (lat[:] < 48) & \
                  (lon[:] > 27) & (lon[:] < 42) & \
                  (times[:] >= firstDate) & (times[:] <= lastDate)
            i = 0;
            while i < len(self.__list_ncvariables):
                arrayOfSateliteData[i] = numpy.hstack(
                    (arrayOfSateliteData[i], ncfile.variables[self.__list_ncvariables[i]][sel]));
                i += 1
            ncfile.close()
            return self.selectSateliteData(arrayOfSateliteData)

    def selectSateliteData(self, arrSatDat):
        sel = [True] * len(arrSatDat[0])
        sel = sel & (arrSatDat[3][:] >= 10)
        sel = sel & (arrSatDat[4][:] >= 0) & (arrSatDat[4][:] <= 200)
        sel = sel & ((arrSatDat[5][:] - arrSatDat[6][:]) >= (-130000)) & \
              ((arrSatDat[5][:] - arrSatDat[6][:]) <= 100000)
        sel = sel & (arrSatDat[7][:] >= (-400)) & (arrSatDat[7][:] <= 40)
        sel = sel & (arrSatDat[8][:] >= (-500)) & (arrSatDat[8][:] <= 0)
        sel = sel & (arrSatDat[9][:] >= (-5000)) & (arrSatDat[9][:] <= 5000)
        sel = sel & (arrSatDat[10][:] >= (-1000)) & (arrSatDat[10][:] <= 1000)
        sel = sel & (arrSatDat[11][:] >= (-150)) & (arrSatDat[11][:] <= 150)
        sel = sel & (arrSatDat[12][:] >= 0) & (arrSatDat[12][:] <= 11000)
        sel = sel & (arrSatDat[13][:] >= 7) & (arrSatDat[13][:] <= 30)
        sel = sel & (arrSatDat[14][:] >= 0) & (arrSatDat[14][:] <= 30)
        sel = sel & (arrSatDat[15][:] >= (-0.2)) & (arrSatDat[15][:] <= 0.64)
        sel = sel & (arrSatDat[16][:] <= 1)
        sel = sel & (arrSatDat[17][:] > 10)
        y = 0;
        while y < len(arrSatDat):
            arrSatDat[y] = numpy.delete(arrSatDat[y], 0);
            arrSatDat[y] = arrSatDat[y][sel]
            y += 1
        return arrSatDat;
