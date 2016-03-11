from nose.tools import assert_equal, assert_true, assert_false
baseurl = 'http://localhost:8888/'

def test_first():
   ''' Logs in and acts as if just asked for a non-existing study.
   Returns True if successfully redirected with an information message'''
   import requests
   url = baseurl
   print url
   r = s.get(url)
   print r.text
   res = 'kandu' in r.text
   assert_true(res)
