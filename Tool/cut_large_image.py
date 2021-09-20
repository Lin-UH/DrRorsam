from skimage.io import imread, imsave,imshow
from skimage.transform import resize
from skimage import exposure
import matplotlib.pyplot as plt
# Image.MAX_IMAGE_PIXELS = None
# a=Image.open('D:/R2C1.tif')
# #
import numpy as np
im1 = imread('D:/Lin_Project/DrRorsam/static/type/Dataset/S1_R2C1.tif')
im2 = imread('D:/Lin_Project/DrRorsam/static/type/Dataset/S1_R2C2.tif')
for x in range(30):
    for y in range(44):
        start=x*1000
        end=y*1000
        im = np.zeros((1000, 1000, 3))
        im[:, :, 0][:im1[start:start+1000,end:end+1000].shape[0],:im1[start:start+1000,end:end+1000].shape[1]] = im1[start:start+1000,end:end+1000]
        im[:, :, 1][:im2[start:start+1000,end:end+1000].shape[0],:im2[start:start+1000,end:end+1000].shape[1]] = im2[start:start+1000,end:end+1000]
        im3=(im1[start:start + 1000, end:end + 1000] + im2[start:start + 1000, end:end + 1000]) / 2
        im[:, :, 2][:im3.shape[0],:im3.shape[1]] = im3
        imsave('D:/Lin_Project/DrRorsam/static/type/S1_images_dapihistone/'+str(end)+'-'+str(start)+'.png',im)

