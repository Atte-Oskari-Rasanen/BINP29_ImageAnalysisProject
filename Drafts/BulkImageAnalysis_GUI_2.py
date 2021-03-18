# -*- coding: utf-8 -*-

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

    global ImRows
    global cells #make the var global for later use
    ImRows=[]
    directory = filedialog.askdirectory()
    filepaths  = [os.path.join(directory, name) for name in os.listdir(directory)]
    all_images = []

    for path in filepaths:
        with open(path) as fIn:
            cells = rgb2gray(imread(os.path.join(directory,fIn))

            # filename=filename.split(" ")[1]
            fIn=fIn.name
            ImRows['ImageID']=fIn

def Thresholds():
    global TH_vals
    global TH
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

    lbl_choice = tk.Label(master=w2, text="Enter own threshold or select automatically defined one based on Otsu's method (recommended)")
    
    lbl_choice.pack()
    btn_stats_a.pack()
    btn_stats_b.pack()
    entry.pack()
    lbl_stats.pack()
    w2.mainloop()


btn1 = tk.Button(master=w, text='Select an image directory', command=UploadAction)
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

