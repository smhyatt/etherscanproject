import sys              # terminal arguments
import time             # timing for multithreading
import helper           # extra methods
import datagather       # module import
import uniquegather     # module import
import pymysql          # to use MySQL
import conn             # connection module 


''' The main function determines the order of 
    execution for each module. 
'''

def main():
  ''' Establishing connection '''
  connection = conn.makeConnection()
  cur = conn.connecting(connection)
  conn.useDB(cur)

  ''' To time the whole execution '''
  starttime = time.time()

  ''' To decide lookup pages '''
  p_from = int(sys.argv[1:][0])
  p_to = int(sys.argv[1:][1])
  
  ''' Get information to Contracts '''
  addresses = datagather.getAddresses(p_from, p_to)
  counter = datagather.getContracts(cur, addresses)
  
  ''' Get information to Selected '''
  sorteddata = uniquegather.sortData(cur)
  uniquegather.transferUnique(cur, sorteddata)

  totaltime = (time.time()-starttime)

  ''' Printing execution information '''
  print("The number of new inserted contracts:", counter)
  print("The number of contract addresses looked at where: ", len(addresses))
  print("Collecting from pages:",p_from,"to",p_to,"took:", totaltime, "seconds.")
  
  ''' Disconnecting from MySQL server '''
  conn.disconnecting(cur, connection)


''' Initialising main funktion '''
if __name__ == '__main__':
  main()


