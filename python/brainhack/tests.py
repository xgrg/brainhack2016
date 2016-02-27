
import os
from pluricent.checkbase.hierarchies import *
from pluricent.checkbase.hierarchies.checkbase import Checkbase

def test_respect_hierarchy(destdir, patterns_fp):
    ''' Checks that every file/folder in pzdir is identified by the hierarchy
    Returns True if the unknown list is empty'''
    from pluricent import checkbase as cb
    cl = TestCheckbase(destdir, patterns_fp)
    import os
    import os.path as osp
    unknown = []
    scanned = 0

    for root, dirs, files in os.walk(destdir):
        for f in files:
            fp = osp.join(root, f)
            scanned += 1
            print fp
            res = cb.parsefilepath(fp, cl.patterns)
            if res is None:
               unknown.append(fp)

    print 'unknown', unknown
    print 'scanned items :', scanned

    # Exceptions
    exceptions = ['pluricent.db']
    exceptions = [osp.join(destdir, e) for e in exceptions]
    nb_excep = 0
    for e in exceptions:
       if e in unknown:
          unknown.remove(e)
          nb_excep += 1
    print 'exceptions :', nb_excep
    return len(unknown) == 0

class TestCheckbase(Checkbase):
    def __init__(self, directory, patterns_fp):
        from pluricent.checkbase.hierarchies import cloudy as cs
        import json
        self.patterns = json.load(open(patterns_fp))
        self.keyitems = cs.keyitems
        Checkbase.__init__(self, directory)

