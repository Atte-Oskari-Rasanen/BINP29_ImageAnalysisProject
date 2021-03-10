# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:29:39 2021

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

w = tk.Tk()
w.title("Fluorescent image analyser")

from tkinter import filedialog

def UploadAction(event=None):
    imagefile = filedialog.askopenfilename()
    print('Selected:', imagefile)
    global cells

    cells = rgb2gray(imread(imagefile))

    return(cells)

def Thresholds():
    TH_vals = {}
    cell_range = np.unique(cells)
    cell_range=np.round(cell_range, 3)
    TH = filters.threshold_otsu(cells)  #apply threshold
    # TH=str(round(TH, 3)
    TH_vals["cell value ranges"]=cell_range
    TH_vals["Otsu threshold"]=TH
    #print("Cell value range: ", cell_range, "Threshold defined by Otsu's method: ", TH)
    #value = str(lbl_value["text"])
    #lbl_value["text"] = "Cell value range: ", cell_range, "Threshold defined by Otsu's method: ", TH
    lbl_value.config(text=TH_vals)

def create_window():
    w2 = tk.Toplevel(w)

    def ImageStats():
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
    lbl_stats = tk.Label(master=w2, text="Stats appear here after you have entered threshold")
    btn_stats = tk.Button(
        master=w2,
        text="Get stats",
        command=ImageStats
    )
    entry.pack()
    lbl_stats.pack()
    btn_stats.pack()
    w2.mainloop()


btn1 = tk.Button(master=w, text='Click here to open a file', command=UploadAction)
btn_ready = tk.Button(
    master=w,
    text="Get threshold values",
    command=lambda:[Thresholds(), create_window()]
)
lbl_info = tk.Label(master=w, text="The values found: ")
lbl_value = tk.Label(master=w, text="")


root = tk.Tk()

btn1.pack()
btn_ready.pack()
lbl_info.pack()
lbl_value.pack()
w.mainloop()

