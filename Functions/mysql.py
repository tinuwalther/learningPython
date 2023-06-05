from pandas.core.base import NoNewAttributesMixin
import pymysql, sys, os, json, re, getpass
import pandas as pd

from bson.json_util import dumps
from datetime import datetime

def validate_string(val):
    '''Do validation and checks before insert'''
    try:
        if val != None:
            if type(val) is int:
                return str(val).encode('utf-8')
            else:
                return val

    except Exception as e:
        print('[WARN]\t{0}():\t{1}\t{2}'.format(sys._getframe().f_code.co_name, val, e))
        return False

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
        figsize = (15,5)
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

def save_barchart(data, x, y, title, path, output = False):
    '''Create chart and save it to downloads'''
    try:
        
        chart = data.plot.bar(
            x       = x,
            y       = y,
            title   = title,
            grid    = True,
            legend  = True,
            figsize = (15,5)
        )
        
        #chart = data.plot.bar(rot=0)
        ### Save chart as png-file
        fig = chart.get_figure()
        fig.savefig(path, facecolor='w', bbox_inches='tight')
        if os.path.exists(path):
            if output:
                print("[INFO]\t{0}():\tChart saved as {1}".format(sys._getframe().f_code.co_name, path))
        else:
            if output:
                print("[INFO]\t{0}():\tCould not save chart as {1}".format(sys._getframe().f_code.co_name, path))

    except Exception as e:
        print("[WARN]\t{0}():\t{1}".format(sys._getframe().f_code.co_name, e))


def save_sumchart(data, title, path, output = False):
    '''Create chart and save it to downloads'''
    first_value    = str(re.findall(r'\d{4}\-\d{2}\-\d{2}', str(data.Date.values[0]))[0])
    
    ### Calculate sum of values
    sum_of_swiss_people  = 8655118
    sum_of_new_cases     = int(sum(data.Cases))
    sum_of_new_hosp      = int(sum(data.Hosp))
    sum_of_new_dead      = int(sum(data.Death))

    ### Calculate percent of values
    pct_swiss_people     = "{:.2%}".format(1)
    pct_new_cases        = "{:.2%}".format(sum_of_new_cases / sum_of_swiss_people)
    pct_new_hosp         = "{:.2%}".format(sum_of_new_hosp  / sum_of_swiss_people)
    pct_new_dead         = "{:.2%}".format(sum_of_new_dead  / sum_of_swiss_people)

    ### Create the dictionary
    sum_pie_dict = {
        'Summe'  :[sum_of_swiss_people,sum_of_new_cases,sum_of_new_hosp,sum_of_new_dead],
        'Percent':[pct_swiss_people,pct_new_cases,pct_new_hosp,pct_new_dead]
    }

    ### Create the data frame set
    sum_pie_df = pd.DataFrame(data=sum_pie_dict)
    pie_index  = [
        f'Total swiss people: {sum_of_swiss_people}',
        f'Total cases: {sum_of_new_cases}',
        f'Total hospitalisations: {sum_of_new_hosp}',
        f'Total deaths: {sum_of_new_dead}'
    ]

    ### Print out the pie cahrt
    sum_plot_colors = ['lightgreen', 'yellow', 'orange', 'red']
    sum_pie_explode = (0,0.3,0.6,2.5)
    pie = sum_pie_df.plot.pie(
        title   = title, 
        labels  = pie_index,
        legend  = True,
        ylabel  = "", y = 'Summe',  
        autopct = '%1.2f%%', 
        #table   = True, 
        colors  = sum_plot_colors, 
        explode = sum_pie_explode, 
        figsize = (20,5), 
    )

    ### Save chart as png-file
    fig = pie.get_figure()
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

def save_avgchart(data, title, path, output = False):
    '''Create chart and save it to downloads'''
    first_value    = str(re.findall(r'\d{4}\-\d{2}\-\d{2}', str(data.Date.values[0]))[0])

    ### Calculate sum of values
    sum_of_new_cases     = int(sum(data.Cases))
    sum_of_new_hosp      = int(sum(data.Hosp))
    sum_of_new_dead      = int(sum(data.Death))

    ## Build average of data
    count_of_datum   = data.Date.count()
    avg_of_new_cases = int(sum_of_new_cases / count_of_datum)
    avg_of_new_hosp  = int(sum_of_new_hosp / count_of_datum)
    avg_of_new_dead  = int(sum_of_new_dead / count_of_datum)

    ## Create the dictionary with avg and sum
    pie_index   = [
        f'Average cases: {avg_of_new_cases}',
        f'Average hospitalisations: {avg_of_new_hosp}',
        f'Average deaths: {avg_of_new_dead}'
    ]

    pie_dict = {
        'Average':[avg_of_new_cases,avg_of_new_hosp,avg_of_new_dead],
        'Summe'  :[sum_of_new_cases,sum_of_new_hosp,sum_of_new_dead],
    }

    ### Print out the pie cahrt
    plot_colors    = ['lightblue', 'orange','red']
    avg_pie_df = pd.DataFrame(data = pie_dict)
    avg_pie_explode = (0,0.6,1.4)
    pie = avg_pie_df.plot.pie(
        #subplots = True, 
        ylabel  = "", y = 'Average', 
        title   = title, 
        labels  = pie_index, 
        #table   = True, 
        autopct = '%1.2f%%', 
        colors  = plot_colors, 
        explode = avg_pie_explode, 
        figsize = (20,5)
    )

    ### Save chart as png-file
    fig = pie.get_figure()
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


def weekly_average(data, table, last_value, output = False):
    '''Create weekly average'''
    try:
        end_date   = dt.datetime.strptime(last_value, '%Y-%m-%d')
        start_date = end_date - dt.timedelta(days=4)
        print(f'From: {start_date}, to: {end_date}')
        str_last_value = end_date.strftime("%d.%m.%Y")

        result_of_weekly_average = []
        for row in data:
            current_date = dt.datetime.strptime(row[0], '%d.%m.%Y')
            if end_date >= current_date >= start_date:
                str_current_date = current_date.strftime("%Y-%m-%d")
                dt_weekday       = dt.datetime.strptime(str_current_date, "%Y-%m-%d").strftime('%A %d.%m.%Y')
                thisdict = {
                    'Date'   : dt_weekday,
                    'Cases'  : row[1],
                    'Hosp'   : row[2],
                    'Death'  : row[3],
                }
                result_of_weekly_average.append(thisdict)

        ## Create a data frame set and print out as table
        df = pd.DataFrame(result_of_weekly_average)
        print(df)

        sum_weekly_dict = {
            'Date'   : last_value,
            'Cases'  : int(sum(df.Cases)/7),
            'Hosp'   : int(sum(df.Hosp)/7),
            'Death'  : int(sum(df.Death)/7),
        }
    
        if get_table(sqlconnection, table, output = False):
            pass
        else:
            create_table(sqlconnection, table, 'date VARCHAR(10) NOT NULL, cases DECIMAL(8, 2), hosp DECIMAL(8, 2), death DECIMAL(8, 2)', output = False)
        
        insert_into(sqlconnection, table, str_last_value, (sum(df.Cases)/7), (sum(df.Hosp)/7), (sum(df.Death)/7), output = False)

        if output:
            print('[INFO]\t{0}():\tWeekly average created {1}'.format(sys._getframe().f_code.co_name, sum_weekly_dict))

        return True

    except Exception as e:
        print('[WARN]\t{0}():\t{1}'.format(sys._getframe().f_code.co_name, e))
        return False


if __name__ =="__main__":

    import datetime as dt

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
    sqlusrpw  = 'my-secret-pw'
    mydb      = 'tinu'
    mytable   = 'covid19'

    # Open database connection
    sqlconnection = pymysql.connect(host = sqlhost, user = sqluser, password = sqlusrpw, db = mydb)

    json_file = os.path.join(downloads, 'MysqlDB.tinu.weekly_average.json')
    import_json(json_file, sqlconnection, 'weekly_average', field1="Date", field2="Cases", field3="Hosp", field4="Death", droptable = True)

    '''
    covid_data = get_rows(sqlconnection, mytable, output = False)
    result_of_history = []
    for row in covid_data:
        thisdict = {
            'Date'   : dt.datetime.strptime(row[0], '%d.%m.%Y'),
            'Cases'  : row[1],
            'Hosp'   : row[2],
            'Death'  : row[3],
        }
        result_of_history.append(thisdict)

    ## Create a data frame set and print out as table
    covid_df = pd.DataFrame(result_of_history)    
    #print(df)

    count_of_datum = covid_df.Date.count()
    first_value    = str(re.findall(r'\d{4}\-\d{2}\-\d{2}', str(covid_df.Date.values[0]))[0])
    last_value     = str(re.findall(r'\d{4}\-\d{2}\-\d{2}', str(covid_df.Date.values[count_of_datum -1]))[0])
    print(f'Total rows: {count_of_datum}, first value: {first_value}, last value: {last_value}')

    #drop_table(sqlconnection, 'weekly_average', output = False)

    weekly_covid_avg = get_rows(sqlconnection, 'weekly_average', output = False)
    #print(weekly_covid_avg)
    result_of_weekly_average = []
    for row in weekly_covid_avg:
        weekly_average = {
            'Date'   : dt.datetime.strptime(row[0], "%d.%m.%Y"),
            'Cases'  : int(row[1]),
            'Hosp'   : int(row[2]),
            'Death'  : int(row[3]),
        }
        result_of_weekly_average.append(weekly_average)
    ## Create a data frame set and print out as table
    weekly_covid_df = pd.DataFrame(result_of_weekly_average)    
    print(weekly_covid_df)  

    save_linechart(weekly_covid_df, "Date", ["Cases","Hosp","Death"], "Weekly-average overview - as of: " + last_value, os.path.join(downloads, "covid-weekly-avg-overview.png"), output = True)
    save_barchart(weekly_covid_df, "Date", ["Cases"], "Weekly-average of cases - as of: " + last_value, os.path.join(downloads, "covid-weekly-bar-cases.png"), output = True)
    save_barchart(weekly_covid_df, "Date", ["Hosp","Death"], "Weekly-average of hospitalisations and death - as of: " + last_value, os.path.join(downloads, "covid-weekly-avg-host-death.png"), output = True)
    '''


    '''
    # Weekly average
    #if weekly_average(covid_data, last_value, output = True):
    weekly_covid_avg = get_rows(sqlconnection, 'weekly_average', output = False)
    #print(weekly_covid_avg)
    result_of_weekly_average = []
    for row in weekly_covid_avg:
        weekly_average = {
            'Date'   : dt.datetime.strptime(row[0], "%d.%m.%Y"),
            'Cases'  : int(row[1]),
            'Hosp'   : int(row[2]),
            'Death'  : int(row[3]),
        }
        result_of_weekly_average.append(weekly_average)

    ## Create a data frame set and print out as table
    df = pd.DataFrame(result_of_weekly_average)    
    print(df)   
    save_linechart(df, "Date", ["Cases","Hosp","Death"], "Weekly-average - as of: " + last_value, os.path.join(downloads, "covid-weekly-average.png"), output = True)


    ALTER TABLE covid19
    ADD 7cases INT AFTER cases;

    ALTER TABLE covid19
    ADD 7hosp INT AFTER hosp;
    
    ALTER TABLE covid19
    ADD 7death INT AFTER death;


    save_sumchart(data=df, title=f"Total-overview in relation to the Swiss population since {first_value} - as of: {last_value}", path = os.path.join(downloads,'covid-sum-overview.png'), output = True)
    save_avgchart(data=df, title=f"Average-overview in relation to the number of days since {first_value} - as of: {last_value}", path = os.path.join(downloads,'covid-avg-overview.png'), output = True)

    #json_file = os.path.join(downloads, 'MysqlDB.tinu.covid19.json')
    #import_json(json_file, sqlconnection, mytable, field1="Date", field2="Cases", field3="Hosp", field4="Death", droptable = True)
    
    #json_file = os.path.join(downloads, 'MongoDB.Atlas.Covid19.json')
    #import_json(json_file, sqlconnection, mytable, field1="Datum", field2="Neue Fälle", field3="Hospitalisationen", field4="Todesfälle", droptable = True)
    
    #result = insert_into(sqlconnection, mytable, '19.07.2021', 1552, 29, 4, output = True)
    #result = export_json(json_file, sqlconnection, mytable, output = True)

    ### Print data frame set as line chart
    #save_linechart(df, 'Date', ['Cases'], f"Laborbestätige neu gemeldete Fälle - Stand: {last_value}", '/home/tinuwalther/images/covid-dayli-newcases.png', output = True)
    #save_linechart(df, 'Date', ['Hosp','Death'], f"Laborbestätige Hospitalisierungen und Todesfälle - Stand: {last_value}", '/home/tinuwalther/images/covid-dayli-host-dead.png', output = True)

    https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-newcases.png
    https://tinuwalther.pythonanywhere.com/static/images/covid-dayli-host-dead.png
    '''
    # disconnect from server
    sqlconnection.close()
