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
                    identified.setdefault(att[firstcol], []).append(datatype)
             else:
                 unknown.append(fp[len(repository)+1:])
     return res

def inventory_table(repository, rules, firstcol = 'subject'):

    res = check_repository(repository, rules)
    unknown, identified, labels = res['unknown'], res['identified'], res['labels']

    stats = len(identified.items()) / float((len(unknown) + len(identified.items()))) * 100.0
