from .mongo import mongodb
from utils.logger import log
from logging import INFO

def init_collections():
    db = mongodb.db
    collections = {
        "users": {
            "validator": {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["username", "password"],
                    "unique": ["username"],
                    "properties": {
                        "username": {
                            "bsonType": "string",
                            "description": "username must be string and unique",
                        },
                        "password": {
                            "bsonType": "string",
                            "description": "password must be string"
                        }
                    }
                }
            }
        },
        
    }
    print(db, "DB")
    for coll in collections:
        if coll not in db.list_collection_names():
            db.create_collection(coll)
        if "unique" in collections[coll]["validator"]["$jsonSchema"]:
            for field in collections[coll]["validator"]["$jsonSchema"]["unique"]:
                db[coll].create_index(field, unique=True)
            collections[coll]["validator"]["$jsonSchema"].pop("unique")
        
        db.command("collMod", coll, validator=collections[coll]["validator"])
    
    log(INFO, "Success validate and connect to collections")
    
    