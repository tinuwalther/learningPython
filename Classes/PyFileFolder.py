import os, sys, glob, time
import pandas as pd
from datetime import datetime, timedelta

class colors():
    """define colors
    """
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
    reset      = '\033[0m'


class pyFileFolder:
    """File and folder class
    """
    pass

    # Constructor   
    def __init__(self) -> None:
        """Constructor of class
        """
        pass

    def list_directory(self, path):
        """List the content of a directory, this can be files and subfolders

        Args:
            path (string): path to the directory
        """
        dirs = os.listdir(path)
        print('{0}{1}{2}'.format(colors.purple, dirs, colors.reset))


    def list_tree(self, path):
        """Walk trough a directory tree

        Args:
            path (string): path to the directory
        """
        for root, directories, files in os.walk(path, topdown=False):
            for name in files:
                fullname = os.path.join(root, name)
                print('{0}file:   {1}{2}'.format(colors.purple, fullname, colors.reset))
            for name in directories:
                fullname = os.path.join(root, name)
                print('{0}folder: {1}{2}'.format(colors.purple, fullname, colors.reset))


    def file_exists(self, path, file):
        """Check if the file exists

        Args:
            path (string): path to the directory
            file (string): name of the file to check
        """
        fullname = os.path.join(path,file)
        if os.path.exists(fullname):
            print('{0}{1} exists{2}'.format(colors.purple, fullname, colors.reset))
        else:
            print('{0}{1} not exists{2}'.format(colors.purple, fullname, colors.reset))


    def get_latest_file(self, path, pattern):
        """Check for the latest (most recent) file of the path

        Args:
            path    (string): path to the directory
            pattern (string): pattern to search for

        Returns:
            string: the name of the latest (most recent) file
        """
        fullpath = os.path.join(path, pattern)
        files = glob.glob(fullpath)
        if not files: 
            return None
        latest_file = max(files, key=os.path.getctime)
        return latest_file


    def get_sorted_list_of_files(self,path,pattern):
        """Get a sorted list of files

        Args:
            path    (string): path to the directory
            pattern (string): pattern to search for

        Returns:
            list: a list of files with the properties LastWriteTime, Name, FullName
        """
        all_files    = glob.glob(os.path.join(path, pattern))
        files_sorted = sorted(all_files, key=lambda t: -os.stat(t).st_mtime)
        file_object  = []
        for file in files_sorted:
            modTimesinceEpoc = os.path.getctime(file)
            modificationtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
            file_dict = {
                'LastWriteTime' : modificationtime,
                'Name'          : os.path.basename(file),
                'FullName'      : file,
            }
            file_object.append(file_dict)

        return file_object


    def get_latest_number_of_files(self,path,pattern,days):
        """Get a list with sorted files newer than specified days

        Args:
            path (string): path to the directory
            pattern (string): pattern to search for
            days (int): number of days

        Returns:
            list: a list of files with the properties LastWriteTime, Name, FullName
        """
        all_files    = glob.glob(os.path.join(path, pattern))
        files_sorted = sorted(all_files, key=lambda t: -os.stat(t).st_mtime)
        file_object  = []
        for file in files_sorted:
            modTimesinceEpoc = os.path.getctime(file)
            modificationtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
            file_datetime    = datetime.strptime(modificationtime, "%Y-%m-%d %H:%M:%S")
            if file_datetime > days:
                file_dict = {
                    'LastWriteTime' : modificationtime,
                    'Name'          : os.path.basename(file),
                    'FullName'      : file,
                }
                file_object.append(file_dict)

        return file_object


# Define the main function
def main(dirpath):
    '''main function'''

    # Get the current direcory
    print('{0}Current location{1}'.format(colors.green, colors.reset))
    print('{0}{1}{2}'.format(colors.purple, os.getcwd(), colors.reset))

    # Execute functions with directory path
    print('{0}Directory{1}'.format(colors.green, colors.reset))
    print('{0}{1}{2}'.format(colors.purple, dirpath, colors.reset))

    # Create an instance of the class
    dir = pyFileFolder()

    # 1. Get a list of files in the directory
    print('{0}{1}{2}'.format(colors.green, dir.list_directory.__doc__, colors.reset))
    dir.list_directory(dirpath)

    # 2. Get a tree list of the directory
    print('{0}{1}{2}'.format(colors.green, dir.list_tree.__doc__, colors.reset))
    dir.list_tree(dirpath)

    # 3. Check if a file exists
    print('{0}{1}{2}'.format(colors.green, dir.file_exists.__doc__, colors.reset))
    dir.file_exists(dirpath,'vscode.png')

    # 4. Get the latest file of a directory
    print('{0}{1}{2}'.format(colors.green, dir.get_latest_file.__doc__, colors.reset))
    print('{0}{1}{2}'.format(colors.purple, dir.get_latest_file(dirpath, '*'), colors.reset))

    # 5. Get sorted file list
    print('{0}{1}{2}'.format(colors.green, dir.get_sorted_list_of_files.__doc__, colors.reset))
    filelist = dir.get_sorted_list_of_files("/Users/Tinu/Temp/", '*.*')
    for file in filelist:
        print(f"{file['LastWriteTime']}\t{file['Name']}\t{file['FullName']}")
    
    # 6. Get all files greater than 3 days before
    print('{0}{1}{2}'.format(colors.green, dir.get_latest_number_of_files.__doc__, colors.reset))
    day3before = (datetime.now() - timedelta(days=3))
    filelist = dir.get_latest_number_of_files("/Users/Tinu/Temp/", '*.*', day3before)
    for file in filelist:
        print('{0}{1}{2}'.format(colors.yellow, file['LastWriteTime'] + ', ' + file['Name']+ ', ' + file['FullName'], colors.reset))

    df = pd.DataFrame(filelist)
    print('{0}{1}{2}'.format(colors.yellow, df, colors.reset))

# Call the main function
if __name__ =='__main__':
    # build the path of the current file
    dirpath = os.path.dirname(str(sys.argv[0]))
    main(dirpath)