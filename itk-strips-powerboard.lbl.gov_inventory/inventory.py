#!/usr/bin/env python

import pkg_resources
import pandas as pd
import numpy as np
import jinja2
import shutil
import datetime
from datetime import date
import os, sys
import re
import cProfile

from database import pwbdbtools
from database import pwbdbpandas

if len(sys.argv)!=2:
    print('usage: {} outdir/'.format(sys.argv[0]))
    sys.exit(1)

#
# Checks on input
output_dir=sys.argv[1]

if not os.path.isdir(output_dir):
    print('ERROR: Output directory does not exist.')
    sys.exit(1)

#
#
c = pwbdbtools.get_db_client()

#
# Powerboards
df=pwbdbpandas.listComponents(c, {'project':'S', 'subproject':'SB', 'componentType':'PWB', 'type':'B3'})
df=df[(df.state=='ready')]

stages=pwbdbpandas.getComponentTypeStages(c, 'PWB')

# Powerboard versions
r=c.get('getComponentTypeByCode',json={'project':'S', 'code':'PWB'})
versionCodeTable={ct['code']:ct['value'] for ct in next(filter(lambda p: p['code']=='VERSION', r['properties']))['codeTable']}
# Count all powerboards
dates=pwbdbpandas.listComponents(c, {'project':'S', 'subproject':'SB', 'componentType':'PWB', 'type':'B3'})
dates=dates[(dates.state=='ready')]
dates['VERSION']=dates['VERSION'].map(versionCodeTable)
for i in range(dates.shape[0]):
    date = datetime.datetime.strptime(dates.cts.iloc[i][0:10], '%Y-%m-%d')
    if date.year < 2022:
        dates.iloc[i, dates.columns.get_loc('cts')] = 'old'
    elif date.year == 2022:
        if date.month == 1:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202201'
        if date.month == 2:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202202'
        if date.month == 3:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202203'
        if date.month == 4:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202204'
        if date.month == 5:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202205'
        if date.month == 6:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202206'
        if date.month == 7:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202207'
        if date.month == 8:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202208'
        if date.month == 9:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202209'
        if date.month == 10:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202210'
        if date.month == 11:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202211'
        if date.month == 12:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202212'
    elif date.year == 2023: 
        if date.month == 1:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202301'
        if date.month == 2:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202302'
        if date.month == 3:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202303'
        if date.month == 4:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202304'
        if date.month == 5:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202305'
        if date.month == 6:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202306'
        if date.month == 7:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202307'
        if date.month == 8:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202308'
        if date.month == 9:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202309'
        if date.month == 10:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202310'
        if date.month == 11:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202311'
        if date.month == 12:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202312'
    elif date.year == 2024: 
        if date.month == 1:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202401'
        if date.month == 2:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202402'
        if date.month == 3:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202403'
        if date.month == 4:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202404'
        if date.month == 5:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202405'
        if date.month == 6:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202406'
        if date.month == 7:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202407'
        if date.month == 8:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202408'
        if date.month == 9:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202409'
        if date.month == 10:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202410'
        if date.month == 11:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202411'
        if date.month == 12:
            dates.iloc[i, dates.columns.get_loc('cts')] = '202412'
    else:
        print('The cts of one of the boards indexed was not categorized. Please modify the code to include it.')
counts=dates.groupby(['VERSION','cts']).code.count()
df_pb_versions=pd.DataFrame(data=counts, index=counts.index)
df_pb_versions['count']=counts

data_pb=[]
for index,pbtype in df_pb_versions.iterrows():
    if (index[0] == '3.0' or index[0] == '3.0b' or index[0] == 'dummy'):
        continue
    else:
        data_pb.append({'title':index[0],'count':pbtype['count'],'date':index[1]})
data_pb = sorted(data_pb, key=lambda k: k['title'])
data_pb = sorted(data_pb, key=lambda k: k['date'])
track_vers=[]
net_vers=[]
net_counts_vers=[]
for vers in range(len(data_pb)):
    currentvers = data_pb[vers]['title']
    if currentvers in track_vers:
        continue
    else:
        track_vers.append(currentvers)
        summation = 0
        for i in range(len(data_pb)):
            if data_pb[i]['title'] == currentvers:
                summation+=data_pb[i]['count']
        net_counts_vers.append(summation)
        net_vers.append(currentvers)

track_dates=[]
net_dates=[]
net_counts_dates=[]
net_counts = 0
for date in range(len(data_pb)):
    currentdate = data_pb[date]['date']
    if currentdate in track_dates:
        continue
    else:
        track_dates.append(currentdate)
        summation = 0
        for i in range(len(data_pb)):
            if data_pb[i]['date'] == currentdate:
                summation+=data_pb[i]['count']
        net_counts_dates.append(summation)
        net_counts += summation
        net_dates.append(currentdate)
for i in range(len(net_vers)):
    for j in range(len(net_dates)):
        check = False
        for k in range(len(data_pb)):
            if data_pb[k]['date'] == net_dates[j] and data_pb[k]['title'] == net_vers[i]:
                check = True
        if check == False:
            data_pb.append({'title':net_vers[i],'count':0,'date':net_dates[j]})
data_pb = sorted(data_pb, key=lambda k: k['title'])
data_pb = sorted(data_pb, key=lambda k: k['date'])
for i in range(len(net_vers)):
    data_pb.append({'title':net_vers[i],'count':net_counts_vers[i],'name':'All Months:'})
for i in range(len(net_dates)):
    data_pb.append({'date':net_dates[i],'count':net_counts_dates[i],'name':'All Versions:'})
data_pb.append({'count':net_counts,'name':'Total:'})

# Count local Powerboards
cnt=df[(df.currentLocation=='LBNL_STRIP_POWERBOARDS')&(df.shipmentDestination.isna())].groupby(['VERSION','currentStage']).code.count().rename('count').reset_index()
stage_counts=stages.merge(cnt,left_on='code',right_on='currentStage',how='outer')
stage_counts['VERSION']=stage_counts['VERSION'].map(versionCodeTable)
stage_counts=stage_counts[['name','count','VERSION']]   
stage_counts=stage_counts.pivot(columns='name',index='VERSION').fillna(0)
stage_counts.columns=map(lambda c: c[1],stage_counts.columns)
stage_counts=stage_counts[~stage_counts.index.isna()]


for index in range(stage_counts.shape[0]):
    if stage_counts.iloc[index].name == '3.0':
        vers3_0 = index

stage_counts.drop(stage_counts.index[vers3_0], inplace=True)

for index in range(stage_counts.shape[0]):
    if stage_counts.iloc[index].name == '3.0b':
        vers3_0b = index

stage_counts.drop(stage_counts.index[vers3_0b], inplace=True)

for index in range(stage_counts.shape[0]):
    if stage_counts.iloc[index].name == 'dummy':
        versdummy = index

stage_counts.drop(stage_counts.index[versdummy], inplace=True)
stage_counts.loc['Total:']=stage_counts.sum()
stage_counts=stage_counts[stages['name']].astype(int)
addtodict = []
for i in range(stage_counts.shape[0]):
    summation = stage_counts.iloc[i].sum()
    addtodict.append(summation)
stage_counts['Total'] = addtodict

front = []
for i in range(stage_counts.shape[0]):
    name = stage_counts.iloc[i].name
    front.append(name)

testing_status = [{a: {'notTested':0, 'inTesting':0,'Tested and Passed':0,'Tested and Failed':0}} for a in front] 

for i in range(len(front)):
    for key in testing_status[i]:
        for j in range(len(stage_counts.loc['Total:'])):
            if (stage_counts.loc[key]).index[j] == 'Thermal Cycling' or (stage_counts.loc[key]).index[j] == 'Burn-In':
                testing_status[i][key]['inTesting'] += (stage_counts.loc[key]).iloc[j]
            elif (stage_counts.loc[key]).index[j] == 'SMD Loading' or (stage_counts.loc[key]).index[j] == 'Coil and Shield Loading' or (stage_counts.loc[key]).index[j] == 'Die Attachment and Bonding':
                testing_status[i][key]['notTested'] += (stage_counts.loc[key]).iloc[j]
            elif (stage_counts.loc[key]).index[j] == 'Module Reception' or (stage_counts.loc[key]).index[j] == 'Loaded on a Module' or (stage_counts.loc[key]).index[j] == 'Loaded on a Hybrid Burn-in Carrier':
                testing_status[i][key]['Tested and Passed'] += (stage_counts.loc[key]).iloc[j]
            elif (stage_counts.loc[key]).index[j] == 'Failed Tests':
                testing_status[i][key]['Tested and Failed'] += (stage_counts.loc[key]).iloc[j]
            elif (stage_counts.loc[key]).index[j] == 'Total':
                continue
            else:
                print('The script inventory.py is currently not counting stage ', (stage_counts.loc['Total:']).index[j], ' in the Not Tested, In Testing, or Tested categories. Please add this stage to one of the three groups.')

#
# Powerboards at locations

# Add special stage for "in shipment"
stages=stages.append({'code':'SHIPPING', 'name':'In Shipment', 'order':4.5}, ignore_index=True)
ship_stages=stages[stages.code.isin(['SMD_LOAD', 'MAN_LOAD', 'BONDED', 'THERMAL', 'BURN_IN', 'SHIPPING','MODULE_RCP','LOADED', 'HYBBURN','FAILED'])].sort_values('order')

# All powerboards at location
cnt=df[df.currentLocation!='LBNL_STRIP_POWERBOARDS'].groupby(['VERSION','currentLocation','currentStage']).code.count().rename('count').reset_index()
# All powerboards being shipped to location
cnt_ship=df[(df.currentLocation=='LBNL_STRIP_POWERBOARDS')&(~df.shipmentDestination.isna())].groupby(['VERSION','shipmentDestination']).code.count().reset_index().rename(columns={'code':'count','shipmentDestination':'currentLocation'})
cnt_ship['currentStage']='SHIPPING'
cnt=pd.concat([cnt,cnt_ship])

# Rotate table into columns=stages at location, rows=location.
# MultiIndex by VERSION and location
ship_counts=ship_stages.merge(cnt,left_on='code',right_on='currentStage',how='left').sort_values('order')
ship_counts['VERSION']=ship_counts['VERSION'].map(versionCodeTable)

ship_counts=ship_counts[['VERSION','currentLocation','name','count']]
ship_counts=ship_counts.pivot(columns=['name'],index=['VERSION','currentLocation'])

vers3_0 = []
for index in range(ship_counts.shape[0]):
    if ship_counts.iloc[index].name[0] == '3.0':
        vers3_0.append(index)
filler = 0
for index in range(len(vers3_0)):
    ship_counts.drop(ship_counts.index[vers3_0[index-filler]], inplace=True)
    filler += 1

vers3_0b = []
for index in range(ship_counts.shape[0]):
    if ship_counts.iloc[index].name[0] == '3.0b':
        vers3_0b.append(index)
filler = 0
for index in range(len(vers3_0b)):
    ship_counts.drop(ship_counts.index[vers3_0b[index-filler]], inplace=True)
    filler += 1

versdummy = []
for index in range(ship_counts.shape[0]):
    if ship_counts.iloc[index].name[0] == 'dummy':
        versdummy.append(index)
filler=0
for index in range(len(versdummy)):
    ship_counts.drop(ship_counts.index[versdummy[index-filler]], inplace=True)
    filler += 1

vers_tracker = []
for index in range(ship_counts.shape[0]):
    if ship_counts.iloc[index].name[0] in vers_tracker:
        continue
    elif pd.isna(ship_counts.iloc[index].name[0]) == True:
        continue
    else:
        vers_tracker.append(ship_counts.iloc[index].name[0])

ship_counts.columns=map(lambda c: c[1],ship_counts.columns)
ship_counts=ship_counts[ship_stages['name']].fillna(0).astype(int)

zeroes=np.zeros((len(vers_tracker),ship_counts.shape[1]),dtype=int)
total_counts=zeroes.tolist()
for vers in range(len(vers_tracker)):
    for index in range(ship_counts.shape[0]):
        if ship_counts.iloc[index].name[0] == vers_tracker[vers]:
            for stage in range(ship_counts.shape[1]):
                total_counts[vers][stage] += ship_counts.iloc[index][stage]

currentvers = 'None'
filler = 0

for index in range(ship_counts.shape[0]):
    if pd.isna(ship_counts.iloc[index].name[0]) == True:
        continue
    elif index - 1 in range(ship_counts.shape[0]):
        if pd.isna(ship_counts.iloc[index - 1].name[0]) == True:
            continue
        else:
            if index == ship_counts.shape[0] - 1:
                fillerframe = pd.Series(total_counts[filler], dtype=int, index=ship_counts.columns, name=(ship_counts.iloc[index].name[0],'ZZZZZTotal:'))
                ship_counts.loc[fillerframe.name,:] = fillerframe
            elif ship_counts.iloc[index].name[0] == currentvers:
                continue
            else: 
                fillerframe = pd.Series(total_counts[filler], dtype=int, index=ship_counts.columns, name=(ship_counts.iloc[index].name[0],'ZZZZZTotal:'))
                ship_counts.loc[fillerframe.name,:] = fillerframe
                currentvers = ship_counts.iloc[index].name[0]
                filler += 1
ship_counts.sort_index(inplace=True)

for column in ship_counts.columns:
    try:
        ship_counts[[column]] = ship_counts[[column]].astype(int)
    except:
        pass

# AMAC
df_amac=pwbdbpandas.listComponents(c, {'project':'S', 'componentType':'AMAC', 'currentLocation':'LBNL_STRIP_POWERBOARDS','assembled':False})

# Get available component types
r=c.get('getComponentTypeByCode', json={'project':'S','code':'AMAC', 'parents':'Nan'})

df_amactype=pd.DataFrame.from_records(r['types'], columns=['code','name','existing','parents'])

df_amactype=df_amactype[df_amactype.existing]
df_amactype=df_amactype.set_index('code')
# Counts
df_amactype['count']=df_amac.groupby('type').code.count()
df_amactype['count']=df_amactype['count'].fillna(0).astype(int)

v1 = []
for index in range(df_amactype.shape[0]):
    if df_amactype.iloc[index].name == 'A1':
        v1.append(index)
filler = 0
for index in range(len(v1)):
    df_amactype.drop(df_amactype.index[v1[index-filler]], inplace=True)
    filler += 1

v2 = []
for index in range(df_amactype.shape[0]):
    if df_amactype.iloc[index].name == '2':
        v2.append(index)
filler = 0
for index in range(len(v2)):
    df_amactype.drop(df_amactype.index[v2[index-filler]], inplace=True)
    filler += 1

v2a = []
for index in range(df_amactype.shape[0]):
    if df_amactype.iloc[index].name == 'TEST':
        v2a.append(index)
filler = 0
for index in range(len(v2a)):
    df_amactype.drop(df_amactype.index[v2a[index-filler]], inplace=True)
    filler += 1

data_amac=[]
for index,amactype in df_amactype.sort_values('name').iterrows():
    data_amac.append({'title':amactype['name'],'count':amactype['count']})
data_amac.append({'title':'Total:','count':df_amactype['count'].sum()})

#
# bPOL
df_bpol = pwbdbpandas.listComponents(c, {'project':'S', 'componentType':'BPOL12V', 'currentLocation':'LBNL_STRIP_POWERBOARDS','assembled':False})

# Get available component types
r=c.get('getComponentTypeByCode', json={'project':'S','code':'BPOL12V'})
df_bpoltype=pd.DataFrame.from_records(r['types'], columns=['code','name','existing'])
df_bpoltype=df_bpoltype[df_bpoltype.existing]
df_bpoltype=df_bpoltype.set_index('code')

# Counts
df_bpoltype['count']=df_bpol.groupby('type').code.count()
df_bpoltype['count']=df_bpoltype['count'].fillna(0).astype(int)

feast1_1 = []
for index in range(df_bpoltype.shape[0]):
    if df_bpoltype.iloc[index].name == 'FEAST11':
        feast1_1.append(index)
filler = 0
for index in range(len(feast1_1)):
    df_bpoltype.drop(df_bpoltype.index[feast1_1[index-filler]], inplace=True)
    filler += 1

feast2_1 = []
for index in range(df_bpoltype.shape[0]):
    if df_bpoltype.iloc[index].name == 'FEAST21':
        feast2_1.append(index)
filler = 0
for index in range(len(feast2_1)):
    df_bpoltype.drop(df_bpoltype.index[feast2_1[index-filler]], inplace=True)

bpol12v3_1 = []
for index in range(df_bpoltype.shape[0]):
    if df_bpoltype.iloc[index].name == 'BPOL12V31':
        bpol12v3_1.append(index)
filler = 0
for index in range(len(bpol12v3_1)):
    df_bpoltype.drop(df_bpoltype.index[bpol12v3_1[index-filler]], inplace=True)

bpol12v4 = []
for index in range(df_bpoltype.shape[0]):
    if df_bpoltype.iloc[index].name == 'BPOL12V4':
        bpol12v4.append(index)
filler = 0
for index in range(len(bpol12v4)):
    df_bpoltype.drop(df_bpoltype.index[bpol12v4[index-filler]], inplace=True)

data_bpol=[]
for index,bpoltype in df_bpoltype.sort_values('name').iterrows():
    data_bpol.append({'title':bpoltype['name'],'count':bpoltype['count']})
data_bpol.append({'title':'Total:','count':df_bpoltype['count'].sum()})

#
# SMD Components
df_shieldbox=pwbdbpandas.listComponents(c, {'project':'S', 'componentType':'PWB_SHIELDBOX', 'currentLocation':'LBNL_STRIP_POWERBOARDS','assembled':False})
N_shieldbox=len(df_shieldbox.index)

df_coil=pwbdbpandas.listComponents(c, {'project':'S', 'componentType':'PWB_COIL', 'currentLocation':'LBNL_STRIP_POWERBOARDS','assembled':False})
N_coil=len(df_coil.index)

df_hvmux=pwbdbpandas.listComponents(c, {'project':'S', 'componentType':'HVMUX', 'currentLocation':'LBNL_STRIP_POWERBOARDS','assembled':False})
N_hvmux=len(df_hvmux.index)

df_linpol = c.get('listComponents', json={'project':'S', 'componentType':'PWB_LINPOL', 'currentLocation':'LBNL_STRIP_POWERBOARDS','assembled':False})

N_linpol=df_linpol.total
#
# Render
template_dir=pkg_resources.resource_filename(__name__,'template')

file_loader = jinja2.FileSystemLoader(template_dir)
env = jinja2.Environment(loader=file_loader)

t=env.get_template('index.html')
output=t.render(
    stages=stage_counts,
    ships=ship_counts,
    teststatus=testing_status,
    allpbs=data_pb,
    vers=track_vers,
    amacs=data_amac,
    bpols=data_bpol,
    
    N_shieldbox=N_shieldbox,
    N_coil=N_coil,
    N_hvmux=N_hvmux,
    N_linpol=N_linpol,

    date_generated=datetime.datetime.strftime(datetime.datetime.now(),'%c')
    )

# Outputs
with open('{output_dir}/index.html'.format(output_dir=output_dir), 'w') as htmlfile:
    htmlfile.write(output)

if os.path.exists(output_dir+'/static'):
    shutil.rmtree(output_dir+'/static')
shutil.copytree(template_dir+'/static',output_dir+'/static')

