import h5py
import numpy as np
import pickle
import pandas as pd
# hf = h5py.File('/project/ece/roysam/lbai/DrRorsam/program/NUCLEAR_SEG/results/merged_labelmask.h5', 'r')   # load wholelabel use 9s
hf = h5py.File('D:/Lin_Project/DrRorsam/static/type/merged_labelmask.h5', 'r')
wholelabel = np.array(hf.get('seg_results'))
hf.close()
Cell_ID_XYlist={}
# print(np.amin(wholelabel)+1,np.amax(wholelabel))
# fTable_merged = pd.read_csv('/project/ece/roysam/lbai/DrRorsam/program/NUCLEAR_SEG/results/fTable_merged.csv')
fTable_merged = pd.read_csv('D:/Lin_Project/DrRorsam/static/type/fTable_merged.csv')
for x in range(30):
    for y in range(44):
        start=x*1000
        end=y*1000
        selected_fTable_merged = np.array(fTable_merged[(end + 1000 > fTable_merged.centroid_y) & (fTable_merged.centroid_y > end) & (start+ 1000 > fTable_merged.centroid_x) & (
                    fTable_merged.centroid_x > start)])

        for Cell_ID in selected_fTable_merged[:,0]:
            X_array=np.where(wholelabel[start:start+ 1000,end:end+ 1000]==Cell_ID)[0]
            Y_array=np.where(wholelabel[start:start+ 1000, end:end + 1000]==Cell_ID)[1]
            XY = []
            for index in range(0,len(X_array)):
                XY.append([X_array[index],Y_array[index]])
            # print(XY)
            Cell_ID_XYlist[Cell_ID] = XY
            # print(Cell_ID,XY)
            # print(len(X_array),len(Y_array),len(XY))
        ID_len = len(Cell_ID_XYlist)
        txt = "%{ID_len:.2f}"
        print(txt.format(ID_len=ID_len/230000*100))
f = open("Cell_ID_XYlist.pkl","wb")
pickle.dump(Cell_ID_XYlist,f)
f.close()
# f = open("file.pkl","rb")
# print(pickle.load(f))
# f.close()