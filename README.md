# GazeVisual-Lib
The GazeVisual-Lib is a repository of software tools for practical evaluation of eye trackers and gaze data quality. All codes in this repository are released under GNU General Public License v3.0.

This repository contains a set of methods implemented as Python codes which can be used on gaze data from generic/commercial eye trackers to evaluate their quality. The codes need Python 2.7 and the libraries imported in each code to be installed in order to run. Also the gaze data should be formatted properly before input to the evaluation codes. Details on data formatting are in the "Gaze data pre-processing" folder.

The repository also contains the source code for "GazeVisual" which is a graphical software tool that implements various metrics and visualizations for evaluating eye gaze datasets. It is in the form of a graphical user interface which will enable gaze researchers and general eye tracker users to effortlessly evaluate the data quality from their eye trackers. Gaze data files can be uploaded to the software to estimate various gaze data accuracy metrics, generate visualizations and extract valuable information regarding gaze data characteristics and determine the capabilities and limits of an eye tracker. Details about input data format for this software are in the “GazeVisual GUI Tool” folder. Links to several demo videos of the GazeVisual software showing its operations may alsobe found in this folder.

Authors: Anuradha Kar, Peter Corcoran
Concept of the gaze data evaluation methods may be found in the paper: 
Anuradha Kar, Peter Corcoran: Performance Evaluation Strategies for Eye Gaze Estimation Systems with Quantitative Metrics and Visualizations. Sensors 18(9): 3151 (2018)
https://www.mdpi.com/1424-8220/18/9/3151

# Installation
To run the codes, Python 2.7 needs to be installed along with the following Python libraries : Tkinter, Pygame, Statsmodels, Seaborn , CSV, Pandas, Sklearn. Scipy, Numpy, Matplotlib, PIL. After this, the codes and relevant data from this repository may be downloaded to a users computer and run as normal Python files in the above Python environment.

# Codes and data
The codes need sample gaze data collected from an eye tracker whose data quality is to be tested. Please follow the column and header conventions in your CSV files as shown in the sample input files included in the repository. Each folder has documentation regarding the codes present in it. Also the codes are commented to make it easy for users to understand the functions implemented.

# Usage
If a user has sample eye gaze data (in pixel coordinates) they need to format their gaze data as shown in the sample input files included in the "Gaze data pre-processing" folder and run the main_proc.py file on them to create an output CSV file with processed gaze data. This output CSV file can then be used with the remaining data evaluation codes. For using the GazeVisual GUI tool, sample gaze and ground truth data has to be formatted in the way shown in the “GazeVisual GUI Tool” folder and saved as a CSV file. This file can then be used with the software to view results.

Note that directly downloading the CSV files may sometime cause problems, so copy the contents of the sample input files provided in the repository to an empty CSV file and save it to use it with the codes and software. Else sample data from the following download link may be used:

Sample data link:
https://1drv.ms/f/s!AnJPJrn6UpiohnwTsfYSz9MYQdQ8


Anuradha Kar,
National University of Ireland, Galway,
For any questions, please mail to : a.kar2@nuigalway.ie

