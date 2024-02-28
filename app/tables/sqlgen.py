sumstats = {"table": "SUMMARY_STATS",
            "columns": "([TABLE], [COLUMN], [MESSAGE], [COUNT])"}

# Document to generate SQL scripts to be executed
def pkcheck(table, pk, message):
    '''
    table: name of table
    pk: primary key of table
    message: error message to provide additional information
    '''
    sql = (f'INSERT INTO {sumstats["table"]} {sumstats["columns"]}\n'+
    f'SELECT \'{table}\',\'{pk[0]}\',\'{message}\',COUNT(DISTINCT {pk[0]})\n'+
    f'FROM {table}\n'+
    f'GROUP BY {pk[0]}\n'+
    f'HAVING COUNT(*) > 1')

    # print(sql)
    return(sql)

def droptable(table):
    '''
    db: database file
    table: name of table
    '''
    sql = f'DROP TABLE IF EXISTS {table}'

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

    sql = f'CREATE TABLE IF NOT EXISTS {table}\n({col})'

    # print(sql)
    return(sql)

def instertdata(table, columns):
    '''
    table: name of table
    columns: columns you want to insert data into
    '''
    value = ''
    col = ''
    n = 0
    for i in columns:
        if n == 0:
            value = '(?'
            col = str(i)
        else:
            value = value + ',?'
            col = col + ',' + str(i)
        n += 1
    value = value + ')'

    sql = f'''INSERT INTO {table} ({col})\nVALUES {value}'''

    # print(sql)
    return(sql)



# Testing ================================
if __name__ == "__main__":
    # setting up example test table
    testtable = {'table_name':'TESTTABLE',
                'columns':['ITEM','DESCRIPTION','ITEM_TYPE','PRODFAM'],
                'pk':['ITEM']}

    testtableconstraints = {'pk':['ITEM'], # primary key of table
                           'fk':['PRODFAM.PRODFAM'], # column that contains reference to another table
                           'av':['ITEM_TYPE = (0,1,2,3,4)'] # allowed values for columns, write in SQL
                           }
    
    # running functions
    print("--SQL SCRIPT TO CREATE TABLE =====================")
    print(createtable(testtable["table_name"], testtable["columns"]))
    print("\n--SQL SCRIPT TO INSERT DATA =====================")
    print(instertdata(testtable["table_name"], testtable["columns"]))
    print("\n--SQL SCRIPT TO CHECK PRIMARY KEY =====================")
    print(pkcheck(testtable["table_name"], testtableconstraints['pk'], "test_test_test"))
    print("\n--SQL SCRIPT TO DROP TABLE =====================")
    print(droptable(testtable["table_name"]))
    
    
