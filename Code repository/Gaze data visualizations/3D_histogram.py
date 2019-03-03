# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 01:58:45 2019

@author: Anuradha Kar
"""

###### 3D_histogram.py ################
## This program plots stacked 3D gaze error distributions using data from 
##two or more data columns (e.g. from different eye trackers or experiments in a 
##single plot, for comparison of data characteristics from two or more datasets.
## For implementation of this code , the CSV file named user_data_proc.csv is used
## Data from yaw, pitch, gaze angle column values are used as an example.

#############################################

import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy import signal

gaze_yaw=[]
gaze_pitch=[]
gaze_ang=[]

with open('C:/Users/Documents/Python Scripts/user_data_proc.csv','r') as csvfile:   
    datavals = csv.reader(csvfile, delimiter=',')
    datavals.next()
    for r1 in datavals:
        gaze_yaw.append(float(r1[10]))   #Load gaze yaw data
        gaze_pitch.append(float(r1[12])) #Load gaze pitch data
        gaze_ang.append(float(r1[14]))   #Load gaze angle data


gaze_ang= signal.medfilt(gaze_ang,41)
gaze_pitch = signal.medfilt(gaze_pitch,41)
gaze_yaw= signal.medfilt(gaze_yaw,41)

######################### Plotting histograms #################################
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
nbins = 50
hist1, bins = np.histogram(gaze_yaw, bins=100)
hist2, bins = np.histogram(gaze_pitch, bins=100)
hist3, bins = np.histogram(gaze_ang, bins=100)
xs = (bins[:-1] + bins[1:])/2

ax.bar(xs, hist1, zs=10, zdir='y', color='r', alpha=0.8)
ax.bar(xs, hist2, zs=20, zdir='y', color='g', alpha=0.8)
ax.bar(xs, hist3, zs=30, zdir='y', color='b', alpha=0.8)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
