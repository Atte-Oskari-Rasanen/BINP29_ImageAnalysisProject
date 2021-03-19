# BINP29_ImageAnalysisProject
# Monofluor Readme
Python (ver. 3.7.6)
Scikit image (ver. 0.16.2) 
Tkinter (ver. 8.6.8)

## Monofluor
Monofluor (Monofluor.py) is a tool developed for python that automatically counts the selected fluorescently
tagged objects in a fluorescent image and calculates average size of the objects.

## Installation
Download the code and example data from github: https://github.com/Atte-Oskari-Rasanen/BINP29_ImageAnalysisProject
Make sure that you have following packages installed: Skimage, Numpy and Tkinter. If using
Anaconda, these packages should be readily installed. Anaconda can be installed from: https://docs.anaconda.com/anaconda/install/

## Usage
Open python and run the program. Select the directory containing images by clicking 
on select image directory. Make sure that no other than .tif files are found in 
the directory or else the program will give an error. After this, the number of
files and their names are presented. Select the ones you want to analyse using 
left mouse click and after you are done selecting, click the right mouse button. 
This opens a frame with two buttons: own threshold and Otsu's threshold. Click 
on the one you want. Otsu's threshold button opens up a new window where you 
can get the fluorescent object counts, average object size and thresholds used
for every individual object.
