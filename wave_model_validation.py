import netCDF4;
from libraries import ftpManager;
from libraries import zipArchiveManager;
from libraries import plotManager;
from datetime import datetime,timedelta;
import numpy;
import os, sys;
import math;
import statistics;
import statsmodels;
import pandas;

enteredDate=datetime.strptime('2017.02.06 00:00:00', '%Y.%m.%d %H:%M:%S')
ifRendering=True;
list_ncvariables=['time','lat','lon','range_numval_ku','range_rms_ku', 'alt','range_ku','iono_corr_alt_ku','sea_state_bias_ku','ocean_tide_sol1','solid_earth_tide','pole_tide','swh_ku','sig0_ku','wind_speed_alt','off_nadir_angle_wf_ku','sig0_rms_ku','sig0_numval_ku'];
firstDate=enteredDate-timedelta(hours=1)#datetime.strptime('2017.02.03 10:00:00', '%Y.%m.%d %H:%M:%S')#"2017.03.02 23:15:00"#Верний порог времени
lastDate=enteredDate+timedelta(hours=25)#datetime.strptime('2017.02.13 08:15:00', '%Y.%m.%d %H:%M:%S')#"2017.03.03 02:15:00"#Нижний порог времени

#Download archive with Satelite Data
#ftp = ftpManager.FTPConnector()
#ftp.getFilesWithSateliteData(firstDate, lastDate) #Format date must be Year.Month.Day Hout:minute:second

#Unpack downloaded archives
#archive = zipArchiveManager.ZIPController()
#archive.sortoutForUnpackSatelite();

arrayOfSateliteData =[0]*len(list_ncvariables)
for nc in os.listdir('ftp/satelite/'):
    ncfile=netCDF4.Dataset('ftp/satelite/'+nc)
    lat=ncfile.variables['lat'][:];
    lon=ncfile.variables['lon'][:];
    time=ncfile.variables['time'][:];
    time_units = ncfile.variables['time'].units
    times=netCDF4.num2date(time,time_units)
    sel=(lat[:]>40) & (lat[:]<48) & \
        (lon[:]>27) & (lon[:]<42) & \
        (times[:]>=firstDate) & (times[:] <=lastDate)
    i=0;
    while i < len(list_ncvariables):
        arrayOfSateliteData[i] = numpy.hstack((arrayOfSateliteData[i], ncfile.variables[list_ncvariables[i]][sel]));
        i += 1
    ncfile.close()

y=0;
while y<len(arrayOfSateliteData):
        arrayOfSateliteData[y] = numpy.delete(arrayOfSateliteData[y], 0);
        y+=1
sel=[True]*len(arrayOfSateliteData[0])
sel=sel&(arrayOfSateliteData[3][:]>=10)
sel=sel&(arrayOfSateliteData[4][:]>=0) & (arrayOfSateliteData[4][:]<=200)
sel=sel&((arrayOfSateliteData[5][:]-arrayOfSateliteData[6][:])>=(-130000)) & ((arrayOfSateliteData[5][:]-arrayOfSateliteData[6][:])<=100000)
sel=sel&(arrayOfSateliteData[7][:]>=(-400)) & (arrayOfSateliteData[7][:]<=40)
sel=sel&(arrayOfSateliteData[8][:]>=(-500)) & (arrayOfSateliteData[8][:]<=0)
sel=sel&(arrayOfSateliteData[9][:]>=(-5000)) & (arrayOfSateliteData[9][:]<=5000)
sel=sel&(arrayOfSateliteData[10][:]>=(-1000)) & (arrayOfSateliteData[10][:]<=1000)
sel=sel&(arrayOfSateliteData[11][:]>=(-150)) & (arrayOfSateliteData[11][:]<=150)
sel=sel&(arrayOfSateliteData[12][:]>=0) & (arrayOfSateliteData[12][:]<=11000)
sel=sel&(arrayOfSateliteData[13][:]>=7) & (arrayOfSateliteData[13][:]<=30)
sel=sel&(arrayOfSateliteData[14][:]>=0) & (arrayOfSateliteData[14][:]<=30)
sel=sel&(arrayOfSateliteData[15][:]>=(-0.2)) & (arrayOfSateliteData[15][:]<=0.64)
sel=sel&(arrayOfSateliteData[16][:]<=1)
sel=sel&(arrayOfSateliteData[17][:]>10)
y=0;
while y<len(arrayOfSateliteData):
        arrayOfSateliteData[y] = arrayOfSateliteData[y][sel]
        y+=1
"""selMan=selectionManager.SelectionController()
arrayOfSateliteData=selMan.getSateliteData(enteredDate)
print(arrayOfSateliteData)"""
#Download archive with Model Data
#ftp = ftpManager.FTPConnector()
#ftp.getFilesWithModelData(enteredDate) #Format date must be Year.Month.Day Hout:minute:second

#Unpack downloaded archives
#archive = zipArchiveManager.ZIPController()
#archive.sortoutForUnpackModel();

arrayOfUnitedData=[0]*6
arrayOfUnitedData[0]=[arrayOfSateliteData[0][:],arrayOfSateliteData[1][:],arrayOfSateliteData[2][:],arrayOfSateliteData[12][:]]
y=1;
for nc in os.listdir('ftp/model/'):
    arrayOfModelData =[0]*4
    ncfile=netCDF4.Dataset('ftp/model/'+nc)
    lat=ncfile.variables['lat'][:];
    lon=ncfile.variables['lon'][:];
    time=ncfile.variables['time'][:];
    mod_time_units=ncfile.variables['time'].units;
    i=0;
    while i < len(arrayOfSateliteData[0]):
        itime=math.floor((arrayOfSateliteData[0][i]-netCDF4.date2num(netCDF4.num2date(time[0], mod_time_units),time_units))/
                         (netCDF4.date2num(netCDF4.num2date(time[1], ncfile.variables['time'].units), time_units)-
                          netCDF4.date2num(netCDF4.num2date(time[0], ncfile.variables['time'].units), time_units)))
        if((itime>=0)&(itime<=23)):
            if((abs(arrayOfSateliteData[0][i]
                          -netCDF4.date2num(netCDF4.num2date(time[itime+1], mod_time_units),time_units)))<
                   (abs(arrayOfSateliteData[0][i]
                          -netCDF4.date2num(netCDF4.num2date(time[itime], mod_time_units),time_units)))):
                itime+=1;
        ilt=math.floor(((arrayOfSateliteData[1][i]-lat[0])/(lat[1]-lat[0])))
        if((ilt>=0)&(ilt<=131)):
            if((abs(arrayOfSateliteData[1][i]-lat[ilt+1]))<(abs(arrayOfSateliteData[1][i]-lat[ilt]))):
                ilt+=1;
        iln=math.floor(((arrayOfSateliteData[2][i]-lon[0])/(lon[1]-lon[0])))
        if((iln>=0)&(iln<=237)):
            if((abs(arrayOfSateliteData[2][i]-lon[iln+1]))<(abs(arrayOfSateliteData[2][i]-lon[iln]))):
                iln+=1;
        arrayOfModelData[0] = numpy.hstack((arrayOfModelData[0], time[itime]));
        arrayOfModelData[1] = numpy.hstack((arrayOfModelData[1], lat[ilt]));
        arrayOfModelData[2] = numpy.hstack((arrayOfModelData[2], lon[iln]));
        arrayOfModelData[3] = numpy.hstack((arrayOfModelData[3], ncfile.variables['hsig'][itime][ilt][iln]));
        i += 1
    arrayOfUnitedData[y]=arrayOfModelData;
    y+=1;
    ncfile.close()

y=1;
while y<len(arrayOfUnitedData):
    arrayOfUnitedData[y][0] = numpy.delete(arrayOfUnitedData[y][0], 0);
    arrayOfUnitedData[y][1] = numpy.delete(arrayOfUnitedData[y][1], 0);
    arrayOfUnitedData[y][2] = numpy.delete(arrayOfUnitedData[y][2], 0);
    arrayOfUnitedData[y][3] = numpy.delete(arrayOfUnitedData[y][3], 0);
    y+=1

RMSE, ME, SD, SI, r=[0]*5,[0]*5,[0]*5,[0]*5,[0]*5
i=0;
while i<len(arrayOfUnitedData[0][0]):
    ME[0]=ME[0]+(arrayOfUnitedData[5][3][i]-arrayOfUnitedData[0][3][i])
    ME[1]=ME[1]+(arrayOfUnitedData[4][3][i]-arrayOfUnitedData[0][3][i])
    ME[2]=ME[2]+(arrayOfUnitedData[3][3][i]-arrayOfUnitedData[0][3][i])
    ME[3]=ME[3]+(arrayOfUnitedData[2][3][i]-arrayOfUnitedData[0][3][i])
    ME[4]=ME[4]+(arrayOfUnitedData[1][3][i]-arrayOfUnitedData[0][3][i])
    RMSE[0]=RMSE[0]+(arrayOfUnitedData[5][3][i]-arrayOfUnitedData[0][3][i])**2
    RMSE[1]=RMSE[1]+(arrayOfUnitedData[4][3][i]-arrayOfUnitedData[0][3][i])**2
    RMSE[2]=RMSE[2]+(arrayOfUnitedData[3][3][i]-arrayOfUnitedData[0][3][i])**2
    RMSE[3]=RMSE[3]+(arrayOfUnitedData[2][3][i]-arrayOfUnitedData[0][3][i])**2
    RMSE[4]=RMSE[4]+(arrayOfUnitedData[1][3][i]-arrayOfUnitedData[0][3][i])**2
    i+=1;
i=0;
while i<len(ME):
    ME[i]=ME[i]/len(arrayOfUnitedData[0][0])
    RMSE[i]=numpy.sqrt(RMSE[i]/len(arrayOfUnitedData[0][0]))
    SD[i]=numpy.sqrt(RMSE[i]**2-ME[i]**2)
    SI[i]=RMSE[i]/statistics.mean(arrayOfUnitedData[0][3])
    r[i]=numpy.corrcoef(arrayOfUnitedData[i+1][3], arrayOfUnitedData[0][3])[1,0]
    i+=1
i=0
print(pandas.DataFrame(data=[ME, RMSE, SD, SI, r], index=['ME','RMSE', 'SD', 'SI', 'r']).head())
if(ifRendering):
    plM=plotManager.plotRenderingController();
    plM.renderHsig(arrayOfUnitedData);