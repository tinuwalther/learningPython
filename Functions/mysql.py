import warnings

warnings.filterwarnings('ignore', message='The NumPy module was reloaded')

import pymysql, sys, os, json, re, getpass
import pandas as pd
from bson.json_util import dumps
from datetime import datetime

def validate_string(val):
    '''Do validation and checks before insert'''
    if val != None:
        if type(val) is int:
            return str(val).encode('utf-8')
        else:
            return val

def get_table(sqlconnection, table, output = False):
    '''Test table exists'''
    sql = "SHOW TABLES LIKE '%s' "% ('%'+str(table)+'%')
    try:
        cursor = sqlconnection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        if output:
            print('[INFO]\t{0}():\tTable {1} = {2}'.format(sys._getframe().f_code.co_name, table, result[0]))
    except Exception as e:
        print('[WARN]\t{0}():\t{1}\t{2}'.format(sys._getframe().f_code.co_name, table, e))
        result = False

    return result

def drop_table(sqlconnection, table, output = False):
    '''Dropping table if already exists'''
    sql = 'DROP TABLE IF EXISTS ' + table
    try:
        cursor = sqlconnection.cursor()
        cursor.execute(sql)
        if output:
            print('[INFO]\t{0}():\tTable {1} dropped'.format(sys._getframe().f_code.co_name, table))
        return True
    except Exception as e:
        print('[WARN]\t{0}():\t{1}'.format(sys._getframe().f_code.co_name, e))
        return False

def create_table(sqlconnection, table, tabledefinition, output = False):
    '''Creating table'''
    sql = "CREATE TABLE " + table + "(" + tabledefinition + ")"
    try:
        cursor = sqlconnection.cursor()
        cursor.execute(sql)
        if output:
            print('[INFO]\t{0}():\tTable {1} created'.format(sys._getframe().f_code.co_name, table))
        return True
    except Exception as e:
        print('[WARN]\t{0}():\t{1}'.format(sys._getframe().f_code.co_name, e))
        return False

def get_rows(sqlconnection, table, output = False):
    '''Get all rows from table'''
    sql = "SELECT * FROM %s"% (str(table))
    try:
        cursor = sqlconnection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if output:
            print('[INFO]\t{0}():\tTable {1} = {2}'.format(sys._getframe().f_code.co_name, table, result[0]))
    except Exception as e:
        print('[WARN]\t{0}():\t{1}'.format(sys._getframe().f_code.co_name, e))

    return result

def insert_into(sqlconnection, table, date, cases, hosp, death, output = False):
    '''Insert one record'''
    errorcount = 0
    try:
        cursor = sqlconnection.cursor()
        cursor.execute(
            "INSERT INTO " + table + " (date, cases, hosp, death) VALUES (%s,%s,%s,%s)", (date, cases, hosp, death)
        )
        sqlconnection.commit()
        if output:
            print('[INFO]\t{0}():\tRecord inserted into table {1}'.format(sys._getframe().f_code.co_name, table))
        return True
    except Exception as e:
        print('[WARN]\t{0}():\t{1}'.format(sys._getframe().f_code.co_name, e))
        errorcount + 1
        return False

def import_json(json_file, sqlconnection, table, field1, field2, field3, field4, droptable = False):
    '''Import data from JSON-file'''
    check_path = os.path.exists(json_file)
    if(check_path == True):

        # Read JSON file
        json_data = open(json_file).read()
        json_obj  = json.loads(json_data)

        print(json_obj)

        if droptable:
            if drop_table(sqlconnection, table, output = True):
                create_table(sqlconnection, table, 'date VARCHAR(10) NOT NULL, cases INT, hosp INT, death INT', output = True)

        # parse json data to SQL insert
        errorcount   = 0
        successcount = 0
        for i, item in enumerate(json_obj):
            date  = validate_string(item.get(field1, None))
            cases = int(validate_string(item.get(field2, None)))
            hosp  = int(validate_string(item.get(field3, None)))
            death = int(validate_string(item.get(field4, None)))

            try:
                result = insert_into(sqlconnection, mytable, date, cases, hosp, death)
                if result:
                    successcount = successcount + 1
                else:
                    errorcount   = errorcount + 1
            except Exception as e:
                print('[WARN]\t{0}():\t{1}'.format(sys._getframe().f_code.co_name, e))
                errorcount + 1

        print('[INFO]\t{0}():\tInserted {1} records with {2} errors'.format(sys._getframe().f_code.co_name, successcount ,errorcount))

def export_json(json_file, sqlconnection, table, output = False):
    '''Export as JSON'''
    sqldata = get_rows(sqlconnection, table, output = False)
    if sqldata:
        try:
            result_of_history = []
            for row in sqldata:
                thisdict = {
                    'Date'   : row[0],
                    'Cases'  : row[1],
                    'Hosp'   : row[2],
                    'Death'  : row[3],
                }
                result_of_history.append(thisdict)

            # Converting to the JSON
            json_data = dumps(result_of_history)

            # Writing data to file data.json
            with open(json_file, "w") as write_file:
                write_file.write(json_data)

            if os.path.exists(json_file):
                if output:
                    print("[INFO]\t{0}():\tFile saved as {1}".format(sys._getframe().f_code.co_name, json_file))
            else:
                if output:
                    print("[INFO]\t{0}():\tCould not save file as {1}".format(sys._getframe().f_code.co_name, json_file))

            return True

        except Exception as e:
            print("[WARN]\t{0}():\t{1}".format(sys._getframe().f_code.co_name, e))
            return False

def save_linechart(data, x, y, title, path, output = False):
    '''Create chart and save it to downloads'''
    chart = data.plot.line(
        x       = x,
        xlabel  = "",
        ylabel  = "",
        y       = y,
        title   = title,
        grid    = True,
        legend  = True,
        figsize = (20,5)
    )
    ### Save chart as png-file
    fig = chart.get_figure()
    fig.savefig(f'{path}', facecolor='w', bbox_inches='tight')
    try:
        if os.path.exists(path):
            if output:
                print('[INFO]\t{0}():\tChart saved as {1}'.format(sys._getframe().f_code.co_name, path))
        else:
            if output:
                print('[INFO]\t{0}():\tCould not save chart as {1}'.format(sys._getframe().f_code.co_name, path))
    except Exception as e:
        print('[WARN]\t{0}():\t{1}'.format(sys._getframe().f_code.co_name, e))

if __name__ =="__main__":

    # Join the path to Downloads
    if sys.platform == "linux" or sys.platform == "linux2":
        home_dir = os.environ['HOME']
    elif sys.platform == "darwin":
        home_dir = os.environ['HOME']
    elif sys.platform == "win32":
        home_dir  = os.environ['USERPROFILE']
    downloads = os.path.join(home_dir,'Downloads')


    # Initiate variables
    sqlhost   = 'localhost'
    sqluser   = 'root'
    sqlusrpw  = getpass.getpass(prompt = 'Enter the password:')
    mydb      = 'tinu'
    mytable   = 'covid19'

    # Open database connection
    sqlconnection = pymysql.connect(host = sqlhost, user = sqluser, password = sqlusrpw, db = mydb)

    json_file = os.path.join(downloads, 'MysqlDB.tinu.covid19.json')
    import_json(json_file, sqlconnection, mytable, field1="Date", field2="Cases", field3="Hosp", field4="Death", droptable = True)
    
    #json_file = os.path.join(downloads, 'MongoDB.Atlas.Covid19.json')
    #import_json(json_file, sqlconnection, mytable, field1="Datum", field2="Neue Fälle", field3="Hospitalisationen", field4="Todesfälle", droptable = True)
    
    #result = insert_into(sqlconnection, mytable, '19.07.2021', 1552, 29, 4, output = True)
    #result = export_json(json_file, sqlconnection, mytable, output = True)

    '''
    covid_data = get_rows(sqlconnection, mytable, output = False)
    #print(covid_data)

    result_of_history = []
    for row in covid_data:
        thisdict = {
            'Date'   : datetime.strptime(row[0], '%d.%m.%Y'),
            'Cases'  : row[1],
            'Hosp'   : row[2],
            'Death'  : row[3],
        }
        result_of_history.append(thisdict)

    ## Create a data frame set and print out as table
    df = pd.DataFrame(result_of_history)
    print(df)

    count_of_datum = df.Date.count()
    first_value    = str(re.findall(r'\d{4}\-\d{2}\-\d{2}', str(df.Date.values[0]))[0])
    last_value     = str(re.findall(r'\d{4}\-\d{2}\-\d{2}', str(df.Date.values[count_of_datum -1]))[0])
    #print(f'Total rows: {count_of_datum}, last value: {last_value}')

    ### Print data frame set as line chart
    #save_linechart(df, 'Date', ['Cases'], f"Laborbestätige neu gemeldete Fälle - Stand: {last_value}", '/home/tinuwalther/images/covid-dayli-newcases.png', output = True)
    #save_linechart(df, 'Date', ['Hosp','Death'], f"Laborbestätige Hospitalisierungen und Todesfälle - Stand: {last_value}", '/home/tinuwalther/images/covid-dayli-host-dead.png', output = True)

    https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-newcases.png
    https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-host-dead.png
    '''
    # disconnect from server
    sqlconnection.close()