#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:32:16 2020

@author: wenninger
"""
from argparse import ArgumentParser
import numpy as np
import os
import scipy.constants as const
import sys

sys.path.insert(0, '../../Helper')
sys.path.insert(0, '../../IV_Mixer_Analysis')
sys.path.insert(0, '../../Superconductivity')

from IV_Class import IV_Response,kwargs_IV_Response_rawData
from plotxy import plot,newfig,pltsettings,lbl
from Read_Filenames import read_Filenames,filenamesstr_of_interest

parser = ArgumentParser()
parser.add_argument('-f', '--folder', action='store',default = 'Default_Folder', help='The folder in which the result is stored in.')
args = parser.parse_args()

directory = args.folder+'/'
if not os.path.exists(directory):
        os.makedirs(directory)

# corresponding with the pumped and unpumped IV curve
filenames = {"univ":None,"iv":None}
filenamesstr = {"univ":None,"iv":None}
for i in filenames: #["univ","iv"]: 
    names,namesstr = read_Filenames("*-%s*"%(i))
    filenames[i] = names
    filenamesstr[i]=np.array(namesstr)

kwargs_IV_Response_rawData['rNThresholds']=[2.,10] #The dataset is to small to validate rN
kwargs_IV_Response_rawData['skip_IV_analysis']=True

#Raw generated with:
#dict(zip(np.hstack([filenames['univ'],filenames['iv']]), np.zeros((80,2))))
#replace "array" with ""
offset ={'c-6.00-univ.csv': ([-1.131, 5.023]),
         'c-5.00-univ.csv': ([-1.233, .4999]),
         'c-4.75-univ.csv': ([-1.2628, -.7698]),
         'c-6.10-univ.csv': ([-1.1239, 5.355]),
         'c-6.20-univ.csv': ([-1.114, 5.875]),
         'c-4.75-45-iv.csv': ([-1.2641, -.9459]),
         'c-6.20-45-iv.csv': ([-1.114, 5.875]),
         'c-5.90-45-iv.csv': ([0., 0.]),
         'c-5.40-45-iv.csv': ([0., 0.]),
         'c-6.00-45-iv.csv': ([1.1299, 5.1355]),
         'c-5.60-45-iv.csv': ([0., 0.]),
         'c-6.30-45-iv.csv': ([0., 0.]),
         'c-5.80-45-iv.csv': ([0., 0.]),
         'c-5.00-45-iv.csv': ([-1.2346, .45755]),
         'c-6.10-45-iv.csv': ([-1.12578, 5.355]),
         'c-5.20-45-iv.csv': ([0., 0.])}

for i in filenames['univ']:
    kwargs_IV_Response_rawData['fixedOffset']=offset[i]
    Unpumped = IV_Response(i,**kwargs_IV_Response_rawData)
    #find the index of the corresponding pumped iv curve
    index = np.where(filenamesstr['iv'][:,1] == i[2:6])[0][0]
    Pumped = IV_Response(filenames['iv'][index],**kwargs_IV_Response_rawData)
    title = newfig('Unpumped_Pumped_at_%s_K'%(i[2:6]))
    plot(Unpumped.binedIVData,label='Unpumped '+i)
    plot(Pumped.binedIVData,label='Pumped '+filenames['iv'][index])
    pltsettings(save=directory+title,fileformat='.pdf',disp = True,close=False, xlabel=lbl['mV'],ylabel=lbl['uA'], 
                title=None,legendColumns=1,skip_legend=False)
    pltsettings(save=directory+title+'zoom',fileformat='.pdf',disp = True,close=False, xlabel=lbl['mV'],ylabel=lbl['uA'], 
                xlim=[0,3.5],ylim=[0,80],title=None,legendColumns=1,skip_legend=False)
    
fLO =831.6 *1e9 # guess from another dataset
vPh = const.h*fLO/const.e *1e3 # mV
print('The photon voltage is %.2f mV'%vPh)