# document.getElementById("link").href;
# document.getElementById("link").target;
# document.getElementById("img").src;
# document.getElementById("img").width;
# document.getElementById("img").height;
# document.getElementById("input").value;
# scancel jobID
# 解包：tar zxvf filename.tar
# 打包：tar czvf filename.tar dirname

# sbatch myjob.shg

# scontrol show node
# ssh compute-0-9
# dos2unix xxx.sh ##
# sbatch xxx.sh
#squeue
#先cd到program


# cd /project/ece/roysam/lbai/DrRorsam/
# module load anaconda3
# source activate
# source deactivate
# conda activate /project/ece/roysam/lbai/DrRorsam/serverenv
# netstat -anp
# 首先创建特定的虚拟环境
#
# conda create -n temp_test python=3.5

# conda create --prefix ./envs
# conda install anaconda
# 切换到该环境
#
# conda activate temp_test
# 切换到requirement.txt的目录
#
# conda install --yes --file requirements.txt
# MarkupSafe==1.0
# anaconda search -t conda package
# conda install -c https://conda.anaconda.org/conda-forge lifelines, 注意conda-forge和lifelines之间没有“/”。

#
# - importlib - metadata == 2.1
# .1
# - cpython == 0.0
# .6
# - opencv - python == 4.4
# .0
# .42
# - wincertstore == 0.2
# - imagecodecs == 2019.12
# .31
# - fits - tools == 0.2

# install cuda cudnn revise environment

# vim  ~/.bashrc
# export CUDA_ROOT=/project/ece/roysam/lbai/DrRorsam/serverenvs/Cuda-environment/bin/
# export LD_LIBRARY_PATH=/project/ece/roysam/lbai/DrRorsam/serverenvs/Cuda-environment/lib64/
import os
import pickle

from flask import Flask,render_template,url_for,request,redirect,jsonify,json,session,abort
import random
from flask_admin import Admin
from sklearn import manifold
from flask_basicauth import BasicAuth
# import matplotlib.pyplot as plt
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
import numpy as np
import flask_wtf
from flask_wtf.csrf import CsrfProtect
import pandas as pd
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
from flask_bootstrap import Bootstrap
basic_auth = BasicAuth(app)
bootstrap = Bootstrap(app)
# app.debug = True
# FLASK_DEBUG = 1

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class
class MyModelView(sqla.ModelView):
    # column_list = ('User', 'Role')
    # def __init__(self, session, **kwargs):
    #     super(MyModelView, self).__init__(News, session, **kwargs)
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
        )

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


# Create admin
admin = flask_admin.Admin(
    app,
    'Example: Auth',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(User, db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()
        print("dddddddddddddddddddddddddddddddddddddddddd")
        test_user = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )

        first_names = [
            'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
            'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
            'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
        ]
        last_names = [
            'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
            'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
            'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
        ]

        for i in range(len(first_names)):
            tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
            tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
            user_datastore.create_user(
                first_name=first_names[i],
                last_name=last_names[i],
                email=tmp_email,
                password=encrypt_password(tmp_pass),
                roles=[user_role, ]
            )
        db.session.commit()
    return

CsrfProtect(app)
class MicroBlogModelView(MyModelView):
    form_base_class = flask_wtf.Form


@app.route('/',methods=['POST',  'GET'])
# @basic_auth.required
def index():
    if request.method == 'POST':
        return redirect('/')
    else:
        return render_template('index.html')

@app.route('/test',methods=['GET'])
def test():
    return render_template('test.html')
@app.route('/Braincells',methods=['GET'])
def BrainCells():
    return render_template('Brain-cells.html')
@app.route('/Braincells_1',methods=['GET'])
def BrainCells_1():
    return render_template('Brain-cells-1.0.html')
@app.route('/segmentation',methods=['POST'])
def segmentation():
    import base64
    from PIL import Image
    from io import BytesIO

    with open("image.jpg", "rb") as image_file:
        data = base64.b64encode(image_file.read())

    im = Image.open(BytesIO(base64.b64decode(data)))
    im.save('image1.png', 'PNG')
    return jsonify({'box_xy': box_xywh, 'results': results, 'features': X_tsne.tolist()})

@app.route('/Braincells_getbox_xy',methods=['GET','POST'])
def BrainCells_getbox_xy():
    # circle_seg=[]
    from Tool.load_fTable_merged import load_Cell_ID_centerXY_pkl
    if request.method=='POST':
        data = json.loads(request.form.get('data'))
        currentpage=data['currentpage']
        # currentpage= request.form.get('currentpage')
        session['currentpage']=currentpage

    else:
        if 'currentpage' in session:
            currentpage = session['currentpage']
        else:
            currentpage = 1
            session['currentpage']=currentpage
    filedirname=""
    # for root, dirs, files in os.walk("./static/type/segmentation"):
    #        filedirname=dirs[currentpage]
    #        break
    for root, dirs, files in os.walk("./static/type/images"):
        filedirname = files[currentpage]
        break
    filedirname = filedirname.split(".")[0]
    start,end=int(filedirname.split("-")[0]),int(filedirname.split("-")[1])

    # Cell_ID_centerXY = load_Cell_ID_centerXY_pkl()
    c = pd.read_csv('./static/type/fTable_merged.csv')
    # box_xywh_=[]
    # for Cell_ID in Cell_ID_centerXY:
    #     if (start+1000 >Cell_ID_centerXY[Cell_ID][1]) & (Cell_ID_centerXY[Cell_ID][1] > start) & (end+1000 > Cell_ID_centerXY[Cell_ID][0]) & (Cell_ID_centerXY[Cell_ID][0] > end):
    #         print(Cell_ID_centerXY[Cell_ID])
    #         box_xywh_.append([each[3] - start, each[4] - end, 2 * (each[1] - each[3]), 2 * (each[2] - each[4])])


    import numpy as np
    newc = np.array(c[(start+1000 > c.centroid_y) & (c.centroid_y > start) & (end+1000 > c.centroid_x) & (c.centroid_x > end)])
    box_xywh=[]
    results =[]
    features=[]
    ID=[]
    #####################load contour information#####################
    contour = []
    f = open('./static/type/Cell_ID_XYlist.pkl', "rb")
    Cell_ID_XYlist = pickle.load(f)
    f.close()
    #####################         future         #####################
    cla_name=["Neun","S100","Olig2","lba1","RECA1"]
    all_features = np.load('./static/type/vector.npy')
    for each in newc:
        ID.append(int(each[0]))
        contour.append(Cell_ID_XYlist[each[0]])
        ###########fake for now   a cross line goes on center###############

        contour.append([[int(each[4] - start)+i*k, int(each[3]-end)+j*k]for i in [-1, 1]
            for j in [-1, 1]
                for k in range(1,15)])
        ###########fake for now   a cross line goes on center###############
        box_xywh.append([int(each[4]-start),int(each[3]-end),int(2*(each[2]-each[4])),int(2*(each[1]-each[3]))])
        for i in range(-5,0):
            if int(each[i])==1:
                results.append(cla_name[i])
        if len(box_xywh)!=len(results):
            results.append("Unasigned")
        features.append(all_features[int(each[0])])






    # 降维
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
    if features==[]:
        X_tsne=features
        return jsonify(
            {'box_xy': box_xywh, 'results': results, 'features': features, 'ID': ID, 'filedirname': filedirname, "contour": contour})
    else:
        X_tsne = tsne.fit_transform(features)
        return jsonify(
            {'box_xy': box_xywh, 'results': results, 'features': X_tsne.tolist(), 'ID': ID, 'filedirname': filedirname, "contour": contour})
    # plt.scatter(X_tsne[:, 0], X_tsne[:, 1], 5, [1,2,3,4,5])  # labels为每一行对应标签，20为标记大小
    # plt.show()
    # return jsonify({'box_xy': box_xy,'results':results,'features':[X_tsne[:, 0],X_tsne[:, 1]]})

if __name__ == '__main__':
    app_dir = os.path.realpath(os.path.dirname(__file__))
    # database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    # if not os.path.exists(database_path):

    # build_sample_db()
    app.run(debug=True)
