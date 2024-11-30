#Run: $ python -B x5data2pandas.py
#     $ python -B x5data2pandas.py 23114

import sys
import numpy as np
import pandas as pd
import json

print("Program: x5data2pandas.py, ver.2024-05-19")
print("Author:  v.zerkin@gmail.com, Vienna, 2024")
print("Purpose: X5json.x4.data --> pandas.DataFrame\n")

def outInfo(obj,key,nam):
    val=obj.get(key)
    if (val is not None):
        print((nam+':').ljust(12,' ')+str(val))

def outEntryInfo(Entry):
    outInfo(Entry,'ENTRY','ENTRY')
    outInfo(Entry,'updated','Version')
    outInfo(Entry,'a1','Author-1')
    outInfo(Entry,'title','Title')
    outInfo(Entry,'ref','Reference')
    outInfo(Entry,'doi1','DOI')

def getDataFrame(Subent,key):
    x4data=Subent.get(key)
    if (x4data is None): return None
    headers=x4data['datacols'][0]
    units=x4data['datacols'][1]
    pointers=x4data['datacols'][2]
    cols=[]
    for ii,header in enumerate(headers):
        #hdr=':'.join([header,units[ii],pointers[ii]])
        hdr=':'.join([header,pointers[ii]])
        hdr=hdr.strip(': ')
        cols.append(hdr)
    data=x4data['data']
    array = np.array(data)
    df = pd.DataFrame(array,columns=cols)
    return df

dir0=""    
entry="41048"
if (len(sys.argv)>1) and (sys.argv[1]!=''): entry=str(sys.argv[1])
entryfile=dir0+entry[:1]+'/'+entry[:3]+'/'+entry[:5]+'.x5.json'

f=open(entryfile)
Entry=json.load(f)
outEntryInfo(Entry)
x4subents=Entry['x4subents']
for i,Subent in enumerate(x4subents):
    print('_'*80)
    outInfo(Subent,'SUBENT','SUBENT')
    bib=Subent['BIB']
    reactions=bib.get('REACTION')
    if (reactions is not None):
        #print('REACTIONS: '+str(len(reactions)))
        for ir,Reaction in enumerate(reactions):
            reaCode=Reaction['x4code']['code'].replace('\n','')
            print('REACTION['+Reaction['x4pointer']+']: '+reaCode)
    dfc=getDataFrame(Subent,'COMMON')
    if (dfc is not None):
        print('COMMON.pandas.DataFrame:')
        print(dfc)
    dfd=getDataFrame(Subent,'DATA')
    if (dfd is not None):
        print('DATA.pandas.DataFrame:')
        print(dfd)

print('\nFinished.')
