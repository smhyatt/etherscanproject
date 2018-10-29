import sys      # exception messages
import pymysql  # to use MySQL


''' Inserting data to Selected
    @cur: cursor object for connection
    @addrss: the address primary key
    @hashes: for the attribute hashaddress
    @sizes: for the attribute sizeofcode 
    @copies: for the attribute no_copies
'''
def insertToSelected(cur, addrss, hashes, sizes, asts, copies):
  try:
    # insertion query
    insrt_qry = """INSERT INTO smartcontract_db.selected 
                    (address, hashaddress, sizeofcode, 
                            ast, no_copies)
                    VALUES ("%s","%s","%s","%s","%s")"""
    insrt_data = (addrss, hashes, sizes, asts, copies)

    # execution of query and commit
    cur.execute(insrt_qry, insrt_data)
    cur.connection.commit()
  except:
      print("Unexpected error inserting to Selected:", sys.exc_info()[0])


''' To select the new items from Contracts
    @cur: cursor object for connection
'''
def selectNonTransferred(cur):
  try:
    # selection from Contracts
    select_qry = """SELECT address,sizeofcode,ast 
                    FROM smartcontract_db.contracts 
                    WHERE transferred = 0"""
    
    # execution of query and commit                    
    cur.execute(select_qry)
    cur.connection.commit()
  except:
      print("Unexpected error selecting transferred:", sys.exc_info()[0])

  return cur.fetchall()


''' To update no_copies in Selected
    @cur: cursor object for connection
    @new_no_copies: for the attribute no_copies
    @hashes: for the attribute hashaddress
'''
def updateNoCopies(cur, new_no_copies, hashes):
  try:
    # update at the matching hash value
    update_qry = """UPDATE smartcontract_db.selected 
                    SET no_copies=("%s") WHERE hashaddress=("%s")"""
    update_data = (new_no_copies, hashes)

    # execution of query and commit
    cur.execute(update_qry, update_data)
    cur.connection.commit()
  except:
    print("Unexpected error updating the number of copies:", sys.exc_info()[0])


''' Updates transferred in Contracts to note that they 
    are transferred. 
    @cur: cursor object for connection.
'''
def updateTransferred(cur):
  try:
    update_qry = """UPDATE smartcontract_db.contracts 
                    SET transferred=1 WHERE transferred=0"""

    # execution of query and commit
    cur.execute(update_qry)
    cur.connection.commit()
  except:
    print("Unexpected error updating transferred:", sys.exc_info()[0])


''' Extracting copies from matching hash values. 
    @cur: cursor object for connection.
    @hashes: to match the attribute hashaddress.
    returns: a dictionary of all matching occurences.
'''
def selectCopiesFromHash(cur, hashes):
  try:
    hashes_qry = """SELECT hashaddress, no_copies 
                    FROM smartcontract_db.selected 
                    WHERE hashaddress=("%s")"""
    cur.execute(hashes_qry, hashes) 
    cur.connection.commit()
  except:
      print("Unexpected error selecting hashaddresses:", sys.exc_info()[0])

  return cur.fetchall()


''' Selecting to check if a mathcing address occurs.
    @cur: cursor object for connection.
    @addr: to match the attribute address.
    returns: the number of matches.
'''
def selectAddrContracts(cur, addr):
  try:
    # selecting matching address 
    select_qry = """SELECT * FROM contracts WHERE address=("%s")"""

    # execution of query and commit
    cur.execute(select_qry, addr)
    cur.connection.commit()
  except:
      print("Unexpected error selecting addresses from contracts:", 
             sys.exc_info()[0])

  return cur.rowcount


''' Inserting data to Contracts.
    @cur: cursor object for connection.
    @addrss: the address primary key.
    @codesize: for the attribute sizeofcode.
    @ast: for the attribute ast.
    @transferred: for the attribute transferred.
    returns: true if successful, false if unsuccessful.
'''
def insertToContracts(cur, addrss, codesize, contract, ast, transferred):
  try:
    # matching order of insertion items
    insrt_qry = """INSERT INTO contracts (address, sizeofcode, 
                                  codefiles, ast, transferred) 
                   VALUES ("%s", "%s", "%s", "%s", "%s")"""
    insrt_dta = (addrss, codesize, contract, ast, transferred)

    # execution of query and commit
    cur.execute(insrt_qry, insrt_dta)
    cur.connection.commit()
    return True

  except:
    print("Unexpected error at insert to contracts:", sys.exc_info()[0])
    return False

