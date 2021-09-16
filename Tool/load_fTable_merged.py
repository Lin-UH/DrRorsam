import pandas as pd
import pickle
def csv2pkl(fTable_merged_address,Cell_ID_centerXY_address):
    table = pd.read_csv(fTable_merged_address)
    Cell_ID_centerXY={}
    for index, row in table.iterrows():
        Cell_ID_centerXY[int(row['ID'])]=[int(row['centroid_x']), int(row['centroid_y'])]
        # print(int(row['ID']),int(row['centroid_x']), int(row['centroid_y']))
    f = open(Cell_ID_centerXY_address,"wb")
    pickle.dump(Cell_ID_centerXY,f)
    f.close()
def load_Cell_ID_centerXY_pkl(Cell_ID_centerXY_address='./Tool/results/Cell_ID_centerXY.pkl'):
    f = open(Cell_ID_centerXY_address,"rb")
    Cell_ID_centerXY = pickle.load(f)
    f.close()
    return Cell_ID_centerXY
if __name__ == "__main__":
    csv2pkl('D:/fTable_merged.csv','.Tool/results/Cell_ID_centerXY.pkl')
