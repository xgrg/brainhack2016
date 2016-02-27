# -*- coding: utf-8 -*-
from brainhack import tests as t

if __name__ == '__main__':

    import sys
    directory, patterns_fp = sys.argv[1:]
    t.test_respect_hierarchy(directory, patterns_fp)




