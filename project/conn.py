import pymysql  # to use MySQL

''' Connecting to the MySQL database '''
def makeConnection():
  localhost = "127.0.0.1"       # IP-address of the db server
  socket = "/tmp/mysql.sock"    # socket path
  usr = "root"                  # username for the db
  psswrd = "F0rPr0j3ct5.."      # user password
  char_set = "utf8mb4"          # character set
  cusror_type = pymysql.cursors.DictCursor

  connection = pymysql.connect(
    host=localhost,
    unix_socket=socket,
    user=usr,
    password=psswrd,
    charset=char_set,
    cursorclass=cusror_type)

  return connection

''' Choosing the database 
    @cur: cursor object for connection
'''
def useDB(cur):
  cur.execute('USE smartcontract_db')


''' Connecting to the MySQL database 
   @connection: pymysql connection for MySQL server
'''
def connecting(connection):
  return connection.cursor()


''' Disconnecting from the MySQL database 
   @cur: cursor object for connection
   @connection: pymysql connection for MySQL server
'''
def disconnecting(cur, connection):
  connection.close()
  cur.close()

