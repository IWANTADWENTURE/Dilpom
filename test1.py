import netCDF4;
from libraries import ftpManager;
from libraries import zipArchiveManager;
from datetime import datetime,timedelta;
import matplotlib as mpl;
import math;
from ftplib import FTP
import matplotlib.pyplot as plt
import numpy;
import os, sys;

def Fun():
    RD= [0]*7;
    return RD;
print(Fun())
"""

__hostSatelite = "avisoftp.cnes.fr"
__hostModel = "innovation.org.ru"
__loginSatelite = ""
__loginModel = "diplom"
__passwordSatelite = ""
__passwordModel = "QNLN9p?7b"
__ftpSatelite = None
__ftpModel = None
ftp = FTP(__hostModel)
ftp.login(__loginModel, __passwordModel)
listfiles=['20170102_hi-MFCBS-MODEL-SWAN-BLS-b20170102-fv01.0.nc', '20170105_hi-MFCBS-MODEL-SWAN-BLS-b20170105-fv01.0.nc']
for file in listfiles:
    ftp.retrbinary("RETR %s" % file, open('ftp/model/' + file, 'wb').write)

lat=43
lon=34
time=datetime.strptime('2017.02.12 08:15:00', '%Y.%m.%d %H:%M:%S')
ncfile = netCDF4.Dataset('ftp/model/20170212_hi-MFCBS-MODEL-SWAN-BLS-b20170212-fv01.0.nc')
time_units = ncfile.variables['time'].units
times=netCDF4.date2num(time,time_units)
ilt=math.floor(((lat-ncfile.variables['lat'][0])/(ncfile.variables['lat'][1]-ncfile.variables['lat'][0])))+1
if((ilt>=1)&(ilt+1<=132)):
    if((abs(lat-ncfile.variables['lat'][ilt+1]))<(abs(lat-ncfile.variables['lat'][ilt]))):
        ilt+=1;
iln=math.floor(((lon-ncfile.variables['lon'][0])/(ncfile.variables['lon'][2]-ncfile.variables['lon'][1])))+1
if((iln>=1)&(iln+1<=238)):
    if((abs(lon-ncfile.variables['lon'][iln+1]))<(abs(lon-ncfile.variables['lon'][iln]))):
        iln+=1;
itime=math.floor(((times-ncfile.variables['time'][0])/(ncfile.variables['time'][1]-ncfile.variables['time'][0])))+1
if((itime>=1)&(itime+1<=24)):
    if((abs(times-ncfile.variables['time'][itime+1]))<(abs(times-ncfile.variables['time'][itime]))):
        itime+=1;
print(ilt)
print(ncfile.variables['lat'][ilt])
print(iln)
print(ncfile.variables['lon'][iln])
print(itime)
print(ncfile.variables['time'][itime])
#print(netCDF4.num2date(ncfile.variables['time'][itime],time_units))
print(ncfile.variables['hsig'][itime][ilt][iln])
#print(len(ncfile.variables['hsig'][23]))

print('{0:26s} {1:9} {2:9} {3:8} {4:20} {5:9} {6:9} {7:8}'.format(
    'time_sat','lat_sat', 'lon_sat', 'hsig_sat', 'time_mod','lat_mod', 'lon_mod', 'hsig_mod'))
while i<len(arrayOfUnitedData[0][0]):
    print('{0:26s} {1:9f} {2:9f} {3:8f} {4:20s} {5:9f} {6:9f} {7:8f}'.format(
        netCDF4.num2date(arrayOfUnitedData[0][0][i], time_units).__str__(),arrayOfUnitedData[0][1][i],arrayOfUnitedData[0][2][i],arrayOfUnitedData[0][3][i],
        netCDF4.num2date(arrayOfUnitedData[1][0][i], mod_time_units).__str__(),arrayOfUnitedData[1][1][i],arrayOfUnitedData[1][2][i],arrayOfUnitedData[1][3][i]))
    i+=1

plt.figure(2)
plt.plot(arrayOfUnitedData[0][3],arrayOfUnitedData[1][3],'ro', ms=1)
plt.show()

print('{0:8} {1:8} {2:8} {3:8} {4:8}'.format(
    'ME','RMSE', 'SD', 'SI', 'r'))
while i<len(ME):
    print('{0:8f} {1:8f} {2:8f} {3:8f} {4:8f}'.format(
        ME[i], RMSE[i], SD[i], SI[i], r[i]))
    i+=1

i=0;
print('{0:8} {1:8}'.format(
    'hsig_sat', 'hsig_mod'))
while i<len(arrayOfUnitedData[0][0]):
    print('{0:8f} {1:8f}'.format(
        arrayOfUnitedData[0][3][i],arrayOfUnitedData[5][3][i]))
    i+=1
"""