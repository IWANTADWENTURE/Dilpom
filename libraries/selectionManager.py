import netCDF4;
import os, sys;
import numpy, math;
from libraries import satelite_FTP_Connector, model_FTP_Connector;
from libraries import zipArchiveManager;
from datetime import datetime,timedelta;

class SelectionController():

    __list_ncvariables = ['time', 'lat', 'lon', 'range_numval_ku', 'range_rms_ku', 'alt', 'range_ku', 'iono_corr_alt_ku',
                        'sea_state_bias_ku', 'ocean_tide_sol1', 'solid_earth_tide', 'pole_tide', 'swh_ku', 'sig0_ku',
                        'wind_speed_alt', 'off_nadir_angle_wf_ku', 'sig0_rms_ku', 'sig0_numval_ku'];
    __time_units=None
    def getSateliteData(self, enteredDate):
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
            self.__time_units = ncfile.variables['time'].units
            times = netCDF4.num2date(time, self.__time_units)
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
        y = 0;
        while y < len(arrSatDat):
            arrSatDat[y] = numpy.delete(arrSatDat[y], 0);
            y += 1
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
            arrSatDat[y] = arrSatDat[y][sel]
            y += 1
        return arrSatDat;

    def getModelData(self, arrSatDat, enteredDate):
        # Download archive with Model Data
        #ftp = model_FTP_Connector.SateliteFTPConnector("innovation.org.ru", "diplom", "QNLN9p?7b")
        #ftp.getFiles() #Format date must be Year.Month.Day Hout:minute:second

        # Unpack downloaded archives
        #archive = zipArchiveManager.ZIPController()
        #archive.sortoutForUnpackModel();
        y = 0;
        arrUnDat = [0] * 5
        for nc in os.listdir('ftp/model/'):
            arrayOfModelData = [0] * 4
            ncfile = netCDF4.Dataset('ftp/model/' + nc)
            lat = ncfile.variables['lat'][:];
            lon = ncfile.variables['lon'][:];
            time = ncfile.variables['time'][:];
            mod_time_units = ncfile.variables['time'].units;
            i = 0;
            while i < len(arrSatDat[0]):
                itime = math.floor((arrSatDat[0][i] - netCDF4.date2num(
                    netCDF4.num2date(time[0], mod_time_units), self.__time_units)) /
                                   (netCDF4.date2num(netCDF4.num2date(time[1], ncfile.variables['time'].units),
                                                     self.__time_units) -
                                    netCDF4.date2num(netCDF4.num2date(time[0], ncfile.variables['time'].units),
                                                     self.__time_units)))
                if ((itime >= 0) & (itime+1 <= 23)):
                    if ((abs(arrSatDat[0][i]
                                 - netCDF4.date2num(netCDF4.num2date(time[itime + 1], mod_time_units), self.__time_units))) <
                            (abs(arrSatDat[0][i]
                                     - netCDF4.date2num(netCDF4.num2date(time[itime], mod_time_units), self.__time_units)))):
                        itime += 1;
                ilt = math.floor(((arrSatDat[1][i] - lat[0]) / (lat[1] - lat[0])))
                if ((ilt >= 0) & (ilt <= 131)):
                    if ((abs(arrSatDat[1][i] - lat[ilt + 1])) < (abs(arrSatDat[1][i] - lat[ilt]))):
                        ilt += 1;
                iln = math.floor(((arrSatDat[2][i] - lon[0]) / (lon[1] - lon[0])))
                if ((iln >= 0) & (iln <= 237)):
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
        return arrUnDat

