import os                     # to check if file exists
import errno                  # error handling 
import hashlib                # to compute the hash values
import unittest               # to use unitesting
import sys                    # to append other directories
sys.path.append('../')
import helper                 # module to test
import requests               # to read HTML pages
from bs4 import BeautifulSoup # to pull data out of HTML


class HelperTestCase(unittest.TestCase):
  def setUp(self):
    self.url = 'http://pythonscraping.com/pages/page1.html'
    self.noneurl = 'http://testnonepage.html'

  def tearDown(self):
    self.url
    self.noneurl


  ''' Test section for getBsObject. '''
  def test_getBsObjectType(self):
    ''' Testing if getBsObject returns a beautifulsoup object. '''
    actual = type(helper.getBsObject(self.url))
    req = requests.get(self.url)
    expected = type(BeautifulSoup(req.text, 'html.parser'))

    self.assertEqual(actual, expected)


  def test_getBsObjectExceptions(self):
    ''' Testing if getBsObject handles request exceptions. '''
    actual = helper.getBsObject(self.noneurl)
    expected = None

    self.assertEqual(actual, expected)    


  def test_getBsObjectContent(self):
    ''' Testing if getBsObject returns the right content. '''
    actual = (helper.getBsObject(self.url)).prettify()
    expected_same = helper.readFile('pythonscraping_example.html')
    expected_diff = helper.readFile('pythonscraping_wrong_example.html')

    self.assertEqual(actual, expected_same)
    self.assertNotEqual(actual, expected_diff)



  ''' Test section for getPage. '''
  def test_getPageType(self):
    ''' Testing if getPage returns a request object. '''
    actual = type(helper.getPage(self.url))
    expected = type(requests.get(self.url))

    self.assertEqual(actual, expected)


  def test_getPageExceptions(self):
    ''' Testing if getPage handles request exceptions. '''
    actual = helper.getPage(self.noneurl)
    expected = None

    self.assertEqual(actual, expected)    



  ''' Test section for clean. '''
  def test_cleanRmFile(self):
    ''' Tests if the file is removed. '''
    filename = 'clean_test_file'
    with open(filename, 'w+') as file:
      file.write("Testing clean method.")
    remove = helper.clean(filename)
    actual = os.path.isfile(filename)
    expected = False
    
    self.assertFalse(actual, expected)


  def test_cleanFileNonexisting(self):
    ''' Tests if it crashes if the file does not exist. '''
    actual = helper.clean('clean_test_nofile')
    expected = False
    self.assertFalse(actual, expected)


  def test_cleanDiffTypes(self):
    ''' Testing if clean handles if it gets a directory. '''  
    actual_dir = helper.clean('test_dir')
    expected = False
    self.assertFalse(actual_dir, expected)



  ''' Test section for readFile. '''
  def test_readFileCorrect(self):
    ''' Tests if the file is read accurately. '''
    actual_simp = helper.readFile('testfile')
    actual_utf8 = helper.readFile('testfile_strange')
    expected_simp = 'Testing if this file gets modified.'
    expected_utf8 = 'Testing with strange input √√«ß‹∫‹∑ ß∆ñ∆œ∑ß...'

    self.assertEqual(actual_simp, expected_simp)
    self.assertEqual(actual_utf8, expected_utf8)


  def test_readFileType(self):
    ''' Tests if readFile returns the correct type. '''
    actual = type(helper.readFile('test_readFile'))
    expected = type('string')

    self.assertEqual(actual, expected)



  ''' Tests for saveToFile. '''
  def test_saveToFileCorrect(self):
    ''' Tests if saveToFile changes the input it saves. '''
    file = 'testsavetofile'
    finput = 'Testing if this file gets modified.'
    save = helper.saveToFile(file, finput)
    actual = helper.readFile(file)
    expected_same = finput
    expected_diff = 'Different input.'

    self.assertEqual(actual, expected_same)
    self.assertNotEqual(actual, expected_diff)



  ''' Tests for removeComments. '''
  def test_removeComments(self):
    ''' Tests if the outputfile has removed comments as it should have. '''
    orginalfile = helper.readFile('removecommentsfile')
    correctfile = helper.readFile('correct_removecomments')

    outputfile  = helper.removeComments(orginalfile)

    actual   = hashlib.md5(str(outputfile).encode()).hexdigest()
    expected = hashlib.md5(str(correctfile).encode()).hexdigest()

    self.assertEqual(actual, expected)



