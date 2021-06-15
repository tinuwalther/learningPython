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
def get_data_version(url):
    '''return JSON-file'''
    from bson.json_util import loads
    response = requests.get(url +"/context")
    if(response.status_code == 200):
        html_content = response.content.decode("utf-8")
        json_data = loads(html_content)
        if "dataVersion" in json_data:
            data = json_data["dataVersion"]
            return data
        else:
            print("dataVersion not found")
    else:
        print(response.status_code)

def get_source_date(url):
    '''return JSON-file'''
    from bson.json_util import loads
    response = requests.get(url +"/context")
    if(response.status_code == 200):
        html_content = response.content.decode('utf-8')
        json_data = loads(html_content)
        if "sourceDate" in json_data:
            data = json_data["sourceDate"]
            return data
        else:
            print("sourceDate not found")
    else:
        print(response.status_code)

def get_apidata(url, type, last_update):
    '''return JSON'''
    from bson.json_util import loads
    #data_json_url = f"{url}/sources/COVID19{type}_geoRegion.json"
    data_json_url = url + "/sources/COVID19" + type + "_geoRegion.json"
    #print(data_json_url)
    response = requests.get(data_json_url)
    if(response.status_code == 200):
        html_content = response.content.decode("utf-8")
        json_data = loads(html_content)
        for row in json_data:
            if row["geoRegion"] == "CH":
                if row["datum"] == last_update:
                    return "Total:\t" + str(row["sumTotal"]) + "\nToday:\t" + str(row["entries_diff_last"])

if __name__ =="__main__":
    api_url      = "https://www.covid19.admin.ch/api/data"
    data_version = get_data_version(api_url)
    source_date  = get_source_date(api_url)
    last_update = source_date[0:10]

    data_version_url = api_url + "/" + data_version
    if data_version_url:
        cases = get_apidata(data_version_url, "Cases", last_update)
        hosp  = get_apidata(data_version_url, "Hosp", last_update)
        death = get_apidata(data_version_url, "Death", last_update)
        discord_data = {
            "Cases": cases,
            "Hospitalisations": hosp,
            "Deaths": death,
        }
        send_discord_message(discord_data, last_update)