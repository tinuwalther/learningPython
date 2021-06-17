# coding=utf-8
# import pymdbc
# pymdbc.import_json('/Users/Tinu/Downloads/Atlas.JupyterNB.Covid19.json','localhost','tinu','covid19')

#  <-- general -->
import pymongo, dns, os, sys, csv, json

# Successfully tested
def get_all_databases(connectionstring):
    """List Database Names

    Args:
        connectionstring (String): Connection-string of the MongoDB

    Example:
        connectionstring = "localhost:27017"
        get_all_collections(connectionstring)
    """
    mongo_client = pymongo.MongoClient(connectionstring)
    for db in mongo_client.list_databases():
        print(db)


# Successfully tested
def get_all_collections(connectionstring, database):
    """List Collection Names

    Args:
        connectionstring (String): Connection-string of the MongoDB
        database (String): Database name to import the data
        
    Example:
        connectionstring = "localhost:27017"
        get_all_collections(connectionstring, 'JupyterNB')
    """
    mongo_client = pymongo.MongoClient(connectionstring)
    mongo_db     = mongo_client[database]        
    for collection in mongo_db.list_collection_names():
        print(collection)


# to test
def import_csv(csv_file, connectionstring, database, collection):
    """Import data from CSV-file. Delimiter must be ';'

    Args:
        csv_file (String): FullName of the CSV-file to import
        connectionstring (String): Connection-string of the MongoDB
        database (String): Database name to import the data
        collection (String): Collection name to import the data

    Example:
        connectionstring = "localhost:27017"
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
        print('[WARN] File not found: ' + csv_file)


# Successfully tested
def import_json(json_file, connectionstring, database, collection):
    """Import data from JSON-file

    Args:
        json_file (String): FullName of the JSON-file to import
        connectionstring (String): Connection-string of the MongoDB
        database (String): Database name to import the data
        collection (String): Collection name to import the data
        
    Example:
        connectionstring = "localhost:27017"
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
        print('[WARN] File not found: ' + json_file)


# Successfully tested
def export_json(json_file, connectionstring, database, collection):
    """Export data to JSON-file, indent = 4

    Args:
        json_file (String): FullName of the JSON-file to export
        connectionstring (String): Connection-string of the MongoDB
        database (String): Database name to export the data
        collection (String): Collection name to export the data

    Example:
        connectionstring = "localhost:27017"
        exp_json_file = "C:\\Users\\Tinu\\Downloads\\poweredOffVMs.json"
        export_json(exp_json_file, connectionstring, 'JupyterNB', 'PoweredOffVMs')
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

    check_path = os.path.exists(json_file)
    if(check_path == True):
        print('[INFO] File saved at: ' + json_file)
    else:
        print('[WARN] File not saved: ' + json_file)


# Successfully tested
def get_all_documents(connectionstring, database, collection):
    """Connect to MongoDB and return all documents from a collection

    Args:
        connectionstring (String): Connection-string of the MongoDB
        database (String): Database name to export the data
        collection (String): Collection name to export the data

    Returns:
        [list]: List of all documents

    Example:
        connectionstring = "localhost:27017"
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
def insert_one_document(connectionstring, database, collection, document, output = False):
    """Connect to MongoDB and insert one document

    Args:
        connectionstring (String): Connection-string of the MongoDB
        database (String): Database name to export the data
        collection (String): Collection name to export the data
        document (JSON-String): Document to insert
        output (bool, optional): Print output. Defaults to False.

    Example:
        connectionstring = "localhost:27017"
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
def search_for_document(connectionstring, database, collection, filter):
    """Search for a document

    Args:
        connectionstring (String): Connection-string of the MongoDB
        database (String): Database name to export the data
        collection (String): Collection name to export the data
        filter (String): Filter to search for

    Example:
        connectionstring = "localhost:27017"
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
        connectionstring = "localhost:27017"
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
def drop_collection(connectionstring, database, collection):
    """Delete Collection

    Args:
        connectionstring (String): Connection-string of the MongoDB
        database (String): Database name
        collection (String): Collection name to delete

    Example:
        connectionstring = "localhost:27017"
        drop_collection(connectionstring, 'JupyterNB', 'PoweredOffVMs')
    """
    mongo_client = pymongo.MongoClient(connectionstring)
    mongo_db     = mongo_client[database]
    mongo_db.drop_collection(collection)

    mongo_client.close()
    

# to test
def drop_database(connectionstring, database):
    """Delete Database

    Args:
        connectionstring (String): Connection-string of the MongoDB
        database (String): Database name to delete

    Example:
        connectionstring = "localhost:27017"
        drop_collection(connectionstring, 'JupyterNB')
    """
    mongo_client = pymongo.MongoClient(connectionstring)
    mongo_client.drop_database(database)
    
    mongo_client.close()


# Successfully tested
def left_join_collection(connectionstring, database, left_collection, right_collection):
    """Performs a left outer join on two collection

    Args:
        connectionstring (String): Connection-string of the MongoDB
        database (String): Database name
        left_collection (String): Collection name
        right_collection (String): Collection name

    Returns:
        [Cursor]: 

    Example:
        connectionstring = "localhost:27017"
        left_join_collection(connectionstring, database, left_collection, right_collection)
    """
    mongo_client = pymongo.MongoClient(connectionstring)
    mongo_db     = mongo_client[database]
    mongo_col    = mongo_db[left_collection]

    # Join with collection
    stage_lookup = {
        "$lookup": {
            "from"         : right_collection,  # the other collection
            "localField"   : "PSComputerName",  # name of the collection field
            "foreignField" : "PSComputerName",  # name of the collection field
            "as"           : "temp_collection", # alias for the new collection
        }
    }
    # Deconstructs an array field from the input documents
    stage_unwind = {
        "$unwind": "$temp_collection"
    }
    # define which fields are you want to fetch, 1 = left_collection
    stage_project = {
        "$project": {
            "_id"                  : 1,
            "PSComputerName"       : 1,
            "PowerState"           : "$temp_collection.PowerState",
            "LastPatchRun"         : 1,
            "LastPatchStatus"      : 1,
            "UpdateServerStatus"   : 1,
            "CcmExecVersion"       : 1,
            "CCMCimInstanceStatus" : 1,
        } 
    }

    pipeline = [
        stage_lookup,
        #stage_unwind,
        stage_project,
    ]
    mongo_client.close()

    return mongo_col.aggregate(pipeline)
