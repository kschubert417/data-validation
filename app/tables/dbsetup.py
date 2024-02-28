import sqlite3

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
        print(i[0])
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
           ''']

    for statement in sql:
        cur.execute(statement)

    con.commit()
    con.close()
