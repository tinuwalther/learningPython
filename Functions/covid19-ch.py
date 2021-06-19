# coding=utf-8
import requests

def send_discord_message(data, date):
    '''Send Discord message'''
    webhook_url         = 'your webhook address'
    author_name         = 'Covid19 Hook'
    author_avatar       = 'https://i2.pngguru.com/preview/189/787/605/covid19-coronavirus-corona-violet-pink-purple-cartoon-magenta-smile-png-clipart-thumbnail.jpg'
    section_title       = '[INFO] COVID-19 Statistics for SWITZERLAND'
    section_description = "Information on the current situation, as of " + date

    embeds = {
        "title": section_title, "description": section_description, "color": 32767,
        "fields": [
            {"name" : "Confirmed Cases", "value" : data["Cases"], "inline": "true"},
            {"name" : "Hospitalisations", "value" : data["Hospitalisations"], "inline": "true"},
            {"name" : "Deaths", "value" : data["Deaths"], "inline": "true"},
            {"name" : "Official website", "value" : "[Federal Office of Public Health FOPH | Bundesamt für Gesundheit BAG](https://www.covid19.admin.ch/en/overview?ovTime=total)"}
        ]
    }

    data = {
        "username": author_name, "avatar_url": author_avatar, "embeds": [embeds],
    }

    headers = {
        "Content-Type": "application/json"
    }

    result = requests.post(webhook_url, json=data, headers=headers)
    if 200 <= result.status_code < 300:
        print("[INFO] Webhook sent {0}".format(result.status_code))
    else:
        print("[WARN] Not sent with {0}, response: {1}".format(result.status_code, result.json()))

# Covid19-CH API
def get_api_context(url):
    '''return JSON-file'''
    from bson.json_util import loads
    response = requests.get(url +"/context")
    if(response.status_code == 200):
        html_content = response.content.decode('utf-8')
        json_data = loads(html_content)
        if "dataVersion" in json_data:
            dataVersion = json_data["dataVersion"]
        else:
            dataVersion = None
            print("dataVersion not found")

        return dataVersion

    else:
        print(response.status_code)


def get_api_data(url, type, last_update):
    '''return JSON'''
    from bson.json_util import loads
    data_json_url = url + "/sources/COVID19" + type + "_geoRegion.json"
    response = requests.get(data_json_url)
    if(response.status_code == 200):
        html_content = response.content.decode("utf-8")
        json_data = loads(html_content)
        for row in json_data:
            if row["geoRegion"] == "CH":
                if row["datum"] == last_update:
                    return "Total:\t" + str(row["sumTotal"]) + "\nToday:\t" + str(row["entries_diff_last"])


def add_document(connectionstring, mongodatabase, collection, document):
    '''Connect to MongoDB and add a document'''
    import pymongo
    mongo_client = pymongo.MongoClient(connectionstring)
    mongo_db     = mongo_client[mongodatabase]
    mongo_col    = mongo_db[collection]
    mongo_col.insert_one(document)
    mongo_client.close()


if __name__ =="__main__":
    import datetime as dt, time
    api_url      = "https://www.covid19.admin.ch/api/data"
    data_version = get_api_context(api_url)
    last_update  = data_version[0:4] + "-" + data_version[4:6] + "-" + data_version[6:8]
    dt_format    = "%Y-%m-%d"
    dt_today     = dt.datetime.today()
    str_today    = dt_today.strftime(dt_format)
    dt_weekday   = dt.datetime.strptime(str_today, dt_format).strftime('%A')
    if dt_weekday == 'Saturday' or dt_weekday == 'Sunday':
        #print('Its weekend: ' + dt_weekday)
        pass
    else:
        #print(dt_weekday)
        data_version_url = api_url + "/" + data_version
        if data_version_url:
            cases = get_api_data(data_version_url, "Cases", last_update)
            hosp  = get_api_data(data_version_url, "Hosp", last_update)
            death = get_api_data(data_version_url, "Death", last_update)
            discord_data = {
                "Cases": cases,
                "Hospitalisations": hosp,
                "Deaths": death,
            }
            #print(discord_data)
            send_discord_message(discord_data, last_update)

            #Adapt data for MongoDB
            connectionstring = "mongodb+srv://tinu:10J9nSVN3XN7srEgYEKI@cluster0.epl3x.mongodb.net/?retryWrites=true&w=majority"        
            dt_last_update   = dt.datetime.strptime(last_update, dt_format)
            dt_format        = "%d.%m.%Y"
            str_last_update  = dt_last_update.strftime(dt_format)
            document = {
                "Datum"            : str_last_update,
                "Neue Fälle"       : cases.split("\t")[2],
                "Hospitalisationen": hosp.split("\t")[2],
                "Todesfälle"       : death.split("\t")[2],
            }
            #print(document)
            add_document(connectionstring, 'JupyterNB', 'Covid19', document)
