# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:14:22 2019

@author: Anuradha Kar
"""
###### data_similarity.py ################
## This program calculates similarity between data from different gaze datasets
## The similarity calculation is based on correlation, intersection
## and Bhattacharya distance computed on histograms of two gaze datasets
## For implementation, the CSV file named user_data_proc.csv is used
##Opencv 2 for Python is needed for implemenetation of this code

############################################# 
import matplotlib.pyplot as plt
import csv
import numpy as np
import cv2
from scipy import signal



gaze_ang=[]
yaw_ang=[]
with open('C:/Users/Documents/Python Scripts/user_data_proc.csv','r') as csvfile:   
    datavals = csv.reader(csvfile, delimiter=',')
    datavals.next()
    for r1 in datavals:
        gaze_ang.append(float(r1[14]))  #Load gaze angle data
        yaw_ang.append(float(r1[10]))   #Load yaw angle data
        

####################### Filter values ##############################
gaze_ang= signal.medfilt(gaze_ang,41) 
yaw_ang= signal.medfilt(yaw_ang,41) 

####################### Plot histograms ############################
f1 = plt.figure(1)
bins = np.linspace(0, 10, 40)  #=[0, 1, 2, 3, 4, 5, 10]
plt.hist(gaze_ang, bins=10, label='gaze_angle', color='r')  #histogram of errors at dist= 45
plt.hist(yaw_ang, bins, label='yaw_angle', color='b')
plt.legend()
plt.grid(True)
plt.show()

##################### Estimate similarity measures from histograms ############
hist1, bins= np.histogram(gaze_ang, bins, normed=1,weights=None )#, color='r', alpha=0.4, label='45 cm')
hist2, bins= np.histogram(yaw_ang, bins, normed=1,weights=None)#, color='g', alpha=0.4, label='60 cm')

h1= np.float32(hist1)
h2= np.float32(hist2)

com1 = cv2.compareHist(h1,h1,cv2.cv.CV_COMP_INTERSECT ) ###Histogram intersection
com2 = cv2.compareHist(h2,h1,cv2.cv.CV_COMP_CORREL)     ###Histogram correlation
com3 = cv2.compareHist(h2,h1,cv2.cv.CV_COMP_BHATTACHARYYA) ##Bhattacharya distance
com4 =  cv2.compareHist(h2,h1,cv2.cv.CV_COMP_CHISQR)

print "Similarity results", com1, com2, com3, com4




