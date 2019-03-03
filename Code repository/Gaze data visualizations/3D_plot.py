# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 01:41:35 2019

@author: 14233242
"""
###### 3D_plot.py ################
## This program plots the 3D distribution of gaze error values (in degrees)
## over the display screen area (in pixels) using data from the input gaze csv file.
## For implementation of this code , the CSV file named user_data_proc.csv is used

#############################################

import matplotlib.pyplot as plt
import csv
import numpy as np
from matplotlib import cm
from scipy import interpolate
from scipy import signal


gt_x=[]
gt_y=[]
gaze_err=[]

with open('C:/Users/14233242/Documents/Python Scripts/repo_codes/user_data_proc.csv','r') as csvfile:   
    datavals = csv.reader(csvfile, delimiter=',')
    datavals.next()
    for r1 in datavals:
        gaze_err.append(float(r1[15]))   #Load gaze error data
        gt_x.append(float(r1[1]))        #Load ground truth XY coordinates
        gt_y.append(float(r1[2]))



gz_err= signal.medfilt(gaze_err,41)
z = np.array(gaze_err)
f = interpolate.interp2d(gt_x, gt_y, z, kind='cubic')

xnew = np.arange(-700, 700)
ynew = np.arange(-500, 500)
znew = f(xnew, ynew)
X, Y = np.meshgrid(xnew, ynew)
Z = znew.reshape(X.shape)

######################## Creating 3D plot######################################
g4 = plt.figure(4)
ax = g4.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, rstride=40, cstride=40,cmap=cm.jet)
ax.set_xlabel('X axis in pixels')
ax.set_ylabel('Y axis in pixels')
ax.set_zlabel('Error in degrees')
plt.show()