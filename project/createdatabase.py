import pymysql
import conn

''' Establish connection to MySQL server '''
db_name = "smartcontract_db"
connection = conn.makeConnection()
cur = conn.connecting(connection)


''' Creates a database 
    @cur: cursor object from the connection
    @db_name: name of the database
'''
def createDatabase(cur, db_name):
  try:
    create_db = "CREATE DATABASE IF NOT EXISTS "+db_name  
    cur.execute(create_db)
  except Exception as e:
    print("Exeception occured:{}".format(e))


''' Creates the table Contracts
    @cur: cursor object from the connection
'''
def createContractsTbl(cur):
  try:
    create_contract_tbl = """CREATE TABLE `smartcontract_db`.`contracts` 
    ( `address` CHAR(44) NOT NULL , 
    `sizeofcode` INT NOT NULL , 
    `codefiles` LONGBLOB NOT NULL , 
    `ast` LONGBLOB NOT NULL , 
    `created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , 
    `transferred` INT(1) NOT NULL DEFAULT '0' , 
    PRIMARY KEY (`address`), 
    INDEX `indx_sizeofcode_contracts` (`sizeofcode`), 
    INDEX `indx_created_contracts` (`created`)) ENGINE = InnoDB;"""
    
    cur.execute(create_contract_tbl)
  except Exception as e:
    print("Exeception occured:{}".format(e))


''' Creates the table Selected
    @cur: cursor object from the connection
'''
def createSelectedRbl(cur):
  try:
    create_selected_tbl = """CREATE TABLE `smartcontract_db`.`selected` 
    ( `address` CHAR(44) NOT NULL , 
    `hashaddress` CHAR(34) NOT NULL , 
    `sizeofcode` INT NOT NULL , 
    `ast` LONGBLOB NOT NULL , 
    `no_copies` INT NOT NULL , 
    PRIMARY KEY (`address`), 
    INDEX `indx_sizeofcode_selected` (`sizeofcode`), 
    INDEX `indx_nocopies_selected` (`no_copies`), 
    UNIQUE (`hashaddress`)) 
    ENGINE = InnoDB;"""
    
    cur.execute(create_selected_tbl)
  except Exception as e:
    print("Exeception occured:{}".format(e))


createDatabase(cur, db_name)
createContractsTbl(cur, db_name)
createSelectedRbl(cur, db_name)


''' Disconnecting from MySQL server '''
conn.disconnecting(cur, connection)

