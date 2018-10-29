import os                     # to get the size of a file
import sys                    # for exception handling
import time                   # timing for multithreading
import helper                 # extra methods
import queries                # module containing queries
import subprocess             # running shell scripts
from bs4 import BeautifulSoup # to pull data out of HTML

''' Getting all addresses that could be contracts

    First part opens pages between 1-100 from etherscan.io's 
    section Internal Transactions.

    Second part is a css selector which (1) finds row (tr) with
    a (td) element directly under, (2) extracts the 5th (td) 
    element (td:nth-of-type(4)), (3) extracts the link (a), (4)
    extracts the address out of the link and appends it to the
    list. 

    @p_from: the first page number to gather from.
    @p_to: the last page number to gather from. 
    returns: a list of addresses from etherscan.io.
'''
def getAddresses(p_from, p_to):
  addresses = []           # stores all page objects

  # First part
  for i in range(p_from, p_to):
    bs = helper.getBsObject("""https://etherscan.io/txsInternal?
                        ps=100&&valid=true&p=""" + str(i))

  # Second part
    bs.select('tr > td:nth-of-type(4) a')     
    for link in bs.select('tr > td:nth-of-type(5) a'):
      addresses.append(link.attrs['href'].split('/')[-1])

  return addresses


''' Uses EtherScan's API to collect existing contracts 
    and processes the contracts to get size and AST 
    before inserting them to Contracts. 

    @cur: cursor object for connection
    @addresses: a list of addresses to contracts 
    returns: the number of inserted contracts 
'''
def getContracts(cur, addresses):
  transferred = 0
  counter = 0

  for addr in addresses:
    # checks if it already is in the database
    if queries.selectAddrContracts(cur, addr) == 0:
      # inserts the address in etherscan.io's api and opens the page
      page = helper.getPage('https://api.etherscan.io/api?module=contract&action=getsourcecode&address={}&apikey=RMo8wU2K53Mm'.format(addr))
      
      # extracing the contract
      res = page.json()['result'][0]
      if not isinstance(res, str):
        source = res['SourceCode']

        # adds to the address to the set, if there is a contract
        if len(source) > 0:
          # removing the comments
          contract = helper.removeComments(source)
          
          # gets the code size 
          codesize = len(contract)

          # create the AST via script
          helper.saveToFile(addr, contract)
          ast = helper.createAST(addr)
          
          # adds to database.
          if queries.insertToContracts(cur,addr,codesize,contract,ast,transferred):
            counter += 1
            helper.clean(addr)

        else: 
          continue
    else:
      continue

  return counter


