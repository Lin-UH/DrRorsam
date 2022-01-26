from sklearn import manifold
import pickle
import numpy as np
all_features = np.load('/project/ece/roysam/lbai/DrRorsam/program/14_14_features.npy')
f1 = open("/project/ece/roysam/lbai/DrRorsam/Tool/ID_TSNE_XY.pkl", "wb")
ID_TSNE_XY = {}
tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
X_tsne = tsne.fit_transform(all_features)
for Cell_index,XY in enumerate(X_tsne):
    ID_TSNE_XY[Cell_index+1] = list(XY)
pickle.dump(ID_TSNE_XY, f1)
f1.close()