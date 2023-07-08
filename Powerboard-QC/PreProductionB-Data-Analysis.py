import scipy.optimize as sp
import numpy as np
m = 0
n = 0
o = 0
files = [0]
directory = 'am_response data/' #folder that contains pbv3-functionality.json files, naming convention is TEMP_XXXYYY, where TEMP is warm or cold, XXX is the last 3 digits of Panel #, YYY is the last 3 digits of Component #

truey = []
truex = []
truez = []
residual_minus750 = np.zeros((21,), dtype=int)
residual_minus675 = np.zeros((21,), dtype=int)
residual_minus600 = np.zeros((21,), dtype=int)
residual_minus525 = np.zeros((21,), dtype=int)
residual_minus450 = np.zeros((21,), dtype=int)
residual_minus375 = np.zeros((21,), dtype=int)
residual_minus300 = np.zeros((21,), dtype=int)
residual_minus225 = np.zeros((21,), dtype=int)
residual_minus150 = np.zeros((21,), dtype=int)
residual_minus075 = np.zeros((21,), dtype=int)
residual_minus000 = np.zeros((21,), dtype=int)
residual_075 = np.zeros((21,), dtype=int)
residual_150 = np.zeros((21,), dtype=int)
residual_225 = np.zeros((21,), dtype=int)
residual_300 = np.zeros((21,), dtype=int)
residual_375 = np.zeros((21,), dtype=int)
residual_450 = np.zeros((21,), dtype=int)
names = ['cold_058', 'cold_059', 'cold_060', 'cold_061', 'cold_062', 'cold_063', 'cold_064', 'cold_065', 'cold_066', 'cold_067', 'cold_068', 'cold_069', 'cold_070', 'cold_071', 'cold_072', 'cold_073', 'cold_074', 'cold_075', 'cold_076', 'cold_077', 'cold_078', 'cold_079', 'cold_080', 'cold_081', 'cold_082', 'cold_083', 'cold_084', 'cold_085', 'cold_086', 'cold_087', 'cold_006', 'cold_007', 'cold_008', 'cold_009', 'cold_010']
factor = 0
coldslope = 1

for name in names:
    for filename in os.listdir(directory): #for every .csv file I've put into the folder in jupyterhub
        if filename == '.ipynb_checkpoints':
            continue
        elif filename == '.nfs000000040334133300000318':
            continue
        elif filename.startswith(name) == False:
            continue
        else:
            file = os.path.join(directory, filename)
            n += 1
            coldfile = open(file)
            colddata = json.load(coldfile)
            for i in range(len(colddata['tests'])):
                try:
                    coldresults = colddata['tests'][i]['results']['AMACCAL']
                except:
                    continue
            for j in range(len(colddata['tests'])):
                try:
                    coldresultsin = colddata['tests'][j]['results']['CALIN']

                except:
                    continue
            for k in range(len(colddata['config'])):
                try:
                    coldslope = colddata['config']['results']['AMSLOPE']
                except:
                    continue
                  
            otherfile = os.path.join(directory, 'warm_' + filename[-11:])
            warmfile = open(otherfile)
            warmdata = json.load(warmfile)
            for i in range(len(warmdata['tests'])):
                try:
                    warmresults = warmdata['tests'][i]['results']['AMACCAL']
                   
                except:
                    continue
            for j in range(len(warmdata['tests'])):
                try:
                    warmresultsin = data['tests'][j]['results']['CALIN']

                except:
                    continue
                  
            
            for i in range(len(coldresultsin)):
                if 730 < coldresults[i]:
                    cutresultsin = coldresultsin[:i]
                    cutresults = coldresults[:i]
                    break

            for i in range(len(coldresults)):
                if coldresults[i] == 1023:
                    del coldresultsin[i:]
                    del coldresults[i:]
                    break
            
            for i in range(len(coldresultsin)):
                if 0.6 < coldresultsin[i]:
                    peakresultsin = coldresultsin[i:]
                    peakresults = coldresults[i:]
                    break
                  
            for i in range(len(peakresults)):
                if 0.8 < peakresultsin[i]:
                    del peakresultsin[i:]
                    del peakresults[i:]
                    break

            for i in range(len(coldresultsin)):
                residualy.append(coldslope*(coldresults[i] - fit[i]))
                residualx.append(coldslope*coldresults[i])
                residualz.append(1000*coldresultsin[i])

            
            plt.plot(residualz,residualy, linewidth=0.5)
            plt.show()

            coldresultsinV = [i*1000 for i in coldresultsin]
            warmresultsinV = [i*1000 for i in warmresultsin]
            fig = plt.figure()
            ax = plt.subplot(111)
            plt.scatter(warmresultsinV, warmresults, label='20', color='goldenrod') 
            plt.scatter(coldresultsinV, coldresults, label='-35', color='navy')
            plt.xlabel('CAL Input (mV)')
            plt.ylabel('AMAC CAL (counts)')
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Temperature ($^{\circ}$C)')
            plt.show()
