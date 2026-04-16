from pymongo import MongoClient
from .variables import CONNECTION_STRING, DB_NAME

def get_database():
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client[DB_NAME]
