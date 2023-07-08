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

names = ['cold_058', 'cold_059', 'cold_060', 'cold_061', 'cold_062', 'cold_063', 'cold_064', 'cold_065', 'cold_066', 'cold_067', 'cold_068', 'cold_069', 'cold_070', 'cold_071', 'cold_072', 'cold_073', 'cold_074', 'cold_075', 'cold_076', 'cold_077', 'cold_078', 'cold_079', 'cold_080', 'cold_081', 'cold_082', 'cold_083', 'cold_084', 'cold_085', 'cold_086', 'cold_087', 'cold_006', 'cold_007', 'cold_008', 'cold_009', 'cold_010']
factor = 0
coldslope = 1

for name in names:
    for filename in os.listdir(directory): #for every .csv file I've put into the folder in jupyterhub
        if filename == '.ipynb_checkpoints': #for jupyter notebooks
            continue
        elif filename == '.nfs000000040334133300000318': #for jupyter notebooks
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
