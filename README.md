# BINP29_ImageAnalysisProject
# Monofluor Readme
Python version: Python 3.7.6

## Monofluor
Monofluor is tool developed for python that counts the number of fluorescently tagged objects
in a fluorescent image.

## Installation
Download the code and example data from github: https://github.com/Atte-Oskari-Rasanen/BINP29_ImageAnalysisProject
Make sure that you have following packages installed: skimage, numpy and tkinter.

## Usage
From the command line the code can be run simply by: python Monofluor. Alternatively
the program can be run by opening python.

Select the directory containing images by clicking on select image directory. Make
sure that no other than .jpg files are found in the directory or else the program
will give an error. After this, the number of files and their names are presented.
Select the ones you want to analyse using left mouse click and after you are done
selecting, click the right mouse button. This opens two buttons: own threshold
and Otsu's threshold. Click on the one you want. Otsu's threshold button opens up
a new window where you can get the cell counts, average cell size and thresholds
used for every individual object.
