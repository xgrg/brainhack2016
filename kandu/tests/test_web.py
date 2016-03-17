from nose.tools import assert_equal, assert_true, assert_false
baseurl = 'http://localhost:8888/'
fp = '/tmp/hierarchy.json'

def test_first():
   ''' Logs in and acts as if just asked for a non-existing study.
   Returns True if successfully redirected with an information message'''
   import requests
   s = requests.Session()
   url = baseurl
   print url
   r = s.get(url)
   res = 'kandu' in r.text
   assert_true(res)

def test_second():
   import requests, json
   from selenium import webdriver

   browser = webdriver.Firefox()
   url = baseurl + 'test'
   print url
   browser.get(url)
   browser.quit()
   j = json.load(open(fp))
   res = len(j.items()) > 5
   assert_true(res)

