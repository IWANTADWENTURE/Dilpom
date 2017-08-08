import netCDF4;
from libraries import ftpManager;
from libraries import zipArchiveManager;
from libraries import plotManager, selectionManager;
from datetime import datetime,timedelta;
import numpy;
import os, sys;
import math;
import statistics;
import statsmodels;
import pandas;

enteredDate=datetime.strptime('2017.02.15 00:00:00', '%Y.%m.%d %H:%M:%S')
ifRendering=True;
list_ncvariables=['time','lat','lon','range_numval_ku','range_rms_ku', 'alt','range_ku','iono_corr_alt_ku','sea_state_bias_ku','ocean_tide_sol1','solid_earth_tide','pole_tide','swh_ku','sig0_ku','wind_speed_alt','off_nadir_angle_wf_ku','sig0_rms_ku','sig0_numval_ku'];
firstDate=enteredDate-timedelta(hours=1)#datetime.strptime('2017.02.03 10:00:00', '%Y.%m.%d %H:%M:%S')#"2017.03.02 23:15:00"#Верний порог времени
lastDate=enteredDate+timedelta(hours=25)#datetime.strptime('2017.02.13 08:15:00', '%Y.%m.%d %H:%M:%S')#"2017.03.03 02:15:00"#Нижний порог времени

selMan=selectionManager.SelectionController();
arrayOfSateliteData=selMan.getSateliteData(enteredDate)

arrayOfUnitedData=[0]*6
arrayOfUnitedData[0]=[arrayOfSateliteData[0][:],arrayOfSateliteData[1][:],arrayOfSateliteData[2][:],arrayOfSateliteData[12][:]]
arrayOfUnitedData[1:]=selMan.getModelData(arrayOfSateliteData, enteredDate)

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