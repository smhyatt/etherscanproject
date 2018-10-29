import os                     # to check if file exists
import sys                    # to append other directories
sys.path.append('../')
import conn                   # connection module 
import errno                  # checking error handling
import pathlib                # getting a path with python3
import os.path                # saving in other directories
import hashlib                # to compute the hash values
import unittest               # to use unitesting
sys.path.append('../')
import datagather             # module to test
sys.path.append('../')
import queries                # module with queries
sys.path.append('../')
import helper                 # module with helper
import requests               # to read HTML pages
import subprocess             # running shell scripts
import createtestDB           # to setup and tear down database
from bs4 import BeautifulSoup # to pull data out of HTML


class DatagatherTestCase(unittest.TestCase):
  def setUp(self):
    ''' Establish connection to MySQL server. '''
    self.connection = conn.makeConnection()
    self.cur = conn.connecting(self.connection)

    ''' Creating testing database with necessary table. '''
    self.createdb  = createtestDB.createDatabase(self.cur)    
    self.createtbl = createtestDB.createContractsTbl(self.cur)
    self.cur.execute('USE testdatabase')

    ''' Known addresses to test on '''
    self.addresses = ['0x02caceb4bfc2669156b2eb3b4d590e7ac10a4e73', 
                      '0x01ceb9dddea083d647fa7b09942474dece629c7e', 
                      '0x02c60d28be3338014fef3fdf50a3218b946c0609']

  def tearDown(self):
    self.dropdb = createtestDB.dropDatabase(self.cur)

  ''' Test section for getAddresses. '''
  def test_getAddressesType(self):
    ''' Tests that the correct type is returned. '''
    actual   = type(datagather.getAddresses(1, 2))
    expected = list

    self.assertEqual(actual, expected)


  def test_getAddresses(self):
    ''' Tests that the addresses are strings of size 42. '''
    addresses  = datagather.getAddresses(1, 2)
    sizeofaddr = 42

    actual   = len(addresses[0])
    expected = sizeofaddr

    self.assertEqual(actual, expected)


  ''' Test section for getContracts '''
  def test_getContractsAddresses(self):
    ''' Testing by addresses that datagather inserts correctly to Contracts. '''
    execute = datagather.getContracts(self.cur, self.addresses)

    # To check is the data is added.
    self.cur.execute("SELECT address FROM testdatabase.contracts")
    self.cur.connection.commit()
    actual   = list(self.cur.fetchall())
    expected = [{'address': "'0x02c60d28be3338014fef3fdf50a3218b946c0609'"},
                {'address': "'0x02caceb4bfc2669156b2eb3b4d590e7ac10a4e73'"},
                {'address': "'0x01ceb9dddea083d647fa7b09942474dece629c7e'"}]

    self.assertEqual(actual, expected)


  def test_getContractsThreeCols(self):
    ''' Testing that three columns are correctly gathered to Contracts. '''
    execute = datagather.getContracts(self.cur, self.addresses)

    # To check is the data is added.
    self.cur.execute("""SELECT address, sizeofcode, transferred 
                        FROM testdatabase.contracts""")
    self.cur.connection.commit()
    actual   = str(self.cur.fetchall())
    expected = helper.readFile('getContractsOutput')

    self.assertEqual(actual, expected)

