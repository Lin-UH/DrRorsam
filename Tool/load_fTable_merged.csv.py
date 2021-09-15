import pandas as pd
import pickle
table = pd.read_csv('F:/results/fTable_merged.csv')
Cell_ID_centerXY={}
for index, row in table.iterrows():
    Cell_ID_centerXY[int(row['ID'])]=[int(row['centroid_x']), int(row['centroid_y'])]
f = open("Cell_ID_centerXY.pkl","wb")
pickle.dump(Cell_ID_centerXY,f)
f.close()
