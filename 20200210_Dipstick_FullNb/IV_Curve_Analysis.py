# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 20:54:57 2020

@author: Jakob
"""
from argparse import ArgumentParser
import matplotlib.pylab as plt
import os
import sys

sys.path.insert(0, '../../IV_Mixer_Analysis')
sys.path.insert(0, '../../Helper')


from IV_Class import kwargs_IV_Response_rawData,IV_Response
from Read_Filenames import read_Filenames
from plotxy import newfig,pltsettings,lbl,plot

kwargs_IV_Response_rawData['skip_IV_simulation']=True
kwargs_IV_Response_rawData['offsetThreshold']= .2

parser = ArgumentParser()
parser.add_argument('-f', '--folder', action='store',default = 'Default_Folder', help='The folder in which the result is stored in.')
args = parser.parse_args()

directory = args.folder+'/'
if not os.path.exists(directory):
        os.makedirs(directory)
        
filenames,filenamesstr = read_Filenames("")

#for i in filenames:
#    kwargs_IV_Response_rawData['fixedOffset']=[0,0]
#    IV = IV_Response(i,**kwargs_IV_Response_rawData)
#    plot(IV.binedIVData)
#    print('plot %s'%i)   
#    plt.show()


ylims = {'Backup_Old_m.csv':[-300,300], 
          'Backup_Old_n.csv':[-300,300], 
          'D1_15_m.csv':[-300,300],
          'D1_15_n.csv':[-300,300], 
          'D1_17_m.csv':[-200,200], 
          'D1_17_n.csv':[-200,200]}

for i in filenames:
    IV = IV_Response(i,**kwargs_IV_Response_rawData)
    title=newfig(i.replace('.csv','_Manual_Offset_Correction'))
    IV.plot_IV_with_Info([-3.9,50,-3.9,50],linespacing=1.7,fontsize=10)
    plt.tight_layout()
    pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=True, xlabel=lbl['uA'],ylabel=lbl['mV'], 
                xlim=[-4,4],ylim=ylims[i],title=None,legendColumns=1,skip_legend=True)


#Old implementation before IV_Class was updated on 14.02.2020.
#
#offsetCorrection={'Backup_Old_m.csv':[(-2.56+2.65)/2,(-1.01+16.5)/2], 
#                  'Backup_Old_n.csv':[(-2.70+2.85)/2,(-33+49)/2], 
#                  'D1_15_m.csv':[(-2.91+3.08)/2,(-148+164.5)/2],
#                  'D1_15_n.csv':[(.07)/2,(-73.84+85.54)/2], 
#                  'D1_17_m.csv':[(-0.12+0.009)/2,-(-44.47+29.64)/2], 
#                  'D1_17_n.csv':[(-2.5+2.67)/2,(-9+22.35)/2]}
#

#
#for i in filenames:
#    kwargs_IV_Response_rawData['fixedOffset']=offsetCorrection[i]
#    IV = IV_Response(i,**kwargs_IV_Response_rawData)
#    title=newfig(i.replace('.csv','_Manual_Offset_Correction'))
#    IV.plot_IV_with_Info([-3.9,50,-3.9,50],linespacing=1.7,fontsize=10)
#    plt.tight_layout()
#    pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=True, xlabel=lbl['uA'],ylabel=lbl['mV'], 
#                xlim=[-4,4],ylim=ylims[i],title=None,legendColumns=1,skip_legend=True)
#
#
#for i in filenames:
#    kwargs_IV_Response_rawData['fixedOffset']=None
#    IV = IV_Response(i,**kwargs_IV_Response_rawData)
#    title=newfig(i.replace('.csv','_Automatic_Correction'))
#    IV.plot_IV_with_Info([-3.9,50,-3.9,50],linespacing=1.7,fontsize=10)
#    plt.tight_layout()
#    pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=True, xlabel=lbl['uA'],ylabel=lbl['mV'], 
#                xlim=[-4,4],ylim=ylims[i],title=None,legendColumns=1,skip_legend=True)
#    
####### Check why automatic correction is not working ######    
#for i in filenames:
#    kwargs_IV_Response_rawData['fixedOffset']=None
#    IV = IV_Response(i,**kwargs_IV_Response_rawData)
#    title=newfig(i.replace('.csv','_Slope'))
#    plt.plot(IV.rawIVData[0],IV.rawIVData[1]*100)
#    IV.plot_slope_raw_unsorted()
#    plt.tight_layout()
#    pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=True, xlabel=lbl['uA'],ylabel=lbl['mV'], 
#                xlim=[-.5,.5],title=None,legendColumns=1,skip_legend=True)
