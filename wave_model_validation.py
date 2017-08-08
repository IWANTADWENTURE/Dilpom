import netCDF4;
from libraries import ftpManager;
from libraries import zipArchiveManager;
from datetime import datetime,timedelta;
import os, sys;

list_ncvariables=['range_numval_ku','range_rms_ku','alt','range_ku','model_dry_tropo_corr','rad_wet_tropo_corr','iono_corr_alt_ku','sea_state_bias_ku','ocean_tide_sol1','solid_earth_tide','pole_tide','swh_ku','sig0_ku','wind_speed_alt','off_nadir_angle_wf_ku','sig0_rms_ku','sig0_numval_ku'];
firstDate=datetime.strptime('2017.03.02 23:15:00', '%Y.%m.%d %H:%M:%S')#"2017.03.02 23:15:00"#Верний порог времени
lastDate=datetime.strptime('2017.03.05 02:15:00', '%Y.%m.%d %H:%M:%S')#"2017.03.03 02:15:00"#Нижний порог времени
"""""
#Разница между порогами времени и точкой отсчета спутника
#firstDateInSecond=timedelta.total_seconds(datetime.strptime(startDate, '%Y.%m.%d %H:%M:%S')-datetime.strptime(firstDate, '%Y.%m.%d %H:%M:%S'))
#lastDateInSecond=timedelta.total_seconds(datetime.strptime(startDate, '%Y.%m.%d %H:%M:%S')-datetime.strptime(lastDate, '%Y.%m.%d %H:%M:%S'))
#print(timedelta.total_seconds(firstDateInSecond))
"""""
#Download archive with Satelite Data
ftp = ftpManager.FTPConnector()
ftp.getFilesFromDir(firstDate, lastDate) #Format date must be Year.Month.Day Hout:minute:second

#Unpack downloaded archives
archive = zipArchiveManager.ZIPController()
archive.sortoutForUnpack();

#
arratOfSateliteData={}
for ncvariable in list_ncvariables:
    arratOfSateliteData[ncvariable] =[]
for nc in os.listdir('ftp/satelite/'):
    ncfile=netCDF4.Dataset('ftp/satelite/'+nc)
    lat=ncfile.variables['lat'][:];
    lon=ncfile.variables['lon'][:];
    time=ncfile.variables['time'][:];
    time_units = ncfile.variables['time'].units
    times=netCDF4.num2date(time,time_units)
    sel=(lat[:]>40) & (lat[:]<48) & (lon[:]>27) & (lon[:]<42) & (times[:]>=firstDate) & (times[:] <=lastDate)
    for ncvariable in list_ncvariables:
        arratOfSateliteData[ncvariable]=arratOfSateliteData[ncvariable]+ncfile.variables[ncvariable][sel]
    ncfile.close()
print(arratOfSateliteData)