import os
import sqlite3

from tables import dbsetup
from tables import masterfile

# print(os.listdir())
# print(os.getcwd())
# print(os.path.join(os.getcwd(), 'app', 'MOCK_DATA.csv'))
mf = os.path.join(os.getcwd(), 'app', 'masterdata.csv')
prodfam = os.path.join(os.getcwd(), 'app', 'prodfam_data.csv')
dbfile = os.path.join(os.getcwd(), 'app', 'schema.db')

dbsetup.cleardb(dbfile)
dbsetup.dbsetup(dbfile)

masterfile.createtable(dbfile)
masterfile.insertdata(mf, dbfile)
masterfile.basiccheck(dbfile)
