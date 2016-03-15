#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path as osp
import os, scandir
from kandu.patterns import parsefilepath
from kandu import patterns as p


def check_repository(repository, rules, firstcol = 'subject'):
     unknown = []
     identified = {}
     for root, dirs, files in scandir.walk(repository):
         for f in files:
             fp = osp.join(root, f)
             res = parsefilepath(fp, rules)
             if not res is None:
                 datatype, att = res
                 if firstcol in att:
                    identified.setdefault(att[firstcol], {}).setdefault(datatype, []).append(fp)
             else:
                 unknown.append(fp[len(repository)+1:])
     return identified, unknown

class Inventory():
   def __init__(self, repository, rules):
       self.repository = repository
       self.rules = p.set_repository(rules, repository)

   def to_html(self, style="standalone"):
       if not hasattr(self, 'identified'):
          raise Exception('run Inventory.run() first')
       if style == 'standalone':
          html = '''<html><head></head><body><style>
               table.table, td, th { border: 1px solid darkgray; text-align:center; vertical-align:middle;
               }
               td.success { background-color:forestgreen}
               td.warning { background-color:goldenrod}
               td.danger {background-color:brown}
               </style>'''
       elif style == 'maxcdn':
          html = '''<html><head>
               <script src="https://code.jquery.com/jquery-1.12.0.min.js"></script>
               <!-- Latest compiled and minified CSS -->
               <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
               <!-- Optional theme -->
               <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">
               <!-- Latest compiled and minified JavaScript -->
               <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
               </head><body>'''
       html += '<table class="table table-hover"><tr><th>%s</th>'%self.firstcol
       html += ''.join(['<th>%s</th>'%each for each in self.headers])
       html += '</tr>'
       colormap = ['danger', 'success', 'warning']
       for s, c in zip(self.index, self.count_table):
           items = self.identified[s]
           html += '<tr><td>%s</td>'%s
           html += ''.join(['<td title="%s" class="%s">%s</td>'%(' \n'.join([each[len(self.repository)+1:] for each in items.get(e1, [])]),
                                                                            colormap[min(2,e2)],
                                                                            e2) for e1, e2 in zip(self.headers, c)])
           html += '</tr>'
       html += '</table></body></html>'
       return html

   def run(self, firstcol='subject'):
       print 'Inventory of %s in progress... This operation may be long.'%self.repository
       print 'Rules:'
       for k,v in self.rules.items():
          print k, ' : ', v
       print 'First column will be "%s"'%firstcol
       res = check_repository(self.repository, self.rules, firstcol)
       self.identified, self.unknown = res
       self.firstcol = firstcol

       self.headers = set() #.intersection([e.keys() for k,e in identified.items()])
       for each in [e.keys() for k,e in self.identified.items()]:
          for e in each:
              self.headers.add(e)
       self.headers = list(self.headers)

       self.count_table = []
       self.table = []
       self.index = self.identified.keys()
       for s in self.index:
          self.count_table.append([len(self.identified[s].get(e, [])) for e in self.headers])
          self.table.append([self.identified[s].get(e, []) for e in self.headers])

