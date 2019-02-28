# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:33:44 2018

@author: 14233242
"""
###### outlier_removal.py ################
## This is the program to implement 3 different outlier removal strategies on gaze data
## For implementation of the outlier removal methods, the CSV file named user_data_proc.csv is used

#############################################

from pandas import Series
from matplotlib import pyplot
import matplotlib.pyplot as plt
import csv
import numpy as np
import math
import os, sys
import scipy.interpolate as sp
import scipy.interpolate
import matplotlib.mlab as mlab
import itertools
from scipy import stats
from scipy import signal


tim_rel=[]
gaze_ang=[]
gaze_gt=[]


###load gaze angle and ground truth data from from user_proc_desk.csv file#####

with open('C:/Users/14233242/Documents/Python Scripts/repo_codes/user_data_proc.csv','r') as csvfile:   
    datavals = csv.reader(csvfile, delimiter=',')
    datavals.next()
    for r1 in datavals:
        tim_rel.append(float(r1[0]))
        gaze_ang.append(float(r1[14]))   #Gaze angle data loaded from CSV file
        gaze_gt.append(float(r1[13]))    #Ground truth angle data loaded from CSV file

################################# 1. Apply median filtering ###################

y2= signal.medfilt(gaze_ang,41)
plt.scatter(tim_rel, y2, color= 'r')

f1 = plt.figure(1)
plt.subplot(2,1,1)
plt.plot(tim_rel,gaze_ang,'ro-')
plt.plot(tim_rel,gaze_gt,'k-')
plt.ylabel('Gaze angle in degree')
plt.title('Input gaze angle data')
plt.subplots_adjust(hspace = 0.4)

plt.grid()
plt.subplot(2,1,2)
plt.plot(tim_rel,y2,'bo-')
plt.plot(tim_rel,gaze_gt,'k-')
plt.title('Output: After outlier removal with median filter')
plt.xlabel('Time in ms')
plt.ylabel('Gaze angle in degree')
plt.show()
plt.grid()

####################### 2. Applying nedian absolute deviation method ##########
threshold = 3.5
ys= gaze_ang[0:2510]
median_y = np.median(ys)
median_absolute_deviation_y = np.median([np.abs(y - median_y) for y in ys])
modified_z_scores = [0.6745 * (y - median_y) / median_absolute_deviation_y
                         for y in ys]

for n, i in enumerate(modified_z_scores):
    if (np.abs(modified_z_scores[n]) > threshold):
        ys[n]= np.mean(ys)

f3 = plt.figure(3)
plt.subplot(2,1,1)
plt.plot(tim_rel,gaze_ang,'ro-')
plt.title('Input gaze angle data')
plt.ylabel('Gaze angle in degree')
plt.title('Input gaze angle data')
plt.subplots_adjust(hspace = 0.4)

plt.grid()
plt.subplot(2,1,2)
plt.plot(tim_rel,ys,'bo-')
plt.plot(tim_rel,gaze_gt,'k-')
plt.title('Output: After outlier removal with MAD')
plt.xlabel('time in ms')
plt.ylabel('Gaze angle in degree')
plt.show()
plt.grid()

####################### 3. Applying IQR method ################################
ys1= gaze_ang[0:2510]      
quartile_1, quartile_3 = np.percentile(ys, [25, 75])
iqr = quartile_3 - quartile_1
lower_bound = quartile_1 - (iqr * 1.5)
upper_bound = quartile_3 + (iqr * 1.5)

outlier1=np.zeros(2517)
for n, i in enumerate(ys):
    if (ys1[n] > upper_bound) | (ys1[n] < lower_bound):
        outlier1[n]= ys1[n]
        ys1[n]= np.mean(ys1)
        
        
f4 = plt.figure(4)
plt.subplot(2,1,1)
plt.plot(tim_rel,gaze_ang,'ro-')
plt.title('Input gaze angle data')
plt.ylabel('Gaze angle in degree')
plt.title('Input gaze angle data')
plt.subplots_adjust(hspace = 0.4)
plt.grid()
plt.subplot(2,1,2)
plt.plot(tim_rel, ys1,'bo-')
plt.plot(tim_rel,gaze_gt,'k-')
#plt.plot(tim_rel, outlier1,'bo-')
plt.title('Output: After outlier removal with IQR')
plt.xlabel('time in ms')
plt.ylabel('Gaze angle in degree')
plt.show()
plt.grid()
