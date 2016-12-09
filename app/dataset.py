from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.reddit

def num_comments():
    return db.comments.count()
