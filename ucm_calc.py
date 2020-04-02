# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 08:59:13 2018

@author: Gaurav Patil
"""
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
from scipy.signal import butter, lfilter
import pickle
import os

#pickle_file = ''
with open('angles_sub2.pickle', 'rb') as handle:    
    angles_dict=pickle.load(handle)

tr= 'C 3 C'
sub_ht=1575
d3= 0.173*sub_ht
d5=0.16*sub_ht
count=0
q1=[]
q2=[]
q3=[]
q4=[]
q5=[]
q6=[]
q7=[]
for i in angles_dict:
    trial = angles_dict[i][1]
    if trial == tr:
        angles=angles_dict[i][2]
        q1.append(angles[0])
        q2.append(angles[1])
        q3.append(angles[2])
        q4.append(angles[3])
        q5.append(angles[4])
        q6.append(angles[5])
        q7.append(angles[6])
    
q1=np.asarray(q1)
q2=np.asarray(q2)
q3=np.asarray(q3)
q4=np.asarray(q4)
q5=np.asarray(q5)
q6=np.asarray(q6)
q7=np.asarray(q7)

q_mean=np.empty([500,7])
q_mean[:,0]=np.mean(q1,axis=0)
q_mean[:,1]=np.mean(q2,axis=0)
q_mean[:,2]=np.mean(q3,axis=0)
q_mean[:,3]=np.mean(q4,axis=0)
q_mean[:,4]=np.mean(q5,axis=0)
q_mean[:,5]=np.mean(q6,axis=0)
q_mean[:,6]=np.mean(q7,axis=0)

eta=np.empty([500,7])
eta[:,0]=d5*cos(q_mean[:,3])*sin(q_mean[:,4])*sin(q_mean[:,6])
eta[:,1]=d5*sin(q_mean[:,4])*sin(q_mean[:,3])*sin(q_mean[:,2])*sin(q_mean[:,6])
eta[:,2]=sin(q_mean[:,6])*(d5*sin(q_mean[:,2])*cos(q_mean[:,4])-d3*sin(q_mean[:,2])+d5*sin(q_mean[:,4])*cos(q_mean[:,2])*cos(q_mean[:,3]))
eta[:,3]=np.zeros([500])
eta[:,4]=-sin(q_mean[:,2])*(d3*cos(q_mean[:,4])*sin(q_mean[:,6])-d5*sin(q_mean[:,6])+d3*cos(q_mean[:,6])*cos(q_mean[:,5])*sin(q_mean[:,4]))
eta[:,5]=-d3*sin(q_mean[:,4])*sin(q_mean[:,2])*sin(q_mean[:,5])*sin(q_mean[:,6])
eta[:,6]=-d3*sin(q_mean[:,2])*cos(q_mean[:,5])*sin(q_mean[:,4])
eta=np.transpose(eta)
th_parallel=np.empty((size(q1,0),size(q1,1)))
th_orth=np.empty((size(q1,0),size(q1,1)))
for j in range(size(q1,0)):
    angles=np.array([q1[j,:],q2[j,:],q3[j,:],q4[j,:],q5[j,:],q6[j,:],q7[j,:]])-np.transpose(q_mean)
    for i in range(size(angles,1)):
        parl=(np.dot(angles[:,i],eta[:,i])/np.dot(eta[:,i],eta[:,i]))*eta[:,i]
        orth=angles[:,i]-parl
        th_orth[j,i]= np.sqrt(orth.dot(orth))
        th_parallel[j,i]=np.sqrt(parl.dot(parl))
V_parallel = np.sum(np.square(th_parallel), axis=0)/4*size(q1,0)
V_orth = np.sum(np.square(th_orth), axis=0)/7*size(q1,0)
UCM= np.sqrt(V_parallel)/np.sqrt(V_orth)

V_parallel_b3b=V_parallel
V_orth_b3b=V_orth
UCM_b3b=UCM
        