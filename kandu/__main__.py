#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
parser = argparse.ArgumentParser(prog='kandu_server', description='Runs the web server. Open a browser at http://localhost:8888 (default port)')
parser.add_argument("--port", help="Port", default=8888, required=False)
parser.add_argument("--maxitems", dest='maxitems', default=500, type=int, help="How many files to preview", required=False)
parser.add_argument("--repository", dest='repository', type=str, help="Repository folder", required=True)
parser.add_argument("--hierarchy", dest='jsonfile', type=str, help="Output hierarchy json", required=True)
parser.add_argument("--ignore", dest='ignorelist', type=str, default=None, help="File listing rules which matching files should be hidden from the preview", required=False)
parser.add_argument("--sep", dest='separators', type=str, default="_", help="Characters to use as potential separators (includes slash by default)", required=False)

args = parser.parse_args()
from web import main
main(args)
