import os.path as osp
import os, json
import scandir
import string
from kandu import parsefilepath
from kandu import patterns as p

class Engine():
    def __init__(self, repository, jsonfile, ignorelist=[], maxitems = 500, unknown_only=False, separators='_'):
        self.repository = osp.abspath(repository)
        self.jsonfile = osp.abspath(jsonfile)
        if osp.isfile(self.jsonfile):
            j = p.set_repository(json.load(open(self.jsonfile)), self.repository)
        else:
            j = {}
            print 'Creating %s'%self.jsonfile
            json.dump(p.strip_repository(j, self.repository), open(self.jsonfile, 'w'))
        self.hierarchy = j
        self.maxitems = maxitems
        self.ignorelist = ignorelist
        self.unknown_only = unknown_only

        allowed_sep = set('_.-')
        removed_sep = list(set(separators).difference(allowed_sep))
        if len(removed_sep) != 0:
           print 'The following separators have been ignored : %s'%', '.join(removed_sep)
        kept_sep = list(set(separators).intersection(allowed_sep))
        if len(kept_sep) == 0:
           raise Exception('no valid separators given in %s (allowed : %s)'%(separators, ' '.join(allowed_sep)))

        self.separators = kept_sep
        self.separators.append('/')

    def check_repository(self):
        unknown = []
        identified = {}
        allatt = {}
        for root, dirs, files in scandir.walk(self.repository):
            for f in files:
                fp = osp.join(root, f)
                res = parsefilepath(fp, self.hierarchy)
                if not res is None:
                    datatype, att = res
                    identified[fp] = datatype
                    for k,v in att.items():
                       allatt.setdefault(k, []).append(v)
                else:
                    unknown.append(fp[len(self.repository)+1:])
        res = {'unknown' : unknown,
               'identified': identified,
               'labels': allatt}
        print 'done'
        return res

    def get_n_first_files(self, repo, n=100, ignorelist=[]):
        all_files = []

        for root, dirs, files in scandir.walk(repo):
            for f in files:
                fp = osp.join(root, f)
                res = parsefilepath(fp, self.hierarchy)
                if res:
                    datatype, att = res
                    if datatype in ignorelist: continue

                all_files.append(fp)
                if len(all_files) == n:
                    return all_files
        return all_files

    def slash_split(self, path):
        bits = path[len(self.repository)+1:].split('/')
        self.bits = []
        self.rules = []
        for each in bits[:-1]:
            self.bits.append(each)
            self.bits.append('/')
        self.bits.append(bits[-1])
        for e in self.bits:
            self.rules.append('')

    def correct_index(self, i):
        # correct i according to '/' and '_'
        print 'before correction', i

        cpt = 0
        j = i
        for each in self.bits:
            if cpt == j:
                break
            if not each in ['/', '_']:
                cpt += 1
                i += 1
        print 'i corrected', i
        return i

    def oversplit(self, i, sep):
        i = self.correct_index(i)
        print self.bits

        bits = self.bits[:i]
        rules = self.rules[:i]

        s = self.bits[i].split(sep)
        for each in s[:-1]:
            bits.append(each)
            bits.append(sep)
            rules.append('')
            rules.append('')
        bits.append(s[-1])
        rules.append('')
        bits.extend(self.bits[i+1:])
        rules.extend(self.rules[i+1:])
        self.bits = bits
        print '2', self.bits
        self.rules = rules

    def build_path_from_bits(self):
        bits = []
        processed = []
        for b,r in zip(self.bits, self.rules):
            if r == '':
                # explicit
                bits.append(b)
            elif r == '**':
                bits.append(b)
                bits.append('/')
                bits.append('.*')
                break
            elif r.startswith('*'):
                bits.append('.*')
            elif r != '' and not b in processed:
                # variable definition (every char except / and _)
                bits.append('(?P<%s>[^/]+)'%r)
                processed.append(b)
            elif r != '' and b in processed:
                # variable repetition
                bits.append('(?P=%s)'%r)

        return '^'+osp.join(self.repository, ''.join(bits))+'$'
