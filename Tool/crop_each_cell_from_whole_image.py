import math

import pandas as pd
from skimage.io import imread, imsave,imshow
from skimage import io, exposure, img_as_uint, img_as_float
import numpy as np
import os
import cv2
from skimage.transform import rescale, resize, downscale_local_mean
from skimage.transform import rescale, resize, downscale_local_mean
#######read ID center and box information#####################
# fTable_merged = pd.read_csv("/project/ece/roysam/lbai/DrRorsam/program/NUCLEAR_SEG/results/fTable_merged.csv")
fTable_merged = pd.read_csv("F:/fTable_merged.csv")
fTable_merged_np = np.array(fTable_merged)
#######Load image#############################################
# im1 = imread('/project/ece/roysam/lbai/S1/final/S1_R2C1.tif')
# im2 = imread('/project/ece/roysam/lbai/S1/final/S1_R2C2.tif')
im1 = imread('F:/Pycharm_Projects/D-backup/DrRorsam/static/type/Dataset/S1_R2C1.tif')
im2 = imread('F:/Pycharm_Projects/D-backup/DrRorsam/static/type/Dataset/S1_R2C2.tif')

# if not os.path.exists('/project/ece/roysam/lbai/DrRorsam/Tool/results/Croped_Cells/'):
#     os.makedirs('/project/ece/roysam/lbai/DrRorsam/Tool/results/Croped_Cells/')
for eachline in fTable_merged_np:
    crop_im1=im1[int(eachline[4]):int(eachline[6]), int(eachline[5]):int(eachline[7])]
    crop_im2=im2[int(eachline[4]):int(eachline[6]), int(eachline[5]):int(eachline[7])]


    im = np.zeros((crop_im1.shape[0], crop_im1.shape[1], 3))
    im[:, :, 0] = crop_im1
    im[:, :, 1] = crop_im2
    im[:, :, 2] = (crop_im1 + crop_im2)/2
    cv2.imshow("S",im)
    cv2.waitKey()
    x = int(eachline[4])
    y = int(eachline[5])
    w = crop_im1.shape[1]
    h = crop_im1.shape[0]
    temp_canvas = cv2.copyMakeBorder(im[y:y + h, x:x + w], 40 - math.floor(h / 2),
                                     40 - math.ceil(h / 2), 40 - math.floor(w / 2), 40 - math.ceil(w / 2),
                                     borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])
    cv2.imshow("S",temp_canvas)
    cv2.waitKey()
    # imsave(
    #     '/project/ece/roysam/lbai/DrRorsam/Tool/results/Croped_Cells/' + str(int(eachline[1])) + '.png',
    #     temp_canvas)





