

from flask import Flask, redirect, render_template,flash, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import true
from werkzeug.utils import secure_filename
import os
import sqlite3 as sq
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from flask import json
from flask import jsonify
matplotlib.use('Agg')


UPLOAD_FOLDER = 'static/files'
UPLOAD_IMAGE = 'static/files/images'
ALLOWED_EXTENSIONS = ['.xlxs', '.csv', '.txt']


app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myuploader.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #signallimiting
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_IMAGE'] = UPLOAD_IMAGE
app.secret_key = "super secret key"
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
db = SQLAlchemy(app)

sn_num =0

class myuploader(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150),nullable=True)
    sname = db.Column(db.String(150),nullable=True)
    
    desc = db.Column(db.String(500),nullable=True)
    
    date_create = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

@app.route('/')
def home():
    dir = 'static/files/images'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    allmyupload = myuploader.query.all()
    return render_template('index.html',allmyupload=allmyupload)



@app.route('/getyeardata', methods=['GET'])
def get():
    return jsonify("{}")
    
    


@app.route('/getdata', methods=['GET'])
def hello():
    file = myuploader.query.get(sn_num)
    df=pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], file.sname),encoding= 'unicode_escape')
    
    categories= list(df.Category.unique())
    map ={}
    for cat in categories:
        map[cat]=0
    profit = list(df.Profit)
    i=0
    for item in df.Category:
        map[item]+=profit[i]
        i=i+1
    
    
    
    mapsales={}
    categories= list(df.Category.unique())
    for item in categories:
        mapsales[item]=0
    sales = list(df.Sales)
    i=0
    for item in df.Category:
        mapsales[item]+=sales[i]
        i=i+1
    
    
    
    

    mapmode = {}

    for item in list(df['Ship Mode'].unique()):
        mapmode[item]=0;
    profit = df['Profit']
    i=0
    for item in df['Ship Mode']:
        mapmode[item]+=profit[i]
        i=i+1
    
    df['Order Date']= pd.to_datetime(df['Order Date'],format="%d-%m-%Y")
    df['year']=df['Order Date'].apply(lambda x : x.year)
    mapsyears={}
    years = list(df.year.unique())
    years.sort()
    print(years)
    for item in years:
        mapsyears[item]=0
    sales =list(df['Sales'])
    i=0
    for item in df.year:
        mapsyears[item]+=sales[i]
        i=i+1
    print(mapsyears)



    jsonResp = {'first': map, 'second': mapsales, 'third': mapmode} 
    print(jsonify(jsonResp))
    return jsonify(jsonResp)
    
    

@app.route('/analyse/<int:sno>')
def analyse(sno):
    global sn_num
    sn_num = sno


    
    file = myuploader.query.get(sno)
    a=os.path.exists(os.path.join(app.config['UPLOAD_IMAGE'], file.sname)+'1.png')

    
    if(a):
        image_names = os.listdir('static/files/images')
        return render_template('analyse.html', image_names=image_names)

    df=pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], file.sname),encoding= 'unicode_escape')
   
    
    
    df['Order Date']= pd.to_datetime(df['Order Date'],format="%d-%m-%Y")
    df['year']=df['Order Date'].apply(lambda x : x.year)
    mapsyears={}
    years = list(df.year.unique())
    print(years)
    for item in years:
        mapsyears[item]=0
    sales =list(df['Sales'])
    i=0
    for item in df.year:
        mapsyears[item]+=sales[i]
        i=i+1
    

    
    
    

    
    plt.title('Sales across years')
    plt.bar(list(mapsyears.keys()),list(mapsyears.values()),color="#71797E")
    

    

    
    
    plt.savefig(os.path.join(app.config['UPLOAD_IMAGE'], file.sname)+'1.png')

    products =0
    products = len(list(df['Product ID'].unique()))
    orders = len(list(df['Order ID'].unique()))
    sales = df['Sales'].sum()
    profit = df['Profit'].sum()


    return render_template('analyse.html',products=products,orders=orders,sales=sales,profit = profit)
   
    
    

    







@app.route('/upload', methods=['POST'])
def uploader():
    name = request.form['name']
    desc = request.form['desc']
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_ext = os.path.splitext(filename)[1]

    if file_ext  not in app.config['UPLOAD_EXTENSIONS']:
        flash("File extension not supported")
        return redirect('/')
        
      
    else:
        conn = sq.connect('my_data.db')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename),encoding = 'unicode_escape')
        df.to_sql(name=name,con=conn)
        conn.commit()
        conn.close()
        
        myupload = myuploader(name = name, desc= desc,sname = filename)
        db.session.add(myupload)
        db.session.commit()
        return redirect('/')
        
        




    

@app.route('/delete/<int:sno>')
def delete(sno):
    file = myuploader.query.get(sno)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.sname))
    db.session.delete(file)
    db.session.commit()

    conn = sq.connect('my_data.db')
    c =conn.cursor()
    query = "DROP TABLE "+file.name
    c.execute(query)
    conn.commit()
    conn.close()
    return redirect('/')
    
    
    
    
    

    

    

@app.errorhandler(413)
def page_not_found(e):
    flash('File size too large')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

