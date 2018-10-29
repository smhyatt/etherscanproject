import hashlib          # to compute the hash values
import unittest         # to use unitesting
import sys              # to append other directories
sys.path.append('../')
import uniquegather     # module to test


class UniquegatherTestCase(unittest.TestCase):
  '''Test section for computeHash.'''
  def test_computeHash(self):
    ''' Testing if computeHash returns the same hash values for the same file 
        and a different hash values for two different files. '''
    file1 = open('testtree1_wo_errs.bin','r')
    file2 = open('testtree2_w_errs.bin','r')

    actual = uniquegather.computeHash(str(file1))
    expected_same = hashlib.md5(str(file1).encode()).hexdigest()
    expected_diff = hashlib.md5(str(file2).encode()).hexdigest()

    self.assertEqual(actual, expected_same)
    self.assertNotEqual(actual, expected_diff)


