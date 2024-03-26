import csv
import sqlite3

try:
    from . import sqlgen
    from . import masterfile
except:
    import sqlgen
    import masterfile

# basic information for table
tableinfo = {'table_name':'PRODFAM',
             'columns':['PRODFAM','DESCRIPTION']}

tableconstraints = {'pk':['ITEM'], # primary key of table
                    'fk':['PRODFAM.PRODFAM'], # column that contains reference to another table
                    'av':{} # allowed values for columns
                    }


class product_family:
    def __init__(self) -> None:
        # yml file to load all appropriate data
        self.tblname = 'PRODFAM'
        self.tblcols = ['PRODFAM','DESCRIPTION']
        # Constraints for table
        # Primary key
        self.pk = ['ITEM']
        # Allowed values
        self.av = {'ITEM_TYPE': '(0,1,2,3,4)'}
        # foreign key
        self.fk = ['PRODFAM.PRODFAM']

    #--------------------------------------------------------------------
    def createtable(self, dbfile):
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
        
        sql = [sqlgen.droptable(self.tblname),
            sqlgen.createtable(self.tblname, self.tblcols)]

        for statement in sql:
            cur.execute(statement)

        con.commit()
        con.close()

        return 'Prodfam Table Created'

    #-------------------------------------------------------------------------------
    def insertdata(self, filename, dbfile):
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        sql = sqlgen.instertdata(self.tblname, self.tblcols)
        
        with open(filename) as file_obj:
            # Skip the header
            nxt = next(file_obj)

            # Create reader object by passing the file  
            # object to reader method 
            reader_obj = csv.reader(file_obj) 
            
            # Iterate over each row in the csv  
            # file using reader object 
            for row in reader_obj: 
                # print(row)
                cur.execute(sql, row)

        con.commit()
        con.close()
        return "Data inserted into Prodfam Table"

    #-----------------------------------------------------------------------    

    def basiccheck(self, dbfile):
        # print("Checking basic masterfile data")
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        # sql statements to execute
        sql = [sqlgen.pkcheck(tableinfo["table_name"], tableconstraints['pk'], "Duplicate item number"),
            sqlgen.checkvalues(tableinfo["table_name"], tableconstraints['av'])]

        # print(sql)
        # print(len(sql))
        for row in sql:
            # print(row)
            cur.execute(row)
        
        con.commit()
        con.close()





# Testing ================================
if __name__ == "__main__":
    dbfile = 'app\schema.db'
    filename = 'app\prodfam_data.csv'
    # print(dbfile)
    # running functions
    pf = product_family()
    print("--SQL SCRIPT TO CREATE TABLE =====================")
    print(pf.createtable(dbfile))
    print("\n--SQL SCRIPT TO INSERT DATA =====================")
    print(pf.insertdata(filename,dbfile))
    print("\n--SQL SCRIPT TO CHECK PRIMARY KEY =====================")
    print(sqlgen.pkcheck(pf.tblname,pf.pk, "test_test_test"))
    '''
    print("\n--SQL SCRIPT TO DROP TABLE =====================")
    print(droptable(testtable["table_name"]))
    print("\n--SQL SCRIPT TO SEE IF VALUES FOR COLUMNS ADHERE TO RULES =====================")
    '''
    '''cv = sqlgen.checkvalues(tableinfo["table_name"], tableconstraints['av'])
    for i in cv:
        print(i)'''
    
