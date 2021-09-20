import pandas as pd
from skimage.io import imread, imsave,imshow
from skimage import io, exposure, img_as_uint, img_as_float
import numpy as np
import os
import cv2
from skimage.transform import rescale, resize, downscale_local_mean
from skimage.transform import rescale, resize, downscale_local_mean
#######read ID center and box information#####################
fTable_merged = pd.read_csv('D:/Lin_Project/DrRorsam/static/type/fTable_merged.csv')
fTable_merged_np = np.array(fTable_merged)
#######Load image#############################################
im1 = imread('D:/Lin_Project/DrRorsam/static/type/Dataset/S1_R2C1.tif')
im2 = imread('D:/Lin_Project/DrRorsam/static/type/Dataset/S1_R2C2.tif')


for eachline in fTable_merged_np:
    crop_im1=im1[eachline[3]:eachline[5], eachline[4]:eachline[6]]
    crop_im2=im2[eachline[3]:eachline[5], eachline[4]:eachline[6]]


    im = np.zeros((crop_im1.shape[0], crop_im1.shape[1], 3))
    im[:, :, 0] = crop_im1
    im[:, :, 1] = crop_im2
    im[:, :, 2] = (crop_im1 + crop_im2)/2
    if not os.path.exists('D:/Lin_Project/DrRorsam/static/type/Croped_Cells/'):
        os.makedirs('D:/Lin_Project/DrRorsam/static/type/Croped_Cells/')
    image_resized = resize(im, (80, 80))
    imsave(
        'D:/Lin_Project/DrRorsam/static/type/Croped_Cells/' + str(eachline[0]) + '.png',
        image_resized)

    #
    # im = exposure.rescale_intensity(im, out_range='float')
    # im = img_as_uint(im)
    # image_resized = resize(im, (100, 100))
    # io.imsave('D:/Lin_Project/DrRorsam/static/type/Croped_Cells/' + str(eachline[0]) + '.png',
    #     image_resized)



