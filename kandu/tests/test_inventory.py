from nose.tools import assert_equal, assert_true, assert_false

def test_inventory():
   ''' Compiles a full inventory of the test repository following the given default patterns.
   The test is passed if there are less than 30 unknown items in the end.'''
   import kandu
   inv = kandu.Inventory('kandu/tests/test_data/BV_database', kandu.patterns.morphologist)
   inv.run()
   res = len(inv.unknown) < 30
   assert_true(res)



