# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:02:13 2021

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


def Thresholds():   #if the user wants to use own threshold, this function gives some suggestions
    global cell_range
    cell_range = np.unique(cells)
    cell_range=np.round(cell_range, 3)
    lbl_value.config(text=cell_range)

def create_window():
    w2 = tk.Toplevel(w)

    def ImageStats_a():
        ImRows={}
        cells_bw=cells>float(entry.get())
        labels = measure.label(cells_bw)
        cell_count=labels.max()
        ImRows['Number_of_cells']=cell_count
        Average_size=labels.mean()
        ImRows['Average_cell_size']=Average_size
        ImRows['Threshold_used']=float(entry.get())
        lbl_stats.config(text=ImRows)
    entry = tk.Entry(w2)
    lbl_choice = tk.Label(master=w, text="Enter own threshold or select automatically defined one based on Otsu's method (recommended)")
    lbl_stats = tk.Label(master=w2, text="Stats appear here after you have entered threshold")
    btn_stats_a = tk.Button(   #btn_stats_a used if chose option a) --- use of own threshold
        master=w2,
        text="Apply own threshold",
        command=ImageStats_a
    )
    def ImageStats_b():
        ImRows={}
        cells_bw=cells>TH
        labels = measure.label(cells_bw)
        cell_count=labels.max()
        ImRows['Number_of_cells']=cell_count
        Average_size=labels.mean()
        ImRows['Average_cell_size']=Average_size
        ImRows['Threshold_used']=float(entry.get())
        lbl_stats.config(text=ImRows)

    btn_stats_b = tk.Button(   #btn_stats_a used if chose option b) --- use of otsu's threshold
        master=w2,
        text="Apply Otsu's threshold",
        command=ImageStats_b
    )

    
    btn_stats_a.pack()
    entry.pack()

    btn_stats_b.pack()
    lbl_choice
    lbl_stats.pack()
    w2.mainloop()
btn1 = tk.Button(master=w, text='Select an image directory', command=UploadAction)
lbl_txt = tk.Label(master=w, text="Number of image files in directory:")

lbl_numbers = tk.Label(master=w, text="")

############

btn_ready = tk.Button(
    master=w,
    text="Select threshold values",
    command=lambda:[Thresholds(), create_window()]
)
lbl_info = tk.Label(master=w, text="The values found: ")
lbl_value = tk.Label(master=w, text="")


# root = tk.Tk()

btn1.pack()
lbl_txt.pack()
lbl_numbers.pack()
btn_ready.pack()
lbl_info.pack()
lbl_value.pack()
w.mainloop()

