from tinydb import TinyDB

db = TinyDB('database/db.json')

Jobs = db.table('jobs')