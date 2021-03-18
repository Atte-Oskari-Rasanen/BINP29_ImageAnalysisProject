# -*- coding: utf-8 -*-
"""
Title: MonoFluor.py
Date: 2020-20-03
Author: Atte Oskari Räsänen

Description
    This programme gets the directory of images the user selects via tkinter GUI
    and runs analyses on the selected images. The user can select an automatically
    generated threshold (based on Otsu's method) or input their own which will be
    applied to all images. The data is stored afterwards into the directory. 
List of functions: 
    def UploadAction:
    create_window1():
    def pre_ImageStats_a():
    ImageStats_a():
    def Output():
    def ImageStats_b():
    
List of "non standard" modules:
    None.

Procedure
    1. After importing the relevant packages, a tkinter main window is created, named and 
    the outlook modified. 
    2. The user selects "Please select an image directory" button from the GUI. This
    tkinter button is connected to the function UploadAction. In this function the 
    selected directory by the user is iterated over, only selecting the image files
    which are defined as ending in .jpg. Subsequently a path version is created 
    by taking the directory name (includes the path) along with the file name at hand. 
    The file name is added as the key into an empty dictionary (images) along with the image
    path as the value. The function outputs the number of image files foundand dsiplays them
    using the label widget lbl_numbers. The images are displayed on the screen after the 
    directory is entered.	
    3. The label widget lbl_txt_expl explains how to select the images and proceed. When
    proceeded, a create_window2 function is called, opening up a pop up window (w2). The window
    is connected to the main window w and a frame is created linked to w2. The window shows
    a label widget lbl_choice and two buttons based on which threshold is selected (Otsu vs own). 
    A label widget lbl_stats is added into the frame. The stats will be displayed on this later. 
    4. If btn_stats_otsu button is selected, then the button opens up a separate window by calling create_window3
    which has a window (w3) connected to the main one. Inside this window a button widget to apply 
    Otsu's threshold can be applied as well one to save the results. Otsu button runs Image_Stats_b
    function which goes over each file, gets its name, grayscales it, transforms it into a numpy array
    of pixel values and then creates a binary file using automatically calculated Otsu's threshold. 
    The results are shown on the interface window 3 using a label widget lbl_outp. 
    5. The results of Image_Stats_b can be saved using save the output button widget which calls
    Output function, giving the user an option to select the output directory after which the 
    results are saved as text file format into it. A label widget lbl_info tells the user where 
    the file was saved. 
    6. On window 2 if the btn_stats_own is selected, the widget call create_window1 is opened, creating
    a pop up window (w1) connected to the main window. Three buttons appear. btn_stats_a connects to 
    Image_stats_a function which calculates the statistics same way as Image_stats_b if the user
    has entered a number into the entry widget of w1 called entry. Otherwise the code raises an error
    message and asks for a valid input. lnl_outpTHs button connects to pre_imageStats_a function that 
    calculates thresholds for images using Otsu's one. These can be used as a point of reference. 
    btn_outp_a button calls for Output function which repeats the same procedure as the function
    in window 3.      
Usage
    Open python and run the code. The GUI appears in a separate window. 
Extra notes

'''

"""


import tkinter as tk
from tkinter import filedialog
import numpy as np
from skimage.io import imread, imshow
from skimage.color import rgb2gray
# import matplotlib.pyplot as plt
from skimage import measure, filters
import os
import ntpath
# import re
w = tk.Tk() #create main window
w.title("Fluorescent image analyser") #give the window a title
main_title=tk.Label(master=w, text="MonoFluor", bg="yellow", fg="purple") #add a main text with colours
main_title.config(font=("Courier", 45)) #change main text size

def UploadAction(event=None): #function for uploading the images from selected directory
# dict with imageid as key and path and otsu as value
    global directory 
    directory = filedialog.askdirectory() #to select the directory
    #print(directory)
    global ImRows
    global cells #make the var global for later use
    global TH
    Paths_and_TH=[]
    global images
    global warning_message
    images = {} #dictionary with keys as image IDs and values contain lists consisting of path
    #to the image as well as its respective otsu value

    for imagefile in os.listdir(directory):  #to go through files in the specific directory
        #print(os.listdir(directory))
        imagepath=directory + "/" + imagefile   #create first of dic values, i.e the path
        if not imagefile.endswith('.jpg'): #exclude files not ending in .jpg
            continue

        #print(imagepath)
        imagename=ntpath.basename(imagepath)#take the name of the file from the path and save it

        #print(imagename)
        #get the threshold
        cells = rgb2gray(imread(imagepath)) #create a gray image of the original one using rgb2gray
        which_im.insert(tk.END, imagefile) #select the images you want to process further
        TH = filters.threshold_otsu(cells)  #apply threshold, save it

        #append everything into a dictionary
        Paths_and_TH.append(imagepath)
        Paths_and_TH.append(TH)
        images[imagename]=Paths_and_TH

        Paths_and_TH.clear() #clear it
    num_of_images= len(images) #calculate the number of images and display it GUI
    lbl_numbers.config(text=num_of_images)
def create_window1(): #create the first pop up window
    w1 = tk.Toplevel(w) #connect window 1 (w1) to the main window (w)
    w1.title("Results using manually set threshold") #window title

    def pre_ImageStats_a(): 
        global results_output_pre
#Round1: get the threshold values using Otsu's method which can be recommended 
#to the user before the user enters his/her own
        selected = which_im.curselection() #create indices of the files
        print(selected)
        sel_list=list() #save the indices into a list
        Imfile_TH=[] #a temporary list for TH values of image files
        final_results_TH=[] #final results with the image name and the threshold
        #os.system(which_im.get(x))
        for a_file in selected: #get the file name based on the indeces (out of the selected files)
            entered=which_im.get(a_file)
            sel_list.append(entered) # save it into the list
        for im in sel_list: #go through each image
            #print(im)
            for file in os.listdir(directory): #open the directory and find the filename, then get the path based on this
                #print(file)
                if file == im:
                    print(file)
                    #print(directory)
                    imagepath=directory + "/" + file #reconstruct the path
                    imagename=file #get the imagename
                    cells_img = rgb2gray(imread(imagepath)) #get the gray image using rgb2gray
                    TH = filters.threshold_otsu(cells_img)  #apply threshold
                    Imfile_TH.append(imagename) #append these values into the list
                    Imfile_TH.append(TH)
                    #create a 'results' string and add the previously created list's values to it
                    results="Image ID: "+ str(Imfile_TH[0]) + "-- Threshold used: "+ str(Imfile_TH[1]) + "\n"
                    final_results_TH.append(results)  #append the results into the final results
                    Imfile_TH.clear() #clear the list holding temporary values
            results_output_pre="" #create an empty string
            for item in final_results_TH:  #for each item in the list, add them to the empty string
                results_output_pre += item

        lbl_outpTHs.config(text=results_output_pre) #output the values into the GUI
    
    def ImageStats_a():
        selected = which_im.curselection() #create indices of the files
        print(selected)
        sel_list=list()  #create a list for the selected files
        
        labels=[]

        results_im=[]
        global final_results1
        final_results1=[]
        global TH1
        global imagename
        #os.system(which_im.get(x))
        for a_file in selected: #get the file name based on the indeces
            entered=which_im.get(a_file) #get the file name based on the indeces (out of the selected files)
            sel_list.append(entered) # save it into the list
        for im in sel_list: #go through each image
            #print(im)
            for file in os.listdir(directory): #open the directory and find the filename, then get the path based on this
                #print(file)
                if file == im:
                    #print(directory)
                    imagepath=directory + "/" + file #reconstruct the path
                    imagename=file #get the name and save it
                    cells_img = rgb2gray(imread(imagepath)) #get the gray version of the image
                    
                    try:
                        TH1 = float(entry.get())
                    except ValueError: #if you get a value error, it will pass
                        err_mess="Faulty input entered, please enter numeric value"
                        lbl_outp.config(text=err_mess)
                        pass

                    cells_bw=cells_img>TH1 #only get the pixel values that are greater than the threshold
                    labels = measure.label(cells_bw) #create a binary format of the numpy array (object or background)
                    cell_count=labels.max() #count the number of objects
                    cell_count=str(cell_count)  #converting int into str
                    Average_size=labels.mean() #calculate the mean size of the objects
                    Average_size=str(Average_size) #converting int into str
                    
                    #append into the temporary list
                    results_im.append(imagename) 
                    results_im.append(cell_count)
                    results_im.append(Average_size)
                    results_im.append(TH1)
                    #create the string with the output format
                    results="Image ID: "+ str(results_im[0]) + "-- Object count: " + str(results_im[1]) + " -- Average object size: "+ str(results_im[2])+ "-- Threshold used: "+ str(results_im[3]) + "\n"
                    final_results1.append(results)  #append all the results-strings into final list
                    results_im.clear() #clear the list for the next round
                    entry.delete(0, tk.END)#empty the entry box
                    entry.insert(0, "")
            results_output="" #create an empty string
            for item in final_results1: #add the final_results1 components into the string
                results_output += item
        #lbl_one_im.config(text=imagename)
        lbl_outp.config(text=results_output)
        
    def Output(): #function for saving the results into a text file
        name_of_file = "Images_output_manual_TH"
        direcotry_path = filedialog.askdirectory()
        
        fullname = os.path.join(direcotry_path, name_of_file +".txt")         
        
        outp_file = open(fullname, "w")
        
        outp_file.write('\n'.join(final_results1))
        outp_file.close()
        lbl_info1.config(text="Output saved to: "+ direcotry_path + " as Images_output_manual_TH.txt")

    btn_stats_a = tk.Button(   #btn_stats_a used if chose option of applying
        #own threshold on GUI --- use the function ImageStats_a()
        master=w1,
        text="Apply own threshold",
        width=20,
        height=3,
        bg="red",
        fg="black",
        command=ImageStats_a
    )
    #btn_stats_a.bind("<Button-1>", ImageStats_a)
    lbl_outp = tk.Label(master=w1, text="") #the output of the ImageStats_a, initially empty

    entry = tk.Entry(w1, text="") #the entry box for ImageStats_a function, initially empty
    lbl_outpTHs = tk.Label(master=w1, text="") #Showing the recommended THs, initially empty
    recommend_TH=tk.Button(master=w1, text="Get recommended THs", width=20,
        height=3,
        command=pre_ImageStats_a) #calculates the recommended THs
    #lbl_one_im=tk.Label(master=w1, text="") #
    
    btn_outp_a=tk.Button(master=w1, text="Save the output",width=20,
        height=3, bg="yellow", fg="black",
        command=Output)
    lbl_outp_a = tk.Label(master=w1, text="")

    lbl_info1=tk.Label(master=w1, text="")

     #Grids for formatting the widgets

    btn_stats_a.grid(row=0, column=0)
    lbl_outp.grid(row=1, column=0)
   # lbl_one_im.grid(row=2, column=0)
    entry.grid(row=3, column=0)
    lbl_outp_a.grid(row=5, column=0)
    lbl_info1.grid(row=6, column=0)
    
    recommend_TH.grid(row=0, column=1)
    lbl_outpTHs.grid(row=1, column= 1)
    btn_outp_a.grid(row=4, column=0)

    w1.mainloop()



def create_window2(event): #creating a pop up window if the user decides to use Otsu's threshold
    w2 = tk.Toplevel(w) #linking the pop up window to the main window
    f2=tk.Frame(master=w2, width=100, height=100) #creating a frame for it
    f2.pack()

    #creating a label widget
    lbl_choice = tk.Label(master=w, text="Enter own threshold or select one based on Otsu:")
    
    #button which takes the user to window1
    btn_stats_own = tk.Button(master=w, text="Own threshold",width=20,
        height=5,
        bg="red",
        fg="black",
command=create_window1)

    btn_stats_own.bind("<Button-1>", create_window1) #brings to a different window for applying own threshold
    
    #the analysis results label, initally empty
    lbl_stats = tk.Label(master=f2, text="")

    btn_stats_otsu = tk.Button(   #btn_stats_b used if the user chose to use 
        #ImageStats_b --- use of otsu's threshold
        master=w,
        text="Otsu's threshold",
        width=20,
        height=5,
        bg="green",
        fg="black",
        command=create_window3)
    #Grids for formatting the widgets
    lbl_choice.grid(row=4, column=0)
    btn_stats_own.grid(row=5, column=0)
    btn_stats_otsu.grid(row=6, column=0)
    lbl_stats.grid(row=7, column=0)

    w2.mainloop()

def create_window3():#create a pop up window for running ImageStats_b
    w3 = tk.Toplevel(w) 
    w3.title("Results using Otsu's method")

    def ImageStats_b():
        selected = which_im.curselection() #create indices of the files
        #print(selected)
        sel_list=list() #create a list for the selected files
        global final_results

        results_im=[] #temporary results file
        final_results=[] #final results file

        for a_file in selected: #get the file name based on the indeces
            entered=which_im.get(a_file) #save the ones the user selected
            sel_list.append(entered) #append into the list

        for im in sel_list: #go through each image
            #print(im)
            for file in os.listdir(directory): #open the directory and find the filename, then get the path based on this
                #print(file)
                if file == im:
                    print(file)
                    #print(directory)
                    imagepath=directory + "/" + file #reconstruct the path

                    cells_img = rgb2gray(imread(imagepath)) #create a gray version of the image, put pixel values into numpy array
                    TH = filters.threshold_otsu(cells_img)  #apply threshold
                    cells_bw=cells_img>TH #only get the pixel values that are greater than the thresh
                    labels = measure.label(cells_bw) #label pixels either as background or object
                    cell_count=labels.max() #count the number of objects
                    cell_count=str(cell_count)  #converting int into str
                    Average_size=labels.mean() #count the average size of the object
                    Average_size=str(Average_size) #converting int into str

                    imagename=file #get the name
                    #append the results into a temporary list
                    results_im.append(imagename)
                    results_im.append(cell_count)
                    results_im.append(Average_size)
                    results_im.append(TH)
                    #create the output format by adding the list's components into a string
                    results="Image ID: "+ str(results_im[0]) + "-- Object count: " + str(results_im[1]) + " -- Average object size: "+ str(results_im[2])+ "-- Threshold used: "+ str(results_im[3]) + "\n"
                    final_results.append(results)  #append all the results-strings into final list
                    results_im.clear()#clear the temporary list
        #return(final_results)
                results_output2=""
        for item in final_results: #add the final_results items into an empty string  
            results_output2 += item

        lbl_outp.config(text=results_output2) #output the results to the GUI
    def Output(): #function for saving the results into a text file
        name_of_file = "Images_output_otsu"
        direcotry_path = filedialog.askdirectory()
        
        fullname = os.path.join(direcotry_path, name_of_file +".txt")         
        
        outp_file = open(fullname, "w")
        
        outp_file.write('\n'.join(final_results))
        outp_file.close()
        lbl_info.config(text="Output saved to: "+ direcotry_path + " as " + name_of_file + ".txt")

    lbl_info=tk.Label(master=w3, text='')
    btn_stats_b = tk.Button(   #btn_stats_b used if chose option b) --- use of otsu's threshold
        master=w3,
        text="Apply Otsu's threshold",
        width=20,
        height=3,
        bg="green",
        fg="black",
        command=ImageStats_b)

    btn_outp_b=tk.Button(master=w3, text="Save the output", width=20,
        height=3, bg="yellow", fg="black",
 command=Output)
    lbl_outp = tk.Label(master=w3, text="")
    
    #Grids for formatting the widgets
    btn_stats_b.grid(row=0, column=0)
    btn_outp_b.grid(row=3,column=0)
    lbl_outp.grid(row=2, column=0)
    lbl_info.grid(row=4, column=0)
    w3.mainloop()



btn1 = tk.Button(master=w, text='Please select an image directory', command=UploadAction)
lbl_txt = tk.Label(master=w, text="Number of image files in directory:")
lbl_txt_expl = tk.Label(master=w, text="Please select the images you want to analyse with left mouse click and after you are done click right mouse button")
lbl_numbers = tk.Label(master=w, text="")
which_im = tk.Listbox(master=w, selectmode=tk.MULTIPLE)      ##########

which_im.bind("<Button-3>", create_window2)   #right button click to proceed
#cellranges=tk.Listbox(master=w)    ########
lbl_txt2 = tk.Label(master=w, text="Please select threshold:")


#Grids for formatting the widgets

main_title.grid(row=0, column=0)

lbl_txt_expl.grid(row=1, column=0, pady=2)
btn1.grid(row=2, column=0, pady=2)
which_im.grid(row=3, column = 0, pady = 2) 
lbl_txt.grid(row=4, column = 0, pady = 2) 
lbl_numbers.grid(row=5, column= 0)


w.mainloop()
