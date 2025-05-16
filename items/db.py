from django.conf import settings
from pymongo import MongoClient

def get_db_handle():
    client = MongoClient(settings.MONGODB_URI)
    db_handle = client[settings.MONGODB_DB]
    return db_handle, client

def get_collection_handle(collection_name):
    db_handle, client = get_db_handle()
    collection_handle = db_handle[collection_name]
    return collection_handle, client 