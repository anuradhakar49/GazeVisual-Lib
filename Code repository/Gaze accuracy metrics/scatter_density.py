# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 17:05:42 2019

@author: 14233242
"""

###### scatter_density.py ################
## This program estimates the scatter density of gaze data over the display area
## For implementation the CSV file named user_data_proc.csv is used

###########################################
import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.stats import gaussian_kde


x=[]
y=[]
with open('C:/Users/14233242/Documents/Python Scripts/repo_codes/user_data_proc.csv','r') as csvfile:   
    datavals = csv.reader(csvfile, delimiter=',')
    datavals.next()
    for r1 in datavals:
        
        x.append(float(r1[3]))
        y.append(float(r1[4]))

################# Plotting ####################################################
g6 = plt.figure(1)
ax6 = g6.add_subplot(111)
xy = np.vstack([x,y])
z = gaussian_kde(xy)(xy)


plt.hist2d(x, y, (40, 40), cmap=plt.cm.jet)
plt.colorbar()
plt.tick_params(labelsize=10)
plt.title("Data density plot")
plt.xlabel('Gaze coordinates (X) in pixels',fontsize=12)
plt.ylabel('Gaze coordinates (Y) in pixels',fontsize=12)
plt.tick_params(labelsize=16)
plt.show()

