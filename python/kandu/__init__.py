import os.path as osp
import os

def parsefilepath(filepath, patterns):
  ''' Matches a filepath with a set of regex given as a dictionary named patterns.
  Returns the key name of the successfully matched pattern, and the identified attributes
  ex : c.parsefilepath('/neurospin/cati/Users/reynal/BVdatabase/Paris/CHBR/t1mri/raw/CHBR.nii')
  ('raw',
     {'acquisition': 'raw',
     'database': '/neurospin/cati/Users/reynal/BVdatabase',
     'extension': 'nii',
     'group': 'Paris',
     'modality': 't1mri',
     'subject': 'CHBR'}) '''
  import re, os
  for datatype, path in patterns.items():
    m = re.match(r"%s"%path, filepath)
    if m:
       return datatype, m.groupdict()

def check_repository(repository, rules, firstcol = 'subject'):
     unknown = []
     identified = {}
     for root, dirs, files in os.walk(repository):
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
       self.rules = rules

   def run(self, firstcol='subject'):
       print 'Inventory of %s in progress... This operation may be long.'%self.repository
       print 'Rules:'
       for k,v in self.rules.items():
          print k, ' : ', v
       print 'First column will be "%s"'%firstcol
       res = check_repository(self.repository, self.rules, firstcol)
       self.identified, self.unknown = res

       self.headers = set() #.intersection([e.keys() for k,e in identified.items()])
       for each in [e.keys() for k,e in self.identified.items()]:
          for e in each:
              self.headers.add(e)

       self.count_table = []
       self.table = []
       self.firstcol = self.identified.keys()
       for s in self.firstcol:
          self.count_table.append([len(self.identified[s].get(e, [])) for e in self.headers])
          self.table.append([self.identified[s].get(e, []) for e in self.headers])




def inventory_table(repository, rules, firstcol = 'subject'):


    #stats = len(identified.items()) / float((len(unknown) + len(identified.items()))) * 100.0
    inv = Inventory(firstcol=firstcol, headers=headers, count_table=count_table, table=table, unknown=unknown)
    return inv



