import pymysql, os, json, sys

# do validation and checks before insert
def validate_string(val):
    if val != None:
        if type(val) is int:
            return str(val).encode('utf-8')
        else:
            return val


# Join the path to Downloads
if sys.platform == "linux" or sys.platform == "linux2":
    home_dir = os.environ['HOME']
elif sys.platform == "darwin":
    home_dir = os.environ['HOME']
elif sys.platform == "win32":
    home_dir  = os.environ['USERPROFILE']
downloads = os.path.join(home_dir,'Downloads')


# read JSON file which is in the downloads folder
json_file = os.path.join(downloads, 'MongoDB.Atlas.Covid19.json')
json_data = open(json_file).read()
json_obj  = json.loads(json_data)
#print(json_obj)

# Define the dtabase and table
mydb    = 'tinu'
mytable = 'covid19'
passwd  = input('password:')

# connect to MySQL
con = pymysql.connect(host = 'localhost', user = 'root', password = passwd, db = mydb)
cursor = con.cursor()

#Dropping EMPLOYEE table if already exists.
sql = 'DROP TABLE IF EXISTS ' + mytable
cursor.execute(sql)

# Creating table as per requirement
sql = "CREATE TABLE " + mytable + "(Datum DATETIME NOT NULL, Fälle INT, Hospitalisationen INT, Todesfälle INT)"
cursor.execute(sql)


# parse json data to SQL insert
for i, item in enumerate(json_obj):
    date  = validate_string(item.get("Datum", None))
    cases = int(validate_string(item.get("Neue Fälle", None)))
    hosp  = int(validate_string(item.get("Hospitalisationen", None)))
    death = int(validate_string(item.get("Todesfälle", None)))
    #print(date, cases, hosp, death)

    cursor.execute(
        "INSERT INTO " + mytable + " (Datum, Fälle, Hospitalisationen, Todesfälle) VALUES (%s,%s,%s,%s)", (date, cases, hosp, death)
    )

con.commit()
con.close()
