sumstats = {"table": "SUMMARY_STATS",
            "columns": "([TABLE], [COLUMN], [MESSAGE], [COUNT])"}

# SQL Builder Class, can run SQL also

# Document to generate SQL scripts to be executed
def pkcheck(table, pk, message):
    '''
    table: name of table
    pk: primary key of table
    message: error message to provide additional information

    EXAMPLE:
        INSERT INTO SUMMARY_STATS ([TABLE], [COLUMN], [MESSAGE], [COUNT])
        SELECT 'MASTERFILE', 'ITEM', 'MESSAGE', COUNT(DISTINCT(ITEM))
        FROM MASTERFILE
        GROUP BY ITEM
        HAVING COUNT(*) > 1
    '''
    run = []
    sql1 = (f'INSERT INTO {sumstats["table"]} {sumstats["columns"]}\n'+
            f'SELECT \'{table}\',\'{pk[0]}\',\'{message}\',COUNT(DISTINCT {pk[0]})\n'+
            f'FROM {table}\n'+
            f'GROUP BY {pk[0]}\n'+
            f'HAVING COUNT(*) > 1\n')

    sql2 = (f'INSERT INTO {table}_ERRORS\n'+
            f'SELECT *, \'{message}\' AS ERROR_MESSAGE\n'+
            f'FROM {table}\n'+
            f'WHERE {pk[0]} IN (\n'+
            f'SELECT {pk[0]}\n'
            f'FROM {table}\n'
            f'GROUP BY {pk[0]}\n'
            f'HAVING COUNT(*) > 1)')

    run = [sql1] + [sql2]
    # print(sql)
    # return(sql)
    return(run)

def droptable(table):
    '''
    db: database file
    table: name of table
    '''
    sql = f'DROP TABLE IF EXISTS {table}\n'

    # print(sql)
    return(sql)

def createtable(table, columns):
    '''
    table: name of table
    columns: columns you want to insert data into
    '''
    col = ''
    type = ' VARCHAR(200)'
    n = 1
    for i in columns:
        if n != len(columns):
            col = col + str(i) + type + ',\n'
        else:
            col = col + str(i) + type + '\n'
        n += 1

    sql = f'CREATE TABLE IF NOT EXISTS {table}\n({col})\n'

    # print(sql)
    return(sql)

def createerrortable(table, columns):
    '''
    table: name of table
    columns: columns you want to insert data into
    '''
    col = ''
    type = ' VARCHAR(200)'
    n = 1
    columns = columns + ["ERROR_MESSAGE"]
    for i in columns:
        if n != len(columns):
            col = col + str(i) + type + ',\n'
        else:
            col = col + str(i) + type + '\n'
        n += 1

    sql = f'CREATE TABLE IF NOT EXISTS {table}_ERRORS\n({col})\n'

    # print(sql)
    return(sql)

def instertdata(table, columns, order=None):
    '''
    table: name of table
    columns: columns you want to insert data into
    '''
    value = ''
    col = ''
    n = 0
    if order == None:
        for i in columns:
            if n == 0:
                value = '(?'
                col = str(i)
            else:
                value = value + ',?'
                col = col + ',' + str(i)
            n += 1
    else:
        for i in order:
            if n == 0:
                value = '(?'
                col = str(i)
            else:
                value = value + ',?'
                col = col + ',' + str(i)
            n += 1

    value = value + ')'

    sql = f'''INSERT INTO {table} ({col})\nVALUES {value}\n'''

    # print(sql)
    return(sql)

def checkvalues(table, av):
    '''
    table: name of table
    av: allowed values for column, ie: item type should be 'ITEM_TYPE = (0,1,2,3,4)'
    message: error message to provide additional information
    '''
    # print(f'Length of AV: {len(av)}')

    sql = []

    if len(av) == 0:
        pass
    else:
        message = ''
        for col in av:
            message = 'INVALID ' + col + ' VALUES'

            sql1 = (f'INSERT INTO {sumstats["table"]} {sumstats["columns"]}\n'+
                    f'SELECT \'{table}\',\'{col}\',\'{message}\', COUNT(*)\n'+
                    f'FROM {table}\n'+
                    f'WHERE {col} NOT IN {av[col]};\n\n')

            sql2 = (f'INSERT INTO {table}_ERRORS\n'+
                    f'SELECT *, \'{message}\'\n'+
                    f'FROM {table}\n'+
                    f'WHERE {col} NOT IN {av[col]};\n\n')            

            sql = sql + [sql1] + [sql2]

    # print(sql)
    return(sql)

    


# Testing ================================
if __name__ == "__main__":
    # setting up example test table
    testtable = {'table_name':'MASTERFILE',
                'columns':['ITEM','DESCRIPTION','ITEM_TYPE','PRODFAM'],
                'pk':['ITEM']}

    testtableconstraints = {'pk':['ITEM'], # primary key of table
                           'fk':['PRODFAM.PRODFAM'], # column that contains reference to another table
                           'av':{'ITEM_TYPE': '(0,1,2,3,4)',
                                 'PRODFAM': '(\'HI\', \'HI2\', \'HI3\')'} # allowed values for columns, write in SQL
                           }
    
    # running functions
    # print("--SQL SCRIPT TO CREATE TABLE =====================")
    # print(createtable(testtable["table_name"], testtable["columns"]))
    # print("\n--SQL SCRIPT TO INSERT DATA =====================")
    # print(instertdata(testtable["table_name"], testtable["columns"]))
    # print("\n--SQL SCRIPT TO CHECK PRIMARY KEY =====================")
    # print(pkcheck(testtable["table_name"], testtableconstraints['pk'], "test_test_test"))
    # for i in pkcheck(testtable["table_name"], testtableconstraints['pk'], "test_test_test"):
    #    print(i)
    # print("\n--SQL SCRIPT TO DROP TABLE =====================")
    # print(droptable(testtable["table_name"]))
    print("\n--SQL SCRIPT TO SEE IF VALUES FOR COLUMNS ADHERE TO RULES =====================")
    cv = checkvalues(testtable["table_name"], testtableconstraints['av'])
    for i in cv:
        print(i)
    # print("\n--SQL SCRIPT TO CREATE ERROR TABLE =====================")
    # print(createerrortable(testtable["table_name"], testtable["columns"]))
    


'''
--insert into SUMMARY_STATS('TABLE', 'COLUMN', 'MESSAGE', 'COUNT')
select DISTINCT MASTERFILE.PRODFAM, Count(*) 
from MASTERFILE
LEFT JOIN PRODFAM on MASTERFILE.PRODFAM = PRODFAM.PRODFAM
where PRODFAM.PRODFAM is NULL
'''

'''
insert into SUMMARY_STATS ([TABLE], [COLUMN], [MESSAGE], [COUNT])
select 'MASTERFILE', 'PRODFAM', 'Invalid Values', count(MASTERFILE.PRODFAM)
from MASTERFILE
left join PRODFAM on MASTERFILE.PRODFAM = PRODFAM.PRODFAM
where PRODFAM.PRODFAM is NULL
'''