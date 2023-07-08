## Temperature test code
import pandas as pd
import seaborn as sns
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from matplotlib import cm


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
            
        
        for i in range(len(z)):
            netx.append(x[i])
            nety.append(y[i])
            netz.append(z[i])
            

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

plt.scatter(temp_35_x, temp_35_y, s=10, label = '$35 ^{\circ} C$', color = 'red')
plt.scatter(temp_30_x, temp_30_y, s=10, label = '$30 ^{\circ} C$', color = 'orangered')
plt.scatter(temp_25_x, temp_25_y, s=10, label = '$25 ^{\circ} C$', color = 'orange')
plt.scatter(temp_20_x, temp_20_y, s=10, label = '$20 ^{\circ} C$', color = 'gold')
plt.scatter(temp_15_x, temp_15_y, s=10, label = '$15 ^{\circ} C$', color = 'yellow')
plt.scatter(temp_10_x, temp_10_y, s=10, label = '$10 ^{\circ} C$', color = 'greenyellow')
plt.scatter(temp_05_x, temp_05_y, s=10, label = '$5 ^{\circ} C$', color = 'green')
plt.scatter(temp_00_x, temp_00_y, s=10, label = '$0 ^{\circ} C$', color = 'aqua')
plt.scatter(temp_neg_05_x, temp_neg_05_y, s=10, label = '$-5 ^{\circ} C$', color = 'deepskyblue')
plt.scatter(temp_neg_10_x, temp_neg_10_y, s=10, label = '$-10 ^{\circ} C$', color = 'midnightblue')
plt.scatter(temp_neg_15_x, temp_neg_15_y, s=10, label = '$-15 ^{\circ} C$', color = 'darkviolet')
plt.xlabel('IOUT (A)')
plt.ylabel('Efficiency (%)')
plt.legend(bbox_to_anchor=[0.5, 0.5],loc='upper center', ncol=3, prop={'size': 7})
plt.axis([0.3, 3.6, 50, 80])
plt.show()


# plot a heatmap with annotation
df = pd.DataFrame(totaly, index=[35,30,25,20,15,10,5,0,-5,-10,-15], columns=[0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.5])
plt.figure(figsize=(36, 20))
sns.set(font_scale=2.5)
g = sns.heatmap(df, cmap=cm.gist_rainbow, annot=True, annot_kws={"size": 25}, cbar_kws={'label': 'Efficiency (%)'})
plt.xlabel('IOUT (A)')
g.set_xticks(np.arange(0.5,34.5,2))
g.set_xticklabels([0.3,0.5,0.7,0.9,1.1,1.3,1.5,1.7,1.9,2.1,2.3,2.5,2.7,2.9,3.1,3.3,3.5])
plt.title('DC/DC Conversion Climate Chamber Test Efficiency Heatmap')
plt.ylabel('Temperature ($^{\circ}$C)')

# create fit for efficiency data in terms of PTAT and IOUT
singletotalx = []
for i in range(len(temp_35_x)):
    singletotalx.append(temp_35_x[i])
for i in range(len(temp_30_x)):
    singletotalx.append(temp_30_x[i])
for i in range(len(temp_25_x)):
    singletotalx.append(temp_25_x[i])
for i in range(len(temp_20_x)):
    singletotalx.append(temp_20_x[i])
for i in range(len(temp_15_x)):
    singletotalx.append(temp_15_x[i])
for i in range(len(temp_10_x)):
    singletotalx.append(temp_10_x[i])
for i in range(len(temp_05_x)):
    singletotalx.append(temp_05_x[i])
for i in range(len(temp_00_x)):
    singletotalx.append(temp_00_x[i])
for i in range(len(temp_neg_05_x)):
    singletotalx.append(temp_neg_05_x[i])
for i in range(len(temp_neg_10_x)):
    singletotalx.append(temp_neg_10_x[i])
for i in range(len(temp_neg_15_x)):
    singletotalx.append(temp_neg_15_x[i])

singletotaly = []
for i in range(len(temp_35_y)):
    singletotaly.append(temp_35_y[i])
for i in range(len(temp_30_y)):
    singletotaly.append(temp_30_y[i])
for i in range(len(temp_25_y)):
    singletotaly.append(temp_25_y[i])
for i in range(len(temp_20_y)):
    singletotaly.append(temp_20_y[i])
for i in range(len(temp_15_y)):
    singletotaly.append(temp_15_y[i])
for i in range(len(temp_10_y)):
    singletotaly.append(temp_10_y[i])
for i in range(len(temp_05_y)):
    singletotaly.append(temp_05_y[i])
for i in range(len(temp_00_y)):
    singletotaly.append(temp_00_y[i])
for i in range(len(temp_neg_05_y)):
    singletotaly.append(temp_neg_05_y[i])
for i in range(len(temp_neg_10_y)):
    singletotaly.append(temp_neg_10_y[i])
for i in range(len(temp_neg_15_y)):
    singletotaly.append(temp_neg_15_y[i])

singletotalz = []
for i in range(len(temp_35_z)):
    singletotalz.append(temp_35_z[i])
for i in range(len(temp_30_z)):
    singletotalz.append(temp_30_z[i])
for i in range(len(temp_25_z)):
    singletotalz.append(temp_25_z[i])
for i in range(len(temp_20_z)):
    singletotalz.append(temp_20_z[i])
for i in range(len(temp_15_z)):
    singletotalz.append(temp_15_z[i])
for i in range(len(temp_10_z)):
    singletotalz.append(temp_10_z[i])
for i in range(len(temp_05_z)):
    singletotalz.append(temp_05_z[i])
for i in range(len(temp_00_z)):
    singletotalz.append(temp_00_z[i])
for i in range(len(temp_neg_05_z)):
    singletotalz.append(temp_neg_05_z[i])
for i in range(len(temp_neg_10_z)):
    singletotalz.append(temp_neg_10_z[i])
for i in range(len(temp_neg_15_z)):
    singletotalz.append(temp_neg_15_z[i])
    
import numpy as np
from scipy.optimize import curve_fit
new = []
def func(X, a, b, c, d, e, f, g, h, j, k, l, m, n, o):
    P,I = X
    return (a*P + b)*(I**6) + (c*P + d)*(I**5) + (e*P + f)*(I**4) + (g*P + h)*(I**3) + (j*P + k)*(I**2) + (l*P + m)*(I) + (n*P + o)


x = singletotalz
y = singletotalx
p0 = 0.00001, -0.0291, -0.0001, 0.3444, 0.0001, -1.6044, -0.0008, 3.6983, 0.0006, -4.4644, -0.0005, 2.7169, 0.0001, 0.0382
z = singletotaly
a_through_o = curve_fit(func, (x,y), z, p0)
