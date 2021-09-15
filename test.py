import os

from skimage.io import imread, imsave,imshow
from skimage.transform import resize
from skimage import exposure
import h5py
# im = imread('/project/ece/roysam/lbai/S1/original/R2C1.tif', plugin='tifffile')[5000:6000, 5000:6000]
# im += imread('/project/ece/roysam/lbai/S1/original/R2C2.tif', plugin='tifffile')[5000:6000, 5000:6000]
# # for i in range(2,12):
# #    im+= imread('/project/ece/roysam/lbai/S1/original/R1C'+str(i)+'.tif', plugin='tifffile')[5000:6000,5000:6000]
# imsave('/project/ece/roysam/lbai/output/DAPI-histone.png',im)
import numpy as np
# (29399, 43055)
f1 = h5py.File('/project/ece/roysam/lbai/output/reconstruction/masking/oligodendrocytes_OUTPUT/oligodendrocytes_reconstruction_results.h5','r')   #打开h5文件
f2 = h5py.File('/project/ece/roysam/lbai/output/reconstruction/masking/neuron_OUTPUT/neuron_reconstruction_results.h5','r')   #打开h5文件
f3 = h5py.File('/project/ece/roysam/lbai/output/reconstruction/masking/microglia_OUTPUT/microglia_reconstruction_results.h5','r')   #打开h5文件
f4 = h5py.File('/project/ece/roysam/lbai/output/reconstruction/masking/endothelial_OUTPUT/endothelial_reconstruction_results.h5','r')   #打开h5文件
f5 = h5py.File('/project/ece/roysam/lbai/output/reconstruction/masking/astrocytes_OUTPUT/astrocytes_reconstruction_results.h5','r')
for x in range(30,44):
    for y in range(30):
        start=x*1000
        end=y*1000
        if os.path.exists('/project/ece/roysam/lbai/output/segmentation/' + str(start) + '-' + str(end) + ''):
            continue
        for f in [f1,f2,f3,f4,f5]:
            for i in range(len(f['index'])):
                if start<=f['x_c'][i]<start+1000 and end<=f['y_c'][i]<end+1000:
                    if not os.path.exists('/project/ece/roysam/lbai/output/segmentation/'+str(start)+'-'+str(end)+'/'+str(int(f['index'][i]))+''):
                        os.makedirs('/project/ece/roysam/lbai/output/segmentation/'+str(start)+'-'+str(end)+'/'+str(int(f['index'][i]))+'')
                    imsave('/project/ece/roysam/lbai/output/segmentation/'+str(start)+'-'+str(end)+'/'+str(int(f['index'][i]))+'/cell-example.png', f['cell_img'][i][0])
                    imsave('/project/ece/roysam/lbai/output/segmentation/'+str(start)+'-'+str(end)+'/'+str(int(f['index'][i]))+'/cytoplasm-example.png', f['cytoplasm_img'][i][0])
                    imsave('/project/ece/roysam/lbai/output/segmentation/'+str(start)+'-'+str(end)+'/'+str(int(f['index'][i]))+'/membrane-example.png', f['membrane_img'][i][0])
                    imsave('/project/ece/roysam/lbai/output/segmentation/'+str(start)+'-'+str(end)+'/'+str(int(f['index'][i]))+'/nucleus-example.png', f['nucleus_img'][i][0])
                    imsave('/project/ece/roysam/lbai/output/segmentation/'+str(start)+'-'+str(end)+'/'+str(int(f['index'][i]))+'/processes-example.png', f['processes_img'][i][0])
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()


# f['cell_img'][0]:#取出主键为data的所有的键值
# print(f['cell_img'][0][0])
# imsave('/project/ece/roysam/lbai/output/cell-example.png', f['cell_img'][0][0])
# imsave('/project/ece/roysam/lbai/output/cytoplasm-example.png', f['cytoplasm_img'][0][0])
# imsave('/project/ece/roysam/lbai/output/membrane-example.png', f['membrane_img'][0][0])
# imsave('/project/ece/roysam/lbai/output/nucleus-example.png', f['nucleus_img'][0][0])
# imsave('/project/ece/roysam/lbai/output/processes-example.png', f['processes_img'][0][0])
# for i in range(len(f['index'])):
# # for x,y in zip(f['index'],f['x_c'],f['y_c']):
#     print(f['index'][i],f['x_c'][i],f['y_c'][i])
# f.close()