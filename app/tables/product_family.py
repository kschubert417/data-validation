import csv
import sqlite3
from tables import sqlgen

'''try:
    from . import sqlgen
except:
    import sqlgen'''

'''
# basic information for table
tableinfo = {'table_name':'PRODFAM',
             'columns':['PRODFAM','DESCRIPTION']}

tableconstraints = {'pk':['ITEM'], # primary key of table
                    'fk':['PRODFAM.PRODFAM'], # column that contains reference to another table
                    'av':{} # allowed values for columns
                    }
'''

class product_family:
    def __init__(self) -> None:
        # yml file to load all appropriate data
        self.tblname = 'PRODFAM'
        self.tblcols = ['PRODFAM','DESCRIPTION']
        # Constraints for table
        # Primary key
        self.pk = ['PRODFAM']
        # Allowed values
        self.av = None
        # foreign key
        self.fk = None

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
               sqlgen.createtable(self.tblname, self.tblcols),
               sqlgen.createerrortable(self.tblname, self.tblcols)]

        for statement in sql:
            cur.execute(statement)

        con.commit()
        con.close()

        return 'Prodfam Table Created'

    #-------------------------------------------------------------------------------
    def insertdata(self, filename, dbfile, order=None):
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        if order == None:
            sql = sqlgen.instertdata(self.tblname, self.tblcols)
        else:
            sql = sqlgen.instertdata(self.tblname, self.tblcols, order)
            # print(sql)
        
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
        sql = []
        sql = sql + sqlgen.pkcheck(self.tblname, self.pk, "Duplicate primary key")
            #sqlgen.checkvalues(self.tblname, self.av)]

        # print(sql)
        # print(len(sql))
        for row in sql:
            print(row)
            cur.execute(row)
        
        con.commit()
        con.close()

#-------------------------------------------------------------------------------------------------------------------
# Class definition end



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
    print("\n--SQL for BASIC CHECKS ========================")
    print(pf.basiccheck(dbfile))
    '''
    print("\n--SQL SCRIPT TO DROP TABLE =====================")
    print(sqlgen.droptable(pf.tblname))
    print("\n--SQL SCRIPT TO SEE IF VALUES FOR COLUMNS ADHERE TO RULES =====================")
    '''
    '''cv = sqlgen.checkvalues(tableinfo["table_name"], tableconstraints['av'])
    for i in cv:
        print(i)'''
    
