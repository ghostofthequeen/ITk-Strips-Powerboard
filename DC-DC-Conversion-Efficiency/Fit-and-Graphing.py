## Temperature test code
import pandas as pd
import seaborn as sns
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


#setting up empty temperature matrices
temp_40_x = [0.0,0.1,0.2]
temp_40_y = []
temp_40_z = []
temp_35_x = [0.0,0.1,0.2]
temp_35_y = []
temp_35_z = []
temp_30_x = [0.0,0.1,0.2]
temp_30_y = []
temp_30_z = []
temp_25_x = [0.0,0.1,0.2]
temp_25_y = []
temp_25_z = []
temp_20_x = [0.0,0.1,0.2]
temp_20_y = []
temp_20_z = []
temp_15_x = [0.0,0.1,0.2]
temp_15_y = []
temp_15_z = []
temp_10_x = [0.0,0.1,0.2]
temp_10_y = []
temp_10_z = []
temp_05_x = [0.0,0.1,0.2]
temp_05_y = []
temp_05_z = []
temp_00_x = [0.0,0.1,0.2]
temp_00_y = []
temp_00_z = []
temp_neg_05_x = [0.0,0.1,0.2]
temp_neg_05_y = []
temp_neg_05_z = []
temp_neg_10_x = [0.0,0.1,0.2]
temp_neg_10_y = []
temp_neg_10_z = []
temp_neg_15_x = [0.0,0.1,0.2]
temp_neg_15_y = []
temp_neg_15_z = []
temp_neg_20_x = [0.0,0.1,0.2]
temp_neg_20_y = []
temp_neg_20_z = []
temp_neg_25_x = [0.0,0.1,0.2]
temp_neg_25_y = []
temp_neg_25_z = []
temp_neg_30_x = [0.0,0.1,0.2]
temp_neg_30_y = []
temp_neg_30_z = []
temp_neg_35_x = [0.0,0.1,0.2]
temp_neg_35_y = []
temp_neg_35_z = []
temp_neg_40_x = [0.0,0.1,0.2]
temp_neg_40_y = []
temp_neg_40_z = []
nettime = []
netw = []
netx = []
nety = []
netz = []
directory = 'pbv3_eff_temp_scan data/'

for filename in os.listdir(directory): #for every .csv file I've put into the folder in jupyterhub
    if filename == '.ipynb_checkpoints':
        continue
    else:
        file = os.path.join(directory, filename)
        print(file)
        currentfile = open(file)

        reader = csv.DictReader(currentfile)
        data = {}
        for row in reader:
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]           #pull out header, store column
        iout = data['iout']
        NTCpb = data[' NTCpb']
        PTAT = data[' PTAT']
        CTAT = data[' CTAT']
        VIN = data[' VIN']
        IIN = data[' IIN']
        IIN_offset = data[' IIN_offset']
        VOUT = data[' VOUT']
        IOUT = data[' IOUT']
        VDCDC = data[' VDCDC']
        DCDCIN = data[' DCDCIN']
        eff1 = data[' eff1']
        eff2 = data[' eff2']
        NTCpbcounts = data[' NTCpbcounts']
        PTATcounts = data[' PTATcounts']
        eff1_corrected = []
        badi = []

        
        
        for i in range(len(iout)):
            val = ((float(VOUT[i]) + 0.0775*float(IOUT[i]))*float(IOUT[i]))/(float(VIN[i])*(float(IIN[i]) - float(IIN_offset[i])))
            eff1_corrected.append(val)

        x = iout                 #convenience
        y = eff1_corrected
        z = PTAT

       # for i in range(len(hour)):
        #    time.append(dt.time(int(float(hour[i])),int(float(minute[i])),int(float(second[i]))))
        
        for i in range(len(x)):
            x[i] = float(x[i])
        
        for i in range(len(y)):
            y[i] = 100*float(y[i])
            if y[i] < 0:
                badi.append(i)
            
        for i in range(len(z)):
            z[i] = float(z[i])
            
        for i in range(len(badi)):
            print(badi[i])
            
            x.pop(badi[i])
            y.pop(badi[i])
            z.pop(badi[i])
         #   time.pop(badi[i])
            
        
        for i in range(len(z)):
            netx.append(x[i])
            nety.append(y[i])
            netz.append(z[i])
          #  nettime.append(time[i])
            

            if -17.5<=z[i]<-12.5:
                if x[i] in temp_neg_15_x:
                    continue
                else:
                    temp_neg_15_x.append(x[i])
                    temp_neg_15_y.append(y[i])
                    temp_neg_15_z.append(z[i])
            elif -12.5<=z[i]<-7.5:
                if x[i] in temp_neg_10_x:
                    continue
                else:
                    temp_neg_10_x.append(x[i])
                    temp_neg_10_y.append(y[i])
                    temp_neg_10_z.append(z[i])
            elif -7.5<=z[i]<-2.5:
                if x[i] in temp_neg_05_x:
                    continue
                else:
                    temp_neg_05_x.append(x[i])
                    temp_neg_05_y.append(y[i])
                    temp_neg_05_z.append(z[i])
            elif -2.5<=z[i]<2.5:
                if x[i] in temp_00_x:
                    continue
                else:
                    temp_00_x.append(x[i])
                    temp_00_y.append(y[i])
                    temp_00_z.append(z[i])
            elif 2.5<=z[i]<7.5:
                if x[i] in temp_05_x:
                    continue
                else:
                    temp_05_x.append(x[i])
                    temp_05_y.append(y[i])
                    temp_05_z.append(z[i])
            elif 7.5<=z[i]<12.5:
                if x[i] in temp_10_x:
                    continue
                else:
                    temp_10_x.append(x[i])
                    temp_10_y.append(y[i])
                    temp_10_z.append(z[i])
            elif 12.5<=z[i]<17.5:
                if x[i] in temp_15_x:
                    continue
                else:
                    temp_15_x.append(x[i])
                    temp_15_y.append(y[i])
                    temp_15_z.append(z[i])
            elif 17.5<=z[i]<22.5:
                if x[i] in temp_20_x:
                    continue
                else:
                    temp_20_x.append(x[i])
                    temp_20_y.append(y[i])
                    temp_20_z.append(z[i])
            elif 22.5<=z[i]<27.5:
                if x[i] in temp_25_x:
                    continue
                else:
                    temp_25_x.append(x[i])
                    temp_25_y.append(y[i])
                    temp_25_z.append(z[i])
            elif 27.5<=z[i]<32.5:
                if x[i] in temp_30_x:
                    continue
                else:
                    temp_30_x.append(x[i])
                    temp_30_y.append(y[i])
                    temp_30_z.append(z[i])
            elif 32.5<=z[i]<37.5:
                if x[i] in temp_35_x:
                    continue
                else:
                    temp_35_x.append(x[i])
                    temp_35_y.append(y[i])
                    temp_35_z.append(z[i])
            else:
                continue

        currentfile.close()
        #shut that file, start on the next

temp_35_x.pop(0)
temp_35_x.pop(0)
temp_35_x.pop(0)
temp_30_x.pop(0)
temp_30_x.pop(0)
temp_30_x.pop(0)
temp_25_x.pop(0)
temp_25_x.pop(0)
temp_25_x.pop(0)
temp_20_x.pop(0)
temp_20_x.pop(0)
temp_20_x.pop(0)
temp_15_x.pop(0)
temp_15_x.pop(0)
temp_15_x.pop(0)
temp_10_x.pop(0)
temp_10_x.pop(0)
temp_10_x.pop(0)
temp_05_x.pop(0)
temp_05_x.pop(0)
temp_05_x.pop(0)
temp_00_x.pop(0)
temp_00_x.pop(0)
temp_00_x.pop(0)
temp_neg_05_x.pop(0)
temp_neg_05_x.pop(0)
temp_neg_05_x.pop(0)
temp_neg_10_x.pop(0)
temp_neg_10_x.pop(0)
temp_neg_10_x.pop(0)
temp_neg_15_x.pop(0)
temp_neg_15_x.pop(0)
temp_neg_15_x.pop(0)

totalx = [temp_35_x]
totalx.append(temp_30_x)
totalx.append(temp_25_x)
totalx.append(temp_20_x)
totalx.append(temp_15_x)
totalx.append(temp_10_x)
totalx.append(temp_05_x)
totalx.append(temp_00_x)
totalx.append(temp_neg_05_x)
totalx.append(temp_neg_10_x)
totalx.append(temp_neg_15_x)
totaly = [temp_35_y]
totaly.append(temp_30_y)
totaly.append(temp_25_y)
totaly.append(temp_20_y)
totaly.append(temp_15_y)
totaly.append(temp_10_y)
totaly.append(temp_05_y)
totaly.append(temp_00_y)
totaly.append(temp_neg_05_y)
totaly.append(temp_neg_10_y)
totaly.append(temp_neg_15_y)
totalz = [temp_35_z]
totalz.append(temp_30_z)
totalz.append(temp_25_z)
totalz.append(temp_20_z)
totalz.append(temp_15_z)
totalz.append(temp_10_z)
totalz.append(temp_05_z)
totalz.append(temp_00_z)
totalz.append(temp_neg_05_z)
totalz.append(temp_neg_10_z)
totalz.append(temp_neg_15_z)

z_only_neg_15 = pd.Series(np.repeat(-15,(36)))
z_only_neg_10 = pd.Series(np.repeat(-10,(36)))
z_only_neg_05 = pd.Series(np.repeat(-5,(36)))
z_only_00 = pd.Series(np.repeat(0,(36)))
z_only_05 = pd.Series(np.repeat(5,(36)))
z_only_10 = pd.Series(np.repeat(10,(36)))
z_only_15 = pd.Series(np.repeat(15,(36)))
z_only_20 = pd.Series(np.repeat(20,(36)))
z_only_25 = pd.Series(np.repeat(25,(36)))
z_only_30 = pd.Series(np.repeat(30,(36)))
z_only_35 = pd.Series(np.repeat(35,(36)))

dfx_neg_15 = pd.Series(temp_neg_15_x)
dfy_neg_15 = pd.Series(temp_neg_15_y)
dfx_neg_10 = pd.Series(temp_neg_10_x)
dfy_neg_10 = pd.Series(temp_neg_10_y)
dfx_neg_05 = pd.Series(temp_neg_05_x)
dfy_05 = pd.Series(temp_neg_05_y)
dfx_00 = pd.Series(temp_00_x)
dfy_00 = pd.Series(temp_00_y)
dfx_05 = pd.Series(temp_05_x)
dfy_05 = pd.Series(temp_05_y)
dfx_10 = pd.Series(temp_10_x)
dfy_10 = pd.Series(temp_10_y)
dfx_15 = pd.Series(temp_15_x)
dfy_15 = pd.Series(temp_15_y)
dfx_20 = pd.Series(temp_20_x)
dfy_20 = pd.Series(temp_20_y)
dfx_25 = pd.Series(temp_25_x)
dfy_25 = pd.Series(temp_25_y)
dfx_30 = pd.Series(temp_30_x)
dfy_30 = pd.Series(temp_30_y)
dfx_35 = pd.Series(temp_35_x)
dfy_35 = pd.Series(temp_35_y)

x_0mA = []
y_0mA = []
x_10mA = []
y_10mA = []
x_20mA = []
y_20mA = []
x_30mA = []
y_30mA = []
x_40mA = []
y_40mA = []
x_50mA = []
y_50mA = []
x_60mA = []
y_60mA = []
x_70mA = []
y_70mA = []
x_80mA = []
y_80mA = []
x_90mA = []
y_90mA = []
x_100mA = []
y_100mA = []
x_110mA = []
y_110mA = []
x_120mA = []
y_120mA = []
x_130mA = []
y_130mA = []
x_140mA = []
y_140mA = []
x_150mA = []
y_150mA = []
x_160mA = []
y_160mA = []
x_170mA = []
y_170mA = []
x_180mA = []
y_180mA = []
x_190mA = []
y_190mA = []
x_200mA = []
y_200mA = []
x_210mA = []
y_210mA = []
x_220mA = []
y_220mA = []
x_230mA = []
y_230mA = []
x_240mA = []
y_240mA = []
x_250mA = []
y_250mA = []
x_260mA = []
y_260mA = []
x_270mA = []
y_270mA = []
x_280mA = []
y_280mA = []
x_290mA = []
y_290mA = []
x_300mA = []
y_300mA = []
x_310mA = []
y_310mA = []
x_320mA = []
y_320mA = []
x_330mA = []
y_330mA = []
x_340mA = []
y_340mA = []
x_350mA = []
y_350mA = []

for i in range(len(totalx)):
    x_30mA.append(totalz[i][0])
    y_30mA.append(totaly[i][0])
    x_40mA.append(totalz[i][1])
    y_40mA.append(totaly[i][1])
    x_50mA.append(totalz[i][2])
    y_50mA.append(totaly[i][2])
    x_60mA.append(totalz[i][3])
    y_60mA.append(totaly[i][3])
    x_70mA.append(totalz[i][4])
    y_70mA.append(totaly[i][4])
    x_80mA.append(totalz[i][5])
    y_80mA.append(totaly[i][5])
    x_90mA.append(totalz[i][6])
    y_90mA.append(totaly[i][6])
    x_100mA.append(totalz[i][7])
    y_100mA.append(totaly[i][7])
    x_110mA.append(totalz[i][8])
    y_110mA.append(totaly[i][8])
    x_120mA.append(totalz[i][9])
    y_120mA.append(totaly[i][9])
    x_130mA.append(totalz[i][10])
    y_130mA.append(totaly[i][10])
    x_140mA.append(totalz[i][11])
    y_140mA.append(totaly[i][11])
    x_150mA.append(totalz[i][12])
    y_150mA.append(totaly[i][12])
    x_160mA.append(totalz[i][13])
    y_160mA.append(totaly[i][13])
    x_170mA.append(totalz[i][14])
    y_170mA.append(totaly[i][14])
    x_180mA.append(totalz[i][15])
    y_180mA.append(totaly[i][15])
    x_190mA.append(totalz[i][16])
    y_190mA.append(totaly[i][16])
    x_200mA.append(totalz[i][17])
    y_200mA.append(totaly[i][17])
    x_210mA.append(totalz[i][18])
    y_210mA.append(totaly[i][18])
    x_220mA.append(totalz[i][19])
    y_220mA.append(totaly[i][19])
    x_230mA.append(totalz[i][20])
    y_230mA.append(totaly[i][20])
    x_240mA.append(totalz[i][21])
    y_240mA.append(totaly[i][21])
    x_250mA.append(totalz[i][22])
    y_250mA.append(totaly[i][22])
    x_260mA.append(totalz[i][23])
    y_260mA.append(totaly[i][23])
    x_270mA.append(totalz[i][24])
    y_270mA.append(totaly[i][24])
    x_280mA.append(totalz[i][25])
    y_280mA.append(totaly[i][25])
    x_290mA.append(totalz[i][26])
    y_290mA.append(totaly[i][26])
    x_300mA.append(totalz[i][27])
    y_300mA.append(totaly[i][27])
    x_310mA.append(totalz[i][28])
    y_310mA.append(totaly[i][28])
    x_320mA.append(totalz[i][29])
    y_320mA.append(totaly[i][29])
    x_330mA.append(totalz[i][30])
    y_330mA.append(totaly[i][30])
    x_340mA.append(totalz[i][31])
    y_340mA.append(totaly[i][31])
    x_350mA.append(totalz[i][32])
    y_350mA.append(totaly[i][32])

#plt.scatter(x_30mA, y_30mA, s=10, label = '$30mA$', color = 'red')
#plt.scatter(x_40mA, y_40mA, s=10, label = '$40mA$', color = 'orangered')
#plt.scatter(x_50mA, y_50mA, s=10, label = '$50mA$', color = 'orange')
#plt.scatter(x_60mA, y_60mA, s=10, label = '$60mA$', color = 'gold')
#plt.scatter(x_70mA, y_70mA, s=10, label = '$70mA$', color = 'yellow')
#plt.scatter(x_80mA, y_80mA, s=10, label = '$80mA$', color = 'greenyellow')
#plt.scatter(x_90mA, y_90mA, s=10, label = '$90mA$', color = 'green')
#plt.scatter(x_100mA, y_100mA, s=10, label = '$100mA$', color = 'aqua')
#plt.scatter(x_110mA, y_110mA, s=10, label = '$110mA$', color = 'deepskyblue')
#plt.scatter(x_120mA, y_120mA, s=10, label = '$120mA$', color = 'midnightblue')
#plt.scatter(x_130mA, y_130mA, s=10, label = '$130mA$', color = 'darkviolet')
#plt.scatter(x_140mA, y_140mA, s=10, label = '$140mA$', color = 'red')
#plt.scatter(x_150mA, y_150mA, s=10, label = '$150mA$', color = 'orangered')
#plt.scatter(x_160mA, y_160mA, s=10, label = '$160mA$', color = 'orange')
#plt.scatter(x_170mA, y_170mA, s=10, label = '$170mA$', color = 'gold')
#plt.scatter(x_180mA, y_180mA, s=10, label = '$180mA$', color = 'yellow')
#plt.scatter(x_190mA, y_190mA, s=10, label = '$190mA$', color = 'greenyellow')
#plt.scatter(x_200mA, y_200mA, s=10, label = '$200mA$', color = 'green')
#plt.scatter(x_210mA, y_210mA, s=10, label = '$210mA$', color = 'aqua')
#plt.scatter(x_220mA, y_220mA, s=10, label = '$220mA$', color = 'deepskyblue')
#plt.scatter(x_230mA, y_230mA, s=10, label = '$230mA$', color = 'midnightblue')
#plt.scatter(x_240mA, y_240mA, s=10, label = '$240mA$', color = 'darkviolet')
#plt.scatter(x_250mA, y_250mA, s=10, label = '$250mA$', color = 'red')
#plt.scatter(x_260mA, y_260mA, s=10, label = '$260mA$', color = 'orangered')
#plt.scatter(x_270mA, y_270mA, s=10, label = '$270mA$', color = 'orange')
#plt.scatter(x_280mA, y_280mA, s=10, label = '$280mA$', color = 'gold')
#plt.scatter(x_290mA, y_290mA, s=10, label = '$290mA$', color = 'yellow')
#plt.scatter(x_300mA, y_300mA, s=10, label = '$300mA$', color = 'greenyellow')
#plt.scatter(x_310mA, y_310mA, s=10, label = '$310mA$', color = 'green')
#plt.scatter(x_320mA, y_320mA, s=10, label = '$320mA$', color = 'aqua')
#plt.scatter(x_330mA, y_330mA, s=10, label = '$330mA$', color = 'deepskyblue')
#plt.scatter(x_340mA, y_340mA, s=10, label = '$340mA$', color = 'midnightblue')
#plt.scatter(x_350mA, y_350mA, s=10, label = '$350mA$', color = 'darkviolet')
plt.scatter(temp_35_x, temp_35_y, s=10, label = '$35 ^{\circ} C$', color = 'red')
#plt.scatter(temp_30_x, temp_30_y, s=10, label = '$30 ^{\circ} C$', color = 'orangered')
#plt.scatter(temp_25_x, temp_25_y, s=10, label = '$25 ^{\circ} C$', color = 'orange')
#plt.scatter(temp_20_x, temp_20_y, s=10, label = '$20 ^{\circ} C$', color = 'gold')
#plt.scatter(temp_15_x, temp_15_y, s=10, label = '$15 ^{\circ} C$', color = 'yellow')
#plt.scatter(temp_10_x, temp_10_y, s=10, label = '$10 ^{\circ} C$', color = 'greenyellow')
#plt.scatter(temp_05_x, temp_05_y, s=10, label = '$5 ^{\circ} C$', color = 'green')
#plt.scatter(temp_00_x, temp_00_y, s=10, label = '$0 ^{\circ} C$', color = 'aqua')
#plt.scatter(temp_neg_05_x, temp_neg_05_y, s=10, label = '$-5 ^{\circ} C$', color = 'deepskyblue')
#plt.scatter(temp_neg_10_x, temp_neg_10_y, s=10, label = '$-10 ^{\circ} C$', color = 'midnightblue')
#plt.scatter(temp_neg_15_x, temp_neg_15_y, s=10, label = '$-15 ^{\circ} C$', color = 'darkviolet')
plt.xlabel('IOUT (A)')
plt.ylabel('Efficiency (%)')
plt.legend(bbox_to_anchor=[0.5, 0.5],loc='upper center', ncol=3, prop={'size': 7})
plt.axis([0.3, 3.6, 50, 80])
plt.show()
