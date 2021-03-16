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


def search_injson(file,search_identifier,search_string):
    '''You can use json.load() method to read a file containing JSON object.'''
    with open(file, "r") as read_file:
        data = json.load(read_file)

    # Find in the list (array)
    for row in data:
        if row[search_identifier] == search_string:
            print(row['DisplayName'], row['ServiceName'], row['BinaryPathName'])
            # Convert to a JSON string
            #print(json.dumps(row, indent = 4))
            #break

#endregion

import os, json

get_current_location = os.path.dirname(__file__)
json_file  = get_current_location + '/test.json'

if test_path(json_file) == True:
    print(colors.fg.green + f'File found: {json_file}' + colors.reset)

    search_injson(json_file, 'ServiceName', 'wuauserv')

else:
    print(colors.fg.yellow + f'File not found: {json_file}' + colors.reset)
