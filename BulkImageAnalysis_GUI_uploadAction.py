# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:20:55 2021

@author: atter
"""


import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
from skimage.io import imread, imshow
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from skimage import measure, filters, morphology
from skimage import measure
import os
w = tk.Tk()
w.title("Fluorescent image analyser")


def UploadAction(event=None):
# dict with imageid as key and path and otsu as value
    directory = filedialog.askdirectory()
    print(directory)
    global ImRows
    global cells #make the var global for later use
    global TH
    Paths_and_TH=[]
    import ntpath
    global images
    images = {} #dictionary with keys as image IDs and values contain lists consisting of path
    #to the image as well as its respective otsu value
    
    for imagefile in os.listdir(directory):
        #print(os.listdir(directory))
        imagepath=directory + "/" + imagefile   #create first of dic values, i.e the path
        # 
        print(imagepath)
        imagename=ntpath.basename(imagepath)#create dic key
        #print(imagename)
        #get the threshold
        cells = rgb2gray(imread(imagepath))
        TH = filters.threshold_otsu(cells)  #apply threshold, second of dic values

        #append everything into the dictionary
        Paths_and_TH.append(imagepath)  #append the values
        Paths_and_TH.append(TH)
        images[imagename]=Paths_and_TH
        
        Paths_and_TH.clear()
        #now the image should be saved into the dictionary so that it can be used later
    num_of_images= len(images)
    lbl_numbers.config(text=num_of_images)

        
btn1 = tk.Button(master=w, text='Select an image directory', command=UploadAction)
lbl_txt = tk.Label(master=w, text="Number of image files in directory:")

lbl_numbers = tk.Label(master=w, text="")

btn1.pack()
lbl_txt.pack()
lbl_numbers.pack()
w.mainloop()
