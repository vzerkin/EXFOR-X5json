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
 *   Viktor Zerkin, PhD, IAEA-NDS(1999-2023), NRDC(1999-2024)                      *
 *   e-mail: v.zerkin@gmail.com                                                    *
 ***********************************************************************************
"""
import datetime
import json
import sys
sys.path.append('./')
from x5subr import *
import plotly
from plotly.graph_objs import Scatter, Layout 
from pprint import pprint

print("Program: x5data8fy.py, ver.2026-07-01")
print("Author:  V.Zerkin, Vienna, 2026")
print("Purpose: find datasets by reaction, load X5-json, extract")
print("         FY - total chain yield of fission products,")
print("         filter data by incident energy, plot by Plotly")

print("")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")
#input("Press the <ENTER> key to continue...")

base='./'

def sort_ya1(ds):
    rr=str(ds['year1'])+','+ds['author1ini']+ds['author1']
    return rr

#datasets=read_csv_file("EXFOR-Datasets.csv")
datasets=read_csv_file("X5-Datasets.csv")
nDatasets=len(datasets)
print('-0-Datasets:'+str(nDatasets))

reacode='92-U-238(N,F)MASS,CHN,FY'
ei=14e6; eiMin=13e6; eiMax=15e6

print('---ReactionCode:',reacode)
print('---Energy.in:   ',str(eiMin),'-',str(eiMax),'eV')

datasets=filter_datasets(datasets,'ReactionCode',reacode)
nDatasets=len(datasets)
print('-1-Datasets:'+str(nDatasets))
if (nDatasets<=0):
    print("---No data found---")
    sys.exit(2)

xtitle=''; ytitle=''
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
    if (ds is None): continue
    print('    c5data:',get_cvars(ds))
    yobj=ds['c5data'].get('y')
    eobj=ds['c5data'].get('x1')		# EN(EV)
    zaobj=ds['c5data'].get('x2')	# ZAM(ARB-UNITS)
    yarr=yobj.get('y');  dyarr=yobj.get('dy')
    earr=eobj.get('x1'); dearr=eobj.get('dx1')
    zaarr=zaobj.get('x2')
#    print('\t--dearr:',dearr)
#    print('\t==arrays:',len(yarr),len(earr))
    if (yarr is None): continue
    if (earr is None): continue
    yy=[]; dy=[]; xx=[]; dx=[]; ee=-777
    for ii in range(len(yarr)):
        y=yarr[ii]
        e=earr[0]
        if len(earr)>1: e=earr[ii]  #--repeating value
        m=zaarr[0]
        if len(zaarr)>1: m=zaarr[ii]  #--repeating value
        if eiMin is not None:
            if (e<eiMin): continue
        if eiMax is not None:
            if (e>eiMax): continue
        ee=e
        e1=e; e2=e
        yy.append(y)
        xx.append(m)
        if dyarr is not None: dy.append(dyarr[ii])
        if dearr is not None: e1=e-dearr[ii]; e2=e+dearr[ii]
    print('    Dataset:'+ds['DatasetID']+' '+str(ds['year1'])+','+ds['author1']
	+' #Pnt:'+str(len(yarr))
	+' #Pnt.selected:'+str(len(yy))
	)
    if len(yy)<=0: continue
    ytitle=ds['quantExpan']+' ('+yobj['units']+')'
    xtitle=zaobj['expansion']+' ('+zaobj['units']+')'

    print('    yy:',yy)
    print('    dy:',dy)
    print('    xx:',xx)
    print('    dx:',dx)
    #pprint(ds)
    ds['y']=yy; ds['dy']=dy
    ds['x']=xx; ds['dx']=dx
    estr=' Ei='+str(round(ee/1e6,1))+'MeV'
    if e2>e1: estr=' Ei='+str(round(e1/1e6,1))+'-'+str(round(e2/1e6,1))+'MeV'
    ds['x4lbl']=str(ds['year1'])+' '+ds['author1ini']+ds['author1']+estr
    dss.append(ds)
dss=sorted(dss,key=sort_ya1,reverse=True)
nDatasets=len(dss)
print('-1-Datasets:'+str(nDatasets))
print('---ReactionCode:',reacode)
print('---Energy.in:   ',str(eiMin),'-',str(eiMax),'eV')
print('---Axis-Y:      ',ytitle)
print('---Axis-X:      ',xtitle)
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
plotTitle=reacode+' Ei=['+str(eiMin/1e6)+'-'+str(eiMax/1e6)+']MeV'

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
plot1['layout']=Layout(title='EXFOR yield of fission products FY(A,Ei): '+plotTitle
	+'  #Datasets:'+str(nDatasets)
	+'<br><i>X5json, by V.Zerkin, NRDC, 2026, ver.2026-07-01 //run:'+ct+'</i>'
	,xaxis=xaxis,yaxis=yaxis
	,plot_bgcolor='white'
	,legend=dict(traceorder="grouped")
)

outhtml='x5data8fy'
plotly.offline.plot(plot1,filename=outhtml+'.html',auto_open=False)

#needs: $ pip3 install -U kaleido
plotly.io.write_image(plot1,outhtml+'.png',width=1200,height=790)

print('\nProgram successfully completed')
