from zipfile import ZipFile;
from netCDF4 import Dataset;
import frpManager;
import urllib.request;
import os, sys;
os.makedirs('/ftp/satelite',mode=0o777, exist_ok=True);
destination = 'ftp/satelite/JA2_IPN_2PdP319_001_20170223_063707_20170223_073320.zip'
url = 'ftp://avisoftp.cnes.fr/AVISO/pub/jason-2/igdr/cycle_319/JA2_IPN_2PdP319_001_20170223_063707_20170223_073320.zip'
urllib.request.urlretrieve(url, destination)
path_to_satelite_ncfile="C://Create/Dip/satelite/JA2_IPN_2PdP313_160_20161231_234407_20170101_004019.nc";
path_to_model_ncfile="C://Create/Dip/model/20170101_hi-MFCBS-MODEL-SWAN-BLS-b20170101-fv01.0.nc";
list_ncvariables=['range_numval_ku','range_rms_ku','alt','range_ku','model_dry_tropo_corr','rad_wet_tropo_corr','iono_corr_alt_ku','sea_state_bias_ku','ocean_tide_sol1','solid_earth_tide','pole_tide','swh_ku','sig0_ku','wind_speed_alt','off_nadir_angle_wf_ku','sig0_rms_ku','sig0_numval_ku'];
# Открываем архив на чтение
#z = ZipFile('C://Create/Dip/satelite/JA2_IPN_2PdP313_160_20161231_234407_20170101_004019.zip', 'r')
# Тестирование архива, пробная распаковка
#z.testzip()
# Список файлов
#print(z.namelist())
# Читаем файл
# rootgrp=Dataset(z.read("C://Create/Dip/satelite/JA2_IPN_2PdP313_160_20161231_234407_20170101_004019.nc"))
array_of_sateliteData={};
array_of_modelData={};
ncfile=Dataset(path_to_satelite_ncfile);
for variable in list_ncvariables:
    array_of_sateliteData[variable]=ncfile.variables[variable][:]
""""ncfile=Dataset(path_to_model_ncfile);
for variable in list_ncvariables:
    array_of_modelData[variable]=ncfile.variables[variable][:]
print(array_of_sateliteData);
print(array_of_modelData);
"""""
array_of_unitedData={'satelite':array_of_sateliteData};
#print(array_of_sateliteData['alt'][1:10]);
#print(array_of_unitedData);
print(ncfile.variables['time'][:])
fgh = frpManager.FTPConnector()
fgh.__init__()
fgh.getFilesFromDir()
#print(range_ku);
#print((ncfile.variables['alt'][9]-ncfile.variables['range_ku'][9])*10000)
""""
print(ncfile.variables['range_numval_ku'])
ncfile.data_model
NUMPY SCPY
arr = ncfile.variables['range_numval_ku'][:]
for ncattr in ncfile.variables['range_numval_ku'].ncattrs():
    print('\t\t%s:' % ncattr,' ')
    repr(ncfile.variables['range_numval_ku'].getncattr(ncattr))
print(ncfile.variables['range_rms_ku'])
print(ncfile.variables['range_rms_ku'][:])
print(ncfile.variables['range_ku'])
print(ncfile.variables['range_ku'][:])
Кооординаты черного моря lon 27-42 lat 40-48
"""""
#print(ncfile.units)
#z.close()
ncfile.close()
