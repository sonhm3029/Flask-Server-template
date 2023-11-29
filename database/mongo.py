import os
import pymongo
from pymongo import MongoClient
from datetime import datetime

from utils.logger import log
from logging import INFO, ERROR

db = None
client = None



class AutoTimestampedCollection(pymongo.collection.Collection):
    def __init__(self, database, name):
        super().__init__(database, name)

    def insert_one(self, document, *args, **kwargs):
        document["created_at"] = datetime.utcnow()
        return super().insert_one(document, *args, **kwargs)

    def insert_many(self, documents, *args, **kwargs):
        for document in documents:
            document["created_at"] = datetime.utcnow()
        return super().insert_many(documents, *args, **kwargs)

    def update_one(self, filter, update, *args, **kwargs):
        if "$set" not in update:
            update["$set"] = {}
        update["$set"]["updated_at"] = datetime.utcnow()
        return super().update_one(filter, update, *args, **kwargs)

    def replace_one(self, filter, replacement, *args, **kwargs):
        replacement["updated_at"] = datetime.utcnow()
        return super().replace_one(filter, replacement, *args, **kwargs)

class MongoDb:
    
    def __init__(self):
        self.db = None
        self.client = None
        self.collections = {}
    
    def connect(self):
        try:
            DB_URL = os.environ["DB_URL"]
            client = MongoClient(f"{DB_URL}")
            db = client["flask_database"]
            self.db = db
            self.client = client
            log(INFO, "Successfully connect to mongodb!")
        except Exception as e:
            log(ERROR, str(e) or "Smt bad occured with database!")
            
    def get_collections(self):
        for coll in self.db.list_collection_names():
            self.collections[coll] = AutoTimestampedCollection(self.db, coll)
        
mongodb = MongoDb()