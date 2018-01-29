from pymongo import MongoClient
conn = MongoClient('mongodb://localhost')
db = conn.testdb
db.col.insert({'name':'yanying','province':'江苏','age':25})
