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

print("Program: x5data4.py, ver.2026-06-30")
print("Author:  V.Zerkin, Vienna, 2026")
print("Purpose: find datasets by reaction, load X5-json, extract data")
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

reacode='26-FE-54(N,EL)26-FE-54,,DA'
ei=5e6; eiMin=ei-0.05e6; eiMax=ei+0.05e6

reacode='8-O-16(N,EL)8-O-16,,DA'
ei=14.1e6; eiMin=ei-0.2e6; eiMax=ei+0.2e6
ei=14.1e6; eiMin=ei-0.5e6; eiMax=ei+0.5e6

print('---ReactionCode:',reacode)
print('---Energy.in:   ',str(eiMin/1e6),'-',str(eiMax/1e6),'MeV')

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
    eobj=ds['c5data'].get('x1')	# EN(EV)
    aobj=ds['c5data'].get('x2')	# ANG(ADEG)
    yarr=yobj.get('y');  dyarr=yobj.get('dy')
    earr=eobj.get('x1'); dearr=eobj.get('dx1')
    aarr=aobj.get('x2'); daarr=aobj.get('dx2')
#    print('\t--dearr:',dearr)
#    print('\t--aarr:',aarr)
#    print('\t==arrays:',len(yarr),len(earr),len(aarr))
    if (yarr is None): continue
    if (earr is None): continue
    if (aarr is None): continue
    yy=[]; dy=[]; xx=[]; dx=[]; ee=-777; ees=[]
    for ii in range(len(yarr)):
        y=yarr[ii]
        e=earr[0]
        if len(earr)>1: e=earr[ii]  #--repeating value
        a=aarr[0]
        if len(aarr)>1: a=aarr[ii]  #--repeating value
        ees.append(e/1e6)
        if (e<eiMin) or (e>eiMax): continue
        ee=e
        yy.append(y)
        xx.append(a)
        if dyarr is not None: dy.append(dyarr[ii])
        if daarr is not None: dx.append(daarr[ii])
    ees=list(set(ees))
    ees=sorted(ees)
    print('    Dataset:'+ds['DatasetID']+' '+str(ds['year1'])+','+ds['author1']
	+' #Pnt:'+str(len(yarr))
	+' #Pnt.selected:'+str(len(yy))
	+' #Einc:'+str(len(ees))
	+' Einc(MeV):'+str(ees[:8])
	)
    if len(yy)<=0: continue
    ytitle=ds['quantExpan']+' ('+yobj['units']+')'
    xtitle=aobj['expansion']+' ('+aobj['units']+')'

    print('    axis-->Y: '+str(ds['quantExpan'])+' ('+str(yobj['units'])+')')
    print('    axis-->X: '+str(aobj['expansion'])+' ('+str(aobj['units'])+')')
    print('    yy:',yy)
    print('    dy:',dy)
    print('    xx:',xx)
    print('    dx:',dx)
    #pprint(ds)
    ds['y']=yy; ds['dy']=dy
    ds['x']=xx; ds['dx']=dx
    ds['x4lbl']=str(ds['year1'])+' '+ds['author1ini']+ds['author1']+' Ei='+str(round(ee/1e6,1))+'MeV'
    dss.append(ds)
dss=sorted(dss,key=sort_ya1,reverse=True)
nDatasets=len(dss)
print('-1-Datasets:'+str(nDatasets))

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
plotTitle=reacode + ' Einc='+str(ei/1e6)+'MeV';

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
plot1['layout']=Layout(title='EXFOR angular distributions d\u03c3/d\u03a9(E,\u03B8): '+plotTitle
	+'  #Datasets:'+str(nDatasets)
	+'<br><i>X5json, by V.Zerkin, NRDC, 2026, ver.2026-06-30 //run:'+ct+'</i>'
	,xaxis=xaxis,yaxis=yaxis
	,plot_bgcolor='white'
	,legend=dict(traceorder="grouped")
)

outhtml='x5data4a'
plotly.offline.plot(plot1,filename=outhtml+'.html',auto_open=False)

#needs: $ pip3 install -U kaleido
plotly.io.write_image(plot1,outhtml+'.png',width=1200,height=790)

print('\nProgram successfully completed')
