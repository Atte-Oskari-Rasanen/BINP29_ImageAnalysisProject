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
from win32com.client import Dispatch
import ntpath
import re
w = tk.Tk()
w.title("Fluorescent image analyser")


def UploadAction(event=None):
# dict with imageid as key and path and otsu as value
    global directory
    directory = filedialog.askdirectory()
    #print(directory)
    global ImRows
    global cells #make the var global for later use
    global TH
    Paths_and_TH=[]
    global images
    images = {} #dictionary with keys as image IDs and values contain lists consisting of path
    #to the image as well as its respective otsu value

    for imagefile in os.listdir(directory):  #to go through files in the specific directory
        #print(os.listdir(directory))
        imagepath=directory + "/" + imagefile   #create first of dic values, i.e the path
        if not imagefile.endswith('.jpg'):
            warning_message="WARNING: The directory contained a file/files that was not in .jpg format! Please remove these files from the directory and try again"
            lbl_numbers.config(text=warning_message)

            break

        #print(imagepath)
        imagename=ntpath.basename(imagepath)#create dic key

        #print(imagename)
        #get the threshold
        cells = rgb2gray(imread(imagepath))
        which_im.insert(tk.END, imagefile)
        TH = filters.threshold_otsu(cells)  #apply threshold, second of dic values

        #append everything into the dictionary
        Paths_and_TH.append(imagepath)  #append the values
        Paths_and_TH.append(TH)
        images[imagename]=Paths_and_TH

        Paths_and_TH.clear()
        #now the image should be saved into the dictionary so that it can be used later
    num_of_images= len(images)
    lbl_numbers.config(text=warning_message)
def create_window1():
    w1 = tk.Toplevel(w)
    def pre_ImageStats_a():
#Round1: get the TH values which can be recommended to the user before the user enters his/her own
        selected = which_im.curselection() #create indices of the files
        print(selected)
        sel_list=list()
        Imfile_TH=[]
        final_results_TH=[]
        #os.system(which_im.get(x))
        for a_file in selected: #get the file name based on the indeces
            entered=which_im.get(a_file)
            sel_list.append(entered)
            #print(sel_list) #save selected images (names) into a list
            # x = which_im.curselection()[0]
            #f = which_im.get(x)
            # with open(f, 'r', encoding='utf-8') as f:
        for im in sel_list: #go through each image
            #print(im)
            for file in os.listdir(directory): #open the directory and find the filename, then get the path based on this
                #print(file)
                if file == im:
                    print(file)
                    #print(directory)
                    imagepath=directory + "/" + file #reconstruct the path
                    imagename=file
                    cells_img = rgb2gray(imread(imagepath)) #get the correct image since
                    TH = filters.threshold_otsu(cells_img)  #apply threshold, second of dic values
                    Imfile_TH.append(imagename)
                    Imfile_TH.append(TH)
                    results="Image ID: "+ str(Imfile_TH[0]) + "-- Threshold used: "+ str(Imfile_TH[1]) + "\n"
                    final_results_TH.append(results)  #######
                    Imfile_TH.clear()
        lbl_outpTHs.config(text=final_results_TH)
    
    def ImageStats_a():
        selected = which_im.curselection() #create indices of the files
        print(selected)
        sel_list=list() #putting the indices into a list
        
        labels=[]

        results_im=[]
        final_results=[]
        global TH1
        #os.system(which_im.get(x))
        for a_file in selected: #get the file name based on the indeces
            entered=which_im.get(a_file)
            sel_list.append(entered)
            #print(sel_list) #save selected images (names) into a list
            # x = which_im.curselection()[0]
            #f = which_im.get(x)
            # with open(f, 'r', encoding='utf-8') as f:
        for im in sel_list: #go through each image
            #print(im)
            for file in os.listdir(directory): #open the directory and find the filename, then get the path based on this
                #print(file)
                if file == im:
                    ########trying to take into account if the user decides to add a text file
                    # if not file.endswith('.jpg'):
                    #     final_results="The file you entered is not in imagefile format!"
                    #     break
                    ##############
                    print(file)
                    #print(directory)
                    imagepath=directory + "/" + file #reconstruct the path
                    imagename=file #get the name
                    #print(entry.get())
                    cells_img = rgb2gray(imread(imagepath)) #get the correct image since
                    
                    #th = entry.get()  #apply threshold, second of dic values
                    try:
                        TH1 = float(entry.get())
                    except ValueError: #if you get a value error, it will pass
                        pass

                    # if th.isdigit():
                    #     TH1=float(th)
                    #     print(TH1)
                    cells_bw=cells_img>TH1
                    labels = measure.label(cells_bw)
                    cell_count=labels.max()
                    cell_count=str(cell_count)  #converting int into str
                    Average_size=labels.mean()
                    Average_size=str(Average_size) #converting int into str

                    results_im.append(imagename)
                    results_im.append(cell_count)
                    results_im.append(Average_size)
                    results_im.append(TH1)

                    results="Image ID: "+ str(results_im[0]) + "-- Cell count: " + str(results_im[1]) + " -- Average cell size: "+ str(results_im[2])+ "-- Threshold used: "+ str(results_im[3]) + "\n"
                    final_results.append(results)  #append all the results-strings into final list
                    results_im.clear()
                    entry.delete(0, tk.END)
                    entry.insert(0, "")

        lbl_one_im.config(text=imagename)
        lbl_outp.config(text=final_results)
        
        
    btn_stats_a = tk.Button(   #btn_stats_a used if chose option a) --- use of own threshold
        master=w1,
        text="Apply own threshold",
        command=ImageStats_a
    )  #this button needs to be applied to each image one by one
    #btn_stats_a.bind("<Button-1>", ImageStats_a)
    lbl_outp = tk.Label(master=w1, text="")

    entry = tk.Entry(w1, text="")
    lbl_outpTHs = tk.Label(master=w1, text="")
    recommend_TH=tk.Button(master=w1, text="Get recommended THs", command=pre_ImageStats_a)
    lbl_one_im=tk.Label(master=w1, text="")
    btn_stats_a.pack()
    recommend_TH.pack()
    btn_stats_a.pack()
    
    lbl_outp.pack()
    lbl_outpTHs.pack()
    
    lbl_one_im.pack()
    entry.pack()
    btn_stats_a.pack()
    w1.mainloop()



def create_window2(event):
    w2 = tk.Toplevel(w)

    def ImageStats_b():
        selected = which_im.curselection() #create indices of the files
        print(selected)
        sel_list=list()
        global final_results

        results_im=[]
        final_results=[]
        #os.system(which_im.get(x))
        for a_file in selected: #get the file name based on the indeces
            entered=which_im.get(a_file)
            sel_list.append(entered)
            #print(sel_list) #save selected images (names) into a list
            # x = which_im.curselection()[0]
            #f = which_im.get(x)
            # with open(f, 'r', encoding='utf-8') as f:
        for im in sel_list: #go through each image
            #print(im)
            for file in os.listdir(directory): #open the directory and find the filename, then get the path based on this
                #print(file)
                if file == im:
                    print(file)
                    #print(directory)
                    imagepath=directory + "/" + file #reconstruct the path

                    cells_img = rgb2gray(imread(imagepath)) #get the correct image since
                    TH = filters.threshold_otsu(cells_img)  #apply threshold, second of dic values
                    cells_bw=cells_img>TH
                    labels = measure.label(cells_bw)
                    cell_count=labels.max()
                    cell_count=str(cell_count)  #converting int into str
                    Average_size=labels.mean()
                    Average_size=str(Average_size) #converting int into str

                    imagename=file #get the name
                    results_im.append(imagename)
                    results_im.append(cell_count)
                    results_im.append(Average_size)
                    results_im.append(TH)

                    results="Image ID: "+ str(results_im[0]) + "-- Cell count: " + str(results_im[1]) + " -- Average cell size: "+ str(results_im[2])+ "-- Threshold used: "+ str(results_im[3]) + "\n"
                    final_results.append(results)  #append all the results-strings into final list
                    results_im.clear()
        #return(final_results)
        # text.delete('1.0', tk.END)
        lbl_outp.config(text=final_results)
    def Output():
        with open("Images_output.txt", "w") as outp:
            print(final_results)
           # for line in final_results:
            outp.write('\n'.join(final_results))
        lbl_info.config(text="Output saved to: "+ directory + "!")

    lbl_choice = tk.Label(master=w, text="Enter own threshold or select automatically defined one based on Otsu's method (recommended)")
    lbl_stats = tk.Label(master=w, text="Stats appear here after you have entered threshold")
    btn_stats_own = tk.Button(master=w, text="Own threshold", command=create_window1)
    btn_stats_own.bind("<Button-1>", create_window1)
    btn_stats_b = tk.Button(   #btn_stats_b used if chose option b) --- use of otsu's threshold
        master=w,
        text="Apply Otsu's threshold",
        command=ImageStats_b
    )
    lbl_info=tk.Label(master=w, text='')
    btn_outp_b=tk.Button(master=w, text="Save the output", command=Output)
    lbl_outp = tk.Label(master=w2, text="")
    
    btn_stats_own.pack()
    btn_stats_b.pack()
    lbl_choice
    lbl_stats.pack()
    btn_stats_b.pack()
    lbl_outp.pack() #####
    lbl_info.pack()
    w2.mainloop()

# theframe=tk.Frame(w,width=400,height=300,bd=2) ####

btn1 = tk.Button(master=w, text='Please select an image directory', command=UploadAction)
lbl_txt = tk.Label(master=w, text="Number of image files in directory:")
lbl_txt_expl = tk.Label(master=w, text="Please select the images you want to analyse with left mouse click and after you are done click right mouse click")
lbl_numbers = tk.Label(master=w, text="")
which_im = tk.Listbox(master=w, selectmode=tk.MULTIPLE)      ##########
which_im.bind("<Button-3>", create_window2)   #right button click to proceed
#cellranges=tk.Listbox(master=w)    ########

# theframe.pack() #####
btn1.pack()
lbl_txt_expl.pack()
lbl_txt.pack()
lbl_numbers.pack()
which_im.pack()  ########


w.mainloop()
