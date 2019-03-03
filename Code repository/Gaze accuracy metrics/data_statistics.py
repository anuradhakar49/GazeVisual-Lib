# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 17:21:33 2019

@author: 14233242
"""

###### data_statistics.py ################
## This program calculates mean, standard and median absolute deviation,
## 95% confidence intervals and Zscore from the input gaze csv file.
## It also plots the 1-D Kernel density estimate of gaze error values
## For implementation,  the CSV file named user_data_proc.csv is used

#############################################

import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy import stats
from scipy import signal
import statsmodels.stats.api as sms
from sklearn.neighbors import KernelDensity


tim_rel=[]
gaze_gt=[]
gaze_ang=[]

with open('C:/Users/14233242/Documents/Python Scripts/repo_codes/user_data_proc.csv','r') as csvfile:   
    datavals = csv.reader(csvfile, delimiter=',')
    datavals.next()
    for r1 in datavals:
        tim_rel.append(float(r1[0]))
        gaze_ang.append(float(r1[14]))   #Load gaze angle data
        gaze_gt.append(float(r1[13]))  #Load gaze ground truth angle
        
############ Estimate gaze error ####################
gz_filt= signal.medfilt(gaze_ang,41) ## Do median filtering to remove outliers
gz_err= [abs(m3-n3) for m3,n3 in zip(gz_filt,gaze_gt)]

################ Statistics calculations
##Mean
avg= np.mean(gz_err)
##95% confidence interval
conf= sms.DescrStatsW(gz_err).tconfint_mean(alpha=0.05)
### Interquartile range ###
qu4, ql4= np.percentile(gz_err, [75 ,25])
IQR= qu4-ql4
#Standard deviation
sd= np.std(gz_err)
#Median absolute deviation
ys= gz_err
median_y = np.median(ys)
median_absolute_deviation_y = np.median([np.abs(y - median_y) for y in ys])
#Zscore
zs= stats.zscore(gaze_ang)
### 1D KDE of gaze errors
xfit = np.linspace(0, 10, 1000) 
x1= np.array(gz_err)
X1 = x1[:, np.newaxis]
Xfit = xfit[:, np.newaxis]
kde1 = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X1) 
density1 = np.exp(kde1.score_samples(Xfit))

###################### Print values ###########################################

print "Mean error", avg
print "95% Confidence Interval", conf
print "Interquartile range", IQR
print "Standard deviation", sd
print "Median_absolute_deviation", median_absolute_deviation_y
###################### Plots ##################################################
fig1 = plt.figure(1)
plt.title('Gaze error distribution')
plt.xlabel('Gaze error (degrees)')
plt.ylabel('Probability')
plt.xlim(0,10)
plt.plot(xfit, density1, color='r', alpha=0.9, linewidth=2)
plt.grid()

fig2 = plt.figure(2)
plt.title('Zscore of gaze error values')
plt.xlabel('Time in ms')
plt.ylabel('Zscore')
plt.xlim(0,max(tim_rel))
plt.plot(tim_rel,zs)
plt.grid()