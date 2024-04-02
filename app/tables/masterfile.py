import csv
import sqlite3
from tables import sqlgen
# import sqlgen

'''try:
    from . import sqlgen
    from . import product_family
except:
    import sqlgen
    import product_family'''

#print(product_family.tableinfo)
#print(product_family.tableconstraints)
'''
# basic information for table
tableinfo = {'table_name':'MASTERFILE',
             'columns':['ITEM','DESCRIPTION','ITEM_TYPE','PRODFAM']}

tableconstraints = {'pk':['ITEM'], # primary key of table
                    'fk':['PRODFAM.PRODFAM'], # column that contains reference to another table
                    'av':{'ITEM_TYPE': '(0,1,2,3,4)'} # allowed values for columns
                    }
'''
class masterfile:
    def __init__(self):
        # yml file to load all appropriate data
        self.tblname = 'MASTERFILE'
        self.tblcols = ['ITEM','DESCRIPTION','ITEM_TYPE','PRODFAM']
        # Constraints for table
        # Primary key
        self.pk = ['ITEM']
        # Allowed values
        self.av = {'ITEM_TYPE': '(0,1,2,3,4)'}
        # foreign key
        # {COLWITHFK:[FKTABLE,FKCOLUMN]}
        self.fk = {'PRODFAM':['PRODFAM','PRODFAM']}
        
    #------------------------------------------------------------------------------------
    # Methods for class objects
    #------------------------------------------------------------------------------------
    
    ## Create table 

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
        return 'Masterfile Created'
    #--------------------------------------------------------------------------------------------------
        
    # Insert Data
        
    def insertdata(self,filename, dbfile):
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
        return 'Data inserted'
    #---------------------------------------------------------------------------------------------------
    def basiccheck(self, dbfile):
        # print("Checking basic masterfile data")
        con = sqlite3.connect(dbfile)
        cur = con.cursor()

        # sql statements to execute
        sql = [sqlgen.pkcheck(mf.tblname, mf.pk, "Duplicate item number"),
            sqlgen.checkvalues(mf.tblname, mf.av)]

        # print(sql)
        # print(len(sql))
        for row in sql:
            # print(row)
            cur.execute(row)
        
        con.commit()
        con.close()
        return 'Basic Check complete'
    #--------------------------------------------------------------------------------------------------------
    # Check foreign key
    def fkcheck(self, dbfile):
        # Assuming column names are same for both the tables
        # print(self.fk)
        for key in self.fk:
            con = sqlite3.connect(dbfile)
            cur = con.cursor()
            # print(key)
            sql = (f'INSERT INTO SUMMARY_STATS ([TABLE], [COLUMN], [MESSAGE], [COUNT])\n'+
                f'SELECT \'{self.tblname}\', \'{key}\', \'Invalid Values\', COUNT({self.tblname}.{key})\n'+
                f'FROM {self.tblname}\n'+
                f'LEFT JOIN {self.fk[key][0]} ON {self.tblname}.{key} = {self.fk[key][0]}.{self.fk[key][1]}\n' +
                f'WHERE {self.fk[key][0]}.{self.fk[key][1]} IS NULL')

            con.commit()
            con.close()
        return 'foreign keys checked'
            

    #--------------------------------------------------------------------------------------------------------
'''class masterfile:
    def __init__(self):
        # yml file to load all appropriate data
        self.tblname = 'MASTERFILE'
        self.tblcols = ['ITEM','DESCRIPTION','ITEM_TYPE','PRODFAM']

        # Constraints for table
        # Primary key
        self.pk = ['ITEM']
        # Allowed values
        self.av = {'ITEM_TYPE': '(0,1,2,3,4)'}
        # foreign key
        self.fk = ['PRODFAM.PRODFAM']

        self.fk = {}

        # Methods for class objects
        ## Create table
        ## Insert data
        ## Basic data check
        #### Validate primary keys
        #### Validate allowed values for columns
        ## Validate foreign keys
        def validate_fk(self, fk):

        '''




# Testing ================================
if __name__ == "__main__":
    dbfile = 'app\schema.db'
    filename = 'app\masterdata.csv'
    mf = masterfile() # mf is object of class masterfile

    # print(dbfile)
    # running functions
    print("--SQL SCRIPT TO CREATE TABLE =====================")
    print(mf.createtable(dbfile))
    
    print("\n--SQL SCRIPT TO INSERT DATA =====================")
    print(mf.insertdata(filename, dbfile))

    print("\n--SQL SCRIPT TO CHECK PRIMARY KEY =====================")
    print(sqlgen.pkcheck(mf.tblname, mf.pk, "test_test_test"))

    print('\n--SQL SCRIPT FOR BASIC CHECKS =====================')
    print(mf.basiccheck(dbfile))

    print("\n--SQL SCRIPT TO DROP TABLE =====================")
    print(sqlgen.droptable(mf.tblname))

    print("\n--SQL SCRIPT TO SEE IF VALUES FOR COLUMNS ADHERE TO RULES =====================")

    print("\n--SQL SCRIPT TO CHECK FK ============================================")
    print(mf.fkcheck(dbfile))
