# -*- coding: utf-8 -*-
"""
Created on Thu Jun 05 13:59:00 2014

@author: houska-t
"""

import pandas as pd
import datetime as dt
import numpy as np


###############################################################################
Datum    ='221014'
Order    =['Startzeit','Endzeit','Sensorset','Mean','Std']
A1       =['13:35' ,'14:15', 2, None, None]
A2       =['13:37' ,'14:17', 1, None, None]
A3       =['14:37' ,'15:17', 1, None, None]
G2       =['14:25' ,'15:05', 2, None, None]
G1       =['15:32' ,'16:12', 1, None, None]
W1       =['16:14' ,'16:54', 2, None, None]
W3       =['15:26' ,'16:06', 2, None, None]
W2       =['16:23' ,'17:03', 1, None, None]
###############################################################################


'''Voodoo'''
print 'Load Temperature data for '+Datum
Transekte    =[A1,A2,A3,G1,G2,W1,W2,W3]#Combine Transects
Transektnames=['A1','A2','A3','G1','G2','W1','W2','W3']
for i in range(len(Transekte)):#run through Transects
    print 'Calculate mean for '+Transektnames[i]
    if Transekte[i][2]==1:#Get Sensorset filenames
        Filenames=[Datum+'_S1.xls',Datum+'_S2.xls',Datum+'_S3.xls',Datum+'_S4.xls',Datum+'_S5.xls']
    if Transekte[i][2]==2:
        Filenames=[Datum+'_S6.xls',Datum+'_S7.xls',Datum+'_S8.xls',Datum+'_S9.xls' ,Datum+'_S10.xls']
   
    meansForChamber=[]
    stdForChamber=[]
    for Filename in Filenames:#Calculate mean for each file between defined start- and endtime 
        parse = lambda x: dt.datetime.strptime(x, '%d.%m.%Y %H:%M:%S')
        df = pd.io.excel.read_excel(Filename, index_col=0, date_parser=parse,skiprows=6)
        df.index=pd.to_datetime(df.index)
        meansForChamber.append(np.mean(df.between_time(Transekte[i][0],Transekte[i][1]))[0])
        for value in df.between_time(Transekte[i][0],Transekte[i][1]).values:        
            stdForChamber.append(value)
    Transekte[i][3]=np.mean(meansForChamber)#Calulate mean for Transect
    Transekte[i][4]=np.std(stdForChamber)#Calulate std for Transect

df1=pd.DataFrame(data=Transekte,index=Transektnames,columns=Order)
print 'Save file in '+Datum+'meanTemp.xls'
df1.to_excel(Datum+'meanTemp.xls')
print 'Done'


