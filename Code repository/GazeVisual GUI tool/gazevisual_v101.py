# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 04:29:29 2018

@author: Anuradha Kar
"""

# -*- coding: utf-8 -*-
"""
GazeVisual GUI software for eye tracker data analysis and visualization

@author: Anuradha Kar,2018
"""
################## gazevisual_v101.py #########################################
## This is the source code of the GazeVisual GUI application
## This code is released under GNU General Public License v3.0
## The LiveTracking function is commented. Uncomment only if you have an Eyetribe eye tracker
## and if you want to use it with this software by connecting the tracker to your computer.
## This software runs with Python 2.7 and all the imported libraries should be installed.
## Please also download and the png image files (in GitHub folder)in the same folder as this code
#######################################
import Tkinter as tk  
from Tkinter import *
import time
import numpy as np
matplotlib.use("TkAgg")
import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import ttk
import Tkinter, Tkconstants, tkFileDialog
import pandas as pd
import csv
import math
import statsmodels.stats.api as sms
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate
from matplotlib import cm
from sklearn.neighbors import KernelDensity
from scipy import stats
#import pygame
#import pytribe
import threading
import Queue
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
#########global variables #######


global diff_gz
global yaw_data
global pitch_data
global gaze_gt
global gaze_ang

x_data=[]
y_data=[]
gtx_mm=[] 
gty_mm=[]
diff_gz=[]
yaw_data=[]
pitch_data=[]
gaze_gt=[]
gaze_ang=[]

res_x = 1680
res_y= 1050
mmpix = 0.28 
  
  
t = Tk()
t.title('GazeVisual')
t.geometry('1010x700')


 
class GUI():
    
    
                
    def __init__(self, r):
        self.r = r
        
        def close_window ():   
            t.destroy()
        
        def load_data_new():
            global x_data
            global y_data 
            global tim_rel
            global z_data
            global gt_z
            global us_dis
            global us_name
            global gtx_mm 
            global gty_mm
            global get_ang
            global gtt_ang
            global diff_gz
            global us_id
            
            gzm_file= tkFileDialog.askopenfilename(initialdir = "C:/Users/14233242/Documents/Python Scripts",title = "Select file",filetypes = [("CSV files","*.csv")])

            df= pd.read_csv(gzm_file)
            
            gz_x = df["Gaze X"].tolist() # gaze x
            gz_y = df["Gaze Y"].tolist() #gaze y
            gtx= df["Gnd tr X"].tolist()  #ground truth x
            gty= df["Gnd tr Y"].tolist()  #ground truth y
            tim_st= df["Timestamp"].tolist()
            st= df["Timestamp"].iloc[0] 
            
            resx= df["Res X"].iloc[0] 
            resy= df["Res Y"].iloc[0]
            mmpix= df["Mmpix"].iloc[0]
            us_dis=df["User Dis"].iloc[0]
            us_id = df["UID"].iloc[0]
            #print df 
            tim_rel= [(l - st)/1000.0 for l in tim_st]
            gtx_mm = [a * mmpix for a in gtx]
            gty_mm=  [b * mmpix for b in gty]
            x_data = [a1 * mmpix for a1 in gz_x]  #in mm
            y_data=  [b1 * mmpix for b1 in gz_y]
            gt_z=np.empty(len(x_data))  
            gt_z.fill(us_dis)
            z_data= gt_z
            #### gaze angle calculation
            dx_sq =[q**2 for q in x_data]	
            dy_sq= [q1**2 for q1 in y_data] 
            mean_z = z_data  #culprit
            
            z_sq = [q2**2 for q2 in mean_z] 
            sum1 = np.array(dx_sq)+np.array(dy_sq)+np.array(z_sq)
            egp = [np.sqrt(q3) for q3 in sum1] 
            #Eye to eye tracker distance
            monitor_h= (resy/2)*mmpix
            x_sq = [q3**2 for q3 in x_data]
            y_1 = [q4+monitor_h for q4 in y_data]  ##### monitor dimensions used in calculating. 147 = (1050/2 ) 0.28 (res/2)*mmperpix
            y_sq = [q5**2 for q5 in y_1]
            sum2= np.array(x_sq)+np.array(y_sq)+np.array(z_sq)
            eet = [np.sqrt(q6) for q6 in sum2] 
            ##Gaze point to eye tracker distance			
            gzx_sq= [q7**2 for q7 in x_data]
            y_2 = [q8+monitor_h for q8 in y_data] 
            gzy_sq= [q9**2 for q9 in y_2]
            sum3= np.array(gzx_sq)+np.array(gzy_sq)
            g_et =[abs(np.sqrt(q10)) for q10 in sum3]
            ########################################
            prod= [2*m10*n10 for m10,n10 in zip(egp,eet)] 
            #prod1= [q11*2 for q11 in prod]
            b92_sq= [q12**2 for q12 in egp]
            b95_sq= [q13**2 for q13 in eet]
            b98_sq= [q14**2 for q14 in g_et]
            sum4= np.array(b92_sq)+np.array(b95_sq)-np.array(b98_sq)
            div = [ai/bi for ai,bi in zip(sum4,prod)]
            for i in xrange(len(div)):
                if div[i] > 1:
                    div[i] = 0.99999999999999999   ##cos exception
                    
            get_ang =[math.degrees(math.acos(q15)) for q15 in div]
            ############ ground truth #################
            gx_sq= [c1**2 for c1 in gtx_mm]
            gy_sq= [c2**2 for c2 in gty_mm]
            gz_sq = [c3**2 for c3 in gt_z]
            sum5 = np.array(gx_sq)+np.array(gy_sq)+np.array(gz_sq)
            gt_et = [abs(np.sqrt(c4)) for c4 in sum5]
            # eye to eye tracker distance
            ge_et = np.empty(len(gtx_mm)) 
            c5 = ((resy/2.0)* mmpix)**2
            c6 = (us_dis)**2
            sum6 = math.sqrt(c5+c6)
            ge_et.fill(sum6)
            ##Gaze point to eye tracker distance
            c7= ((resy/2.0)* mmpix)
            sum7 = [(c8+c7)**2 for c8 in gty_mm]
            sum8 = np.array(gx_sq)+np.array(sum7)
            ggp_et = [abs(np.sqrt(c9)) for c9 in sum8]
            ##Gaze angle relative to eye tracker
            sq1= [d1**2 for d1 in gt_et]
            sq2 = [d2**2 for d2 in ge_et]
            sq3= [d3**2 for d3 in ggp_et]
            sum9 = np.array(sq1)+np.array(sq2)- np.array(sq3)
            prod3= [2*m1*n1 for m1,n1 in zip(gt_et,ge_et)] 
            div2= [m2/n2 for m2,n2 in zip(sum9,prod3)] 
            gtt_ang =[math.degrees(math.acos(q16)) for q16 in div2]
            
            ############## error#
            diff_gz=[abs(m3-n3) for m3,n3 in zip(get_ang,gtt_ang)]

            
             ##################### plots ######################
            fs = Figure(figsize=(5.5,3.7), dpi=100)      
            fs.subplots_adjust(wspace = 0.4)
            self.canvas_s = FigureCanvasTkAgg(fs, page2)
            self.canvas_s.show()
        
            fs.add_subplot(111).scatter(x_data,y_data, color='black')
            fs.add_subplot(111).plot(gtx_mm,gty_mm,'b')
        
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).set_xlabel('Gaze X data vs GT X(mm)',size=8)
            fs.add_subplot(111).set_ylabel('Gaze Y data vs GT Y (mm)',size=8)
            fs.add_subplot(111).set_title('gaze vs ground truth scatter', size=10)
            fs.add_subplot(111).grid()
                        
            self.toolbar_frame2 = Frame(page2) 
            self.toolbar_frame2.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar_s = NavigationToolbar2TkAgg( self.canvas_s, self.toolbar_frame2 )
            self.canvas_s._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            
            
            us_det= "\nUser name: "+ us_id 
            us_det1= "\nUser distance: "+ str(us_dis) + "mm"
            self.T21.delete(1.0, END) 
            self.T21.insert(END,  "Uploaded gaze dataset")
            self.T21.insert(END,  us_det)
            self.T21.insert(END,  us_det1)
            self.T21.insert(END,  "\nGaze vs ground truth data scatter plotted")
   
        def zscore():
            zs= stats.zscore(get_ang)
            f2 = Figure(figsize=(5.5,3.7), dpi=100)      
            f2.subplots_adjust(wspace = 0.4)
            self.canvas2 = FigureCanvasTkAgg(f2, page2)
            self.canvas2.show()
            

            
            f2.add_subplot(121).plot(tim_rel,zs)
            
            f2.add_subplot(121).set_xticks(np.arange(0.0, 91.0, 30.0))
            f2.add_subplot(121).xaxis.set_tick_params(labelsize=8)
            f2.add_subplot(121).yaxis.set_tick_params(labelsize=8)
            f2.add_subplot(121).set_xlabel('Time (sec)',size=8)
            f2.add_subplot(121).set_ylabel('Zscore',size=8)
            f2.add_subplot(121).set_title('Zscore vs time', size=12)
            f2.add_subplot(121).grid()
            
            
            f2.add_subplot(122).plot(tim_rel,gtt_ang)
            
            f2.add_subplot(122).set_xticks(np.arange(0.0, 91.0, 30.0))
            f2.add_subplot(122).xaxis.set_tick_params(labelsize=8)
            f2.add_subplot(122).yaxis.set_tick_params(labelsize=8)
            f2.add_subplot(122).set_xlabel('Time(sec)',size=8)
            f2.add_subplot(122).set_ylabel('Gaze angle(degrees)',size=8)
            f2.add_subplot(122).set_title('Gaze angle vs time', size=12)
            f2.add_subplot(122).grid()
            
            
            self.toolbar_frame2 = Frame(page2) 
            self.toolbar_frame2.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar2 = NavigationToolbar2TkAgg( self.canvas2, self.toolbar_frame2 )
            self.canvas2._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            
            self.T21.delete(1.0, END) 
            self.T21.insert(END,  "Displaying gaze angle Zscore values and ground truth data")
     
            ###############################################################################
    
        def accu_met():

            mean_err = abs(sum(diff_gz)/len(diff_gz))
            conf= sms.DescrStatsW(diff_gz).tconfint_mean(alpha=0.05)
            us_det= "\nUser name: "+ us_id 
            us_det1= "\nUser distance: "+ str(us_dis) + "mm"
            g_ang= "\nMax gaze angle(degrees): "+ str(round(max(get_ang),2))
            max_err= "\nMax gaze error(degrees): "+ str(round(abs(max(diff_gz)),2))
            min_err= "\nMin gaze error(degrees): "+str(round(abs(min(diff_gz)),2))
            mean_val= "\nMean gaze error(degrees): "+str(round(mean_err,2))
            std_1= "\nError standard deviation: "+str(round(np.std(diff_gz),2))
            conf_1 = "\nError 95% Confidence interval: "+ str(conf)#str(round(conf,2))
            ##################### plots ######################
            fs = Figure(figsize=(5.5,3.7), dpi=100)      
            fs.subplots_adjust(wspace = 0.4)
            self.canvas_s = FigureCanvasTkAgg(fs, page2)
            self.canvas_s.show()
            
          
            #fs.add_subplot(111).plot(tim_rel,get_ang,'g')
            fs.add_subplot(111).plot(tim_rel,diff_gz, 'b')
            fs.add_subplot(111).set_xticks(np.arange(0.0, 91.0, 30.0))
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).set_xlabel('Time (sec)',size=8)
            fs.add_subplot(111).set_ylabel('Gaze error (degrees)',size=8)
            fs.add_subplot(111).set_title('Gaze error vs time', size=10)
            fs.add_subplot(111).grid()                       
            
            self.toolbar_frame2 = Frame(page2) 
            self.toolbar_frame2.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar_s = NavigationToolbar2TkAgg( self.canvas_s, self.toolbar_frame2 )
            self.canvas_s._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            
            self.T21.delete(1.0, END) 
            self.T21.insert(END,  "Displaying gaze data accuracy and statistics")
            self.T21.insert(END,  us_det)
            self.T21.insert(END,  us_det1)
            self.T21.insert(END,  g_ang) 
            self.T21.insert(END,  max_err)
            self.T21.insert(END,  min_err) 
            self.T21.insert(END,  mean_val)
            self.T21.insert(END,  std_1) 
            self.T21.insert(END,  conf_1)

        #t.destroy()
        def yawpitch():
            yaw_gt = [math.degrees(math.atan(i/ us_dis)) for i in gtx_mm]
            pitch_gt = [math.degrees(math.atan(m/ us_dis)) for m in gty_mm]
            yaw_data = [math.degrees(math.atan(k/ us_dis)) for k in x_data]
            pitch_data = [math.degrees(math.atan(p/ us_dis)) for p in y_data]
            diff_yaw = np.array(yaw_gt)-np.array(yaw_data)
            diff_pitch = np.array(pitch_gt)-np.array(pitch_data)
            max_yaw= "Max yaw value(degrees): "+ str(round(max(yaw_data),2))
            min_yaw= "\nMin yaw value(degrees): "+str(round(min(yaw_data),2))
            
            max_pitch= "\nMax pitch value (degrees): "+str(round(max(pitch_data),2))
            min_pitch= "\nMin pitch value (degrees): "+str(round(min(pitch_data),2))
            mn_eyaw= sum(abs(diff_yaw))/len(diff_yaw)
            mn_epit= sum(abs(diff_pitch))/len(diff_pitch)
            mean_eyaw= "\nMean yaw error (degrees): "+ str(round(mn_eyaw,2))
            mean_epit= "\nMean pitch error (degrees): "+ str(round(mn_epit,2))
            
            us_det= "User name: "+ us_id+ "\n"
            us_det1= "User distance: "+ str(us_dis) + "mm\n"
            
            f2 = Figure(figsize=(5.5,3.7), dpi=100)      
            f2.subplots_adjust(wspace = 0.4)
            self.canvas2 = FigureCanvasTkAgg(f2, page2)
            self.canvas2.show()
            

            
            f2.add_subplot(121).plot(tim_rel,yaw_gt)
            f2.add_subplot(121).plot(tim_rel,yaw_data)
            f2.add_subplot(121).set_xticks(np.arange(0.0, 91.0, 30.0))
            f2.add_subplot(121).xaxis.set_tick_params(labelsize=8)
            f2.add_subplot(121).yaxis.set_tick_params(labelsize=8)
            f2.add_subplot(121).set_xlabel('Time (sec)',size=8)
            f2.add_subplot(121).set_ylabel('Yaw angle (degrees)',size=8)
            f2.add_subplot(121).set_title('Gaze yaw vs time', size=12)
            f2.add_subplot(121).grid()
            
            
            f2.add_subplot(122).plot(tim_rel,pitch_gt)
            f2.add_subplot(122).plot(tim_rel,pitch_data)
            f2.add_subplot(122).set_xticks(np.arange(0.0, 91.0, 30.0))
            f2.add_subplot(122).xaxis.set_tick_params(labelsize=8)
            f2.add_subplot(122).yaxis.set_tick_params(labelsize=8)
            f2.add_subplot(122).set_xlabel('Time(sec)',size=8)
            f2.add_subplot(122).set_ylabel('Pitch Angle(degrees)',size=8)
            f2.add_subplot(122).set_title('Gaze pitch vs time', size=12)
            f2.add_subplot(122).grid()
            
            
            self.toolbar_frame2 = Frame(page2) 
            self.toolbar_frame2.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar2 = NavigationToolbar2TkAgg( self.canvas2, self.toolbar_frame2 )
            self.canvas2._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
         
            self.T21.delete(1.0, END) 
            self.T21.insert(END,  us_det)
            self.T21.insert(END,  us_det1)
            self.T21.insert(END,  max_yaw) 
            self.T21.insert(END,  min_yaw)
            self.T21.insert(END,  max_pitch) 
            self.T21.insert(END,  min_pitch)
            self.T21.insert(END,  mean_eyaw) 
            self.T21.insert(END,  mean_epit)
#######################################################################

        def upload_d1():   
            
            global x_d1
            global y_d1
            global tim_rel_d1
            global z_data_d1
            global gt_z_d1
            global us_dis_d1
            global us_id_d1
            global get_ang_d1
            global gtt_ang_d1
            global diff_gz_d1
            global dev1
            
            gzm_file= tkFileDialog.askopenfilename(initialdir = "C:/Users/14233242/Documents/Python Scripts",title = "Select file",filetypes = [("CSV files","*.csv")])

            df= pd.read_csv(gzm_file)
            
            gz_x = df["Gaze X"].tolist() # gaze x
            gz_y = df["Gaze Y"].tolist() #gaze y
            gtx= df["Gnd tr X"].tolist()  #ground truth x
            gty= df["Gnd tr Y"].tolist()  #ground truth y
            tim_st= df["Timestamp"].tolist()
            st= df["Timestamp"].iloc[0] 
            
            resx= df["Res X"].iloc[0] 
            resy= df["Res Y"].iloc[0]
            mmpix= df["Mmpix"].iloc[0]
            us_dis_d1=df["User Dis"].iloc[0]
            us_id_d1 = df["UID"].iloc[0]
            #print df 
            tim_rel_d1= [(l - st)/1000.0 for l in tim_st]
            gtx_mm = [a * mmpix for a in gtx]
            gty_mm=  [b * mmpix for b in gty]
            x_data = [a1 * mmpix for a1 in gz_x]  #in mm
            y_data=  [b1 * mmpix for b1 in gz_y]
            gt_z=np.empty(len(x_data))  
            gt_z.fill(us_dis_d1)
            z_data= gt_z
            z_data_d1=z_data
            #### gaze angle calculation
            dx_sq =[q**2 for q in x_data]	
            dy_sq= [q1**2 for q1 in y_data] 
            mean_z = z_data  #culprit
            
            z_sq = [q2**2 for q2 in mean_z] 
            sum1 = np.array(dx_sq)+np.array(dy_sq)+np.array(z_sq)
            egp = [np.sqrt(q3) for q3 in sum1] 
            #Eye to eye tracker distance
            monitor_h= (resy/2)*mmpix
            x_sq = [q3**2 for q3 in x_data]
            y_1 = [q4+monitor_h for q4 in y_data]  ##### monitor dimensions used in calculating. 147 = (1050/2 ) 0.28 (res/2)*mmperpix
            y_sq = [q5**2 for q5 in y_1]
            sum2= np.array(x_sq)+np.array(y_sq)+np.array(z_sq)
            eet = [np.sqrt(q6) for q6 in sum2] 
            ##Gaze point to eye tracker distance			
            gzx_sq= [q7**2 for q7 in x_data]
            y_2 = [q8+monitor_h for q8 in y_data] 
            gzy_sq= [q9**2 for q9 in y_2]
            sum3= np.array(gzx_sq)+np.array(gzy_sq)
            g_et =[abs(np.sqrt(q10)) for q10 in sum3]
            ########################################
            prod= [2*m10*n10 for m10,n10 in zip(egp,eet)] 
            #prod1= [q11*2 for q11 in prod]
            b92_sq= [q12**2 for q12 in egp]
            b95_sq= [q13**2 for q13 in eet]
            b98_sq= [q14**2 for q14 in g_et]
            sum4= np.array(b92_sq)+np.array(b95_sq)-np.array(b98_sq)
            div = [ai/bi for ai,bi in zip(sum4,prod)]
            for i in xrange(len(div)):
                if div[i] > 1:
                    div[i] = 0.99999999999999999   ##cos exception
                    
            get_ang_d1 =[math.degrees(math.acos(q15)) for q15 in div]
            ############ ground truth #################
            gx_sq= [c1**2 for c1 in gtx_mm]
            gy_sq= [c2**2 for c2 in gty_mm]
            gz_sq = [c3**2 for c3 in gt_z]
            sum5 = np.array(gx_sq)+np.array(gy_sq)+np.array(gz_sq)
            gt_et = [abs(np.sqrt(c4)) for c4 in sum5]
            # eye to eye tracker distance
            ge_et = np.empty(len(gtx_mm)) 
            c5 = ((resy/2.0)* mmpix)**2
            c6 = (us_dis_d1)**2
            sum6 = math.sqrt(c5+c6)
            ge_et.fill(sum6)
            ##Gaze point to eye tracker distance
            c7= ((resy/2.0)* mmpix)
            sum7 = [(c8+c7)**2 for c8 in gty_mm]
            sum8 = np.array(gx_sq)+np.array(sum7)
            ggp_et = [abs(np.sqrt(c9)) for c9 in sum8]
            ##Gaze angle relative to eye tracker
            sq1= [d1**2 for d1 in gt_et]
            sq2 = [d2**2 for d2 in ge_et]
            sq3= [d3**2 for d3 in ggp_et]
            sum9 = np.array(sq1)+np.array(sq2)- np.array(sq3)
            prod3= [2*m1*n1 for m1,n1 in zip(gt_et,ge_et)] 
            div2= [m2/n2 for m2,n2 in zip(sum9,prod3)] 
            gtt_ang_d1 =[math.degrees(math.acos(q16)) for q16 in div2]
            
            ############## error#
            diff_gz_d1=[abs(m3-n3) for m3,n3 in zip(get_ang_d1,gtt_ang_d1)]
             ##################### plots ######################
            fs = Figure(figsize=(5.5,3.7), dpi=100)      
            fs.subplots_adjust(wspace = 0.4)
            self.canvas_s = FigureCanvasTkAgg(fs, page2)
            self.canvas_s.show()
        
            fs.add_subplot(111).scatter(x_data,y_data, color='black')
            fs.add_subplot(111).plot(gtx_mm,gty_mm,'b')
            #fs.add_subplot(122).set_xticks(np.arange(0.0, 91.0, 30.0))
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).set_xlabel('Gaze X data vs GT X(mm)',size=8)
            fs.add_subplot(111).set_ylabel('Gaze Y data vs GT Y (mm)',size=8)
            fs.add_subplot(111).set_title('gaze vs ground truth scatter', size=10)
            fs.add_subplot(111).grid()
                        
            self.toolbar_frame2 = Frame(page2) 
            self.toolbar_frame2.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar_s = NavigationToolbar2TkAgg( self.canvas_s, self.toolbar_frame2 )
            self.canvas_s._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            
            
            us_det= "\nUser/Experiment ID: "+ us_id_d1
            us_det1= "\nUser distance: "+ str(us_dis_d1) + "mm"
            self.T21.delete(1.0, END) 
            self.T21.insert(END,  "Uploaded gaze dataset 1")
            self.T21.insert(END,  us_det)
            self.T21.insert(END,  us_det1)
            self.T21.insert(END,  "\nGaze vs ground truth data (Data-1) plotted")

#########################################################################################
        def upload_d2():   
            
            global x_d1
            global y_d1
            global tim_rel_d2
            global z_data_d2
            global gt_z_d2
            global us_dis_d2
            global us_id_d2
            global get_ang_d2
            global gtt_ang_d2
            global diff_gz_d2
            global dev1
            
            gzm_file= tkFileDialog.askopenfilename(initialdir = "C:/Users/14233242/Documents/Python Scripts",title = "Select file",filetypes = [("CSV files","*.csv")])
#            if gzm_file is None: # askopenfile return `None` if dialog closed with "cancel".
#                return
            df= pd.read_csv(gzm_file)
            
            gz_x = df["Gaze X"].tolist() # gaze x
            gz_y = df["Gaze Y"].tolist() #gaze y
            gtx= df["Gnd tr X"].tolist()  #ground truth x
            gty= df["Gnd tr Y"].tolist()  #ground truth y
            tim_st= df["Timestamp"].tolist()
            st= df["Timestamp"].iloc[0] 
            
            resx= df["Res X"].iloc[0] 
            resy= df["Res Y"].iloc[0]
            mmpix= df["Mmpix"].iloc[0]
            us_dis_d2=df["User Dis"].iloc[0]
            us_id_d2 = df["UID"].iloc[0]
            #print df 
            tim_rel_d2= [(l - st)/1000.0 for l in tim_st]
            gtx_mm = [a * mmpix for a in gtx]
            gty_mm=  [b * mmpix for b in gty]
            x_data = [a1 * mmpix for a1 in gz_x]  #in mm
            y_data=  [b1 * mmpix for b1 in gz_y]
            gt_z=np.empty(len(x_data))  
            gt_z.fill(us_dis_d2)
            z_data= gt_z
            z_data_d2= z_data
            #### gaze angle calculation
            dx_sq =[q**2 for q in x_data]	
            dy_sq= [q1**2 for q1 in y_data] 
            mean_z = z_data  #culprit
            
            z_sq = [q2**2 for q2 in mean_z] 
            sum1 = np.array(dx_sq)+np.array(dy_sq)+np.array(z_sq)
            egp = [np.sqrt(q3) for q3 in sum1] 
            #Eye to eye tracker distance
            monitor_h= (resy/2)*mmpix
            x_sq = [q3**2 for q3 in x_data]
            y_1 = [q4+monitor_h for q4 in y_data]  ##### monitor dimensions used in calculating. 147 = (1050/2 ) 0.28 (res/2)*mmperpix
            y_sq = [q5**2 for q5 in y_1]
            sum2= np.array(x_sq)+np.array(y_sq)+np.array(z_sq)
            eet = [np.sqrt(q6) for q6 in sum2] 
            ##Gaze point to eye tracker distance			
            gzx_sq= [q7**2 for q7 in x_data]
            y_2 = [q8+monitor_h for q8 in y_data] 
            gzy_sq= [q9**2 for q9 in y_2]
            sum3= np.array(gzx_sq)+np.array(gzy_sq)
            g_et =[abs(np.sqrt(q10)) for q10 in sum3]
            ########################################
            prod= [2*m10*n10 for m10,n10 in zip(egp,eet)] 
            #prod1= [q11*2 for q11 in prod]
            b92_sq= [q12**2 for q12 in egp]
            b95_sq= [q13**2 for q13 in eet]
            b98_sq= [q14**2 for q14 in g_et]
            sum4= np.array(b92_sq)+np.array(b95_sq)-np.array(b98_sq)
            div = [ai/bi for ai,bi in zip(sum4,prod)]
            for i in xrange(len(div)):
                if div[i] > 1:
                    div[i] = 0.99999999999999999   ##cos exception
                    
            get_ang_d2 =[math.degrees(math.acos(q15)) for q15 in div]
            ############ ground truth #################
            gx_sq= [c1**2 for c1 in gtx_mm]
            gy_sq= [c2**2 for c2 in gty_mm]
            gz_sq = [c3**2 for c3 in gt_z]
            sum5 = np.array(gx_sq)+np.array(gy_sq)+np.array(gz_sq)
            gt_et = [abs(np.sqrt(c4)) for c4 in sum5]
            # eye to eye tracker distance
            ge_et = np.empty(len(gtx_mm)) 
            c5 = ((resy/2.0)* mmpix)**2
            c6 = (us_dis_d2)**2
            sum6 = math.sqrt(c5+c6)
            ge_et.fill(sum6)
            ##Gaze point to eye tracker distance
            c7= ((resy/2.0)* mmpix)
            sum7 = [(c8+c7)**2 for c8 in gty_mm]
            sum8 = np.array(gx_sq)+np.array(sum7)
            ggp_et = [abs(np.sqrt(c9)) for c9 in sum8]
            ##Gaze angle relative to eye tracker
            sq1= [d1**2 for d1 in gt_et]
            sq2 = [d2**2 for d2 in ge_et]
            sq3= [d3**2 for d3 in ggp_et]
            sum9 = np.array(sq1)+np.array(sq2)- np.array(sq3)
            prod3= [2*m1*n1 for m1,n1 in zip(gt_et,ge_et)] 
            div2= [m2/n2 for m2,n2 in zip(sum9,prod3)] 
            gtt_ang_d2 =[math.degrees(math.acos(q16)) for q16 in div2]
            
            ############## error#
            diff_gz_d2=[abs(m3-n3) for m3,n3 in zip(get_ang_d2,gtt_ang_d2)]
             ##################### plots ######################
            fs = Figure(figsize=(5.5,3.7), dpi=100)      
            fs.subplots_adjust(wspace = 0.4)
            self.canvas_s = FigureCanvasTkAgg(fs, page2)
            self.canvas_s.show()
        
            fs.add_subplot(111).scatter(x_data,y_data, color='black')
            fs.add_subplot(111).plot(gtx_mm,gty_mm,'b')
            #fs.add_subplot(122).set_xticks(np.arange(0.0, 91.0, 30.0))
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).set_xlabel('Gaze X data vs GT X(mm)',size=8)
            fs.add_subplot(111).set_ylabel('Gaze Y data vs GT Y (mm)',size=8)
            fs.add_subplot(111).set_title('gaze vs ground truth scatter', size=10)
            fs.add_subplot(111).grid()
                        
            self.toolbar_frame2 = Frame(page2) 
            self.toolbar_frame2.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar_s = NavigationToolbar2TkAgg( self.canvas_s, self.toolbar_frame2 )
            self.canvas_s._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            
            
            us_det= "\nUser/Experiment ID: "+ us_id_d2
            us_det1= "\nUser distance: "+ str(us_dis_d2) + "mm"
            self.T21.delete(1.0, END) 
            self.T21.insert(END,  "Uploaded gaze dataset 2")
            self.T21.insert(END,  us_det)
            self.T21.insert(END,  us_det1)
            self.T21.insert(END,  "\nGaze vs ground truth data (Data-2) plotted")  

 
          
            
           
        def compare_data():
            self.T21.delete(1.0, END) 
            fs = Figure(figsize=(5.4,3.7), dpi=100)      
            fs.subplots_adjust(wspace = 0.4)
            self.canvas_s = FigureCanvasTkAgg(fs, page2)

            max_d1= str(round(max(diff_gz_d1),2))
            max_d2= str(round(max(diff_gz_d2),2))
            avg_d1= str(round(np.mean(diff_gz_d1),2))
            avg_d2= str(round(np.mean(diff_gz_d2),2))
            std_d1= str(round(np.std(diff_gz_d1),2))
            std_d2= str(round(np.std(diff_gz_d2),2))
            gz_d1= str(round(max(get_ang_d1),2))
            gz_d2= str(round(max(get_ang_d2),2))
            us_d1= str(round(us_dis_d1,2))
            us_d2= str(round(us_dis_d2,2))
            col_labels = ['Dataset 1', 'Dataset 2']
            row_labels = [' User distance(mm)',' Max Error (deg)', ' Mean Error (deg)',' Error stdev',' Max Gaze angle (deg)']
            table_vals = [[us_d1, us_d2], [max_d1,max_d2],[avg_d1,avg_d2],[std_d1,std_d2],[gz_d1, gz_d2]]
            
            the_table = fs.add_subplot(111).table(cellText=table_vals,
                                  colWidths=[0.1] * 3,
                                  rowLabels=row_labels,
                                  colLabels=col_labels,loc='center right')
            the_table.auto_set_font_size(False)                      
            the_table.set_fontsize(10)
            the_table.scale(3,3)
            self.canvas_s.show()
            self.toolbar_frame2 = Frame(page2) 
            self.toolbar_frame2.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar_s = NavigationToolbar2TkAgg( self.canvas_s, self.toolbar_frame2 )
            self.canvas_s._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            fs.add_subplot(111).set_title('Comparison of two datasets')
            fs.add_subplot(111).xaxis.set_tick_params(bottom=False, top=False, labelbottom=False)
            fs.add_subplot(111).yaxis.set_tick_params(bottom=False, top=False, labelbottom=False)
            us1= "\nUser name for dataset1: "+ us_id_d1
            us2= "\nUser name for dataset2: "+ us_id_d2
            self.T21.insert(END,  "Comparison of two datasets Data-1 and Data-2")
            self.T21.insert(END,  us1)
            self.T21.insert(END,  us2)
         
        def gaze_angles():

            f2 = Figure(figsize=(5.5,3.7), dpi=100)      
            f2.subplots_adjust(wspace = 0.4)
            self.canvas2 = FigureCanvasTkAgg(f2, page2)
            self.canvas2.show()
            


            
            f2.add_subplot(121).plot(tim_rel_d1,get_ang_d1)
            f2.add_subplot(121).plot(tim_rel_d1,gtt_ang_d1)
            f2.add_subplot(121).set_xticks(np.arange(0.0, 91.0, 30.0))
            f2.add_subplot(121).xaxis.set_tick_params(labelsize=8)
            f2.add_subplot(121).yaxis.set_tick_params(labelsize=8)
            f2.add_subplot(121).set_xlabel('Time (sec)',size=8)
            f2.add_subplot(121).set_ylabel('Gaze angle (degrees)',size=8)
            f2.add_subplot(121).set_title('Gaze angles Data-1', size=12)
            f2.add_subplot(121).grid()
            
            
            f2.add_subplot(122).plot(tim_rel_d2, get_ang_d2)
            f2.add_subplot(122).plot(tim_rel_d2,gtt_ang_d2)
            f2.add_subplot(122).set_xticks(np.arange(0.0, 91.0, 30.0))
            f2.add_subplot(122).xaxis.set_tick_params(labelsize=8)
            f2.add_subplot(122).yaxis.set_tick_params(labelsize=8)
            f2.add_subplot(122).set_xlabel('Time(sec)',size=8)
            f2.add_subplot(122).set_ylabel('Gaze Angle(degrees)',size=8)
            f2.add_subplot(122).set_title('Gaze angles Data-2', size=12)
            f2.add_subplot(122).grid()
            
            
            self.toolbar_frame2 = Frame(page2) 
            self.toolbar_frame2.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar2 = NavigationToolbar2TkAgg( self.canvas2, self.toolbar_frame2 )
            self.canvas2._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
           
            self.T21.delete(1.0, END) 
            self.T21.insert(END,  "Gaze angles from two datasets vs ground truth")
            
        def kde_compare():
            
            xfit = np.linspace(0, 10, 1000) 
            x1= np.array(diff_gz_d1)
            x2= np.array(diff_gz_d2)
            
            X1 = x1[:, np.newaxis]
            X2 = x2[:, np.newaxis]
            Xfit = xfit[:, np.newaxis]
            
            kde1 = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X1) 
            kde2 = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X2) 
            density1 = np.exp(kde1.score_samples(Xfit))
            density2 = np.exp(kde2.score_samples(Xfit))
            

            f2 = Figure(figsize=(5.5,3.7), dpi=100)      
            f2.subplots_adjust(wspace = 0.4)
            self.canvas2 = FigureCanvasTkAgg(f2, page2)
            self.canvas2.show()
            

            
            f2.add_subplot(121).plot(xfit, density1)
            
            f2.add_subplot(121).set_xticks(np.arange(0.0,10.0, 1.0))
            f2.add_subplot(121).xaxis.set_tick_params(labelsize=8)
            f2.add_subplot(121).yaxis.set_tick_params(labelsize=8)
            f2.add_subplot(121).set_xlabel('Gaze error values (deg)',size=8)
            f2.add_subplot(121).set_ylabel('Density',size=8)
            f2.add_subplot(121).set_title('KDE of gaze errors: Data-1', size=10)
            f2.add_subplot(121).grid()
            
            
            f2.add_subplot(122).plot(xfit, density2)
           
            f2.add_subplot(122).set_xticks(np.arange(0.0,10.0, 1.0))
            f2.add_subplot(122).xaxis.set_tick_params(labelsize=8)
            f2.add_subplot(122).yaxis.set_tick_params(labelsize=8)
            f2.add_subplot(122).set_xlabel('Gaze error values (deg)',size=8)
            f2.add_subplot(122).set_ylabel('Density',size=8)
            f2.add_subplot(122).set_title('KDE of gaze errors: Data-2', size=10)
            f2.add_subplot(122).grid()
            
            
            self.toolbar_frame2 = Frame(page2) 
            self.toolbar_frame2.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar2 = NavigationToolbar2TkAgg( self.canvas2, self.toolbar_frame2 )
            self.canvas2._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)

            self.T21.delete(1.0, END) 
            self.T21.insert(END,  "Comparing smoothed gaze error distributions \nfrom two datasets Data-1, Data-2 using \nKernel Density Estimation and fitting.")
            self.T21.insert(END,  "\nGaussian Kernel used with bandwidth of 0.2")
           
            

######################################## visualizations    
        def load_data_vis():
            global gt_xv
            global gt_yv
            global diff_gz_v
            global x_v
            global y_v
           
            
            gzm_file= tkFileDialog.askopenfilename(initialdir = "C:/Users/14233242/Documents/Python Scripts",title = "Select file",filetypes = [("CSV files","*.csv")])

            df= pd.read_csv(gzm_file)
            
            gz_x = df["Gaze X"].tolist() # gaze x
            gz_y = df["Gaze Y"].tolist() #gaze y
            gtx= df["Gnd tr X"].tolist()  #ground truth x
            gty= df["Gnd tr Y"].tolist()  #ground truth y
            tim_st= df["Timestamp"].tolist()
            st= df["Timestamp"].iloc[0] 
            
            resx= df["Res X"].iloc[0] 
            resy= df["Res Y"].iloc[0]
            mmpix= df["Mmpix"].iloc[0]
            us_dis=df["User Dis"].iloc[0]
            us_id = df["UID"].iloc[0]
            #print df 
            tim_rel= [(l - st)/1000.0 for l in tim_st]
            gtx_mm = [a * mmpix for a in gtx]
            gty_mm=  [b * mmpix for b in gty]
            
            gt_xv= gtx_mm 
            gt_yv=  gty_mm
            x_data = [a1 * mmpix for a1 in gz_x]  #in mm
            y_data=  [b1 * mmpix for b1 in gz_y]
            x_v=x_data 
            y_v=y_data 
            gt_z=np.empty(len(x_data))  
            gt_z.fill(us_dis)
            z_data= gt_z
            #### gaze angle calculation
            dx_sq =[q**2 for q in x_data]	
            dy_sq= [q1**2 for q1 in y_data] 
            mean_z = z_data  #culprit
            
            z_sq = [q2**2 for q2 in mean_z] 
            sum1 = np.array(dx_sq)+np.array(dy_sq)+np.array(z_sq)
            egp = [np.sqrt(q3) for q3 in sum1] 
            #Eye to eye tracker distance
            monitor_h= (resy/2)*mmpix
            x_sq = [q3**2 for q3 in x_data]
            y_1 = [q4+monitor_h for q4 in y_data]  ##### monitor dimensions used in calculating. 147 = (1050/2 ) 0.28 (res/2)*mmperpix
            y_sq = [q5**2 for q5 in y_1]
            sum2= np.array(x_sq)+np.array(y_sq)+np.array(z_sq)
            eet = [np.sqrt(q6) for q6 in sum2] 
            ##Gaze point to eye tracker distance			
            gzx_sq= [q7**2 for q7 in x_data]
            y_2 = [q8+monitor_h for q8 in y_data] 
            gzy_sq= [q9**2 for q9 in y_2]
            sum3= np.array(gzx_sq)+np.array(gzy_sq)
            g_et =[abs(np.sqrt(q10)) for q10 in sum3]
            ########################################
            prod= [2*m10*n10 for m10,n10 in zip(egp,eet)] 
            #prod1= [q11*2 for q11 in prod]
            b92_sq= [q12**2 for q12 in egp]
            b95_sq= [q13**2 for q13 in eet]
            b98_sq= [q14**2 for q14 in g_et]
            sum4= np.array(b92_sq)+np.array(b95_sq)-np.array(b98_sq)
            div = [ai/bi for ai,bi in zip(sum4,prod)]
            for i in xrange(len(div)):
                if div[i] > 1:
                    div[i] = 0.99999999999999999   ##cos exception
                    
            get_ang_v =[math.degrees(math.acos(q15)) for q15 in div]
            ############ ground truth #################
            gx_sq= [c1**2 for c1 in gtx_mm]
            gy_sq= [c2**2 for c2 in gty_mm]
            gz_sq = [c3**2 for c3 in gt_z]
            sum5 = np.array(gx_sq)+np.array(gy_sq)+np.array(gz_sq)
            gt_et = [abs(np.sqrt(c4)) for c4 in sum5]
            # eye to eye tracker distance
            ge_et = np.empty(len(gtx_mm)) 
            c5 = ((resy/2.0)* mmpix)**2
            c6 = (us_dis)**2
            sum6 = math.sqrt(c5+c6)
            ge_et.fill(sum6)
            ##Gaze point to eye tracker distance
            c7= ((resy/2.0)* mmpix)
            sum7 = [(c8+c7)**2 for c8 in gty_mm]
            sum8 = np.array(gx_sq)+np.array(sum7)
            ggp_et = [abs(np.sqrt(c9)) for c9 in sum8]
            ##Gaze angle relative to eye tracker
            sq1= [d1**2 for d1 in gt_et]
            sq2 = [d2**2 for d2 in ge_et]
            sq3= [d3**2 for d3 in ggp_et]
            sum9 = np.array(sq1)+np.array(sq2)- np.array(sq3)
            prod3= [2*m1*n1 for m1,n1 in zip(gt_et,ge_et)] 
            div2= [m2/n2 for m2,n2 in zip(sum9,prod3)] 
            gtt_ang_v =[math.degrees(math.acos(q16)) for q16 in div2]
            
            ############## error#
            diff_gz_v=[abs(m3-n3) for m3,n3 in zip(get_ang_v,gtt_ang_v)]

            
             ##################### plots ######################
            fs = Figure(figsize=(5.5,3.8), dpi=100)      
            fs.subplots_adjust(wspace = 0.4)
            self.canvas_s = FigureCanvasTkAgg(fs, page3)
            self.canvas_s.show()
        
            fs.add_subplot(111).scatter(x_data,y_data, color='black')
            fs.add_subplot(111).plot(gtx_mm,gty_mm,'b')

            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).set_xlabel('Gaze X data vs GT X(mm)',size=8)
            fs.add_subplot(111).set_ylabel('Gaze Y data vs GT Y (mm)',size=8)
            fs.add_subplot(111).set_title('gaze vs ground truth scatter', size=10)
            fs.add_subplot(111).grid()
                        
            self.toolbar_frame3 = Frame(page3) 
            self.toolbar_frame3.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar_s = NavigationToolbar2TkAgg( self.canvas_s, self.toolbar_frame3 )
            self.canvas_s._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)

################################# datavis1################################################
        def load_data_vis1():
            global gt_xv1
            global gt_yv1
            global diff_gz_v1
            global x_v1
            global y_v1
            global get_ang_v1
            
            gzm_file= tkFileDialog.askopenfilename(initialdir = "C:/Users/14233242/Documents/Python Scripts",title = "Select file",filetypes = [("CSV files","*.csv")])

            df= pd.read_csv(gzm_file)
            
            gz_x = df["Gaze X"].tolist() # gaze x
            gz_y = df["Gaze Y"].tolist() #gaze y
            gtx= df["Gnd tr X"].tolist()  #ground truth x
            gty= df["Gnd tr Y"].tolist()  #ground truth y
            tim_st= df["Timestamp"].tolist()
            st= df["Timestamp"].iloc[0] 
            
            resx= df["Res X"].iloc[0] 
            resy= df["Res Y"].iloc[0]
            mmpix= df["Mmpix"].iloc[0]
            us_dis=df["User Dis"].iloc[0]
            us_id = df["UID"].iloc[0]
            #print df 
            tim_rel= [(l - st)/1000.0 for l in tim_st]
            gtx_mm = [a * mmpix for a in gtx]
            gty_mm=  [b * mmpix for b in gty]
            
            gt_xv1= gtx_mm 
            gt_yv1=  gty_mm
            x_data = [a1 * mmpix for a1 in gz_x]  #in mm
            y_data=  [b1 * mmpix for b1 in gz_y]
            x_v1=x_data 
            y_v1=y_data 
            gt_z=np.empty(len(x_data))  
            gt_z.fill(us_dis)
            z_data= gt_z
            #### gaze angle calculation
            dx_sq =[q**2 for q in x_data]	
            dy_sq= [q1**2 for q1 in y_data] 
            mean_z = z_data  #culprit
            
            z_sq = [q2**2 for q2 in mean_z] 
            sum1 = np.array(dx_sq)+np.array(dy_sq)+np.array(z_sq)
            egp = [np.sqrt(q3) for q3 in sum1] 
            #Eye to eye tracker distance
            monitor_h= (resy/2)*mmpix
            x_sq = [q3**2 for q3 in x_data]
            y_1 = [q4+monitor_h for q4 in y_data]  ##### monitor dimensions used in calculating. 147 = (1050/2 ) 0.28 (res/2)*mmperpix
            y_sq = [q5**2 for q5 in y_1]
            sum2= np.array(x_sq)+np.array(y_sq)+np.array(z_sq)
            eet = [np.sqrt(q6) for q6 in sum2] 
            ##Gaze point to eye tracker distance			
            gzx_sq= [q7**2 for q7 in x_data]
            y_2 = [q8+monitor_h for q8 in y_data] 
            gzy_sq= [q9**2 for q9 in y_2]
            sum3= np.array(gzx_sq)+np.array(gzy_sq)
            g_et =[abs(np.sqrt(q10)) for q10 in sum3]
            ########################################
            prod= [2*m10*n10 for m10,n10 in zip(egp,eet)] 
            #prod1= [q11*2 for q11 in prod]
            b92_sq= [q12**2 for q12 in egp]
            b95_sq= [q13**2 for q13 in eet]
            b98_sq= [q14**2 for q14 in g_et]
            sum4= np.array(b92_sq)+np.array(b95_sq)-np.array(b98_sq)
            div = [ai/bi for ai,bi in zip(sum4,prod)]
            for i in xrange(len(div)):
                if div[i] > 1:
                    div[i] = 0.99999999999999999   ##cos exception
                    
            get_ang_v1 =[math.degrees(math.acos(q15)) for q15 in div]
            ############ ground truth #################
            gx_sq= [c1**2 for c1 in gtx_mm]
            gy_sq= [c2**2 for c2 in gty_mm]
            gz_sq = [c3**2 for c3 in gt_z]
            sum5 = np.array(gx_sq)+np.array(gy_sq)+np.array(gz_sq)
            gt_et = [abs(np.sqrt(c4)) for c4 in sum5]
            # eye to eye tracker distance
            ge_et = np.empty(len(gtx_mm)) 
            c5 = ((resy/2.0)* mmpix)**2
            c6 = (us_dis)**2
            sum6 = math.sqrt(c5+c6)
            ge_et.fill(sum6)
            ##Gaze point to eye tracker distance
            c7= ((resy/2.0)* mmpix)
            sum7 = [(c8+c7)**2 for c8 in gty_mm]
            sum8 = np.array(gx_sq)+np.array(sum7)
            ggp_et = [abs(np.sqrt(c9)) for c9 in sum8]
            ##Gaze angle relative to eye tracker
            sq1= [d1**2 for d1 in gt_et]
            sq2 = [d2**2 for d2 in ge_et]
            sq3= [d3**2 for d3 in ggp_et]
            sum9 = np.array(sq1)+np.array(sq2)- np.array(sq3)
            prod3= [2*m1*n1 for m1,n1 in zip(gt_et,ge_et)] 
            div2= [m2/n2 for m2,n2 in zip(sum9,prod3)] 
            gtt_ang_v =[math.degrees(math.acos(q16)) for q16 in div2]
            
            ############## error#
            diff_gz_v1=[abs(m3-n3) for m3,n3 in zip(get_ang_v1,gtt_ang_v)]

             ##################### plots ######################
            fs = Figure(figsize=(5.5,3.8), dpi=100)      
            fs.subplots_adjust(wspace = 0.4)
            self.canvas_s = FigureCanvasTkAgg(fs, page3)
            self.canvas_s.show()
        
            fs.add_subplot(111).scatter(x_data,y_data, color='black')
            fs.add_subplot(111).plot(gtx_mm,gty_mm,'b')
            #fs.add_subplot(122).set_xticks(np.arange(0.0, 91.0, 30.0))
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).set_xlabel('Gaze X data vs GT X(mm)',size=8)
            fs.add_subplot(111).set_ylabel('Gaze Y data vs GT Y (mm)',size=8)
            fs.add_subplot(111).set_title('Gaze vs ground truth: Data-1', size=12)
            fs.add_subplot(111).grid()
                        
            self.toolbar_frame3 = Frame(page3) 
            self.toolbar_frame3.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar_s = NavigationToolbar2TkAgg( self.canvas_s, self.toolbar_frame3 )
            self.canvas_s._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)        
        
            
        def load_data_vis2():
            global gt_xv2
            global gt_yv2
            global diff_gz_v2
            global x_v2
            global y_v2
            global get_ang_v2
            
            gzm_file= tkFileDialog.askopenfilename(initialdir = "C:/Users/14233242/Documents/Python Scripts",title = "Select file",filetypes = [("CSV files","*.csv")])

            df= pd.read_csv(gzm_file)
            
            gz_x = df["Gaze X"].tolist() # gaze x
            gz_y = df["Gaze Y"].tolist() #gaze y
            gtx= df["Gnd tr X"].tolist()  #ground truth x
            gty= df["Gnd tr Y"].tolist()  #ground truth y
            tim_st= df["Timestamp"].tolist()
            st= df["Timestamp"].iloc[0] 
            
            resx= df["Res X"].iloc[0] 
            resy= df["Res Y"].iloc[0]
            mmpix= df["Mmpix"].iloc[0]
            us_dis=df["User Dis"].iloc[0]
            us_id = df["UID"].iloc[0]
            #print df 
            tim_rel= [(l - st)/1000.0 for l in tim_st]
            gtx_mm = [a * mmpix for a in gtx]
            gty_mm=  [b * mmpix for b in gty]
            
            gt_xv2= gtx_mm 
            gt_yv2=  gty_mm
            
            x_data = [a1 * mmpix for a1 in gz_x]  #in mm
            y_data=  [b1 * mmpix for b1 in gz_y]
            x_v2=x_data 
            y_v2=y_data 
            gt_z=np.empty(len(x_data))  
            gt_z.fill(us_dis)
            z_data= gt_z
            #### gaze angle calculation
            dx_sq =[q**2 for q in x_data]	
            dy_sq= [q1**2 for q1 in y_data] 
            mean_z = z_data  #culprit
            
            z_sq = [q2**2 for q2 in mean_z] 
            sum1 = np.array(dx_sq)+np.array(dy_sq)+np.array(z_sq)
            egp = [np.sqrt(q3) for q3 in sum1] 
            #Eye to eye tracker distance
            monitor_h= (resy/2)*mmpix
            x_sq = [q3**2 for q3 in x_data]
            y_1 = [q4+monitor_h for q4 in y_data]  ##### monitor dimensions used in calculating. 147 = (1050/2 ) 0.28 (res/2)*mmperpix
            y_sq = [q5**2 for q5 in y_1]
            sum2= np.array(x_sq)+np.array(y_sq)+np.array(z_sq)
            eet = [np.sqrt(q6) for q6 in sum2] 
            ##Gaze point to eye tracker distance			
            gzx_sq= [q7**2 for q7 in x_data]
            y_2 = [q8+monitor_h for q8 in y_data] 
            gzy_sq= [q9**2 for q9 in y_2]
            sum3= np.array(gzx_sq)+np.array(gzy_sq)
            g_et =[abs(np.sqrt(q10)) for q10 in sum3]
            ########################################
            prod= [2*m10*n10 for m10,n10 in zip(egp,eet)] 
            #prod1= [q11*2 for q11 in prod]
            b92_sq= [q12**2 for q12 in egp]
            b95_sq= [q13**2 for q13 in eet]
            b98_sq= [q14**2 for q14 in g_et]
            sum4= np.array(b92_sq)+np.array(b95_sq)-np.array(b98_sq)
            div = [ai/bi for ai,bi in zip(sum4,prod)]
            for i in xrange(len(div)):
                if div[i] > 1:
                    div[i] = 0.99999999999999999   ##cos exception
                    
            get_ang_v2 =[math.degrees(math.acos(q15)) for q15 in div]
            ############ ground truth #################
            gx_sq= [c1**2 for c1 in gtx_mm]
            gy_sq= [c2**2 for c2 in gty_mm]
            gz_sq = [c3**2 for c3 in gt_z]
            sum5 = np.array(gx_sq)+np.array(gy_sq)+np.array(gz_sq)
            gt_et = [abs(np.sqrt(c4)) for c4 in sum5]
            # eye to eye tracker distance
            ge_et = np.empty(len(gtx_mm)) 
            c5 = ((resy/2.0)* mmpix)**2
            c6 = (us_dis)**2
            sum6 = math.sqrt(c5+c6)
            ge_et.fill(sum6)
            ##Gaze point to eye tracker distance
            c7= ((resy/2.0)* mmpix)
            sum7 = [(c8+c7)**2 for c8 in gty_mm]
            sum8 = np.array(gx_sq)+np.array(sum7)
            ggp_et = [abs(np.sqrt(c9)) for c9 in sum8]
            ##Gaze angle relative to eye tracker
            sq1= [d1**2 for d1 in gt_et]
            sq2 = [d2**2 for d2 in ge_et]
            sq3= [d3**2 for d3 in ggp_et]
            sum9 = np.array(sq1)+np.array(sq2)- np.array(sq3)
            prod3= [2*m1*n1 for m1,n1 in zip(gt_et,ge_et)] 
            div2= [m2/n2 for m2,n2 in zip(sum9,prod3)] 
            gtt_ang_v =[math.degrees(math.acos(q16)) for q16 in div2]
            
            ############## error#
            diff_gz_v2=[abs(m3-n3) for m3,n3 in zip(get_ang_v2,gtt_ang_v)]

             ##################### plots ######################
            fs = Figure(figsize=(5.5,3.8), dpi=100)      
            fs.subplots_adjust(wspace = 0.4)
            self.canvas_s = FigureCanvasTkAgg(fs, page3)
            self.canvas_s.show()
        
            fs.add_subplot(111).scatter(x_data,y_data, color='black')
            fs.add_subplot(111).plot(gtx_mm,gty_mm,'b')
            
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).set_xlabel('Gaze X data vs GT X(mm)',size=8)
            fs.add_subplot(111).set_ylabel('Gaze Y data vs GT Y (mm)',size=8)
            fs.add_subplot(111).set_title('Gaze vs ground truth: Data-2', size=12)
            fs.add_subplot(111).grid()
                        
            self.toolbar_frame3 = Frame(page3) 
            self.toolbar_frame3.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar_s = NavigationToolbar2TkAgg( self.canvas_s, self.toolbar_frame3 )
            self.canvas_s._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)        
        
            
        def plothist_v1():
            bin1=self.T35.get("1.0","end-1c")
            bins = np.linspace(0, 10, int(float(bin1)))
            lab1= "bin size: "+ bin1
            add_anno = self.T33.get("1.0","end-1c")
            
            plot_bg= self.T32.get("1.0","end-1c")
            plot_cl= self.T31.get("1.0","end-1c")
            print plot_cl,plot_bg
            fs = Figure(figsize=(5.5,3.7), dpi=100)
            self.canvas = FigureCanvasTkAgg(fs, page3)
            self.canvas.show()
            fs.add_subplot(111).hist(diff_gz_v, bins, histtype='stepfilled', normed=False, color=plot_cl, alpha=0.4, label=lab1)
            fs.add_subplot(111).set_facecolor(plot_bg)
            fs.add_subplot(111).set_xlabel('Error in degrees',size=8)
            fs.add_subplot(111).set_ylabel('Instances',size=8)
            fs.add_subplot(111).set_title('Gaze data error histogram', size=12)
            fs.add_subplot(111).legend()
            fs.add_subplot(111).annotate(add_anno, xy=(5, 8), xytext=(8, 400))
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).grid()
            
            #self.canvas_s.show()
            self.toolbar_frame = Frame(page3) 
            self.toolbar_frame.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.toolbar_frame )
            self.canvas._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
        
        def threedplot():
                       
            plot_bg= self.T32.get("1.0","end-1c")
            plot_cmap= self.T34.get("1.0","end-1c")
            aoi_dict={}
            mean_err =[]
            
            
            for m9 in range(0, 28):
                aoi_dict['aoi_%02d' % m9]= diff_gz_v[(m9*90)-30:m9*90]#: (m9*90)+60]
                lst = diff_gz_v[(m9*90)-25:(m9*90-5)]
                avg_1= sum(lst)/30
                mean_err.append(avg_1)  #mean gaze angle differences
            aoi_ind= [90*n for n in range(0,28)]     
            aoi_x= [gt_xv[m5] for m5 in aoi_ind]      # x value at aoi points
            aoi_y= [gt_yv[m6] for m6 in aoi_ind]  
            z = np.array(mean_err)

            xnew, ynew = np.mgrid[-200:200:70j, -100:100:70j]
            tck = interpolate.bisplrep(aoi_x, aoi_y, z, s=0)
            znew = interpolate.bisplev(xnew[:,0], ynew[0,:], tck)           
                    
            fs = Figure(figsize=(5.5,3.8), dpi=100)
            self.canvas = FigureCanvasTkAgg(fs, page3)

            ax= fs.add_subplot(111, projection='3d')
            p= ax.plot_surface(xnew, ynew , znew , rstride=40, cstride=60,cmap=plot_cmap, antialiased=True)
            fs.colorbar(p,boundaries=np.arange(min(mean_err),max(mean_err),.5))
            ax.set_xlabel('Diplay X (mm)',size=8)
            ax.set_ylabel('Diplay Y (mm)',size=8)
            ax.set_title('Gaze error 3D plot', size=12)
            ax.set_facecolor(plot_bg)
            

            ax.xaxis.set_tick_params(labelsize=8)
            ax.yaxis.set_tick_params(labelsize=8)
            ax.grid()
            
            
            self.toolbar_frame = Frame(page3) 
            self.toolbar_frame.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.toolbar_frame )
            self.canvas._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
       
        def plothist_v2():
           
            plot_bg= self.T32.get("1.0","end-1c")           
            bin1=self.T35.get("1.0","end-1c")
            bins = np.linspace(0, 10, int(float(bin1)))
            add_anno = self.T33.get("1.0","end-1c")
            
            fs = Figure(figsize=(5.5,3.8), dpi=100)
            self.canvas = FigureCanvasTkAgg(fs, page3)
            self.canvas.show()
            fs.add_subplot(111).hist(diff_gz_v1, bins, histtype='stepfilled', normed=False, color='r', alpha=0.4, label="data1")
            fs.add_subplot(111).hist(diff_gz_v2, bins, histtype='stepfilled', normed=False, color='b', alpha=0.4, label="data2")
            
            fs.add_subplot(111).set_xlabel('Error in degrees',size=8)
            fs.add_subplot(111).set_ylabel('Instances',size=8)
            fs.add_subplot(111).set_title('Gaze error histogram comparison', size=12)
            fs.add_subplot(111).legend()
            fs.add_subplot(111).annotate(add_anno, xy=(5, 8), xytext=(8, 600))
            fs.add_subplot(111).set_facecolor(plot_bg)
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).grid()
            
            
            self.toolbar_frame = Frame(page3) 
            self.toolbar_frame.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.toolbar_frame )
            self.canvas._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)

            
        def data_density():
            plot_bg= self.T32.get("1.0","end-1c") 
            plot_cmap= self.T34.get("1.0","end-1c") 
            cmap1= "plt.cm."+plot_cmap
            add_anno = self.T33.get("1.0","end-1c") 
            
            bin2=self.T35.get("1.0","end-1c")
            bin2= int(float(bin2))
            fs = Figure(figsize=(5.5,3.8), dpi=100)
            
            self.canvas = FigureCanvasTkAgg(fs, page3)
            self.canvas.show()
            
            ax = fs.add_subplot(1,1,1)            
            im= ax.hist2d(x_v, y_v, (bin2, bin2), cmap=plot_cmap)
            
            fs.colorbar(im[3])
                    
            
            fs.add_subplot(111).set_xlabel('X dimension (mm)',size=8)
            fs.add_subplot(111).set_ylabel('Y dimension (mm)',size=8)
            fs.add_subplot(111).set_title('Gaze data density plot', size=12)
            fs.add_subplot(111).legend()
            fs.add_subplot(111).set_facecolor(plot_bg)
            fs.add_subplot(111).annotate(add_anno, xy=(50, 100), xytext=(30, 15))
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).grid()
            
           
            self.toolbar_frame = Frame(page3) 
            self.toolbar_frame.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.toolbar_frame )
            self.canvas._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            
        
        def bubble():
            aoi_dict={}
            mean_err =[]
            aoi_std=[]
            plot_bg= self.T32.get("1.0","end-1c")
            plot_cl= self.T31.get("1.0","end-1c")
            add_anno = self.T33.get("1.0","end-1c")
            for m9 in range(0, 28):
                aoi_dict['aoi_%02d' % m9]= diff_gz_v[(m9*90)-30:m9*90]
                lst =  diff_gz_v[(m9*90)-25:(m9*90-5)]
                avg_1= sum(lst)/30
                std_1= np.std(lst)
                mean_err.append(avg_1)  
                aoi_std.append(std_1)
            print len(mean_err)
           
            aoi_ind= [90*n for n in range(0,28)]
     
           
            aoi_x= [gt_xv[m5] for m5 in aoi_ind]      
            aoi_y= [gt_yv[m6] for m6 in aoi_ind]  
            print aoi_x[9], aoi_y[9]
            aoi_x1= [aoi_x[0], aoi_x[1], aoi_x[2],aoi_x[5],aoi_x[6],
                     aoi_x[9], aoi_x[10],aoi_x[11], aoi_x[14], aoi_x[15], 
                        aoi_x[19], aoi_x[20], aoi_x[21],aoi_x[24],aoi_x[25]]
            
            aoi_y1= [aoi_y[0], aoi_y[1], aoi_y[2],aoi_y[5],aoi_y[6],
                     aoi_y[9], aoi_y[10],aoi_y[11], aoi_y[14],aoi_y[15], 
                        aoi_y[19], aoi_y[20], aoi_y[21],aoi_y[24],aoi_y[25]]
            
                                
            meanvals = [mean_err[0], mean_err[1],mean_err[2],mean_err[5],mean_err[6],
                        mean_err[9],mean_err[10],mean_err[11], mean_err[14],mean_err[15],
                        mean_err[19], mean_err[20], mean_err[21],mean_err[24],mean_err[25]]
                        
            stdvals = [aoi_std[0],aoi_std[1],aoi_std[2],aoi_std[5],aoi_std[6],
                        aoi_std[9],aoi_std[10],aoi_std[11], aoi_std[14],aoi_std[15],
                        aoi_std[19], aoi_std[20], aoi_std[21],aoi_std[24],aoi_std[25]]
                        
            fs = Figure(figsize=(5.5,3.8), dpi=100)
            self.canvas = FigureCanvasTkAgg(fs, page3)
            self.canvas.show()
            fs.add_subplot(111).scatter(aoi_x1, aoi_y1, color=plot_cl, alpha=0.4)
            for m10 in range(0, 15):
                fs.add_subplot(111).annotate('e='+ str(round(meanvals[m10],2)),xy=(aoi_x1[m10],aoi_y1[m10]), horizontalalignment='center', verticalalignment='bottom',fontsize=8)
                fs.add_subplot(111).annotate('s='+ str(round(stdvals[m10],2)),xy=(aoi_x1[m10],aoi_y1[m10]), horizontalalignment='center', verticalalignment='top',fontsize=8)
            
            
            fs.add_subplot(111).set_xlabel('X dimension (mm)',size=8)
            fs.add_subplot(111).set_ylabel('Y dimension (mm)',size=8)
            fs.add_subplot(111).set_title('Local mean/SD plot of gaze error over display', size=12)
            fs.add_subplot(111).legend()
            fs.add_subplot(111).set_facecolor(plot_bg)
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).grid()
            fs.add_subplot(111).annotate(add_anno, xy=(50, 100), xytext=(30, 15))
         
            self.toolbar_frame = Frame(page3) 
            self.toolbar_frame.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.toolbar_frame )
            self.canvas._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            
        def reg_plot():
            
            add_anno = self.T33.get("1.0","end-1c")
            plt.ioff()
            fs = Figure(figsize=(5.5,3.8), dpi=100)
            self.canvas = FigureCanvasTkAgg(fs, page3)
            self.canvas.show()

            
            ax1 = fs.add_subplot(1,1,1) 
            g = sns.regplot(np.array(diff_gz_v1), np.array(diff_gz_v2),data=None,  ax=ax1)
            
            fs.add_subplot(111).set_xlabel('Error in degrees-Data1',size=8)
            fs.add_subplot(111).set_ylabel('Error in degrees-Data2',size=8)
            fs.add_subplot(111).set_xlim([0, 10])
            fs.add_subplot(111).set_ylim([0, 10])
            fs.add_subplot(111).set_title('Gaze error regression plot', size=8)
            fs.add_subplot(111).legend()
            fs.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            fs.add_subplot(111).grid()
            fs.add_subplot(111).annotate(add_anno, xy=(5, 8), xytext=(8, 8))
            
            self.toolbar_frame = Frame(page3) 
            self.toolbar_frame.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.toolbar_frame )
            self.canvas._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            

        def bar_plot():
            mean_err = np.array([np.mean(diff_gz_v1), np.mean(diff_gz_v2)])
            max_err = np.array([max(diff_gz_v1),max(diff_gz_v2)])
            max_gz= np.array([max(get_ang_v1),max(get_ang_v2)])
            add_anno = self.T33.get("1.0","end-1c")
            x= np.arange(2)
            
            f1 = Figure(figsize=(5.5,3.8), dpi=100)
            self.canvas1 = FigureCanvasTkAgg(f1, page3)
            self.canvas1.show()
            ax1 = f1.add_subplot(1,1,1) 
            f1.add_subplot(111).bar(x+0.2, mean_err, width=0.2,color='b',align='center',label="Mean er")
            f1.add_subplot(111).bar(x, max_err,width=0.2,color='g',align='center',label="Max_er")
            f1.add_subplot(111).bar(x-0.2, max_gz,width=0.2,color='r',align='center',label="Max ga")
            
            f1.add_subplot(111).set_xlabel('Gaze variables',size=8)
            f1.add_subplot(111).set_ylabel('Degrees',size=8)
       
            f1.add_subplot(111).set_title('Gaze angles bar plot', size=12)
            f1.add_subplot(111).legend(prop={'size': 8})
            f1.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            f1.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            f1.add_subplot(111).grid()
            f1.add_subplot(111).annotate(add_anno, xy=(1, 2), xytext=(1, 25))

            self.toolbar_frame1 = Frame(page3) 
            self.toolbar_frame1.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar1 = NavigationToolbar2TkAgg( self.canvas1, self.toolbar_frame1 )
            self.canvas1._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            
            
        def box_plot():
            add_anno = self.T33.get("1.0","end-1c")
            f1 = Figure(figsize=(5.5,3.8), dpi=100)
            self.canvas1 = FigureCanvasTkAgg(f1, page3)
            self.canvas1.show()
            ax1 = f1.add_subplot(1,1,1) 
            data = [diff_gz_v1, diff_gz_v2]
            f1.add_subplot(111).boxplot(data,showfliers=False)
                   
            f1.add_subplot(111).set_xlabel('Gaze datasets',size=8)
            f1.add_subplot(111).set_ylabel('Degrees',size=8)
       
            f1.add_subplot(111).set_title('Box plots of Data-1 & Data-2', size=12)
           
            
           
            f1.add_subplot(111).xaxis.set_tick_params(labelsize=8)
            f1.add_subplot(111).yaxis.set_tick_params(labelsize=8)
            
            f1.add_subplot(111).grid()            
            f1.add_subplot(111).annotate(add_anno, xy=(2, 6), xytext=(2, 6))
            
             #canvas.get_tk_widget().pack(side=tk.BOTTOM)
            self.toolbar_frame1 = Frame(page3) 
            self.toolbar_frame1.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar1 = NavigationToolbar2TkAgg( self.canvas1, self.toolbar_frame1 )
            self.canvas1._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            
        def line_plot():
            f2 = Figure(figsize=(5.5,3.8), dpi=100)      
            self.canvas2 = FigureCanvasTkAgg(f2, page3)
            self.canvas2.show()
            f2.add_subplot(211).plot(diff_gz_v1, color= 'r')
            f2.add_subplot(211).set_ylabel('Gaze error (degrees)',size=8)
            f2.add_subplot(211).set_title('Error vs data points (red:Data-1,blue: Data-2)', size=10)
            f2.add_subplot(211).grid()
            
            
            f2.add_subplot(212).plot(diff_gz_v2,color= 'b')
            f2.add_subplot(212).set_ylabel('Gaze error (degrees)',size=8)
            f2.add_subplot(212).grid()
            
            
            self.toolbar_frame2 = Frame(page3) 
            self.toolbar_frame2.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
            self.toolbar2 = NavigationToolbar2TkAgg( self.canvas2, self.toolbar_frame2 )
            self.canvas2._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
            

        def file_save2():
            save_file1 = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
            if save_file1 is None: 
                return
            text2save = str(self.T21.get(1.0, END)) 
            save_file1.write(text2save)
            save_file1.close() 
        
        def clear_text_field():   
             self.T21.delete(1.0, END)
             self.T21.insert(END, quote21)
             f1 = Figure(figsize=(5.5,3.7), dpi=100)
             self.canvas1 = FigureCanvasTkAgg(f1, page2)
             self.canvas1.show()
             t1 = np.arange(0, 3, .01)
             f1.add_subplot(111).plot(t1, 2 * np.sin(2 * np.pi * t1))

             self.toolbar_frame1 = Frame(page2) 
             self.toolbar_frame1.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
             self.toolbar1 = NavigationToolbar2TkAgg( self.canvas1, self.toolbar_frame1 )
             self.canvas1._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)

        def change_dropdown(*args):
            print( self.var1.get() )
        
        def demostaticui1():
            self.T41.delete(1.0, END) 
            self.T41.insert(END, "Static UI-1 demo shown above")
            bgco= self.T45.get("1.0","end-1c")
            self.canvas5 = Canvas(page4,width=540, height= 420, bg= bgco,highlightthickness=1, highlightbackground="black")
            self.canvas5.grid(row=1,column=4,rowspan=8, columnspan=3, padx = 10,pady = 10, sticky=N)
            button1 = Button(self.canvas5, text = "Button1", anchor = W)
            button1.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button1_window = self.canvas5.create_window(20, 50, anchor=NW, window=button1)
            
            button2 = Button(self.canvas5, text = "Button2", anchor = W)
            button2.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button2_window = self.canvas5.create_window(200, 50, anchor=NW, window=button2)
            
            button3 = Button(self.canvas5, text = "Button3", anchor = W)
            button3.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button3_window = self.canvas5.create_window(400, 50, anchor=NW, window=button3)
            
            button4 = Button(self.canvas5, text = "Button4", anchor = W)
            button4.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button4_window = self.canvas5.create_window(20, 300, anchor=NW, window=button4)
            
            button5 = Button(self.canvas5, text = "Button5", anchor = W)
            button5.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button5_window = self.canvas5.create_window(200, 300, anchor=NW, window=button5)
            
            button6 = Button(self.canvas5, text = "Button6", anchor = W)
            button6.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button6_window = self.canvas5.create_window(400, 300, anchor=NW, window=button6)
            
        def demostaticui2():
            self.T41.delete(1.0, END) 
            self.T41.insert(END, "Static UI-2 demo shown above")
            ballsize =self.T44.get("1.0","end-1c")
            bs = int(float(ballsize))
            bgco= self.T45.get("1.0","end-1c")
            interv1= self.T46.get("1.0","end-1c")
            interv = int(float(interv1))
            
            self.canvas4 = Canvas(page4,width=540, height= 420, bg= bgco,highlightthickness=1, highlightbackground="black")
            self.canvas4.grid(row=1,column=4,rowspan=8, columnspan=3, padx = 10,pady = 10, sticky=N)
            ball = self.canvas4.create_oval( 0, 0, 10, 10 )
            xInc = 90
            yInc = 100
            ballX = 40
            ballY=10
            while ballY < 400:
                time.sleep( 0.05 )
                self.canvas4.delete( ball )
                ball = self.canvas4.create_oval( ballX, ballY, ballX + bs, ballY+bs, fill = "blue" )
                time.sleep(interv)
                ballX += xInc
                if ballX > 490 :
                    ballY += yInc
                    ballX=40
                self.canvas4.update()
                
        def demodynui():
            self.T41.delete(1.0, END) 
            self.T41.insert(END, "Dynamic UI demo shown above")
            ballsize =self.T44.get("1.0","end-1c")
            bs = int(float(ballsize))
            bgco= self.T45.get("1.0","end-1c")
           
            
            self.canvas4 = Canvas(page4,width=540, height= 420, bg= bgco,highlightthickness=1, highlightbackground="black")
            self.canvas4.grid(row=1,column=4,rowspan=8, columnspan=3, padx = 10,pady = 10, sticky=N)
            ball = self.canvas4.create_oval( 0, 0, 10, 10 )
            xInc = 8
            yInc = 100
            ballX = 40
            ballY=10
            while ballY < 400:
                time.sleep( 0.05 )
                self.canvas4.delete( ball )
                ball = self.canvas4.create_oval( ballX, ballY, ballX + bs, ballY+bs, fill = "blue" )
                time.sleep(0.01)
                ballX += xInc
                if ballX > 490 :
                    ballY += yInc
                    ballX=40
                self.canvas4.update()
        
        def startstaticui2():
            self.T41.delete(1.0, END) 
            ballsize =self.T44.get("1.0","end-1c")
            bs = int(float(ballsize))
            bgco= self.T45.get("1.0","end-1c")
            interv1= self.T46.get("1.0","end-1c")
            interv = int(float(interv1))
            
            window_w =self.T42.get("1.0","end-1c")
            ww = int(float(window_w))
            window_h= self.T43.get("1.0","end-1c")
            wh = int(float(window_h))
            dimval= window_w+ "x"+window_h
            
            self.top = Toplevel()
            self.top.title('Static Test UI-2')
            self.top.wm_geometry(dimval)
            self.window_canv = Canvas(self.top, width=ww, height= wh, bg= bgco,highlightthickness=1, highlightbackground="black")
            self.window_canv.grid(row=0,column=0)#,rowspan=8, columnspan=3, padx = 10,pady = 10, sticky=S)
            ball = self.window_canv.create_oval( 0, 0, 10, 10 )
            xInc = 250
            yInc = 200
            ballX = 50
            ballY=10
            while ballY < 700:
                time.sleep( interv ) #interv
                self.window_canv.delete( ball )
                ball = self.window_canv.create_oval( ballX, ballY, ballX + bs, ballY+bs, fill = "blue" )
                time.sleep(0.01)
                ballX += xInc
                if ballX > 1300 :
                    ballY += yInc
                    ballX=50
                self.window_canv.update()
                console_ent = "Ground truth (x,y):"+ str(ballX)+ ", "+ str(ballY)+ "\n"
                self.T41.insert(END, console_ent)   
                
##############################################################################################              
################################## LiveTracking functions ####################################
                
#        def getxy1(event): 
#            valx= float(event.x)+50 
#            valy= float(event.y)+10
#            
#            valb1= "Button: 1 GT: "+ str(valx)+" , "+ str(valy)
#            hb_thread = threading.Thread(target=pytribe.heartbeat_loop,
#                             kwargs={})
#            hb_thread.daemon = True
#            hb_thread.start()
#            time.sleep(0.5)
#
#            q=Queue.Queue()
#            query_thread = threading.Thread(target=pytribe.queue_tracker_frames, args=(q,),
#                                kwargs=dict(interval=0.15))
#            query_thread.daemon=True
#            query_thread.start()
#            time.sleep(1)
#
#            list_of_data_dicts = pytribe.extract_queue(q)
#            time.sleep(0.5)
#
#            gdx=[]
#            gdy=[]
#            for item in list_of_data_dicts:
#            
#             
#                dict1 = item['values']['frame']['avg']
#                a= dict1['x']
#                b= dict1['y']
#                gdx.append(float(a))
#                gdy.append(float(b))
#            
#            print valb1,"gaze", round(abs(np.mean(gdx)),2), round(abs(np.mean(gdy)),2)
#            stat= str(valb1)+" gaze " + str(round(abs(np.mean(gdx)),2))+ ", "+str(round(abs(np.mean(gdy)),2))
#            
#            self.T41.delete(1.0, END) 
#            self.T41.insert(END,  stat)
#
#            
#        def getxy2(event): 
#            valx= float(event.x)+650
#            valy= float(event.y)+10
#            global valb2
#            valb2= "Button: 2 GT: "+ str(valx)+" , "+ str(valy)
#            hb_thread = threading.Thread(target=pytribe.heartbeat_loop,
#                             kwargs={})
#            hb_thread.daemon = True
#            hb_thread.start()
#            time.sleep(0.5)
#            #Start collecting samples from the eye tracker and add to a queue
#            q=Queue.Queue()
#            query_thread = threading.Thread(target=pytribe.queue_tracker_frames, args=(q,),
#                                kwargs=dict(interval=0.15))
#            query_thread.daemon=True
#            query_thread.start()
#            time.sleep(1)
#            #Extract all of the samples from the queue
#            list_of_data_dicts = pytribe.extract_queue(q)
#            time.sleep(0.5)
#            #First "average" data point
#            gdx=[]
#            gdy=[]
#            for item in list_of_data_dicts:
#            
#             
#                dict1 = item['values']['frame']['avg']
#                a= dict1['x']
#                b= dict1['y']
#                gdx.append(float(a))
#                gdy.append(float(b))
#            
#            print valb2,"gaze data2", round(abs(np.mean(gdx)),2), round(abs(np.mean(gdy)),2)
#            stat= "\n"+str(valb2)+" gaze "+str(round(abs(np.mean(gdx)),2))+ " , "+str(round(abs(np.mean(gdy)),2))
#
#            self.T41.insert(END,  stat)
#
#            
#        def getxy3(event): 
#            valx= float(event.x)+1250
#            valy= float(event.y)+10
#            global valb3
#            valb3= "Button: 3 GT: "+ str(valx)+" , "+ str(valy)
#            hb_thread = threading.Thread(target=pytribe.heartbeat_loop,
#                             kwargs={})
#            hb_thread.daemon = True
#            hb_thread.start()
#            time.sleep(0.5)
#            #Start collecting samples from the eye tracker and add to a queue
#            q=Queue.Queue()
#            query_thread = threading.Thread(target=pytribe.queue_tracker_frames, args=(q,),
#                                kwargs=dict(interval=0.15))
#            query_thread.daemon=True
#            query_thread.start()
#            time.sleep(1)
#
#            list_of_data_dicts = pytribe.extract_queue(q)
#            time.sleep(0.5)
#            #First "average" data point
#            gdx=[]
#            gdy=[]
#            for item in list_of_data_dicts:
#            
#             
#                dict1 = item['values']['frame']['avg']
#                a= dict1['x']
#                b= dict1['y']
#                gdx.append(float(a))
#                gdy.append(float(b))
#            
#            print valb3, "gaze data3", round(abs(np.mean(gdx)),2), round(abs(np.mean(gdy)),2)
#            stat= "\n"+str(valb3)+" gaze "+ str(round(abs(np.mean(gdx)),2))+ " , "+str(round(abs(np.mean(gdy)),2))
#            
#            self.T41.insert(END,  stat)
#            
#        def getxy4(event): 
#            valx= float(event.x)+50
#            valy=float(event.y)+310
#            global valb4
#            valb4= "Button: 4 GT: "+ str(valx)+" , "+ str(valy)
#            hb_thread = threading.Thread(target=pytribe.heartbeat_loop,
#                             kwargs={})
#            hb_thread.daemon = True
#            hb_thread.start()
#            time.sleep(0.5)
#            #Start collecting samples from the eye tracker and add to a queue
#            q=Queue.Queue()
#            query_thread = threading.Thread(target=pytribe.queue_tracker_frames, args=(q,),
#                                kwargs=dict(interval=0.15))
#            query_thread.daemon=True
#            query_thread.start()
#            time.sleep(1)
#            #Extract all of the samples from the queue
#            list_of_data_dicts = pytribe.extract_queue(q)
#            time.sleep(0.5)
#            #First "average" data point
#            gdx=[]
#            gdy=[]
#            for item in list_of_data_dicts:
#            
#             
#                dict1 = item['values']['frame']['avg']
#                a= dict1['x']
#                b= dict1['y']
#                gdx.append(float(a))
#                gdy.append(float(b))
#            
#            print valb4,"gaze data4", round(abs(np.mean(gdx)),2), round(abs(np.mean(gdy)),2)
#            stat= "\n"+str(valb4)+" gaze "+str(round(abs(np.mean(gdx)),2))+ " , "+str(round(abs(np.mean(gdy)),2))
#
#            self.T41.insert(END,  stat)
#            
#        def getxy5(event): 
#            valx= float(event.x)+550,
#            valy= float(event.y)+310
#            global valb5
#            valb5= "Button: 5 GT: "+ str(valx)+" , "+ str(valy)
#            hb_thread = threading.Thread(target=pytribe.heartbeat_loop,
#                             kwargs={})
#            hb_thread.daemon = True
#            hb_thread.start()
#            time.sleep(0.5)
#            #Start collecting samples from the eye tracker and add to a queue
#            q=Queue.Queue()
#            query_thread = threading.Thread(target=pytribe.queue_tracker_frames, args=(q,),
#                                kwargs=dict(interval=0.15))
#            query_thread.daemon=True
#            query_thread.start()
#            time.sleep(1)
#            #Extract all of the samples from the queue
#            list_of_data_dicts = pytribe.extract_queue(q)
#            time.sleep(0.5)
#            #First "average" data point
#            gdx=[]
#            gdy=[]
#            for item in list_of_data_dicts:
#            
#             
#                dict1 = item['values']['frame']['avg']
#                a= dict1['x']
#                b= dict1['y']
#                gdx.append(float(a))
#                gdy.append(float(b))
#            
#            print valb5, "gaze data5", round(abs(np.mean(gdx)),2), round(abs(np.mean(gdy)),2)
#            stat= "\n"+str(valb5)+" gaze "+str(round(abs(np.mean(gdx)),2))+ " , "+str(round(abs(np.mean(gdy)),2))
#
#            self.T41.insert(END,  stat)
#            
#        def getxy6(event): 
#            valx= float(event.x)+1050
#            valy= float(event.y)+310
#            global valb6
#            valb6= "Button: 6 GT: "+ str(valx)+" , "+ str(valy)
#            hb_thread = threading.Thread(target=pytribe.heartbeat_loop,
#                             kwargs={})
#            hb_thread.daemon = True
#            hb_thread.start()
#            time.sleep(0.5)
#            #Start collecting samples from the eye tracker and add to a queue
#            q=Queue.Queue()
#            query_thread = threading.Thread(target=pytribe.queue_tracker_frames, args=(q,),
#                                kwargs=dict(interval=0.15))
#            query_thread.daemon=True
#            query_thread.start()
#            time.sleep(1)
#            #Extract all of the samples from the queue
#            list_of_data_dicts = pytribe.extract_queue(q)
#            time.sleep(0.5)
#            #First "average" data point
#            gdx=[]
#            gdy=[]
#            for item in list_of_data_dicts:
#            
#             
#                dict1 = item['values']['frame']['avg']
#                a= dict1['x']
#                b= dict1['y']
#                gdx.append(float(a))
#                gdy.append(float(b))
#            
#            print valb6, "gaze data6", round(abs(np.mean(gdx)),2), round(abs(np.mean(gdy)),2)
#            stat= "\n"+str(valb6)+" gaze "+str(round(abs(np.mean(gdx)),2))+ ", "+str(round(abs(np.mean(gdy)),2))
#
#            self.T41.insert(END,  stat)
#        
#        def getxy7(event): 
#
#            valx= float(event.x)+50
#            valy= float(event.y)+610
#            
#            valb7= "Button: 4 GT: "+ str(valx)+","+ str(valy)
#            hb_thread = threading.Thread(target=pytribe.heartbeat_loop,
#                             kwargs={})
#            hb_thread.daemon = True
#            hb_thread.start()
#            time.sleep(0.5)
#            #Start collecting samples from the eye tracker and add to a queue
#            q=Queue.Queue()
#            query_thread = threading.Thread(target=pytribe.queue_tracker_frames, args=(q,),
#                                kwargs=dict(interval=0.15))
#            query_thread.daemon=True
#            query_thread.start()
#            time.sleep(1)
#            #Extract all of the samples from the queue
#            list_of_data_dicts = pytribe.extract_queue(q)
#            time.sleep(0.5)
#            #First "average" data point
#            gdx=[]
#            gdy=[]
#            for item in list_of_data_dicts:
#            
#             
#                dict1 = item['values']['frame']['avg']
#                a= dict1['x']
#                b= dict1['y']
#                gdx.append(float(a))
#                gdy.append(float(b))
#            
#            stat= "\n"+str(valb7)+" gaze "+str(round(abs(np.mean(gdx)),2))+ ", "+str(round(abs(np.mean(gdy)),2))
#            self.T41.insert(END,  stat)
#            print valb7, "gaze data6", round(abs(np.mean(gdx)),2), round(abs(np.mean(gdy)),2)
#                 
#                 
#        def getxy8(event): 
#            valx= float(event.x)+650
#            valy= float(event.y)+610
#            
#            valb8= "Button: 5 GT: "+ str(valx)+","+ str(valy)
#            hb_thread = threading.Thread(target=pytribe.heartbeat_loop,
#                             kwargs={})
#            hb_thread.daemon = True
#            hb_thread.start()
#            time.sleep(0.5)
#            #Start collecting samples from the eye tracker and add to a queue
#            q=Queue.Queue()
#            query_thread = threading.Thread(target=pytribe.queue_tracker_frames, args=(q,),
#                                kwargs=dict(interval=0.15))
#            query_thread.daemon=True
#            query_thread.start()
#            time.sleep(1)
#            #Extract all of the samples from the queue
#            list_of_data_dicts = pytribe.extract_queue(q)
#            time.sleep(0.5)
#            #First "average" data point
#            gdx=[]
#            gdy=[]
#            for item in list_of_data_dicts:
#            
#             
#                dict1 = item['values']['frame']['avg']
#                a= dict1['x']
#                b= dict1['y']
#                gdx.append(float(a))
#                gdy.append(float(b))
#            
#            stat= "\n"+str(valb8)+" gaze "+str(round(abs(np.mean(gdx)),2))+ ", "+str(round(abs(np.mean(gdy)),2))
#            self.T41.insert(END,  stat)
#            print valb8, "gaze data6", round(abs(np.mean(gdx)),2), round(abs(np.mean(gdy)),2)
#        
#        def getxy9(event): 
#            valx= float(event.x)+1250
#            valy= float(event.y)+610
#            
#            valb9= "Button: 6 GT: "+ str(valx)+","+ str(valy)
#            hb_thread = threading.Thread(target=pytribe.heartbeat_loop,
#                             kwargs={})
#            hb_thread.daemon = True
#            hb_thread.start()
#            time.sleep(0.5)
#            #Start collecting samples from the eye tracker and add to a queue
#            q=Queue.Queue()
#            query_thread = threading.Thread(target=pytribe.queue_tracker_frames, args=(q,),
#                                kwargs=dict(interval=0.15))
#            query_thread.daemon=True
#            query_thread.start()
#            time.sleep(1)
#            #Extract all of the samples from the queue
#            list_of_data_dicts = pytribe.extract_queue(q)
#            time.sleep(0.5)
#            #First "average" data point
#            gdx=[]
#            gdy=[]
#            for item in list_of_data_dicts:
#            
#             
#                dict1 = item['values']['frame']['avg']
#                a= dict1['x']
#                b= dict1['y']
#                gdx.append(float(a))
#                gdy.append(float(b))
#            
#            stat= "\n"+str(valb9)+" gaze "+str(round(abs(np.mean(gdx)),2))+ ", "+str(round(abs(np.mean(gdy)),2))
#            self.T41.insert(END,  stat)
#            print valb9, "gaze data6", round(abs(np.mean(gdx)),2), round(abs(np.mean(gdy)),2)
##############################################################################################
                
        def startstaticui1():
            bgco= self.T45.get("1.0","end-1c")
            
            window_w =self.T42.get("1.0","end-1c")
            ww = int(float(window_w))
            window_h= self.T43.get("1.0","end-1c")
            wh = int(float(window_h))
            dimval= window_w+ "x"+window_h
            
            self.top = Toplevel()
            self.top.title('Static Test UI-1')
            self.top.wm_geometry(dimval)
            
            self.window_canv = Canvas(self.top, width=ww, height= wh, bg= bgco,highlightthickness=1, highlightbackground="black")
            self.window_canv.grid(row=0,column=0)#,rowspan=8, columnspan=3, padx = 10,pady = 10, sticky=S)
            self.button1 = Button(self.window_canv, text = "Button1", anchor = W)
            self.button1.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            self.button1_window = self.window_canv.create_window(50, 10, anchor=NW, window=self.button1)
            
            self.button2 = Button(self.window_canv, text = "Button2", anchor = W)
            self.button2.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            self.button2_window = self.window_canv.create_window(50+ww/3, 10, anchor=NW, window=self.button2)
            
            self.button3 = Button(self.window_canv, text = "Button3", anchor = W)
            self.button3.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            self.button3_window = self.window_canv.create_window(50+2*ww/3, 10, anchor=NW, window=self.button3)
            
            self.button4 = Button(self.window_canv, text = "Button4", anchor = W)
            self.button4.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            self.button4_window = self.window_canv.create_window(50, 2*wh/3+10, anchor=NW, window=self.button4)
            
            self.button5 = Button(self.window_canv, text = "Button5", anchor = W)
            self.button5.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            self.button5_window = self.window_canv.create_window(50+ww/3, 2*wh/3+10, anchor=NW, window=self.button5)
            
            self.button6 = Button(self.window_canv, text = "Button6", anchor = W)
            self.button6.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            self.button6_window = self.window_canv.create_window(50+2*ww/3, 2*wh/3+10, anchor=NW, window=self.button6)

                       
        def startdynui():
            ballsize =self.T44.get("1.0","end-1c")
            bs = int(float(ballsize))
            bgco= self.T45.get("1.0","end-1c")
            
            window_w =self.T42.get("1.0","end-1c")
            ww = int(float(window_w))
            window_h= self.T43.get("1.0","end-1c")
            wh = int(float(window_h))
            dimval= window_w+ "x"+window_h
            
            self.top = Toplevel()
            self.top.title('Test UI-Dynamic')
            self.top.wm_geometry(dimval)
            self.window_canv = Canvas(self.top, width=ww, height= wh, bg= bgco,highlightthickness=1, highlightbackground="black")
            self.window_canv.grid(row=0,column=0)#,rowspan=8, columnspan=3, padx = 10,pady = 10, sticky=S)
            ball = self.window_canv.create_oval( 0, 0, 10, 10 )
            xInc = 10
            yInc = 200
            ballX = 50
            ballY=10
            while ballY < 700:
                time.sleep( 0.05 ) #interv
                self.window_canv.delete( ball )
                ball = self.window_canv.create_oval( ballX, ballY, ballX + bs, ballY+bs, fill = "blue" )
                time.sleep(0.01)
                ballX += xInc
                if ballX > 1300 :
                    ballY += yInc
                    ballX=50
                self.window_canv.update()
                
####################################### LiveTracking main function #######################################        
        def livetrack1():
            print "Use this if you want to collect data from an eye tracker"
#            bgco= self.T45.get("1.0","end-1c")
#            
#            window_w =self.T42.get("1.0","end-1c")
#            ww = int(float(window_w))
#            window_h= self.T43.get("1.0","end-1c")
#            wh = int(float(window_h))
#            dimval= window_w+ "x"+window_h
#            
#            self.top = Toplevel()
#            self.top.title('Live_tracking_window')
#            self.top.wm_geometry(dimval)
#            
#            self.window_canv = Canvas(self.top, width=ww, height= wh, bg= bgco,highlightthickness=1, highlightbackground="black")
#            self.window_canv.grid(row=0,column=0)#,rowspan=8, columnspan=3, padx = 10,pady = 10, sticky=S)
#            self.button1 = Button(self.window_canv, text = "Button1", anchor = W)
#            self.button1.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
#            self.button1_window = self.window_canv.create_window(50, 10, anchor=NW, window=self.button1)
#            
#            self.button2 = Button(self.window_canv, text = "Button2", anchor = W)
#            self.button2.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
#            self.button2_window = self.window_canv.create_window(650, 10, anchor=NW, window=self.button2)
#            
#            self.button3 = Button(self.window_canv, text = "Button3", anchor = W)
#            self.button3.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
#            self.button3_window = self.window_canv.create_window(1250, 10, anchor=NW, window=self.button3)
#            
#            self.button4 = Button(self.window_canv, text = "Button4", anchor = W)
#            self.button4.configure(width = 10, bg="black", fg="black", relief = FLAT)
#            self.button4_window = self.window_canv.create_window(50, 310, anchor=NW, window=self.button4)
#            
#            self.button5 = Button(self.window_canv, text = "Button5", anchor = W)
#            self.button5.configure(width = 10, bg="black", fg="black", relief = FLAT)
#            self.button5_window = self.window_canv.create_window(650, 310, anchor=NW, window=self.button5)
#            
#            self.button6 = Button(self.window_canv, text = "Button6", anchor = W)
#            self.button6.configure(width = 10, bg="black", fg="black", relief = FLAT)
#            self.button6_window = self.window_canv.create_window(1250, 310, anchor=NW, window=self.button6)
#            
#            self.button7 = Button(self.window_canv, text = "Button4", anchor = W)
#            self.button7.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
#            self.button7_window = self.window_canv.create_window(50, 610, anchor=NW, window=self.button7)
#            
#            self.button8 = Button(self.window_canv, text = "Button5", anchor = W)
#            self.button8.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
#            self.button8_window = self.window_canv.create_window(650, 610, anchor=NW, window=self.button8)
#            
#            self.button9 = Button(self.window_canv, text = "Button6", anchor = W)
#            self.button9.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
#            self.button9_window = self.window_canv.create_window(1250, 610, anchor=NW, window=self.button9)            
#            
#            self.button1.bind('<Button-1>', getxy1)
#            self.button2.bind('<Button-1>', getxy2)
#            self.button3.bind('<Button-1>', getxy3)
#            self.button4.bind('<Button-1>', getxy4)
#            self.button5.bind('<Button-1>', getxy5)
#            self.button6.bind('<Button-1>', getxy6)
#            self.button7.bind('<Button-1>', getxy7)
#            self.button8.bind('<Button-1>', getxy8)
#            self.button9.bind('<Button-1>', getxy9)
############################################################################################################        
        def refresh4():
            self.c4 = Canvas(page4,width=540, height= 400, bg= "black")
            self.c4.grid(row=1,column=4,rowspan=8, columnspan=3, padx = 10,pady = 10, sticky=S)
            self.imgpg4 = PhotoImage(file='C:/Users/14233242/Documents/Python Scripts/tui1.gif')
            self.c4.create_image(6,4,image=self.imgpg4,anchor="nw")
        
        def refresh5():
            self.T34.delete(1.0, END)
            self.T31.delete(1.0, END)
            self.T32.delete(1.0, END)
            self.T33.delete(1.0, END)
            quote2 = """rainbow"""
            self.T34.insert(END, quote2)
            quote3 = """blue"""
            self.T31.insert(END, quote3)
            quote4 = """white"""
            self.T32.insert(END, quote4)
            
           
            
            
            
#######################################################################    

        nb = ttk.Notebook(t)
        nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

        page1 = ttk.Frame(nb)
        nb.add(page1, text='Home Page')
 
        page2 = ttk.Frame(nb)
        nb.add(page2, text='Data Analysis')
    
        page3 = ttk.Frame(nb)
        nb.add(page3, text='Visualizations')
        
        page4 = ttk.Frame(nb)
        nb.add(page4, text='Test UI & Track')
    
        page5 = ttk.Frame(nb)
        nb.add(page5, text='Help')
    ############### main page ###################
        self.tex1 = Label(page1,  text='GazeVisual: A Graphical Software Tool \nfor Performance Evaluation of Eye Trackers', font = 'Lucida 18 bold').grid(row=0,column=1, columnspan=2, padx = 20,pady = 5,sticky = S)#ack(fill=X, padx=10,pady=10)
        self.f11 = LabelFrame(page1, text = 'Software Description', font = "Helvetica 12 bold", height = 340, width = 300).grid(row=1,column=0,padx = 10,pady = 5,sticky = NW)#.pack(fill=X,side=LEFT,padx=20,pady=5)
        self.f12 = LabelFrame(page1, text = 'Authors & License', font = "Helvetica 12 bold", height = 200, width = 300).grid(row=2,column=0,padx = 10,pady = 5,sticky = NW)#.pack(fill=X,side=LEFT,padx=20,pady=5)
        self.fnew1 = LabelFrame(page1, text = 'Features & utilities', font = "Helvetica 12 bold", height = 140, width = 550).grid(row=2,column=2,padx = 0,pady = 5,sticky = SW)#.pack(fill=X,side=LEFT,padx=20,pady=5)
        self.c1 = Canvas(page1,width=550, height= 400, bg= "black")
        self.c1.grid(row=1,column=1,rowspan=3, columnspan=2, padx = 30,pady = 5, sticky=N)
        self.texv11 = Label(page1,  text=  
    """   GazeVisual is a solution for complete 
   evaluation of eye trackers and eye tracking 
   based systems and applications.
   
   It implements several accuracy metrics 
   and visualizations for understanding 
   eye tracking data qyality and characteristics.
   
   Users can navigate to the Data Analysis or 
   Visualizations tabs to access different evaluation 
   tools. The required input is the 
   gaze and corresponding  ground truth 
   data coordinates saved in a CSV file.  
     
   The Help tab provides information on the
   formatting of input data files and other 
   functionalities built in this software 
   interface.""", 
                   font = 'Helvetica 9 bold',justify="left", anchor= "nw").grid(row=1,column=0, padx = 0,pady =0)
        self.texv12 = Label(page1,  text=  
    """   Creators: Anuradha Kar, Peter Corcoran 
   College of Engineering & Informatics
   National University of Ireland, Galway, 2018.
       
   GazeVisual is an open source software 
   intended for eye gaze researchers. It is 
   flexible towards further development and 
   contributions from the eye gaze and related 
   research & development groups.   
   """,
                   font = 'Helvetica 9 bold',justify="left", anchor= "nw").grid(row=2,column=0, padx = 0,pady =0)
        
        
        
        self.img = PhotoImage(file='C:/Users/14233242/Documents/Python Scripts/gui_main2.gif')
        self.c1.create_image(6,4,image=self.img,anchor="nw")
        
        self.c2 = Canvas(page1,width=550, height= 90, bg= "black")
        self.c2.grid(row=2,column=1,rowspan=1, columnspan=2, padx = 30,pady = 25, sticky=S)
        self.imgu1 = PhotoImage(file='C:/Users/14233242/Documents/Python Scripts/utilities1.gif')
        self.c2.create_image(6,4,image=self.imgu1,anchor="nw")
        
        
    
    ############################ Metrics page ###################################
        self.tex2 = Label(page2,  text='Calculate accuracy metrics & view results/plots', font = 'Lucida 16 bold').grid(row=0,column=3, columnspan=2, padx = 20,pady = 10)#ack(fill=X, padx=10,pady=10)
        self.f21 = LabelFrame(page2, text = 'Accuracy parameters ', font = "Helvetica 12 bold", height = 600, width = 420).grid(row=1,column=0,rowspan=8, columnspan=3,padx = 10,pady = 5,sticky = NW)#.pack(fill=X,side=LEFT,padx=20,pady=5)
        self.f23 = LabelFrame(page2, text = 'Output Console', font = "Helvetica 12 bold", height = 170, width = 550).grid(row=3,column=3,rowspan=7,columnspan=3, padx = 10,pady = 5,sticky = SW)
    
    ######################## old canvas
    
        self.texv26= Label(page2,  text=  """  
    Load a gaze data CSV file using the Upload csv file' 
    button below. The gaze angular accuracy and data statistics 
    outputs can be viewed in the output console. Various 
    gaze data analysis plots may be created and viewed in 
    the plot area. Use buttons Data1 and Data2 to load multiple 
    gaze datasets to compare and plot data statistics. """, font = 'Helvetica 10',justify="left", anchor= "w").grid(row=1,column=0, columnspan=3,padx = 25,pady =25, sticky = NW)#, padx = 5, pady = 5,sticky= N )
    
        self.texv23 = Label(page2,  text= "Load gaze data" ,fg="blue", font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=2,column=0, padx = 20,pady =5, sticky = NW)
        self.but21= Button(page2, text='Upload csv file',height=2, width=23, font='Lucida 10 bold',fg='black',command=load_data_new).grid(row=2,column=1,columnspan=2,padx = 5,pady =5,sticky= NW)
        
        self.texv25= Label(page2,  text= "Analysis results/plots" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=3,column=0, padx = 20,pady =5, sticky = NW)#, padx = 5, pady = 5,sticky= N )
        self.but23=Button(page2, text='Statistics',height=2,width=9, font='Lucida 10 bold', fg='black', command= accu_met).grid(row=3,column=1,columnspan=1,padx = 5,pady =0,sticky= NW)#, padx = 5, pady = 5,sticky= W )
        self.but24=Button(page2, text='Yaw/Pitch', height=2, width=9, font='Lucida 10 bold',fg='black',command= yawpitch).grid(row=3,column=2, padx = 0,pady =0,sticky= NW)
           
        self.texv24 = Label(page2,  text= "Gaze angle/Zscore" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=4,column=0, padx = 25,pady =5, sticky = NW)
        self.but22= Button(page2, text='Z score plot', height=2,  width=23, font='Lucida 10 bold',fg='black',command= zscore).grid(row=4,column=1,columnspan=2,padx = 5,pady =5,sticky= NW)
    
        
        self.texv26= Label(page2,  text= "Upload multiple files" , fg="blue", font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=5,column=0, padx = 20,pady =5, sticky = NW)
        self.but25=Button(page2, text='Data-1',height=2, width=9, font='Lucida 10 bold',fg='black',command= upload_d1).grid(row=5,column=1,columnspan=1,padx = 5,pady =0,sticky= NW )
        self.but26=Button(page2, text='Data-2',height=2, width=9, font='Lucida 10 bold',fg='black',command= upload_d2).grid(row=5,column=2,columnspan=1,padx = 0,pady =0,sticky= NW )
        self.texv27= Label(page2,  text= "Compare datasets" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=6,column=0, padx = 25,pady=5, sticky = NW)
        self.but27= Button(page2, text='Statistics table',height=2,width=23,font='Lucida 10 bold', fg='black',command= compare_data).grid(row=6,column=1,columnspan=2,padx = 5,pady =0,sticky= NW)
        
        self.texv27= Label(page2,  text= "Plot datasets" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=7,column=0, padx = 25,pady=5, sticky = NW)
        self.but28= Button(page2, text='Gaze angles',height=2,width=10,font='Lucida 10 bold', fg='black',command =gaze_angles).grid(row=7,column=1,columnspan=1,padx = 5,pady =0,sticky= NW)
        self.but281=Button(page2, text='KDE', height=2, width=9, font='Lucida 10 bold',fg='black',command= kde_compare).grid(row=7,column=2, padx = 0,pady =0,sticky= NW)

    
    ################# output text box
    
        self.T21 = Text(page2, height=8, width=45,bd = 5)
        self.T21.grid(row=5, column=3, rowspan= 4, columnspan=2,padx = 20, pady = 15,sticky= SW)
        global quote21
        quote21 = """
    The gaze data accuracy and statistical 
    results will be printed here. Press 
    Save results to save console values in 
    a text file. Press Refresh to clear 
    the console and plot area."""
        self.T21.insert(END, quote21)
        self.but28=Button(page2, text='Save results',height=1,width=13,font='Lucida 10 bold', fg='black', command=file_save2).grid(row=6,column=4,padx = 10,pady =0,sticky= E)
        self.but29=Button(page2, text='Refresh',width=13,font='Lucida 10 bold', fg='black',command= clear_text_field).grid(row=7,column=4,padx = 10,pady =0,sticky= E)
    
    
    ########### canvas on page 2 #######################
     
        f1 = Figure(figsize=(5.5,3.7), dpi=100)
        self.canvas1 = FigureCanvasTkAgg(f1, page2)
        self.canvas1.show()
        t1 = np.arange(0, 3, .01)
        f1.add_subplot(111).plot(t1, 2 * np.sin(2 * np.pi * t1))
   
        self.toolbar_frame1 = Frame(page2) 
        self.toolbar_frame1.grid(row=2,column=3,rowspan=7,columnspan=3,padx = 0,pady = 5,sticky= W) 
        self.toolbar1 = NavigationToolbar2TkAgg( self.canvas1, self.toolbar_frame1 )

        self.canvas1._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)

      
    
##############################################################################################    
#    ##################################### Visual page  #####################
        self.tex31 = Label(page3,  text='Visualize gaze data characteristics', font = 'Lucida 16 bold').grid(row=0,column=3, columnspan=3, padx = 20,pady = 10,sticky = W)#ack(fill=X, padx=10,pady=10)
        self.f31 = LabelFrame(page3, text = 'Visualizations ', font = "Helvetica 12 bold", height = 600, width = 420).grid(row=1,column=0,rowspan=8, columnspan=3,padx = 10,pady = 5,sticky = NW)#.pack(fill=X,side=LEFT,padx=20,pady=5)
        self.f33 = LabelFrame(page3, text = 'Alter plot features', font = "Helvetica 12 bold", height = 170, width = 550).grid(row=3,column=3,rowspan=7,columnspan=4, padx = 10,pady = 5,sticky = SW)

#    
        self.texv36= Label(page3,  text=  """  
    Load gaze input data CSV file to implement several 
    visualization functions and display them in the plot area.
    Load multiple datasets using the buttons Data-1 and Data-2 
    and study the nature of relationships between them using 
    histograms, regression, bar and box plots.Plot attributes 
    like colormaps and background may be altered. Also one can 
    save, pan and zoom into the plots. Click Add to add text to the 
    plot area and click Refresh to reset the plot area.
        """, font = 'Helvetica 10',justify="left", anchor= "w").grid(row=1,column=0, columnspan=3,padx = 25,pady =25, sticky = NW)    
#    
        self.texv32 = Label(page3,  text= "Load gaze data" ,fg="blue",font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=2,column=0, padx = 25,pady =5, sticky = NW)
        self.but31=Button(page3, text='Upload csv file',height=2, width=16, font='Lucida 10 bold',fg='black', command= load_data_vis).grid(row=2,column=1,columnspan=2,padx = 10,pady =5,sticky= NW)
     
    
        self.but33=Button(page3, text='Data density plot',height=2,width=18, font='Lucida 10 bold', fg='black',command=data_density).grid(row=4,column=0,padx = 20,pady =0,sticky= NW)
        self.but34=Button(page3, text='Mean/SD',height=2,width=8, font='Lucida 10 bold', fg='black',command= bubble).grid(row=4,column=1,padx = 4,pady =0,sticky= NW)#, padx = 5, pady = 5,sticky= W )
        self.but35=Button(page3, text='3D plot', height=2, width=8, font='Lucida 10 bold',fg='black',command=threedplot).grid(row=4,column=2, padx = 5,pady =0,sticky= NW)
#    
        self.texv26= Label(page3,  text= "Upload multiple files" ,fg="blue",font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=5,column=0, padx = 25,pady =5, sticky = NW)
        self.but36=Button(page3, text='Data-1',height=2, width=8, font='Lucida 10 bold',fg='black',command= load_data_vis1).grid(row=5,column=1,columnspan=1,padx = 6,pady =0,sticky= NW )
        self.but37=Button(page3, text='Data-2',height=2, width=8, font='Lucida 10 bold',fg='black',command= load_data_vis2).grid(row=5,column=2,columnspan=1,padx = 6,pady =0,sticky= NW )
        self.texv27= Label(page3,  text= "Compare datasets" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=6,column=0, padx = 25,pady=5, sticky = NW)
        self.but38=Button(page3, text='Histograms',height=2,font='Lucida 10 bold', fg='black',command=plothist_v2).grid(row=6,column=1,padx = 5,pady =0,sticky= NW)
        self.but39=Button(page3, text='Regression',height=2,font='Lucida 10 bold', fg='black',command=reg_plot).grid(row=6,column=2,padx = 5,pady =0,sticky= NW)
        
        self.but381=Button(page3, text='Error line plots',height=2, width=18,font='Lucida 10 bold', fg='black',command=line_plot).grid(row=7,column=0,padx = 20,pady =0,sticky= NW)
        self.but38=Button(page3, text='Box plot',height=2, width=9,font='Lucida 10 bold', fg='black',command=box_plot).grid(row=7,column=1,padx = 6,pady =0,sticky= NW)
        self.but39=Button(page3, text='Bar plot',height=2, width=9,font='Lucida 10 bold', fg='black',command=bar_plot).grid(row=7,column=2,padx = 6,pady =0,sticky= NW)
        
        
        self.texv29= Label(page3,  text= "Error histogram" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=3,column=0, padx = 25,pady =5, sticky = NW)
     
        self.but_plot=Button(page3, text='Plot',height=1,width=8,font='Lucida 10 bold', fg='black',command= plothist_v1).grid(row=3,column=2,padx = 0,pady =0,sticky= NW)
        self.T35= Text(page3, height=1, width=8,bd = 5)
        self.T35.grid(row=3,column=1,padx = 0,pady =0,sticky= NW)  #screen size

        quote35 = """20"""
        self.T35.insert(END, quote35)    
#    #################### alter plot features ##########################
        self.texv27= Label(page3,  text= "Set plot color" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=6,column=3, padx = 15,pady =5, sticky = NE)
        self.texv28= Label(page3,  text= "Set background" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=7,column=3, padx = 15,pady =5, sticky = NE)
    
    
        self.but310=Button(page3, text='Refresh',font='Lucida 10 bold', height=1, width=5,fg='black',command= refresh5).grid(row=7,column=5,padx =10,pady =0,sticky= NE)
        self.but311=Button(page3, text='Add',font='Lucida 10 bold',height=1, width=5, fg='black').grid(row=6,column=5,padx =10,pady =0,sticky= NE)
        self.T31 = Text(page3, height=1, width=10,bd = 5)
        self.T31.grid(row=6, column=4, rowspan= 1, padx = 0, pady = 5,sticky= NW)
        self.T32 = Text(page3, height=1, width=10,bd = 5)
        self.T32.grid(row=7, column=4, rowspan= 1, padx =0, pady = 5,sticky= NW)
        self.T33 = Text(page3, height=1, width=12,bd = 5)
        self.T33.grid(row=6, column=5, rowspan= 1, padx =0, pady = 5,sticky= NW)
        quote1 = """ """
        self.T33.insert(END, quote1)
    
        self.T34 = Text(page3, height=1, width=12,bd = 5)
        self.T34.grid(row=7, column=5, rowspan= 1, padx =0, pady = 5,sticky= NW)
        quote2 = """rainbow"""
        self.T34.insert(END, quote2)
        
        quote3 = """blue"""
        self.T31.insert(END, quote3)
    
        quote4 = """white"""
        self.T32.insert(END, quote4)
    
    ################## canvas on page 3
        f = Figure(figsize=(5.5,3.7), dpi=100)
        self.canvas = FigureCanvasTkAgg(f, page3)
        self.canvas.show()
        t3 = np.arange(0, 3, .01)
        f.add_subplot(111).plot(t3, 2 * np.sin(2 * np.pi * t3))
   
        self.toolbar_frame = Frame(page3) 
        self.toolbar_frame.grid(row=2,column=3,rowspan=6,columnspan=3,padx = 0,pady = 5,sticky= W) 
        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.toolbar_frame )

        self.canvas._tkcanvas.grid(row=1,column=3,rowspan=5, columnspan=3, padx = 0,pady = 0, sticky=N)
###################################################################################################
########################### Test UI and Live track ##################################
        self.f41 = LabelFrame(page4, text = 'Test UI', font = "Helvetica 12 bold", height = 450, width = 400).grid(row=0,column=0,rowspan=8, columnspan=3,padx = 10,pady = 5,sticky = NW)#.pack(fill=X,side=LEFT,padx=20,pady=5)
        self.texv40= Label(page4,  text=  """ 
User interfaces having known target locations for 
testing an eye tracker may be created here. Both 
static and dynamic UIs may be created and customized.
The Static UI-1 shows buttons where a user should 
look at and click. In Static UI-2 and Dynamic UI, a 
user follows a ball appearing on screen """, font = 'Helvetica 10',justify="left", anchor= "w").grid(row=1,column=0, columnspan=3,padx = 0,pady =10, sticky = S)
        
        
        self.f42 = LabelFrame(page4, text = 'LiveTracking', font = "Helvetica 12 bold", height = 200, width = 400).grid(row=8,column=0,rowspan=6, columnspan=3,padx = 10,pady = 5,sticky = NW)
        self.c4 = Canvas(page4,width=530, height= 420, bg= "black")
        self.c4.grid(row=1,column=4,rowspan=8, columnspan=3, padx = 10,pady = 10, sticky=N)
        self.imgpg4 = PhotoImage(file='C:/Users/14233242/Documents/Python Scripts/tui1.gif')
        self.c4.create_image(6,4,image=self.imgpg4,anchor="nw")
        
        self.f43 = LabelFrame(page4, text = 'Gaze data output console', font = "Helvetica 12 bold", height = 200, width = 550).grid(row=8,column=3,rowspan=7,columnspan=4, padx = 10,pady = 5,sticky = NW)
        self.T41 = Text(page4, height=8, width=50,bd = 5)
        self.T41.grid(row=9, column=3, rowspan= 4, columnspan=2,padx = 10, pady = 5,sticky= SW)
        global quote41
        quote41 = """
    On using the LiveTracking function, 
    the gaze data obtained from an eye tracker 
    connected to this computer will be printed 
    here. Press Save results to save tracker 
    data and ground truth values in a text file. 
    Press Refresh to clear console area. """
        self.T41.insert(END, quote41)
        self.but41=Button(page4, text='Save results',height=1,width=13,font='Lucida 10 bold', fg='black', command=file_save2).grid(row=10,column=5,padx = 5,pady =0,sticky= E)
        self.but42=Button(page4, text='Refresh',width=13,font='Lucida 10 bold', fg='black',command= refresh4).grid(row=11,column=5,padx = 5,pady =0,sticky= E)
        
        self.texv41= Label(page4,  text= "Set window size" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=2,column=0, padx = 15,pady =10, sticky = NW)
        self.T42= Text(page4, height=1, width=8,bd = 5)
        self.T42.grid(row=2,column=1,padx = 5,pady =5,sticky= NW)  #screen size
        self.T43= Text(page4, height=1, width=7,bd = 5)
        self.T43.grid(row=2,column=2,padx = 5,pady =5,sticky= NW)  #screen size
        quote42 = """1366"""
        self.T42.insert(END, quote42)
        quote43 = """768"""
        self.T43.insert(END, quote43)
        self.texv42= Label(page4,  text= "Set stimulus size/speed" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=3,column=0, padx = 15,pady =5, sticky = NW)
        
        self.texv42= Label(page4,  text= "Change bg/stimuli color" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=4,column=0, padx = 15,pady =5, sticky = NW)
        
        self.texv43 = Label(page4,  text= "Show static UI-1" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=5,column=0, padx = 15,pady =5, sticky = NW)
        self.texv44 = Label(page4,  text= "Show dynamic UI" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=7,column=0, padx = 15,pady =5, sticky = NW)
        self.texv45 = Label(page4,  text= "Show static UI-2" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=6,column=0, padx = 15,pady =5, sticky = NW)
        
        self.but43=Button(page4, text='Demo',height=1,width=8,font='Lucida 10 bold', fg='black', command=demostaticui2).grid(row=6,column=1,padx = 10,pady =0,sticky= NW)
        self.but44=Button(page4, text='Start',width=8,font='Lucida 10 bold', fg='black',command= startstaticui2).grid(row=6,column=2,padx = 10,pady =0,sticky= NW)
        
        self.but45=Button(page4, text='Demo',height=1,width=8,font='Lucida 10 bold', fg='black', command=demodynui).grid(row=7,column=1,padx = 10,pady =0,sticky= NW)
        self.but46=Button(page4, text='Start',width=8,font='Lucida 10 bold', fg='black',command= startdynui).grid(row=7,column=2,padx = 10,pady =0,sticky= NW)
        
        self.but47=Button(page4, text='Demo',height=1,width=8,font='Lucida 10 bold', fg='black', command=demostaticui1).grid(row=5,column=1,padx = 10,pady =5,sticky= NW)
        self.but48=Button(page4, text='Start',width=8,font='Lucida 10 bold', fg='black',command= startstaticui1).grid(row=5,column=2,padx = 10,pady =0,sticky= NW)
        
        
        self.T44= Text(page4, height=1, width=8,bd = 5)
        self.T44.grid(row=3,column=1,padx = 5,pady =5,sticky= NW)  #screen size
        self.T45= Text(page4, height=1, width=8,bd = 5)
        self.T45.grid(row=4,column=1,padx = 5,pady =5,sticky= NW)  #screen size
        self.T46= Text(page4, height=1, width=8,bd = 5)
        self.T46.grid(row=3,column=2,padx = 5,pady =5,sticky= NW)
        self.T47= Text(page4, height=1, width=8,bd = 5)
        self.T47.grid(row=4,column=2,padx = 5,pady =5,sticky= NW)
        
        quote44 = """10"""
        self.T44.insert(END, quote44)
        
        quote45 = """black"""
        self.T45.insert(END, quote45)
        
        quote46 = """3"""
        self.T46.insert(END, quote46)
        
        quote47 = """grey"""
        self.T47.insert(END, quote47)
        
        self.texv40= Label(page4,  text=  """ 
Connect an eye tracker and calibrate it. Then press
'Start tracking' to fetch data from the tracker without
or with a Test UI to collect gaze data. """, font = 'Helvetica 10',justify="left", anchor= "w").grid(row=10,column=0, columnspan=3,padx = 0,pady =10, sticky = N)
      
        self.texv42= Label(page4,  text= "Start with Test UI" ,font = 'Helvetica 12 bold',justify="left", anchor= "w").grid(row=11,column=0, padx = 15,pady =5, sticky = NW)

        self.but47=Button(page4, text='Start tracking',height=1,width=20,font='Lucida 10 bold', fg='black', command=livetrack1).grid(row=11,column=1,columnspan=2,padx = 10,pady =0,sticky= NW)

####### help page############################################################
        self.ch1 = Canvas(page5,width=900, height= 700, bg= "black")
        self.ch1.grid(row=1,column=1,rowspan=3, columnspan=2, padx = 30,pady = 5, sticky=N)
        self.imgh1 = PhotoImage(file='C:/Users/14233242/Documents/Python Scripts/help_page1.gif')
        self.ch1.create_image(6,4,image=self.imgh1,anchor="nw")
  

GUI(t)
img = PhotoImage(file='C:/Users/14233242/Documents/Python Scripts/eye2.gif')
t.tk.call('wm', 'iconphoto', t._w, img)
t.mainloop()
