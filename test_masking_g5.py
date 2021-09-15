import os

from skimage.io import imread, imsave,imshow
from skimage.transform import resize
from skimage import exposure
import h5py


f1 = h5py.File('/project/ece/roysam/lbai/output/reconstruction/masking/oligodendrocytes_OUTPUT/oligodendrocytes_reconstruction_results.h5','r')   #打开h5文件

for each in f1:
    print(each)

