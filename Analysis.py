#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 14:48:14 2022

@author: Mathew
"""

from skimage.io import imread
import os
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.cluster import DBSCAN
from skimage import filters,measure
from skimage.filters import threshold_local
# Open all files with this: 
filename_contains = "_515.tif"

# Pixel threhsold
pixel_thresh=5

# Where to store data:
root_path="/Users/Mathew/Documents/Current analysis/Lipo/"

# Folders to look in:
    
pathList = []

pathList.append(r"/Users/Mathew/Documents/Current analysis/Lipo/1in100liposomes_1uMC12_play_2022-06-16_09-37-49")
pathList.append(r"/Users/Mathew/Documents/Current analysis/Lipo/1in100liposomes_10nMC12_2022-06-16_10-17-44")

# Useful functions

def load_image(toload):
    
    image=imread(toload)
    
    return image

def z_project(image):
    
    mean_int=np.max(image,axis=0) 
  
    return mean_int

def save_im(image,path,name):
    im = Image.fromarray(image)
    im.save(path+'/'+name)

def threshold_image(input_image):
    threshold_value=filters.threshold_otsu(input_image)  
    # threshold_value=1200
    # threshold_value=input_image.mean()+2*input_image.std()
    # print(threshold_value)
    binary_image=input_image>threshold_value
    
    return threshold_value,binary_image

# Label and count the features in the thresholded image:
def label_image(input_image):
    labelled_image=measure.label(input_image)
    number_of_features=labelled_image.max()
 
    return number_of_features,labelled_image

def analyse_labelled_image(labelled_image,original_image):
    measure_image=measure.regionprops_table(labelled_image,intensity_image=original_image,properties=('area','perimeter','centroid','orientation','major_axis_length','minor_axis_length','mean_intensity','max_intensity'))
    measure_dataframe=pd.DataFrame.from_dict(measure_image)
    return measure_dataframe

Output_all_cases = pd.DataFrame(columns=['Path','Number_of_events','Intensity_mean'])

for path in pathList:
    # Integer to make file
    j=0
    # Look for files:
    for root, dirs, files in os.walk(path):
                for name in files:
                        if filename_contains in name:
         
                                    resultsname = name
                                    print(resultsname)
                                    
                                    # New path to make
                                    newpath=path+'/'+str(j)
                                    if not os.path.isdir(newpath):
                                        os.mkdir(newpath)
                                    
                                    j+=1
                                    
                                    #  Load the image
                                    image=load_image(path+'/'+resultsname)
                                    
                                    # Z-project the image
                                    
                                    flat=z_project(image)
                                    
                                    save_im(flat,newpath,'flat.tif')
                                    
                                    # Thresholding
                                    
                                    threshold,binary=threshold_image(flat)
                                    save_im(binary,newpath,'binary.tif')
                                    
                                    # Label the image
                                    
                                    number,labelled=label_image(binary)
                                    save_im(labelled,newpath,'labelled.tif')
                                    
                                    
                                    # Analyse the image
                                    analysis=analyse_labelled_image(labelled,flat)
                                    
                                    
                                    index_names = analysis[analysis['area']<pixel_thresh].index
                                    analysis.drop(index_names, inplace = True)
                                    
                                    analysis.to_csv(newpath + '/' + 'Metrics.csv', sep = '\t')
                                    
                                    
                                    intensities=analysis['max_intensity']
                                    plt.hist(intensities, bins = 20,range=[1000,5000], rwidth=0.9,color='#ff0000')
                                    plt.xlabel('Intensity (ADU)',size=20)
                                    plt.ylabel('Number of Features',size=20)
                                    plt.title('Intensity',size=20)
                                    plt.savefig(newpath+"/intensities.pdf")
                                    plt.show()
                                    
                                    labeltot=len(intensities)
                                    mean_intensity=np.mean(intensities)
                                    
                                    Output_all_cases = Output_all_cases.append({'Path':newpath,'Number_of_events':labeltot,'Intensity_mean':mean_intensity},ignore_index=True)


                                    Output_all_cases.to_csv(root_path + 'all_metrics.csv', sep = '\t')