import re                     # use of regular expressions
import requests               # to read HTML pages
import subprocess             # running shell scripts
from bs4 import BeautifulSoup # to pull data out of HTML


''' Opens a page, specifies headers and 
    extracts html text. 
    @url: the url it should open and pull from.
    returns: a beautifulsoup object if successful,
    None if unsuccessful.
'''
def getBsObject(url):
  # creating a session and defining headers and output preferences
  session = requests.Session()
  headers = [insert]
  # request the page given by url                         
  try:
    page = session.get(url, headers=headers)
  except requests.exceptions.RequestException:
    return None
  # creates the BeautifulSoup object
  bs = BeautifulSoup(page.text, "html.parser")

  return bs


''' Opens a page, specifies headers.
    @url: the url it should open and pull from.
    returns: a page request if successful,
    None if unsuccessful.
'''
def getPage(url):
  # creating a session and defining headers and output preferences
  session = requests.Session()
  headers = [insert]
  # request the page given by url                         
  try:
    page = session.get(url, headers=headers)
  except requests.exceptions.RequestException:
    return None

  return page


''' Simplifying the process of saving to a file, in 
    addition to handling potential exceptions. 
    @filename: the name of the file to create.
    @data: the data to save to the file. 
'''
def saveToFile(filename, data):
  try:
    with open(filename, 'w+') as filename:
      filename.write(data)
  except FileExistsError:
    print("Unexpected error using saveToFile.")


''' Processes a file into a string. 
    @file: the name of the file to open. 
    returns: a string with the file input.
'''
def readFile(file):
  try:
    with open(file) as in_file:
      # in_file ensures the file handle is closed at completion.
      content = in_file.read()
  except FileExistsError:
    print("Unexpected error using readFile.")
  return content


''' Removes the temporary files created in the directory.
    @file: the name of the file to remove. 
'''
def clean(file):
  try:
    # executing the file: clean.sh
    subprocess.call(['./clean.sh', file])
  except FileExistsError:
    print("The file ", file, "does not exist, moving on.")


''' Call to the process of creating an AST using ANTLR.
    @file: the contract file to create an AST from. 
    returns: an execution of create_ast.sh, creating an AST.
'''
def createAST(file):
  # executing the file: create_ast.sh
  script = './create_ast.sh'
  return subprocess.check_output([script, file],universal_newlines=True)


''' Removes comments from contracts, to avoid unnecessary 
    space consumption. 
    @contract: a string that is a Solidity contract.
    returns: a string of a contract without any comments. 
'''
def removeComments(contract):
  replacement = " "
  comments = re.compile(r'(?<!https:)//.*?$|/\*.*?\*/',
    re.DOTALL | re.MULTILINE
  )
  return re.sub(comments, replacement, contract)


