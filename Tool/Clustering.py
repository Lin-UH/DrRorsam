from sklearn.cluster import KMeans
import numpy as np
import  cv2
image = cv2.imread("E:/Project/DrRorsam/static/type/RDGH_visEnhanced_all_cells/222543.png")
X = np.array([[1, 2], [1, 4], [1, 0],
              [10, 2], [10, 4], [10, 0]])
factor =1
factor1 =10
index_xy = {}
index_feature = []
index = 0
for i in range(100):
    for j in range(100):
        if image[i][j][0]!=0 or image[i][j][1]!=0 or image[i][j][2]!=0:
            # if i < 50:
            #     feature0 = 50-i
            # else:
            #     feature0 = i-50
            # if j < 50:
            #     feature1 = 50-j
            # else:
            #     feature1 = j - 50
            feature0 = i -50
            feature1 = j - 50
            print(feature0,feature1)
            index_feature.append( [feature0*factor,feature1*factor,image[i][j][0]/factor1,image[i][j][1]/factor1,image[i][j][2]/factor1])
            index_xy[index] = [i,j]
            index+=1

kmeans = KMeans(n_clusters=2, random_state=0).fit(index_feature)
# # kmeans.labels_
canvas = np.zeros((100, 100,3))
for index in range(len(index_feature)):
    x = int(index_xy[index][0])
    y = int(index_xy[index][1])
    print(x,y)
    if kmeans.predict([index_feature[index]])[0]==0:
        canvas[x][y][0]=255.0
        canvas[x][y][1]=255.0
        canvas[x][y][2]=255.0
    elif kmeans.predict([index_feature[index]])[0]==1:
        canvas[x][y][0]=255.0
        canvas[x][y][1]=0.0
        canvas[x][y][2]=255.0
    else:
        canvas[x][y][0]=255.0
        canvas[x][y][1]=0.0
        canvas[x][y][2]=0.0
cv2.imshow("after",canvas)
cv2.waitKey()

# kmeans.predict([[0, 0], [12, 3]])

# kmeans.cluster_centers_