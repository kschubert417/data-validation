import os
from tables.masterfile import masterfile
from tables.product_family import product_family

from tables import dbsetup
# from tables import masterfile, product_family
'''from tables.masterfile import *
from tables.product_family import *'''

mf = masterfile()
pf = product_family()
# print(os.listdir())
# print(os.getcwd())
# print(os.path.join(os.getcwd(), 'app', 'MOCK_DATA.csv'))
mf = os.path.join(os.getcwd(), 'app', 'masterdata.csv')
prodfam = os.path.join(os.getcwd(), 'app', 'prodfam_data.csv')

dbfile = os.path.join(os.getcwd(), 'app', 'schema.db')

dbsetup.cleardb(dbfile)
dbsetup.dbsetup(dbfile)

mf.createtable(dbfile)
pf.createtable(dbfile)

mf.insertdata(mf, dbfile)
pf.insertdata(prodfam, dbfile)
'''
masterfile.basiccheck(dbfile)
'''