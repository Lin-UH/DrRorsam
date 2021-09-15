import shutil

from flask import Flask,render_template,url_for,request,redirect,jsonify,json,session
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
import xlrd  # 读取excel的库
import csv
import matplotlib.pyplot as plt
import os
from matplotlib import gridspec
# from skimage.external import tifffile as tiff
# import tifffile as tiff
import random
# import config
import pandas as pd
# from skimage.util import img_as_ubyte
# from skimage import exposure
import pandas as pd
from skimage.io import imread
import matplotlib.pyplot as plt
import os
from matplotlib import gridspec
# from skimage.external import tifffile as tiff
import tifffile as tiff
import random
import pandas as pd
print(pd.__version__)
import numpy as np
from skimage.util import img_as_ubyte
from skimage import exposure
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# # three forward slashes are project location,four are absolute location
# db=SQLAlchemy(app)
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
def crop_and_label(dir,startnum,num_crops,username):
    class_table = os.path.join(dir,'classification_results/classification_table.csv')
    table1 = pd.read_csv(class_table, sep=',')
    table1.set_index('ID', inplace=True)
    size=300
    dir_channels = os.path.join(dir, 'final')
    dapi_im1 = img_as_ubyte(tiff.imread(os.path.join(dir_channels, 'cut_n30w120.tif')))
    neun_im1 = img_as_ubyte(tiff.imread(os.path.join(dir_channels, 'cut_n30w120.tif')))
    gad67_im1 = img_as_ubyte(tiff.imread(os.path.join(dir_channels, 'cut_n30w120.tif')))
    print("start")
    for each in range(1,int(num_crops)+1):
        print(each)
        try:
            y1 = random.randrange(min(table1.centroid_y), max(table1.centroid_y) - size)
            y2 = y1 + size
            x1 = random.randrange(min(table1.centroid_x), max(table1.centroid_x) - size)
            x2 = x1 + size
            dapi_im = dapi_im1[y1:y2, x1:x2]
            neun_im = neun_im1[y1:y2, x1:x2]
            gad67_im = gad67_im1[y1:y2, x1:x2]

            im_neuron_1 = np.zeros((size, size, 3), 'uint8')
            im_neuron_2 = np.zeros((size, size, 3), 'uint8')
            im_neuron_3 = np.zeros((size, size, 3), 'uint8')
            im_neuron_4 = np.zeros((size, size, 3), 'uint8')

            neun_im_rescale = exposure.adjust_log(neun_im, 1.3)
            gad67_im_rescale = exposure.adjust_log(gad67_im, 1.3)
            dapi_im_rescale = exposure.adjust_log(dapi_im, 1.3)
            im_neuron_1[:, :, 0] = neun_im_rescale
            im_neuron_1[:, :, 1] = gad67_im_rescale
            im_neuron_1[:, :, 2] = dapi_im_rescale
            im_neuron_2[:, :, 0] = neun_im_rescale
            im_neuron_3[:, :, 1] = gad67_im_rescale
            im_neuron_4[:, :, 2] = dapi_im_rescale
            table = table1[table1['centroid_y'] > y1]
            table = table[table['centroid_y'] < y2]
            table = table[table['centroid_x'] > x1]
            table = table[table['centroid_x'] < x2]
            region_points = table.to_numpy().transpose()[1:3]
            region_points[0] -= x1
            region_points[1] -= y1
            region_points = region_points.transpose()
            x1y1=np.array([x1,y1])
            num=startnum+each
            np.save('static/'+username+'/region_points'+str(num)+'.npy',region_points)
            np.save('static/' + username + '/x1y1' + str(num) + '.npy', x1y1)

            from skimage.io import imsave
            imsave('static/'+username+'/composite'+str(num)+'.png',im_neuron_1)
            imsave('static/'+username+'/neun_'+str(num)+'.png',im_neuron_2)
            imsave('static/'+username+'/gad67_'+str(num)+'.png',im_neuron_3)
            imsave('static/'+username+'/dapi_'+str(num)+'.png',im_neuron_4)
        except:
            continue


    return 0
@app.route('/',methods=['POST',  'GET'])
def index():
    if request.method=='POST':
        data=request.form.get('newname')
        # print(request.values.get("data") )
        # data = json.loads(request.form.get('newname'))
        print(data)
        print(type(data))
        filename = os.path.join('labels_all', str(data) + '_labels.csv')
        df_full = pd.DataFrame(columns=['BrainName', 'NeuNLabel', 'GAD67Label', 'centroid_x', 'centroid_y'])
        df_full.to_csv(filename)
        return redirect('/')
    else :
        # session.clear()
        # # give the existing user names
        # # the labels for user "Jane" will be saved as Jane_labels.csv
        # labels_all_users = os.listdir('labels_all')
        # names = [f[:f.find('_')] for f in labels_all_users if f.endswith('.csv')]
        # print(names)
        # print("ahhahahahha")
        # test = "Iam"
        # if "kk" in names:
        #     test="success"

        # if len(existing_users) > 0:
        #     print('Currently existing users in the system:')
        #     print(existing_users)
        #     check_if_user_exists = input("Do you exist in the system, Enter Y for Yes and N for No \n")
        #     if check_if_user_exists == 'Y' or check_if_user_exists == 'y':
        #         # get the existing user
        #         user_name = input("Please enter your Name existing in the system\n")
        #         mode = 1  # appending to current labels by this user
        #     else:
        #         user_name = input("Please enter your Name\n")
        #         mode = 0  # starting new work by this user
        # else:
        #     user_name = input("Please enter your Name\n")
        #     mode = 0  # starting new work by this user
        # filename = os.path.join('labels_all', user_name + '_labels.csv')
        # names=["bai","lin"]
        # {'results': column1, 'xname': newone[0], 'yname': newone[1]}

        # df = pd.read_csv('F:\\uhdata\\fTable.csv')
        # print(df['eccentricity'])
        # features = df.loc[:, feature_names]
        # hist = features.hist(bins=20, range=(0, 1), figsize=(8, 8))
        # plt.show()
        # pd.plotting.scatter_matrix(features, alpha=0.2, figsize=(15, 15))
        # feature_names = ['eccentricity', 'equivalent_diameter']
        # print(column2)
        # return jsonify({'results': column1, 'results1': column2, 'results3': column3})
        return render_template('index.html')

@app.route('/getnames',methods=['GET'])
def getnames():
    if not os.path.exists('labels_all'):
        # create directory
        os.makedirs('labels_all')
    # # give the existing user names
    # # the labels for user "Jane" will be saved as Jane_labels.csv
    labels_all_users = os.listdir('labels_all')
    names = [f[:f.find('_')] for f in labels_all_users if f.endswith('.csv')]

    if 'username'in session:
        current=session['username']
    else:
        current ="none"
    # print(session['username'])

    return jsonify({'names': names,'currents':current})
@app.route('/saveusername',methods=['POST'])
def saveusername():
    data = json.loads(request.form.get('data'))

    session.clear()
    name=data['username']
    if not os.path.exists('static/'+name+''):
        # create directory
        os.makedirs('static/'+name+'')
    session['username']= data['username']
    print(session['username'], " [pppp")
    # session.permanent = True
    return jsonify({'result': data['username']})
@app.route('/del_session',methods=['POST'])
def del_session():
    username=session['username']
    if os.path.exists('static/'+username+'/'):
        shutil.rmtree('static/'+username+'/')
    session.clear()
    # print(session['username']," ooooooo")
    # session.clear()
    return jsonify()

# @app.route('/startlabel',methods=['GET'])
# def startlabel():
#     return  render_template('see.html')
@app.route('/startlabel', methods=['POST'])
def startlabel():
    name = session['username']
    region_points=np.load('static/'+name+'/region_points1.npy')
    im_neuron_1=imread('static/'+name+'/composite1.png')
    print(im_neuron_1)
    print(region_points.tolist())
    return jsonify({'region':region_points.tolist()})
@app.route('/showmarker', methods=['GET'])
def showmarker():
    if('currentcrops' in session ):
        name = session['username']
        region_points = np.load('static/'+name+'/region_points'+str(session['currentcrops'])+'.npy')
        if 'labeledinfor' in session :
            if str(session['currentcrops']) in session['labeledinfor']:
                # alreadylabelindex = []
                # for i in range(0,len(session['labeledinfor'][str(session['currentcrops'])])):
                   # alreadylabelindex.append(session['labeledinfor'][str(session['currentcrops'])][0])
                print(region_points.tolist())
                print(session['allcrops'])
                print(session['currentcrops'])
                print(session['labeledinfor'][str(session['currentcrops'])])
                return jsonify({'region1': region_points.tolist(), 'crops1': session['allcrops'],'currentcrops1': session['currentcrops'],'alreadylabelindex':session['labeledinfor'][str(session['currentcrops'])]})
            else:
                return jsonify({'region1': region_points.tolist(),'crops1': session['allcrops'],'currentcrops1': session['currentcrops'],'alreadylabelindex':"none"})
        else:
            return jsonify({'region1': region_points.tolist(),'crops1': session['allcrops'],'currentcrops1': session['currentcrops'],'alreadylabelindex':"none"})
    else:
        print('MEIYOU')
        return jsonify({'region1': "none",'crops1': "none",'currentcrops1': "none",'alreadylabelindex':"none"})
@app.route('/savecrops', methods=['POST'])
def savecrops():
    data = json.loads(request.form.get('data'))
    session['allcrops'] = data['crops']
    session['currentcrops'] = 1
    name = session['username']
    print(session['allcrops'], "allcrops")
    print(session['currentcrops'], "currentcrops")
    base_path = r'd:/guiflask/project/ece/roysam/datasets/TBI/'
    brain_type = os.listdir(base_path)
    num_crops = int(int(data['crops'])/12)
    brainnum = 0
    for brain_t in brain_type:
        if os.path.isdir(os.path.join(base_path, brain_t)):
            # is directory
            brains = os.listdir(os.path.join(base_path, brain_t))
            # find every brain in this directory
            for brain in brains:
                print('----------------------')
                print('----------------------')
                print('Current Brain:', brain)
                print('----------------------')
                output_dir = os.path.join(base_path, brain_t, brain)
                crop_and_label(output_dir, brainnum, num_crops,session['username'])
                brainnum += num_crops
    region_points = np.load('static/'+name+'/region_points' + str(session['currentcrops']) + '.npy')
    return jsonify({'result': data['crops'],'firstregion': region_points.tolist()})
@app.route('/savecurrentcrops', methods=['POST'])
def savecurrentcrops():
    data1 = json.loads(request.form.get('data'))
    session['currentcrops'] = str(data1['currentcrops'])
    print(session['currentcrops'], "currentcrops")
    name = session['username']
    region_points = np.load('static/'+name+'/region_points' + str(session['currentcrops']) + '.npy')
    if 'labeledinfor' in session:
        if str(session['currentcrops']) in session['labeledinfor']:
            # alreadylabelindex = []
            # for i in range(0,len(session['labeledinfor'][str(session['currentcrops'])])):
            # alreadylabelindex.append(session['labeledinfor'][str(session['currentcrops'])][0])
            print(region_points.tolist())
            print(session['allcrops'])
            print(session['currentcrops'])
            print(session['labeledinfor'][str(session['currentcrops'])])
            return jsonify({'region1': region_points.tolist(), 'crops1': session['allcrops'],
                            'currentcrops1': session['currentcrops'],
                            'alreadylabelindex': session['labeledinfor'][str(session['currentcrops'])]})
        else:
            return jsonify({'region1': region_points.tolist(), 'crops1': session['allcrops'],
                            'currentcrops1': session['currentcrops'], 'alreadylabelindex': "none"})
    else:
        return jsonify({'region1': region_points.tolist(), 'crops1': session['allcrops'],
                        'currentcrops1': session['currentcrops'], 'alreadylabelindex': "none"})
@app.route('/putonelabeledinsession', methods=['POST'])
def putonelabeledinsession():
    # 'selectedgreencircleid': selectedgreencircleid,
    # 'neulabeled': neulabeled,
    # 'gadlabeled': gadlabeled,
    data = json.loads(request.form.get('data'))
    print(data)
    # data['selectedgreencircleid']
    if 'labeledinfor' in session :
        temp=session['labeledinfor']
        temp1 = str(session['currentcrops'])
        if temp1 in temp:
            sign=0
            for each in temp[temp1]:
                if data['selectedgreencircleid']==each[0]:
                    each[1] = data['neulabeled']
                    each[2] = data['gadlabeled']
                    sign=1
            if sign==0:
                temp[temp1].append([data['selectedgreencircleid'],data['neulabeled'],data['gadlabeled']])
        else:
            temp[str(temp1)]=[]
            temp[str(temp1)].append([data['selectedgreencircleid'],data['neulabeled'],data['gadlabeled']])
        session['labeledinfor']=temp
    else:
        labeledinfor1={}
        # print(session['currentcrops'],"currentcrops")
        now=str(session['currentcrops'])
        labeledinfor1[now] = []
        # print(data['selectedgreencircleid'], data['neulabeled'], data['gadlabeled'])
        labeledinfor1[now].append([data['selectedgreencircleid'], data['neulabeled'], data['gadlabeled']])
        session['labeledinfor'] = labeledinfor1
    # session.permanent = True
    print(session['labeledinfor'])
    tmp=session['currentcrops']
    return jsonify({'currentcrop':tmp,'alreadylabel':session['labeledinfor'][str(tmp)]})
@app.route('/savetocsv', methods=['POST'])
def savetocsv():
    filename = os.path.join('labels_all', str(session['username']) + '_labels.csv')
    df=pd.read_csv(filename)
    import csv
    indexfields=df.shape[0] + 1

    base_path = r'd:/guiflask/project/ece/roysam/datasets/TBI/'
    brain_type = os.listdir(base_path)
    brainnames=[]
    allcrops=int(int(session['allcrops'])/12)
    for brain_t in brain_type:
        if os.path.isdir(os.path.join(base_path, brain_t)):
            # is directory
            brains = os.listdir(os.path.join(base_path, brain_t))
            # find every brain in this directory
            for brain in brains:
                for each in range(1,allcrops+1):
                    brainnames.append(brain)
    print(brainnames)
    username=session['username']
    with open(filename, 'a') as f:
        writer = csv.writer(f,lineterminator='\n')
        if 'labeledinfor' in session:
            for each in session['labeledinfor']:
                region_points = np.load('static/' + username + '/region_points' + str(each) + '.npy')
                x1y1 = np.load('static/' + username + '/x1y1' + str(each) + '.npy')
                print(x1y1)
                for eachone in session['labeledinfor'][each]:
                    fields=[indexfields,brainnames[int(each)-1],eachone[1],eachone[2],x1y1[0]+region_points[int(eachone[0])][0],x1y1[1]+region_points[int(eachone[0])][1]]
                    writer.writerow(fields)
                    indexfields+=1
            feedback="finished"
        else:
            feedback="nothing to save"

    session.clear()

    return jsonify({'feedback':feedback})



if __name__ == '__main__':
    app.run()
