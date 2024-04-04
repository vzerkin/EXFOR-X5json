"""
 ***********************************************************
 * Copyright: (C) 2024, Viktor Zerkin, V.Zerkin@gmail.com  *
 ***********************************************************
"""

def auto_corr_x5dataset(ds):
    FcDecayData=None
    DecayData=ds.get('DECAY-DATA')
    if (DecayData is not None): FcDecayData=DecayData.get('FcCorrDECAY_DATA')

    FcDecayMon=None
    DecayMon=ds.get('DECAY-MON')
    if (DecayMon is not None): FcDecayMon=DecayMon.get('FcCorrDECAY_MON')

    Fc0=None
    m0=None; m1=None; dm0=None; dm1=None
    c5mon=ds.get('c5mon')
    if (c5mon is not None):
        m0=c5mon.get('m0')
        m1=c5mon.get('m1')
        dm0=c5mon.get('dm0')
        dm1=c5mon.get('dm1')
        Fc0=c5mon.get('Fc0')
        if (dm0 is None): dm1=None
        if (dm1 is None): dm0=None

    if (Fc0 is None) and (FcDecayData is None) and (FcDecayMon is None): return False

    oy=ds['c5data'].get('y')
    yy=oy['y']
    dyy=oy.get('dy')

#    print('\tDataset:'+ds['DatasetID']+' '+str(ds['year1'])+','+ds['author1']+'*')
#    print('\tFcDecayData:',FcDecayData,'\tFcDecayMon:',FcDecayMon,'\tc5mon:',c5mon)
    if (FcDecayData is not None):	print('\t\tFcDecayData:',FcDecayData)
    if (FcDecayMon  is not None):	print('\t\tFcDecayMon:',FcDecayMon)
    if (Fc0         is not None):	print('\t\tFc0:',len(Fc0),' yy:',len(yy),yy)
    #if (c5mon      is not None):	print('\t\tc5mon:',c5mon)

    ynew=[None]*len(yy); FcMin=0; FcMax=0;
    if (dyy is not None): dynew=[None]*len(yy);
    else: dynew=None
    for ii in range(len(yy)):
        y0=yy[ii]
        fc=1
        if (Fc0 is not None):
            if (Fc0[ii] is not None):	fc*=Fc0[ii]
        if (FcDecayData is not None):	fc*=FcDecayData
        if (FcDecayMon  is not None):	fc*=FcDecayMon

        if (ii==0): fcMin=fcMax=fc
        else:
            if (fc<fcMin): fcMin=fc
            if (fc>fcMax): fcMax=fc

        y=y0*fc	#correction exp.cs
        print("\t\t"+str(ii)+"__.__fcorr-val:"+ds['DatasetID']+' y0='+str(y0)+' y='+str(y)+' fc='+str(fc))
        ynew[ii]=y
        if (dyy is not None):
            dy=dyy[ii]*fc
            if (y0!=0) and (m0 is not None) and (dm0 is not None) and (m1 is not None) and (dm1 is not None):
                dy=dyy[ii]/y0
                dm0t=dm0[ii]/m0[ii]
                dm1t=dm1[ii]/m1[ii]
                print("\t\t"+str(ii)+"__1__fcorr-err:"+ds['DatasetID']+' dy='+str(round(dy*100,3))+' dm0='+str(round(dm0t*100,3))+' dm1='+str(round(dm1t*100,3)))
                if (dy>dm0t):
                    dy=dy**2-dm0t**2+dm1t**2; #determination the quadrature of new total error
                else:
                    dy=dy**2+dm1t**2; #determination the quadrature of new total error
                print("\t\t"+str(ii)+"__2__fcorr-err:"+ds['DatasetID']+' dy='+str(round((dy**0.5)*100,3)))
                dy=dy**0.5*y;	#determination the absolute value of new total error
            dynew[ii]=dy
    ds['ynew']=ynew
    if (dyy is not None): ds['dynew']=dynew

    print('\t\tfc.Min, fc.Max:',fcMin,',',fcMax)

    ds['fcMax']=fcMax
    ds['fcMin']=fcMin
    maxDiff=fcMax
    if maxDiff>0:
        if 1/fcMax>maxDiff: maxDiff=1/fcMax
        if 1/fcMin>maxDiff: maxDiff=1/fcMin
    ds['maxDiff']=maxDiff
    ds['txtDiff']=Fc2Diff(fcMin,fcMax)

    return True



def Fc2Diff(FcMin,FcMax):
    if FcMax==0: return ''
    if FcMin<FcMax:
#        ss=f'[{addedFcPercent(FcMin)}..{addedFcPercent(FcMax)}]%'
        ss='['+addedFcPercent(FcMin)+'..'+addedFcPercent(FcMax)+']%'
    else:
#        ss=f'{addedFcPercent(FcMin)}%'
        ss=addedFcPercent(FcMin)+'%'
    return ss

def addedFcPercent(RRR):
#    if RRR<1: ss=f'{(RRR-1)*100:.2f}'
#    else:     ss=f'+{(RRR-1)*100:.2f}'
    if RRR<1: ss="%.2f" % ((RRR-1)*100)
    else:     ss="+%.2f" % ((RRR-1)*100)
    return ss
