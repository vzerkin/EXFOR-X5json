"""
 ***********************************************************************************
 * Copyright (C) 2026 Viktor Zerkin (NRDC), v.zerkin@gmail.com                     *
 *-----------------------------------------------------------------------------    *
 * Permission is hereby granted, free of charge, to any person obtaining a copy    *
 * of this software and associated documentation files (the "Software"), to deal   *
 * in the Software without restriction, including without limitation the rights    *
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       *
 * copies of the Software, and to permit persons to whom the Software is furnished *
 * to do so, subject to the following conditions:                                  *
 *                                                                                 *
 * The above copyright notice and this permission notice shall be included in all  *
 * copies or substantial portions of the Software.                                 *
 *                                                                                 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      *
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        *
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     *
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          *
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   *
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN       *
 * THE SOFTWARE.                                                                   *
 *                                                                                 *
 *-----------------------------------------------------------------------------    *
 *   AUTHOR:                                                                       *
 *   Viktor Zerkin, PhD, IAEA-NDS(1999-2023), NRDC(1999-2026)                      *
 *   e-mail: v.zerkin@gmail.com                                                    *
 ***********************************************************************************
"""
import datetime
import json
import math
import sys
sys.path.append('./')
from x5subr import *
import plotly
from plotly.graph_objs import Scatter, Layout 
from pprint import pprint

print("Program: x5data6dae.py, ver.2026-07-01")
print("Author:  V.Zerkin, Vienna, 2026")
print("Purpose: find datasets by reaction, load X5-json,")
print("         extract double differential cross section data")
print("         filter data by angle and incident energy, plot by Plotly")
print("")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")
#input("Press the <ENTER> key to continue...")

nexample='default'
if (len(sys.argv)>1) and (sys.argv[1]!=''): nexample=str(sys.argv[1])

base='./'

def sort_ya1(ds):
#   rr=str(ds['year1'])+','+ds['author1ini']+ds['author1']
    rr=str(ds['ei'])+':'+str(ds['year1'])+','+ds['author1ini']+ds['author1']
    return rr

#datasets=read_csv_file("EXFOR-Datasets.csv")
datasets=read_csv_file("X5-Datasets.csv")
nDatasets=len(datasets)
print('-0-Datasets:'+str(nDatasets))

eiMin=None; eiMax=None

reacode='9-F-19(N,X)0-NN-1,,DA/DE'
an=45; anMin=an-0.5; anMax=an+0.5
eiMin=14.1e6; eiMax=14.2e6

print('---ReactionCode:',reacode)
print('---Angle.out:   ',anMin,'-',anMax,'deg.')
print('---Energy.in:   ',str(eiMin),'-',str(eiMax),'eV')

datasets=filter_datasets(datasets,'ReactionCode',reacode)
nDatasets=len(datasets)
print('-1-Datasets:'+str(nDatasets))
if (nDatasets<=0):
    print("---No data found---")
    sys.exit(2)

xtitle=''; ytitle=''
outDatasets={}
vary='y'; varEN='x1'; varAN='x3'; varE2='x2'
dss=[];ids=0
for dataset in datasets:
    entryfile=base+dataset['dir']+'/'+dataset['Entry']+'.x5.json'
    EntryID=dataset['Entry']
    SubentID=dataset['DatasetID'][:8]
    DatasetID=dataset['DatasetID']
    print(str(ids)+') File:['+entryfile+'] Subent:'+SubentID+' Dataset:'+DatasetID)
    f=open(entryfile)
    Entry=json.load(f)
    ids+=1
    Subent=get_subent(Entry,SubentID)
    if (Subent is None): continue
    ds=get_dataset(Subent,DatasetID)
#    print('\n\n++++\n'+json.dumps(ds,indent=2))
    if (ds is None): continue
    print('    c5data:',get_cvars(ds))
    varEN=get_cvar4fam(ds['c5data'],'EN')
    varAN=get_cvar4fam(ds['c5data'],'ANG')
    varE2=get_cvar4fam(ds['c5data'],'E2')
    if (varE2 is None): continue
    yobj=ds['c5data'].get('y')
    eobj=ds['c5data'].get(varEN)	# EN(EV)
    aobj=ds['c5data'].get(varAN)	# ANG(ADEG)
    e2obj=ds['c5data'].get(varE2)	# E2(EV)
    ytitle=ds['quantExpan']+' ('+yobj['units']+')'
    xtitle=e2obj['expansion']+' ('+e2obj['units']+')'
    yarr=yobj.get('y');  dyarr=yobj.get('dy')
    earr=eobj.get(varEN); dearr=eobj.get('d'+varEN)
    aarr=aobj.get(varAN); daarr=aobj.get('d'+varAN)
    e2arr=e2obj.get(varE2); de2arr=aobj.get('d'+varE2)
#    print('\t==arrays:'+' Data:'+str(len(yarr))+' En:'+str(len(earr))+' An:'+str(len(aarr))+' E2:'+str(len(e2arr)))
#    print('\t Da:',yarr)
#    print('\t En:',earr)
#    print('\t An:',aarr)
#    print('\t E2:',e2arr)
    if (yarr is None): continue
    if (earr is None): continue
    if (aarr is None): continue
    if (e2arr is None): continue
    nPnt=0
    yy=[]; dy=[]; xx=[]; dx=[]; aa=-777; aas=[]; ee=-777; ees=[]
    for ii in range(len(yarr)):
        y=yarr[ii]
        e=earr[0]
        if len(earr)>1: e=earr[ii]	#--repeating value
        a=aarr[0]
        if len(aarr)>1: a=aarr[ii]	#--repeating value
        e2=e2arr[0]
        if len(e2arr)>1: e2=e2arr[ii]	#--repeating value
#        print(' y=',y,' e=',e,' a=',a,' e2=',e2)

        aa=a; ee=e
        aas.append(a)
        ees.append(e)

        if eiMin is not None:
            if (e<eiMin): continue
        if eiMax is not None:
            if (e>eiMax): continue

        if (a<anMin) or (a>anMax): continue

#        print(' y=',y,' e=',e,' a=',a,' e2=',e2)

        nowDatasetSplit=ds['DatasetID']+' '+str(round(a))+' '+str(round(e/1e6))
#        print('---nowDatasetSplit:['+nowDatasetSplit+']')
        nowDataset=outDatasets.get(nowDatasetSplit)
        if nowDataset is None:
            nowDataset={}
            outDatasets[nowDatasetSplit]=nowDataset
            nowDataset['DatasetID']=ds['DatasetID']
            nowDataset['year1']=ds['year1']
            nowDataset['author1ini']=ds['author1ini']
            nowDataset['author1']=ds['author1']
            yy=[]; dy=[]; xx=[]; dx=[]
            nowDataset['y']=yy; nowDataset['dy']=dy
            nowDataset['x']=xx; nowDataset['dx']=dx
            nowDataset['x4lbl']=str(ds['year1'])+' '+ds['author1ini']+ds['author1']+' An='+str(round(aa,1))+'deg'+' Ein='+str(round(e/1e6,1))+'MeV'
            nowDataset['ei']=e
#           print('++++\n'+json.dumps(nowDataset,indent=2))
        else:
            yy=nowDataset['y']; dy=nowDataset['dy']
            xx=nowDataset['x']; dx=nowDataset['dx']
        nPnt+=1
        yy.append(y)
        xx.append(e2)
        if dyarr is not None: dy.append(dyarr[ii])
        if de2arr is not None: dx.append(de2arr[ii])
    ees=list(set(ees));    ees=sorted(ees)
    aas=list(set(aas));    aas=sorted(aas)
#   print('    outDatasets:'+str(len(outDatasets)))
    print('    Dataset:'+ds['DatasetID']+' '+str(ds['year1'])+','+ds['author1']
	+' #Pnt:'+str(len(yarr))
	+' #Pnt.selected:'+str(nPnt)
	+' #Aout:'+str(len(aas))
	+' Aout(deg):'+str(aas[:8])
	+' #Ein:'+str(len(ees))
	+' Ein(eV):'+str(ees[:8])
	)
#    if ids>0: break

#print('++++++++\n'+json.dumps(outDatasets,indent=2))
outDatasets=list(outDatasets.values())
print('---ReactionCode:',reacode)
print('---Angle.out:   ',anMin,'-',anMax,'deg.')
print('---Energy.in:   ',str(eiMin),'-',str(eiMax),'eV')
print('---Data selected---')
dss=[];ids=0
for dataset in outDatasets:
    ids+=1
    print(str(ids).rjust(4)+' '+dataset['x4lbl']+' ly:'+str(len(dataset['y'])))
    if len(dataset['y'])>0: dss.append(dataset)
#    print('++++\n'+json.dumps(dataset,indent=2))

dss=sorted(dss,key=sort_ya1,reverse=True)
nDatasets=len(dss)
print('-1-Datasets:'+str(nDatasets))
if (nDatasets<=0):
    print("---No data to plot---")
    sys.exit(2)

#_________________Preparing EXFOR data for plot_________________
data1=[]; ii=0
for ds in dss:
    tr=Scatter(x=ds['x'],y=ds['y']
	,text=ds['x4lbl']
	,name=str(ii+1)+') '+ds['x4lbl']+' pt:'+str(len(ds['x']))+' #'+ds['DatasetID']
	,marker_symbol=str(ii%33)
	,marker_size=8
	,mode="markers"
	)
    if (ds['dy'] is not None): tr.error_y=dict(type='data',array=ds['dy'],visible=True,thickness=0.9)
    if (ds['dx'] is not None): tr.error_x=dict(type='data',array=ds['dx'],visible=True,thickness=0.9)
    data1.append(tr)
    ii+=1

xtype='linear';ytype='linear'
#xtype='log';
ytype='log'
plotTitle=reacode + ' An='+str(an)+'deg'+' Einc=['+str(eiMin/1e6)+'-'+str(eiMax/1e6)+']MeV';

#_________________Plot data from EXFOR_________________
plot1={}
plot1['data']=data1
xaxis=dict(title=xtitle,showline=True,linecolor='black',ticks='outside'
,showgrid=True,gridcolor='#aaaaaa',type=xtype)
yaxis={'title':ytitle,'showline':True,'linecolor':'black'
	,'showgrid':True, 'gridcolor':'#aaaaaa','ticks':'outside','type':ytype
	,'zeroline':True, 'zerolinecolor':'#dddddd'#, 'zerolinewidth':0.1
}
xaxis['mirror']='ticks'
yaxis['mirror']='ticks' 
plot1['layout']=Layout(title='EXFOR double differential cross sections: '+plotTitle
	+'  #Datasets:'+str(nDatasets)
	+'<br><i>X5json, by V.Zerkin, NRDC, 2026, ver.2026-06-01 //run:'+ct+'</i>'
	,xaxis=xaxis,yaxis=yaxis
	,plot_bgcolor='white'
	,legend=dict(traceorder="grouped")
)

outhtml='x5data6dae'
plotly.offline.plot(plot1,filename=outhtml+'.html',auto_open=False)

#needs: $ pip3 install -U kaleido
plotly.io.write_image(plot1,outhtml+'.png',width=1200,height=790)

print('\nProgram successfully completed')
