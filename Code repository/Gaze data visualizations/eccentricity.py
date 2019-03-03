# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 03:12:18 2019

@author: Anuradha Kar
"""

###### eccentricity.py ################
## This program plots 2D distribution of gaze errors as a function of visual angles
## or eccentricity. Gaze error is plotted as function of gaze yaw (X) and pitch (Y) values
## For implementation of this code , the CSV file named user_data_proc.csv is used
## Data from yaw, pitch, gaze error column values are used

#############################################

import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy import interpolate
from mpl_toolkits.axes_grid1 import make_axes_locatable

gt_yaw=[]
gt_pitch=[]
gaze_er=[]

with open('C:/Users/Documents/Python Scripts/user_data_proc.csv','r') as csvfile:   
    datavals = csv.reader(csvfile, delimiter=',')
    datavals.next()
    for r1 in datavals:
        gt_yaw.append(float(r1[9]))   #Load gaze yaw data
        gt_pitch.append(float(r1[11])) #Load gaze pitch data
        gaze_er.append(float(r1[15]))   #Load gaze angle data

        
z= gaze_er
print max(z)
xi = np.linspace(min(gt_yaw),max(gt_yaw), 100)
yi= np.linspace(min(gt_pitch), max(gt_pitch), 100)

rbf = interpolate.interp2d(gt_yaw, gt_pitch, gaze_er, kind='cubic')
zi = rbf(xi, yi)

g4 = plt.figure(1)
ax = plt.gca()
im= ax.imshow(zi, vmin=0, vmax=3, origin='lower',
           extent=[min(gt_yaw), max(gt_yaw), min(gt_pitch), max(gt_pitch)])
plt.scatter(gt_yaw, gt_pitch, c=z)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1) 
plt.colorbar(im, cax=cax)
ax.set_title('Error vs visual angles')
