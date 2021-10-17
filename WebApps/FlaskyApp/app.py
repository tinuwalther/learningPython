
# A very simple Flask Hello World app for you to get started with...
import os, csv, json, pandas, pymongo

from flask import Flask, render_template, url_for, redirect, request
from datetime import datetime

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['FILE_UPLOADS'] = "/Volumes/GitRepository/git/internal/Database/Files/"

@app.route('/')
def load_page():
    timestamp     = datetime.now()
    app_titel     = "FlaskyApp"
    nav_title     = "TiFA"
    page_title    = "Tinu's FlaskyApp"
    page_subtitle = "Welcome to " + page_title + ". Choose an option from the Menu."
    return render_template("index.html", **locals()) 


@app.route('/csv')
def load_csv():
    timestamp     = datetime.now()
    app_titel     = "FlaskyApp"
    nav_title     = "TiFA"
    page_title    = "Tinu's CSV-Viewer"
    page_subtitle = "Browse to the CSV-file to load."
    page_label    = "Choose a CSV-file to load"
    page_action   = "rcsv"
    return render_template("choose_file.html", **locals()) 


@app.route('/json')
def load_json():
    timestamp     = datetime.now()
    app_titel     = "FlaskyApp"
    nav_title     = "TiFA"
    page_title    = "Tinu's JSON-Viewer"
    page_subtitle = "Browse to the JSON-file to load."
    page_label    = "Choose a JSON-file to load"
    page_action   = "rjson"
    return render_template("choose_file.html", **locals()) 


@app.route('/mdbc')
def load_mongodb():
    timestamp     = datetime.now()
    app_titel     = "FlaskyApp"
    nav_title     = "TiFA"
    page_title    = "Tinu's MongoDB-Viewer"
    page_subtitle = "Connect to the local MongoDB to load."
    page_label    = "Choose a JSON-file to load"
    page_action   = "readmdbc"

    connectionstring = "mongodb://0.0.0.0:27017"
    database         = 'tinu'
    collection       = 'inventory'

    mongo_client = pymongo.MongoClient(connectionstring)
    mongo_db     = mongo_client[database]
    mongo_col    = mongo_db[collection]
    mongo_client.close()
    result = mongo_col.find()

    data = []
    for doc in result:
        thisdict = { 
            #'ID'             : doc['ID'],
            'RunTime'        : doc['RunTime'],
            'DeviceType'     : doc['DeviceType'],
            'DeviceName'     : doc['DeviceName'],
            'Physical cores' : doc['Physical cores'],
            'MemoryGB'       : doc['MemoryGB'],
            'DiskspaceGB'    : doc['DiskspaceGB'],
            'PurchaseDate'   : doc['PurchaseDate'],
            'Price'          : doc['Price'],
            'Payment'        : doc['Payment'],
            'Warranty'       : doc['Warranty'],
            'Link'           : doc['Link'],
        }
        data.append(thisdict)    

    return render_template("read_json.html", **locals()) 


@app.route("/rcsv", methods=["POST"])
def read_csv():
    timestamp     = datetime.now()
    app_titel     = "FlaskyApp"
    nav_title     = "TiFA"
    page_title    = "Tinu's CSV-Viewer"
    filepath      = os.path.join(app.config['FILE_UPLOADS'], request.form["file"])
    page_subtitle = "Data from: " + filepath

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
    app_titel     = "FlaskyApp"
    nav_title     = "TiFA"
    page_title    = "Tinu's JSON-Viewer"
    filepath      = os.path.join(app.config['FILE_UPLOADS'], request.form["file"])
    page_subtitle = "Data from: " + filepath

    data = []
    with open(filepath) as file:
        json_file = json.load(file)

        for row in json_file:
            row.pop('_id', None)
            row.pop('ID', None)
            data.append(row)

    return render_template("read_json.html", **locals()) 


if __name__ == '__main__':
    app.run(debug=True)
