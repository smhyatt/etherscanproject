# Guide

## Prerequisites and Requisites
Prerequisites to run this program are:

1. It has to be run on a Linux or Mac computer.
2. Python 3, including `pip`, `pymysql`, `requests`, `BeautifulSoup` 4, `numpy` and `matplotlib`. 
3. MySQL, including MySQL server and preferably an administration tool such as PhPMyAdmin. 
4. ANTLR4 will be installed if not installed already. 


## Running the Programs

### First Step
`conn.py` contains the information specific setting up the connection to a MySQL server. Modify this to suit the computer executing the application. The program nor tests will work unless the set-up is correct. 

### Creating the Database and Tables
The first step is to create the database. Do this once by running the command: `python3 createdatabase.py`.

### Collecting and Organizing Contracts
EtherScan has a limit of 5000 contracts, that can be accessed through their API, divided into 100 pages. Run command `python3 main.py 1 100`, and you will start collecting valid contracts, not already stored in your database, from pages 1 to 100. The program runs slowly, and therefore it is advised to run chunks at a time. This command can be run as many times as you like, since EtherScan updates in realtime with new smart contracts.

### Running Tests
To run all the tests at once, go to the `tests` directory and use the command: `python3 -m unittest -v`. To run a test file separately, run the filename in Python 3, as this example: `python3 filename.py`, remaining in the `tests` directory. 
