import h5py
import numpy as np
import pickle
hf = h5py.File('/project/ece/roysam/lbai/DrRorsam/program/NUCLEAR_SEG/results/merged_labelmask.h5', 'r')   # load wholelabel use 9s
wholelabel = np.array(hf.get('seg_results'))
hf.close()
Cell_ID_XYlist={}
# print(np.amin(wholelabel)+1,np.amax(wholelabel))
for Cell_ID in range(np.amin(wholelabel)+1,np.amax(wholelabel)+1):
    X_array=np.where(wholelabel==Cell_ID)[0]
    Y_array=np.where(wholelabel==Cell_ID)[1]
    XY = []
    for index in range(0,len(X_array)):
        XY.append([X_array[index],Y_array[index]])
    Cell_ID_XYlist[Cell_ID] = XY
    # print(Cell_ID,XY)
    # print(len(X_array),len(Y_array),len(XY))
f = open("Cell_ID_XYlist.pkl","wb")
pickle.dump(Cell_ID_XYlist,f)
f.close()
# f = open("file.pkl","rb")
# print(pickle.load(f))
# f.close()