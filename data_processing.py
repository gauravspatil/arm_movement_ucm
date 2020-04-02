# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 08:40:48 2018

@author: Gaurav Patil
"""

import matplotlib.pyplot as plt
from pylab import *
from numpy import *
import time
import csv
from scipy.signal import butter, lfilter
import pickle
import os
import pandas as pd  

def fill_blanks(data):
    not_nan = np.logical_not(np.isnan(data))
    indices = np.arange(len(data))
    output=np.interp(indices, indices[not_nan], data[not_nan])
    return output

def calc_dist(a,b):
    dist = np.empty([1,size(a,1)])
    for i in range(size(a,1)):
        dist[:,i]=np.linalg.norm(a[:,i]-b[:,i])
    return dist

data_file= 'F:\\Github\\arm_ucm\\Part_102_Data\\trial8.csv'
df = pd.read_csv(data_file)
trig_sig=df['Column18'].tolist()[4:]
trig_sig=[float(i) for i in trig_sig]

trial_file = 'F:\\Github\\arm_ucm\\2\\Zoe_6_21_8.txt'
f = open(trial_file, 'r')
trial_order = f.read().split('\n')

trig_sig=[float(i) for i in df['Column18'].tolist()[4:]]

trig_indx = []
for i in range(len(trig_sig)-2):
    if (trig_sig[i]-2)*(trig_sig[i+1]-2)<0:
        trig_indx.append(i)
st=4
joint_angles= np.empty([7,len(trig_sig)])        
joint_angles[0,:]=fill_blanks(np.asarray([float(i) for i in df['Column2'].tolist()[st:]]))
joint_angles[1,:]=fill_blanks(np.asarray([float(i) for i in df['Column3'].tolist()[st:]]))
joint_angles[2,:]=fill_blanks(np.asarray([float(i) for i in df['Column4'].tolist()[st:]]))
joint_angles[3,:]=fill_blanks(np.asarray([float(i) for i in df['Column5'].tolist()[st:]]))
joint_angles[4,:]=fill_blanks(np.asarray([float(i) for i in df['Column6'].tolist()[st:]]))
joint_angles[5,:]=fill_blanks(np.asarray([float(i) for i in df['Column7'].tolist()[st:]]))
joint_angles[6,:]=fill_blanks(np.asarray([float(i) for i in df['Column8'].tolist()[st:]]))

obj_pos=np.empty([3,len(trig_sig)])
knuc_pos= np.empty([3,len(trig_sig)])
obj_pos[0,:]=fill_blanks(np.asarray([float(i) for i in df['Column9'].tolist()[st:]]))
obj_pos[1,:]=fill_blanks(np.asarray([float(i) for i in df['Column10'].tolist()[st:]]))
obj_pos[2,:]=fill_blanks(np.asarray([float(i) for i in df['Column11'].tolist()[st:]]))
knuc_pos[0,:]=fill_blanks(np.asarray([float(i) for i in df['Column15'].tolist()[st:]]))
knuc_pos[1,:]=fill_blanks(np.asarray([float(i) for i in df['Column16'].tolist()[st:]]))
knuc_pos[2,:]=fill_blanks(np.asarray([float(i) for i in df['Column17'].tolist()[st:]]))
dist= calc_dist(obj_pos,knuc_pos)
if 'flg' not in globals():
    angles_dict={}
    tc=0
    flg=1
    
trial_no=0
x_new = np.linspace(0, 499, 500)
for i in range(int(len(trig_indx)/2)):  # start and stop None, step 2
    if trig_indx[2*i+1]-trig_indx[2*i]>115:
        trial_no+=1
    else:
        
        angles=joint_angles[:,trig_indx[2*i]:trig_indx[2*i+1]]
        knuc_dist = dist[:,trig_indx[2*i]:trig_indx[2*i+1]]
        a=np.empty([7,500])
        grad=gradient(knuc_dist[0,:])
        for k in range(45, len(grad)):
            if grad[k]*grad[k-1]<=0 and abs(grad[k])<2:
                c_pt=k
                break
            
        jt_angles=angles[:,0:c_pt]
        x = np.linspace(0, 499, num=size(jt_angles,1))
        a[0] = radians(np.interp(x_new, x, jt_angles[0]))
        a[1] = radians(np.interp(x_new, x, jt_angles[1]))
        a[2] = radians(np.interp(x_new, x, jt_angles[2]))
        a[3] = radians(np.interp(x_new, x, jt_angles[3]))
        a[4] = radians(np.interp(x_new, x, jt_angles[4]))
        a[5] = radians(np.interp(x_new, x, jt_angles[5]))
        a[6] = radians(np.interp(x_new, x, jt_angles[6]))
        tc+=1
        angles_dict[tc]=[tc,trial_order[trial_no],a]
        trial_no+=1
        
        
        
