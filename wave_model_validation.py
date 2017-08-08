import netCDF4;
from libraries import plotManager, Satelite_Selector,Model_Selector;
from datetime import datetime;
import numpy;
import os, sys;
import statistics;
import pandas;

if __name__=="__main__":
    if len(sys.argv) == 3:
        enteredDate = datetime.strptime(sys.argv[1]+' 00:00:00', '%Y.%m.%d %H:%M:%S')
        numberOfPrognosis=sys.argv[2]
    elif len(sys.argv) == 2:
        enteredDate = datetime.strptime(sys.argv[1] + ' 00:00:00', '%Y.%m.%d %H:%M:%S')
        numberOfPrognosis=6
    else:
        enteredDate=datetime.strptime('2017.02.15 00:00:00', '%Y.%m.%d %H:%M:%S')
        numberOfPrognosis=6


list_ncvariables1 = ['time', 'lat', 'lon', 'range_numval_ku', 'range_rms_ku', 'alt', 'range_ku', 'iono_corr_alt_ku',
                    'sea_state_bias_ku', 'ocean_tide_sol1', 'solid_earth_tide', 'pole_tide', 'swh_ku', 'sig0_ku',
                    'wind_speed_alt', 'off_nadir_angle_wf_ku', 'sig0_rms_ku', 'sig0_numval_ku'];
list_ncvariables=['time', 'lat', 'lon', 'swh_ku', 'range_rms_ku', 'range_numval_ku',
                  'sea_state_bias_ku', 'off_nadir_angle_wf_ku', 'sig0_ku', 'sig0_rms_ku', 'sig0_numval_ku', 'wind_speed_alt']
ifRendering=True;
#list_ncvariables=['time','lat','lon','range_numval_ku','range_rms_ku', 'alt','range_ku','iono_corr_alt_ku','sea_state_bias_ku','ocean_tide_sol1','solid_earth_tide','pole_tide','swh_ku','sig0_ku','wind_speed_alt','off_nadir_angle_wf_ku','sig0_rms_ku','sig0_numval_ku'];

sel=Satelite_Selector.SateliteSelector(list_ncvariables);
arrayOfSateliteData, time_units=sel.getData(enteredDate)

sel=Model_Selector.ModelSelector()
arrayOfUnitedData=[0]*6
arrayOfUnitedData[0]=[arrayOfSateliteData[0][:],arrayOfSateliteData[1][:],arrayOfSateliteData[2][:],arrayOfSateliteData[3][:]]
arrayOfUnitedData[1:], mod_time_units=sel.getData(arrayOfSateliteData, enteredDate, numberOfPrognosis, time_units)
i=0
print('{0:26} {1:19} {2:9} {3:9} {4:9} {5:9} {6:8} {7:8}'.format(
    'timeSat', 'timeMod', 'lon', 'lonMod', 'lat', 'latMod', 'hsig', 'hsig_mod'))
while i<len(arrayOfUnitedData[0][0]):
    print('{0:} {1:} {2:9f} {3:9f} {4:9f} {5:9f} {6:8f} {7:8f}'.format(
        netCDF4.num2date(arrayOfUnitedData[0][0][i],time_units), netCDF4.num2date(arrayOfUnitedData[5][0][i], mod_time_units),
        arrayOfUnitedData[0][2][i],arrayOfUnitedData[5][2][i], arrayOfUnitedData[0][1][i],arrayOfUnitedData[5][1][i],
        arrayOfUnitedData[0][3][i],arrayOfUnitedData[5][3][i]
    ))
    i+=1
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