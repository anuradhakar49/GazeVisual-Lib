# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 17:10:51 2019

@author: Anuradha Kar
"""
###### data_augmentation.py ################
## This is the program to implement 7 different augmentation strategies on gaze data
## For implementation of the augmentation methods, the CSV file named user_data_proc.csv is used

#############################################

from pandas import Series
import matplotlib.pyplot as plt
import csv
import numpy as np
import math
import os, sys
from scipy.stats import gaussian_kde
import scipy.interpolate as sp
import matplotlib.cm as cmx
import matplotlib.colors as colors
import scipy.interpolate
from scipy.stats import norm
import matplotlib.mlab as mlab
import itertools
from scipy import stats
from scipy import signal
from scipy.interpolate import interp1d
from scipy.ndimage.interpolation import shift

gtx=[]
gty=[]
tim_rel=[]
gaze_gt=[]
gaze_inp=[]
dff=[]
gaze_ang=[]

with open('C:/Users/Documents/Python Scripts/user_data_proc.csv','r') as csvfile:   
    datavals = csv.reader(csvfile, delimiter=',')
    datavals.next()
    for r1 in datavals:
        tim_rel.append(float(r1[0]))
               
        gaze_ang.append(float(r1[14]))   #Load gaze angle data
        gaze_inp.append(float(r1[14]))
        gaze_gt.append(float(r1[13]))  #Load gaze ground truth angle

        
#### Outlier removal and error calculation
gz_filt= signal.medfilt(gaze_ang,41) ## Do median filtering to remove outliers
for n, i in enumerate(gz_filt):   ### Add thresholding to further remove outliers
    if i > 50:
        gz_filt[n] = np.median(gz_filt)
gz_err= [abs(m3-n3) for m3,n3 in zip(gz_filt,gaze_gt)]	# Filtered gaze error data
gz_err=gz_err[0:2510] # Converting gz_err to fixed array lengths
tim_rel= tim_rel[0:2510]
######## 1. Add Gaussian noise #############

g_noise= np.random.normal(0, 0.2, len(gz_err))
g_noise= g_noise 
data_aug1= gz_err+g_noise

########### 2. Add pink noise ###############################

def one_over_f(f, knee, alpha):
    desc = np.ones_like(f)
    desc[f<KNEE] = np.abs((f[f<KNEE]/KNEE)**(-alpha))
    desc[0] = 1
    return desc

white_noise_sigma =  0.2 

SFREQ = 2 #Hz
KNEE = 5 / 1e3 #Hz
ALPHA = .7
N = len(gz_err)

wn=np.random.normal(0.,white_noise_sigma*np.sqrt(SFREQ),N)

#shaping in freq domain
s = np.fft.rfft(wn)
f = np.fft.fftfreq(N, d=1./SFREQ)[:len(s)]
f[-1]=np.abs(f[-1])
fft_sim = s * one_over_f(f, KNEE, ALPHA)
T_sim = np.fft.irfft(fft_sim)  #pink noise data

pn= np.append(T_sim, min(T_sim))
pn= pn[0:2510]  #Size of noise array should be same as gaze data
data_aug2= gz_err+pn

#################### 3. Coarse interpolation ###################################################

interp = interp1d(tim_rel,gz_err, kind='cubic',bounds_error=False)
xnew = np.arange(0, 90612,36)#
xnew= xnew[0:2510] 
data_aug3 = interp(xnew)

############################### 4. Add white and pink noise to interpolated data ###################################
data_aug4 = data_aug3+ g_noise

data_aug5 = data_aug3+ pn

############################### 6. Implement cosine convolution ############################################
win = signal.hann(30)
data_aug6 = signal.convolve(gz_err, win, mode="full")/sum(win) #imp: crop data to length 2517

#################### 7.Implement time shift to data points ################################################################

val= np.mean(gz_filt[0:10])
xs = np.array(gz_filt)
ys= shift(xs, 10, cval=val)
data_aug7= [abs(m3-n3) for m3,n3 in zip(ys,gaze_gt)]

############################# Plot orginal and augmented data ###################################################

f1 = plt.figure(1)
plt.plot(tim_rel,gz_err)
plt.title("Original data")
plt.xlabel('time in ms')
plt.ylabel('Gaze angle in degrees')
plt.grid(True)

f2 = plt.figure(2)
plt.plot(tim_rel,data_aug1,'r')
plt.plot(tim_rel,gz_err,'b')
plt.title("Added White noise")
plt.xlabel('time in ms')
plt.ylabel('Gaze angle in degrees')
plt.grid(True)

f3 = plt.figure(3)
plt.plot(tim_rel,data_aug2,'r')
plt.plot(tim_rel,gz_err,'b')
plt.title("Added pink noise")
plt.xlabel('time in ms')
plt.ylabel('Gaze angle in degrees')
plt.grid(True)

f4 = plt.figure(4)
plt.title("Coarse interpolation")
plt.plot(xnew, data_aug3, 'r')
plt.plot(tim_rel,gz_err,'b')
plt.xlabel('time in ms')
plt.ylabel('Gaze angle in degrees')
plt.grid(True)

f5 = plt.figure(5)
plt.title("Combination-interpolation+white noise")
plt.plot(tim_rel,data_aug4,'r')
plt.plot(tim_rel,gz_err,'b')
plt.xlabel('time in ms')
plt.ylabel('Gaze angle in degrees')
plt.grid(True)

f6 = plt.figure(6)
plt.title("Combination-interpolation+pink noise")
plt.plot(tim_rel,data_aug5,'r')
plt.plot(tim_rel,gz_err,'b')
plt.xlabel('time in ms')
plt.ylabel('Gaze angle in degrees')
plt.grid(True)

f7 = plt.figure(7)
plt.title("Cosine convolution")
plt.plot(tim_rel,data_aug6[0:2510],'r')
plt.plot(tim_rel,gz_err,'b')
plt.xlabel('time in ms')
plt.ylabel('Gaze angle in degrees')
plt.grid(True)

f8 = plt.figure(8)
plt.title("Time shifting")
plt.plot(tim_rel, gz_err, 'b')
plt.plot(tim_rel,data_aug7, 'r')
plt.xlabel('time in ms')
plt.ylabel('Gaze angle in degrees')
plt.grid(True)

