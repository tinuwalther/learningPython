# Flask WebApp

How to install python and Flask on Mac OS X foound on [GitHub Gist](https://gist.github.com/dineshviswanath/af72af0ae2031cd9949f) of Dinesh Viswanath.

## Table of content

- [Flask WebApp](#flask-webapp)
  - [Table of content](#table-of-content)
  - [Installing virtaulenv](#installing-virtaulenv)
  - [Now lets create the first flask app](#now-lets-create-the-first-flask-app)
  - [Now we will create a virtualenv](#now-we-will-create-a-virtualenv)
  - [Activate your new virtualenv](#activate-your-new-virtualenv)
  - [Install Flask](#install-flask)
  - [Create the WebApp](#create-the-webapp)
  - [MSSQL Server](#mssql-server)
  - [Run next time](#run-next-time)

## Installing virtaulenv

````bash
pip3 install virtualenv
virtualenv --version
````

## Now lets create the first flask app

````bash
cd Volumes/GitRepository/git/internal/
mkdir Sites
cd Sites
````

## Now we will create a virtualenv

````bash
virtualenv inventory_db
cd inventory_db
````

## Activate your new virtualenv

````bash
source bin/activate
````

## Install Flask

````bash
pip3 install Flask
````

## Create the WebApp

Create a new file called app.py:

````bash
touch app.py
````

Add the following code:

````
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return 'Hello, Flask!'

if __name__ == '__main__':
	app.run(debug=True)
````

Start the app:

````bash
python3 app.py
````

Open the web browser with http://localhost:5000

## MSSQL Server

````bash
pip3 install SQLAlchemy
pip3 install pymssql

conn_uri = "mssql+pymssql://<username>:<password>@<servername>/<dbname>"
````

## Run next time

````bash
cd Sites/inventory_db
source bin/activate
python3 app.py
````
