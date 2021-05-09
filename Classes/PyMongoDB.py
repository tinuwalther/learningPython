# <-- general -->
from re import T
import pymongo, dns, os, sys, csv, json

from pymongo.message import query

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


class pyMongoDB:
    """MongoDB Class
    """
    pass


    # Constructor   
    def __init__(self) -> None:
        """Constructor of class
        """
        pass


    # Successfully tested
    def get_all_databases(self, connectionstring):
        """List Database Names

        Args:
            connectionstring (String): Connection-string of the MongoDB

        Example:
            connectionstring = "localhost:27017"
            get_all_collections(self, connectionstring)
        """
        mongo_client = pymongo.MongoClient(connectionstring)
        for db in mongo_client.list_databases():
            print(db)


    # Successfully tested
    def get_all_collections(self, connectionstring, database):
        """Get list of MongoDB Collections

        Args:
            connectionstring (String): Connection-string of the MongoDB
            database (String): Database name to import the data
            
        Example:
            connectionstring = "localhost:27017"
            get_all_collections(self, connectionstring, 'JupyterNB')
        """
        mongo_client = pymongo.MongoClient(connectionstring)
        mongo_db     = mongo_client[database]        
        for collection in mongo_db.list_collection_names():
            print(collection)
    
    
    # to test
    def import_csv(self, csv_file, connectionstring, database, collection):
        """Import data from CSV-file. Delimiter must be ';'

        Args:
            csv_file (String): FullName of the CSV-file to import
            connectionstring (String): Connection-string of the MongoDB
            database (String): Database name to import the data
            collection (String): Collection name to import the data

        Example:
            credentials = input('user:password')
            connectionstring = "mongodb+srv://"+credentials+"@cluster0.epl3x.mongodb.net/?retryWrites=true&w=majority"
            imp_csv_file = "C:\\Users\\Tinu\\Downloads\\poweredOffVMs.csv"
            import_csv(imp_csv_file, connectionstring, 'JupyterNB', 'PoweredOffVMs')
        """
        check_path = os.path.exists(csv_file)
        if(check_path == True):
            
            mongo_client = pymongo.MongoClient(connectionstring)
            mongo_db     = mongo_client[database]
            mongo_col    = mongo_db[collection]

            with open(csv_file, mode='r', newline='') as read_csv_file:
                csv_data = csv.DictReader(read_csv_file, delimiter=';')
                try:
                    mongo_col.insert_many(csv_data)

                except csv.Error as e:
                    sys.exit('file {}, line {}: {}'.format(csv_file, csv_data.line_num, e))

            mongo_client.close()

        else:
            print(f'File not found: {csv_file}')
    
    
    # Successfully tested
    def import_json(self, json_file, connectionstring, database, collection):
        """Import data from JSON-file

        Args:
            json_file (String): FullName of the JSON-file to import
            connectionstring (String): Connection-string of the MongoDB
            database (String): Database name to import the data
            collection (String): Collection name to import the data
            
        Example:
            credentials = input('user:password')
            connectionstring = "mongodb+srv://"+credentials+"@cluster0.epl3x.mongodb.net/?retryWrites=true&w=majority"
            imp_json_file = "C:\\Users\\Tinu\\Downloads\\poweredOffVMs.json"
            import_json(imp_json_file, connectionstring, 'JupyterNB', 'PoweredOffVMs')
        """
        check_path = os.path.exists(json_file)
        if(check_path == True):
            
            mongo_client = pymongo.MongoClient(connectionstring)
            mongo_db     = mongo_client[database]
            mongo_col    = mongo_db[collection]

            with open(json_file, "r") as read_file:
                json_data = json.load(read_file)

            # It is important to remove the _id field in order to import it into mongodb
            for element in json_data:
                element.pop('_id', None)

            try:
                if isinstance(json_data, list):
                    mongo_col.insert_many(json_data)  
                else:
                    mongo_col.insert_one(json_data)
                
            except:
                sys.exit('file {}'.format(json_file))
                    
            mongo_client.close()

        else:
            print(f'File not found: {json_file}')


    # Successfully tested
    def export_json(self, json_file, connectionstring, database, collection):
        """Export data to JSON-file, indent = 4

        Args:
            json_file (String): FullName of the JSON-file to export
            connectionstring (String): Connection-string of the MongoDB
            database (String): Database name to export the data
            collection (String): Collection name to export the data

        Example:
            credentials = input('user:password')
            connectionstring = "mongodb+srv://"+credentials+"@cluster0.epl3x.mongodb.net/?retryWrites=true&w=majority"
            exp_json_file = "C:\\Users\\Tinu\\Downloads\\poweredOffVMs.json"
            export_json(self, exp_json_file, connectionstring, 'JupyterNB', 'PoweredOffVMs')
        """
        from bson.json_util import dumps, loads
        mongo_client = pymongo.MongoClient(connectionstring)
        mongo_db     = mongo_client[database]
        mongo_col    = mongo_db[collection]
        cursor       = mongo_col.find()
        docs         = list(cursor)
        
        mongo_client.close()

        # Converting to the JSON
        json_data = dumps(docs) 
        
        # Writing data to file data.json
        with open(json_file, 'w') as write_file:
            write_file.write(json_data)


    # Successfully tested
    def get_all_documents(self, connectionstring, database, collection):
        """Connect to MongoDB and return all documents from a collection

        Args:
            connectionstring (String): Connection-string of the MongoDB
            database (String): Database name to export the data
            collection (String): Collection name to export the data

        Returns:
            [list]: List of all documents

        Example:
            credentials = input('user:password')
            connectionstring = "mongodb+srv://"+credentials+"@cluster0.epl3x.mongodb.net/?retryWrites=true&w=majority"
            all_documents = get_all_documents(connectionstring, 'JupyterNB', 'PoweredOffVMs')
            for doc in all_documents:
                print(doc)
        """
        mongo_client = pymongo.MongoClient(connectionstring)
        mongo_db     = mongo_client[database]
        mongo_col    = mongo_db[collection]
        mongo_client.close()
        return mongo_col.find()


    # to test
    def insert_one_document(self, connectionstring, database, collection, document, output = False):
        """Connect to MongoDB and insert one document

        Args:
            connectionstring (String): Connection-string of the MongoDB
            database (String): Database name to export the data
            collection (String): Collection name to export the data
            document (JSON-String): Document to insert
            output (bool, optional): Print output. Defaults to False.

        Example:
            credentials = input('user:password')
            connectionstring = "mongodb+srv://"+credentials+"@cluster0.epl3x.mongodb.net/?retryWrites=true&w=majority"
            insert_one_document(connectionstring, 'JupyterNB', 'PoweredOffVMs', { "PSComputerName": "xsc0000989.child.domain.com", "PowerState": "Off" }, True)
        """
        mongo_client = pymongo.MongoClient(connectionstring)
        mongo_db     = mongo_client[database]
        mongo_col    = mongo_db[collection]
        mongo_col.insert_one(document)
        
        if output:
            for doc in mongo_col.find():
                print(doc)

        mongo_client.close()


    # Successfully tested
    def search_for_document(self, connectionstring, database, collection, filter):
        """Search for a document

        Args:
            connectionstring (String): Connection-string of the MongoDB
            database (String): Database name to export the data
            collection (String): Collection name to export the data
            filter (String): Filter to search for

        Example:
            credentials = input('user:password')
            connectionstring = "mongodb+srv://"+credentials+"@cluster0.epl3x.mongodb.net/?retryWrites=true&w=majority"
            search_for_document(connectionstring, 'JupyterNB', 'PoweredOffVMs', { "PSComputerName": "TIN87500803.child.domain.com" })
        """
        mongo_client = pymongo.MongoClient(connectionstring)
        mongo_db     = mongo_client[database]
        mongo_col    = mongo_db[collection]
        for doc in mongo_col.find(filter):
            print(doc)
            
        mongo_client.close()
       
        
    # to test
    def delete_all_documents(connectionstring, database, collection, query, output = False):
        """Connect to MongoDB and delete all documents

        Args:
            connectionstring (String): Connection-string of the MongoDB
            database (String): Database name to export the data
            collection (String): Collection name to export the data
            query (JSON-String): Search for 
            output (bool, optional): Print output. Defaults to False.

        Example:
            credentials = input('user:password')
            connectionstring = "mongodb+srv://"+credentials+"@cluster0.epl3x.mongodb.net/?retryWrites=true&w=majority"
            delete_collection(connectionstring, 'JupyterNB', 'PoweredOffVMs', {'address':'India'}, True)
        """
        mongo_client = pymongo.MongoClient(connectionstring)
        mongo_db     = mongo_client[database]
        mongo_col    = mongo_db[collection]
        mongo_col.delete_many(query)
        
        if output:
            for doc in mongo_col.find():
                print(doc)

        mongo_client.close()
        
        
    # Successfully tested
    def drop_collection(self, connectionstring, database, collection):
        """Delete Collection

        Args:
            connectionstring (String): Connection-string of the MongoDB
            database (String): Database name
            collection (String): Collection name to delete
        """
        mongo_client = pymongo.MongoClient(connectionstring)
        mongo_db     = mongo_client[database]
        mongo_db.drop_collection(collection)

        mongo_client.close()
        

    # to test
    def drop_database(self, connectionstring, database):
        """Delete Database

        Args:
            connectionstring (String): Connection-string of the MongoDB
            database (String): Database name to delete
        """
        mongo_client = pymongo.MongoClient(connectionstring)
        mongo_client.drop_database(database)
        
        mongo_client.close()
        
        
# Define the main function
def main():
    """Main function, call the help of each function of the class
    """
    # Create an instance of the class
    mongo = pyMongoDB()

    # Join the path to Downloads
    if sys.platform == "linux" or sys.platform == "linux2":
        home_dir = os.environ['HOME']
    elif sys.platform == "darwin":
        home_dir = os.environ['HOME']
    elif sys.platform == "win32":
        home_dir  = os.environ['USERPROFILE']
    downloads = os.path.join(home_dir,'Downloads')

    """
    credentials = input('user:password')
    connectionstring = "mongodb+srv://"+credentials+"@cluster0.epl3x.mongodb.net/?retryWrites=true&w=majority"
    
    connectionstring = "mongodb://localhost:27017"    
    mongo.drop_collection(connectionstring,'JupyterNB','PatchingHistory')
    mongo.import_json("D:\docker\JupyterNB.PatchingHistory.json",connectionstring,'JupyterNB','PatchingHistory')
 
    ## Build history from MongoDB
    from datetime import datetime
    import pandas as pd
    result_of_history = []
    connectionstring = "localhost:27017"
    for doc in mongo.get_all_documents("mongodb://localhost:27017", 'JupyterNB', 'Covid19'):
        thisdict = {     
            'Datum'             : datetime.strptime(doc['Datum'], '%d.%m.%Y'),
            'Neue Fälle'        : int(doc['Neue Fälle']),
            'Hospitalisationen' : int(doc['Hospitalisationen']),
            'H/NF'              : "{:.2%}".format(int(doc['Hospitalisationen']) / int(doc['Neue Fälle'])),
            'Todesfälle'        : int(doc['Todesfälle']),
            'T/NF'              : "{:.2%}".format(int(doc['Todesfälle']) / int(doc['Neue Fälle'])),
            'T/H'               : "{:.2%}".format(int(doc['Todesfälle']) / int(doc['Hospitalisationen']))
        }
        result_of_history.append(thisdict)

    ## Create a data frame set and print out
    df = pd.DataFrame(result_of_history)
    print(df.tail(7))
    
    # Print out all methods of the class
    method_list = []
    # attribute is a string representing the attribute name
    for attribute in dir(pyMongoDB):
        # Get the attribute value
        attribute_value = getattr(pyMongoDB, attribute)
        # Check that it is callable
        if callable(attribute_value):
            # Filter all dunder (__ prefix) methods
            if attribute.startswith('__') == False:
                method_list.append(attribute)
    
    print(method_list)
    
    # Print out the help
    print('{0}{1}{2}'.format(colors.green, mongo.import_csv.__doc__, colors.reset))
    """
        
# Call the main function
if __name__ =='__main__':
    # build the path of the current file
    print(os.path.dirname(str(sys.argv[0])))
    main()
