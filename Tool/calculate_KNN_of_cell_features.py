import pickle
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn import manifold

f1 = open("../static/type/ID_TSNE_XY.pkl", "rb")
ID_TSNE_XY = pickle.load(f1)
all_features = []
print(len(ID_TSNE_XY))
for ID in range(1,222758+1):
    all_features.append(ID_TSNE_XY[ID])
# all_features = np.load('../static/type/14_14_features.npy')

f = open("../static/type/ID_topnear_after_TSNE.pkl", "wb")

ID_topnear = {}
# all_features = all_features.tolist()
neigh = NearestNeighbors(n_neighbors=11)
neigh.fit(all_features)
print("here")
for Cell_index,each_feature in enumerate(all_features):
    topnear = neigh.kneighbors([each_feature], return_distance=False).tolist()
    topnear = topnear[0]
    topnear.pop(0)
    # print(Cell_index+1,topnear)
    ID_topnear[Cell_index+1] = [each+1 for each in topnear]
pickle.dump(ID_topnear, f)
f.close()


