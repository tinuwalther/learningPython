def import_csv(file):
    '''Import-CSV -File'''
    import csv
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        collection = []
        for row in csv_reader:
            collection.append(row)

def get_csvrow(file):
    '''Import-CSV and do somesthing with one row'''
    import csv
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            VMName = row["VMName"]
            if(VMName == 'TINU0052016'):
                print(row["Hostname"], row["IpV4Address"])
                #print(row)

def convertto_json(object):
    '''ConvertTo-Json -Object'''
    import json
    for row in object:
        line = json.dumps(row, indent = 4)
        print(line)

csv_file  = 'd:\\DevOps\\github.com\\learningPython\\Functions\\test.csv'
get_csvrow(csv_file)
#csvobject = import_csv(csv_file)
#convertto_json(csvobject)