import web
from storm.locals import *

def get_db():
    db = web.database(dbn='postgres', user='cameron', pw='cameron', db='cameron')
    return db

def get_store():
    db = create_database("postgres://cameron:cameron@localhost:5432/cameron")
    return Store(db)

#database = create_database("scheme://username:password@hostname:port/database_name")
