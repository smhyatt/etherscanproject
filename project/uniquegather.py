import re       # use of regular expressions
import sys      # for exception handling
import hashlib  # to compute the hash values
import queries  # module containing queries
import pymysql  # to use MySQL

''' Computes a hash value of a string.
    @ast: a AST given as a string.
    returns: 32 character hash string.
'''
def computeHash(ast):
    hash_obj = hashlib.md5(ast.encode())
    return hash_obj.hexdigest()


''' Collects and organises newly added items.
    @cur: cursor object for connection.
    returns: a nested list.
'''
def sortData(cur): 
  # selecting the newly added items from contracts
  datalist = queries.selectNonTransferred(cur)

  collecteddata, insrtions = ([] for i in range(2))
  nocopies, sizes = ({} for i in range(2))

  # grouping the sizes with the matching hash value
  for elm in datalist:
    size_before = list(elm.values())[1]
    ast_before  = list(elm.values())[2]
    hashkey_before = computeHash(str(ast_before))
    sizes.setdefault(hashkey_before, []).append(size_before)

  # adding the total number copies to each hash in dict nocopies
  for x in sizes:
    nocopies.update({x:(len(sizes[x]))})

  # combining all the matching values in a list of lists
  for elm in datalist:
    addr, size, ast = (list(elm.values())[i] for i in range(3))
    hashkey = computeHash(str(ast))
    # looking up the number of copies matching the hash value
    copies  = nocopies.get(hashkey, 'The hash value is not found')

    if not hashkey in [j for i in collecteddata for j in i]:
      insrtions = [hashkey, addr, size, copies, ast]
      collecteddata.append(list(insrtions))

  return collecteddata


''' Inserts new items to Selected or updates the
    number of copies, based on matching hash values.
    @cur: cursor object for connection
    @collecteddata: nested list with data
'''
def transferUnique(cur, collecteddata):
  oldcopies = {}

  # runs through the list  an either inserts or updates to Selected
  for insrtions in collecteddata:
    hashes, addrss, sizes, copies, asts = (insrtions[i] for i in range(5))

    # gets the matching hashvalues from the db, if any
    hashaddresses = queries.selectCopiesFromHash(cur, hashes)

    # inserts the unique AST
    if len(hashaddresses) == 0:
      queries.insertToSelected(cur, addrss, hashes, sizes, asts, copies)
    
    # each iteration restores the number of copies to zero
    nocopies_in_db = 0

    # gets the number of copies already stored
    for elem in hashaddresses:
      hashkey_in_db, nocopies_in_db = (list(elem.values())[i] for i in range(2))
      oldcopies.setdefault(hashkey_in_db, []).append(nocopies_in_db)

    # updates the stored hash with the new number of copies
    if len(hashaddresses) == 1:
      new_no_copies = copies+nocopies_in_db
      queries.updateNoCopies(cur, new_no_copies, hashes)

  # updates: contracts.transferred, to avoid duplicate inputs
  queries.updateTransferred(cur)



