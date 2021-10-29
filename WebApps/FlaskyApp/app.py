
# A very simple Flask Hello World app for you to get started with...
import os, csv, json, pandas, pymongo, docker

from flask import Flask, render_template, url_for, redirect, request
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
#app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = "/Volumes/GitRepository/git/internal/Sites/inventory_db/uploads/"
app.config['APP_TITEL']     = "FlaskyApp"
app.config['NAV_TITLE']     = "TiFA"
app.config['PAGE_TITLE']    = "Tinu's "

@app.errorhandler(404)
def page_not_found(e):
    timestamp     = datetime.now()
    app_titel     = app.config['APP_TITEL']
    nav_title     = app.config['NAV_TITLE']
    page_title    = app.config['PAGE_TITLE'] + "Flasky App"
    page_subtitle = "There is something wring in paradise!"
    return render_template("404.html", **locals()), 404


@app.route('/')
def load_page():
    timestamp     = datetime.now()
    app_titel     = app.config['APP_TITEL']
    nav_title     = app.config['NAV_TITLE']
    page_title    = app.config['PAGE_TITLE'] + "Flasky App"
    page_subtitle = "Welcome to " + page_title + ". Choose an option from the Menu."
    return render_template("index.html", **locals()) 


@app.route('/upld')
def upload():
    timestamp     = datetime.now()
    app_titel     = app.config['APP_TITEL']
    nav_title     = app.config['NAV_TITLE']
    page_title    = app.config['PAGE_TITLE'] + "File-Uploader"
    page_subtitle = "Browse to the file to upload."
    page_label    = "Choose a file to upload"
    page_action   = "upload"
    return render_template("upload_file.html", **locals()) 


@app.route('/csv')
def load_csv():
    timestamp     = datetime.now()
    app_titel     = app.config['APP_TITEL']
    nav_title     = app.config['NAV_TITLE']
    page_title    = app.config['PAGE_TITLE'] + "CSV-Viewer"
    page_subtitle = "Browse to the CSV-file to load."
    page_label    = "Choose a CSV-file to load"
    page_action   = "rcsv"
    return render_template("choose_file.html", **locals()) 


@app.route('/json')
def load_json():
    timestamp     = datetime.now()
    app_titel     = app.config['APP_TITEL']
    nav_title     = app.config['NAV_TITLE']
    page_title    = app.config['PAGE_TITLE'] + "JSON-Viewer"
    page_subtitle = "Browse to the JSON-file to load."
    page_label    = "Choose a JSON-file to load"
    page_action   = "rjson"
    return render_template("choose_file.html", **locals()) 


@app.route('/mdbc')
def load_mongodb():
    timestamp     = datetime.now()
    app_titel     = app.config['APP_TITEL']
    nav_title     = app.config['NAV_TITLE']
    page_title    = app.config['PAGE_TITLE'] + "MongoDB-Viewer"
    page_title    = "Tinu's MongoDB-Viewer"
    page_subtitle = "Connect to the MongoDB to load."
    page_label    = "Choose a MongoDB to load"
    page_action   = "rmdbc"
    return render_template("choose_mdbc.html", **locals()) 


@app.route("/upload", methods=["POST"])
def upload_file():
    timestamp     = datetime.now()
    app_titel     = app.config['APP_TITEL']
    nav_title     = app.config['NAV_TITLE']
    page_title    = app.config['PAGE_TITLE'] + "File-Uploader"
    page_label    = "Choose a file to upload"
    f = request.files['file']
    page_subtitle = "File uploaded: " + f.filename

    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    return render_template("upload_file.html", **locals()) 
 

@app.route("/rcsv", methods=["POST"])
def read_csv():
    timestamp     = datetime.now()
    app_titel     = app.config['APP_TITEL']
    nav_title     = app.config['NAV_TITLE']
    page_title    = app.config['PAGE_TITLE'] + "CSV-Viewer"
    filepath      = os.path.join(app.config['UPLOAD_FOLDER'], request.form["file"])
    page_subtitle = "Data from: " + request.form["file"]

    data = []
    with open(filepath) as file:
        csv_file = csv.reader(file)
        header = next(csv_file)
        if header is not None:
            for row in csv_file:
                data.append(row)

    return render_template("read_csv.html", **locals()) 


@app.route("/rjson", methods=["POST"])
def read_json():
    timestamp     = datetime.now()
    app_titel     = app.config['APP_TITEL']
    nav_title     = app.config['NAV_TITLE']
    page_title    = app.config['PAGE_TITLE'] + "JSON-Viewer"
    filepath      = os.path.join(app.config['UPLOAD_FOLDER'], request.form["file"])
    page_subtitle = "Data from: " + request.form["file"]

    data = []
    with open(filepath) as file:
        json_file = json.load(file)

        for row in json_file:
            row.pop('_id', None)
            row.pop('ID', None)
            data.append(row)

    return render_template("read_json.html", **locals()) 

@app.route('/rmdbc', methods=["POST"])
def read_mongodb():
    timestamp     = datetime.now()
    app_titel     = app.config['APP_TITEL']
    nav_title     = app.config['NAV_TITLE']
    page_title    = app.config['PAGE_TITLE'] + "MongoDB-Viewer"

    mongostring = request.form["connectionstring"]
    if not mongostring:
        connectionstring = "localhost:27017"
    else:
        connectionstring = request.form["connectionstring"]

    page_subtitle = "Connect to " + connectionstring + ", Database: " + request.form["database"] + ", Collection: " + request.form["collection"]

    #client = docker.from_env()
    #container = client.containers.get('mongodb1')
    #container.start()

    '''
    credentials = input('user:password')
    connectionstring = "mongodb+srv://"+credentials+"@cluster0.epl3x.mongodb.net/?retryWrites=true&w=majority"
    '''

    provider         = request.form["provider"]
    connectionstring = provider + "://" + connectionstring
    database         = request.form["database"]         #'tinu'
    collection       = request.form["collection"]       #'inventory'

    mongo_client = pymongo.MongoClient(connectionstring)
    mongo_db     = mongo_client[database]
    mongo_col    = mongo_db[collection]
    mongo_client.close()
    result = mongo_col.find()

    data = []
    for row in result:
        row.pop('_id', None)
        row.pop('ID', None)
        data.append(row)

    #container.stop()

    return render_template("read_json.html", **locals()) 


if __name__ == '__main__':
    app.run(debug=True)
