#region define colors
class colors: 
    '''Colors class:reset all colors with colors.reset'''

    reset         = '\033[0m'
    bold          = '\033[01m'
    disable       = '\033[02m'
    underline     = '\033[04m'
    reverse       = '\033[07m'
    strikethrough = '\033[09m'
    invisible     = '\033[08m'

    class fg: 
        ''' Define the foreground-colors
        use as colors.fg.colorname
        '''
        black      = '\033[30m'
        red        = '\033[31m'
        green      = '\033[32m'
        orange     = '\033[33m'
        blue       = '\033[34m'
        purple     = '\033[35m'
        cyan       = '\033[36m'
        lightgrey  = '\033[37m'
        darkgrey   = '\033[90m'
        lightred   = '\033[91m'
        lightgreen = '\033[92m'
        yellow     = '\033[93m'
        lightblue  = '\033[94m'
        pink       = '\033[95m'
        lightcyan  = '\033[96m'

    class bg: 
        ''' Define the background-colors
        use as colors.bg.colorname
        '''
        black     = '\033[40m'
        red       = '\033[41m'
        green     = '\033[42m'
        orange    = '\033[43m'
        blue      = '\033[44m'
        purple    = '\033[45m'
        cyan      = '\033[46m'
        lightgrey = '\033[47m'
#endregion

#region define functions
def test_path(file):
    '''The Test-Path function determines whether all elements of the path exist.
    It returns True if all elements exist and False if any are missing.'''
    check_path = os.path.exists(file)
    return(check_path)


def import_csv(file):
    '''The Import-Csv function creates table-like custom objects from the items in CSV files.
    Each column in the CSV file becomes a property of the custom object and the items in rows become the property values.'''
    import csv, sys
    with open(file, mode='r') as csv_file:
        try:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            collection = []
            for row in csv_reader:
                collection.append(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(file, csv_reader.line_num, e))

    return(collection)


def get_csvrow(file,filter):
    '''Import-CSV and do something with one row'''
    import csv, sys
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        try:
            for row in csv_reader:
                VMName = row["VMName"]
                if(VMName == filter):
                    print(row["Hostname"], row["IpV4Address"])
                    
                    #print(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(file, csv_reader.line_num, e))


def convertto_json(object):
    '''The ConvertTo-Json function converts any object to a string in JavaScript Object Notation (JSON) format.'''
    import json
    line_number = 0
    for row in object:
        line = json.dumps(row, indent = 4)
        line_number += 1
        print(colors.fg.green + f'Row {line_number}' + colors.reset)
        print(line)

#endregion

#region process
import os
get_current_location = os.getcwd()

csv_file  = get_current_location + '/test.csv'
if(test_path(csv_file) == True):
    print(colors.fg.blue + 'Import-Csv in a collection:' + colors.reset)
    csvobject = import_csv(csv_file)
    print(csvobject)

    print(colors.fg.blue + 'JavaScript Object Notation (JSON):' + colors.reset)
    convertto_json(csvobject)

    print(colors.fg.blue + 'Import-CSV and do something with one row:' + colors.reset)
    get_csvrow(csv_file,'SBB')
else:
    print(f'File not found: {csv_file}')

#endregion