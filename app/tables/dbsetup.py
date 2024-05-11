import sqlite3

# function to map data by finding the db table each file represents
def mapdata(dbfile, data):
    '''
    data argument like: 
    data = {'masterdata.csv':{'MASTERFILE':['item', 'type', 'desc']},
            'prodfam.csv':{'PRODFAM':['family', 'desc']}}  
    '''
    for file in data:
        filename = file
        # print(data[file])
        for dbtable in data[file]:
            dbtn = dbtable
            '''print(data[file][dbtable])
            print(len(data[file][dbtable]))'''
        # print(f"File name: {file} | DB Table: {dbtn}")
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        sql = f"""INSERT INTO CONFIG_FILEMAP ([FILE], [DB_TABLE])
                    VALUES ({filename}, {dbtn})
                """

        cur.execute(sql)

        con.commit()
        con.close()

# mapdata(data)

def getmaps(dbfile):
    # dictionary to hold metadata
    mappings = {}

    columnmap = "SELECT FILE, DB_TABLE, DB_COLUMN, FILE_COLUMN FROM CONFIG_COLUMNMAP"

    # getting files that map to certain db tables
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute(columnmap)
    rows = cur.fetchall()
    conn.close()

    filemap = {}
    for file, dbtable, dbcol, filecol in rows:
        # print(f'File: {file} | DB Table: {dbtable} | DB Column: {dbcol} | File Col: {filecol}')
        # Generates dict like the following to map the database to the files 
        #                         {DBTABLE: {'file': 'file1.csv', 'cols': {'DBCOL': 'FILECOL'}},
        #                       MASTERFILE: {'file': 'MASTERFILE.csv', 'cols': {'ITEM': 'item', 'DESC': 'desc', 'TYPE': 'type'}}}
        try:
            filemap[dbtable]
        except KeyError:
            # If DB not present do this
            print("IS NOT THERE")
            filemap[dbtable] = {'file': file, 'cols': {dbcol: filecol}}
        else:
            # if DB present do this
            print("IS THERE")
            filemap[dbtable]['cols'][dbcol] = filecol
    print('\n\n', filemap)
    return filemap


# Clear all tables from database
def cleardb(dbfile):
    """Short summary.
    Will clear db of all tables
    ----------
    con : type
        Connector for database
    Returns
    -------
    type
        Description of returned object.
    """
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    sql = """SELECT name 
            FROM sqlite_master 
            WHERE type='table' AND name != 'sqlite_sequence'"""

    cur.execute(sql)
    listdelete = []

    for i in cur:
        # print(i[0])
        listdelete.append(i[0])

    for i in listdelete:
        delete = f'DROP TABLE IF EXISTS {i}'
        # print(delete)
        cur.execute(delete)

    con.commit()
    con.close()

# Create table to store problems and summary statistics
def dbsetup(dbfile):
    """Short summary.
    Will create table in database to insert data into
    Parameters
    ----------
    con : type
        Connector for database
    Returns
    -------
    type
        Description of returned object.
    """
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    sql = ['''DROP TABLE IF EXISTS SUMMARY_STATS''',
           '''CREATE TABLE IF NOT EXISTS SUMMARY_STATS (
           [TABLE]      VARCHAR (200), -- name of table
           --[ROW_COUNT]  INT, -- count of rows within table
           [COLUMN]     VARCHAR (200), -- column within table
           [MESSAGE]    VARCHAR (200), -- column from table this column references (IE: item would reference item master)
           [COUNT]      INT) -- count of errors
           ''',
           '''CREATE TABLE IF NOT EXISTS CONFIG_COLUMNMAP (
           [FILE]          VARCHAR (200), -- file name
           [DB_TABLE]      VARCHAR (200), -- database table
           [DB_COLUMN]     VARCHAR (200), -- database columm
           [FILE_COLUMN]   VARCHAR (200)) -- database column that file is mapped to
           '''
           ]

    for statement in sql:
        # print(statement)
        cur.execute(statement)

    con.commit()
    con.close()

if __name__ == "__main__":
    dbfile = 'app\schema.db'

    # cleardb(dbfile)
    # dbsetup(dbfile)
    getmaps(dbfile)
