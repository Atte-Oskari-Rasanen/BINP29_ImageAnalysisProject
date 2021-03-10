# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 17:32:42 2021

@author: atter
"""


# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 13:03:57 2021

@author: atter
"""
# from math import sqrt
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.io import imread, imshow
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from skimage import measure, filters, morphology

from math import sqrt
from skimage.feature import blob_doh
import matplotlib.pyplot as plt
import os
from scipy import ndimage
from skimage import measure, filters, morphology


# from skimage.feature import blob_dog, blob_log, blob_doh
ImRows={}
with open("Hela.jpg") as fIn:
    ImageRow=[]
   # filename=filename.split(" ")[1]
    fIn=fIn.name
    ImRows['ImageID']=fIn

    #print(ImageRow)



#####
# binarizing source image into black and white and threshilding
cells = rgb2gray(imread('Hela.jpg'))
print(np.unique(cells))
# IThresh = (cells>=118).astype(np.uint8)*255
TH = filters.threshold_otsu(cells)  #apply threshold
print(TH)
#cells = ndimage.binary_fill_holes(cells < TH)  #include only the cells that are lower than threshold


#apply threshold
cells_bw = cells>TH         #User Adjustable parameter (UAP)

from skimage.filters import try_all_threshold
from skimage.filters import threshold_otsu


#try different thresholds
fig, ax = try_all_threshold(cells_bw, figsize=(10, 10), verbose=False)
plt.show()

#find out the range of the pixel values --- find the threshold thats best

#######
#try removing small objects, use threshold otsu
cells_bw_edited = morphology.remove_small_objects(cells_bw, min_size=30)
imshow(cells_bw_edited)


#use boolean image, use label (morphology) or measure

######
#adding contours (preceded by cell counting)
import cv2 as cv #scimage does not have a function for calculating contour A, so CVopen is used

#define contours
contours = measure.find_contours(cells_bw, 0.8)

#calculate the area and centroid
# area = measure.regionprops(cells_bw, 'Area', intensity_image=None)
perim = measure.perimeter(cells_bw, neighbourhood=4)
print("Perim of cells: ", perim)
# print('Average perimeter is %f' %(perim.mean()))

# # Expand numpy dimensions
# c = np.expand_dims(contours.astype(np.float32), 1)
# # Convert it to UMat object
# c = cv.UMat(c)
# area = cv.contourArea(c)
# print("Mean cell surface area", area)


# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(cells_bw, cmap=plt.cm.gray)

for contour in contours:
      ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()


#cell count:
from skimage import measure
labels = measure.label(cells_bw)
cell_count=labels.max()
ImRows['Number_of_cells']=cell_count
Average_size=labels.mean()
ImRows['Average_cell_size']=Average_size
ImRows['Threshold_used']=TH

print("Cell count: %f" %(labels.max()))
print('Average coverage of a cell is %f' %(labels.mean()))

print(ImRows)
col_names=['ImageID','Number_of_cells', 'Average_cell_size', 'Threshold_used']

df = pd.DataFrame(list(ImRows.items()),columns = ['ImageID','Number_of_cells', 'Average_cell_size', 'Threshold_used'])
# df = pd.DataFrame(ImRows.items(), columns=col_names)

# ImageRow.append(cell_count)
# ImageRow.append(Average_size)
# ImageRow.append(TH)


# #Counting cells attempt:
# from scipy import ndimage

# labels, nlabels = ndimage.label(cells_bw)
# label_arrays = []
# for label_num in range(1, nlabels+1):
#       label_mask = np.where(labels == label_num, 1, 0)
#       label_arrays.append(label_mask)

# print('There are {} separate components / objects detected.'.format(nlabels)) #doesnt work


# blobs_doh = blob_doh(cells_bw, max_sigma=50, threshold=.01)  #UAP
# print("2d array of a location of each blob: {}".format(blobs_doh))
