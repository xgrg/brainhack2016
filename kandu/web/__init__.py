import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path as osp
import os
import json
import string
from kandu import parsefilepath

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Engine():
    def __init__(self, repository, jsonfile, ignorelist=[], maxitems = 500, unknown_only=False):
        self.repository = osp.abspath(repository)
        self.jsonfile = osp.abspath(jsonfile)
        if osp.isfile(self.jsonfile):
            j = json.load(open(self.jsonfile))
        else:
            j = {}
            print 'Creating %s'%self.jsonfile
            json.dump(j, open(self.jsonfile, 'w'))
        self.hierarchy = j
        self.maxitems = maxitems
        self.ignorelist = ignorelist
        self.unknown_only = unknown_only

    def check_repository(self):
        unknown = []
        identified = {}
        allatt = {}
        for root, dirs, files in os.walk(self.repository):
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

        for root, dirs, files in os.walk(repo):
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

    def underscore_split(self, i):
        i = self.correct_index(i)

        bits = self.bits[:i]
        rules = self.rules[:i]

        s = self.bits[i].split('_')
        for each in s[:-1]:
            bits.append(each)
            bits.append('_')
            rules.append('')
            rules.append('')
        bits.append(s[-1])
        rules.append('')
        bits.extend(self.bits[i+1:])
        rules.extend(self.rules[i+1:])
        self.bits = bits
        self.rules = rules

    def build_path_from_bits(self):
        bits = []
        processed = []
        for b,r in zip(self.bits, self.rules):
            if r == '':
                # explicit
                bits.append(b)
            elif r != '' and not b in processed:
                # variable definition (every char except / and _)
                bits.append('(?P<%s>[^/]+)'%r)
                processed.append(b)
            elif r != '' and b in processed:
                # variable repetition
                bits.append('(?P=%s)'%r)

        return '^'+osp.join(self.repository, ''.join(bits))+'$'



class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, engine):
        self.engine = engine

    def bits_to_html(self):
        html = ''
        processed = []
        for each, r in zip(self.engine.bits, self.engine.rules):
            if each in ['/', '_']:
                html += ' %s '%each
            else:
                if r == '':
                    bit = each
                elif r != '':
                    bit = '%s=%s'%(r,each)
                html = html + self.render_string('html/identify_button.html', bit=bit)
        return html

    def hierarchy_to_html(self, hierarchy=None):
        import tornado.escape
        if hierarchy is None:
            hierarchy = self.engine.hierarchy
        return self.render_string('html/hierarchy_body.html', jsonfile = self.engine.jsonfile, hierarchy = hierarchy, repository = self.engine.repository)


    def get_repository_section(self):

        ignorelist = []
        ignorelist.extend(self.engine.ignorelist)
        if self.engine.unknown_only:
            ignorelist.extend(self.engine.hierarchy.keys())

        j = self.engine.get_n_first_files(self.engine.repository, n=self.engine.maxitems, ignorelist=ignorelist)

        heading_info = ''
        if len(self.engine.ignorelist) != 0:
            heading_info += 'Files matching following rules are not displayed : %s<br><br>'%', '.join([e for e in self.engine.ignorelist if e in self.engine.hierarchy])
        if self.engine.unknown_only:
            heading_info += 'Files matching rules are not displayed<br><br>'
        files = ''.join(['<a data-path="%s" class="btn btn-default btn-xs" role="button">%s</a><br>'\
            %(fp, fp[len(self.engine.repository)+1:]) for fp in j])
        closing_info = '%s items max. displayed'%self.engine.maxitems

        return self.render_string('html/preview_body.html', unknown_only = self.engine.unknown_only,
                     jsonfile = self.engine.jsonfile,
                     heading_info = heading_info,
                     files = files,
                     closing_info = closing_info)

class SplitHandler(BaseHandler):
    def post(self):
        i = self.get_argument('i')
        self.engine.underscore_split(string.atoi(i))
        path = self.engine.path
        html = '<span id="path">%s</span><br>'%(path)
        html += self.bits_to_html()
        self.write(html);

class PresetHandler(BaseHandler):
    def post(self):
        from kandu import patterns as p
        preset = self.get_argument('p')
        if preset == 'loadopenfmri':
            h = {'raw': os.path.join(self.engine.repository, '(?P<subject>\w+)', '(?P<session>\w+)', 'anatomy', '(?P=subject)_T1w.nii.gz$')}
            self.engine.hierarchy.update(h)
        elif preset == 'loadjson':
            print self.engine.jsonfile
            self.engine.hierarchy.update(json.load(open(self.engine.jsonfile)))
        elif preset == 'loadfreesurfer':
            self.engine.hierarchy.update(p.set_repository(p.freesurfer, self.engine.repository))
        elif preset == 'loadmorpho':
            self.engine.hierarchy.update(p.set_repository(p.morphologist, self.engine.repository))
        elif preset == 'reset':
            self.engine.hierarchy = {}

        html = self.hierarchy_to_html()
        self.write(html)


class SetRuleHandler(BaseHandler):
    def post(self):
        i = self.get_argument('i')
        variable = self.get_argument('v')
        i = self.engine.correct_index(string.atoi(i))
        self.engine.rules[i] = variable

        path = self.engine.path
        html = '<span id="path">%s</span><br>%s'%(path, path[:len(self.engine.repository)])
        html += self.bits_to_html()
        self.write(html);

class IdentifyHandler(BaseHandler):
    def post(self):
        path = self.get_argument('path')
        self.engine.path = path
        self.engine.slash_split(path)
        html = '<span id="path">%s</span><br>%s'%(path, path[:len(self.engine.repository)])
        html += self.bits_to_html()
        self.write(html);

class SendTextHandler(BaseHandler):
    def post(self):

        if 'text' in self.request.arguments:
            rulename = self.get_argument('text')
            rule = self.engine.build_path_from_bits()
            print rule
            self.engine.hierarchy.update({rulename: rule})
            html = self.hierarchy_to_html()
            self.write(html)


class MainHandler(BaseHandler):
    def get(self):
        unknown_only = self.get_argument('unknown_only', '0')
        print unknown_only

        self.engine = Engine(repository = self.engine.repository,
                    jsonfile = self.engine.jsonfile,
                    ignorelist = self.engine.ignorelist,
                    maxitems = self.engine.maxitems,
                    unknown_only = {'0':False, '1':True}[unknown_only])
        html = self.get_repository_section()
        h = self.hierarchy_to_html()
        self.render("html/index.html", repository = html, hierarchy = h)

class ToggleHandler(BaseHandler):
    def get(self):
        unknown_only = self.get_argument('unknown_only', '0')
        print unknown_only

        self.engine = Engine(repository = self.engine.repository,
                    jsonfile = self.engine.jsonfile,
                    ignorelist = self.engine.ignorelist,
                    maxitems = self.engine.maxitems,
                    unknown_only = {'0':False, '1':True}[unknown_only])
        html = self.get_repository_section()
        self.write(html)


class ValidateHandler(BaseHandler):
    def post(self):
        valid = []
        labels = []

        if 'files[]' in self.request.arguments:
            files = self.get_arguments('files[]')
            selected = self.get_arguments('selected[]')
            h = dict([(e, self.engine.hierarchy[e]) for e in selected])
            for fp in files:
                res = parsefilepath(fp, h)
                if not res is None:
                    valid.append(fp)
                    labels.append(res[0])

        else:
            action = self.get_argument('validate')
            if action == 'validate':
                res = self.engine.check_repository()
                unknown, identified, labels = res['unknown'], res['identified'], res['labels']

                stats = len(identified.items()) / float((len(unknown) + len(identified.items()))) * 100.0
                html = '%.2f %% identified (%s over %s in total)<br><br>'%(stats, len(identified.items()), len(unknown) + len(identified.items()))
                html += "<div id='stats'><table class='table table-condensed'><tr><th>#</th><th>unknown filename</th></tr>"
                for i, each in enumerate(unknown):
                    html += '<tr><td>%s</td><td>%s</td></tr>'%(i, each)
                html += "</table></div>"
                self.write(html)
            elif action == 'save':
                print 'saved'
                json.dump(self.engine.hierarchy, open(self.engine.jsonfile, 'w'), indent=2)
            return

        res = {'valid':valid,
               'labels': labels,
               'repo': self.get_repository_section()}
        html = json.dumps(res)

        self.write(html);

class Application(tornado.web.Application):
    def __init__(self, engine):
        handlers = [
            (r"/", MainHandler, {'engine': engine}),
            (r"/identify", IdentifyHandler,{'engine': engine}),
            (r"/split", SplitHandler,{'engine': engine}),
            (r"/setrule", SetRuleHandler,{'engine': engine}),
            (r"/validate", ValidateHandler, {'engine': engine} ),
            (r"/addrule", SendTextHandler, {'engine': engine} ),
            (r"/preset", PresetHandler, {'engine': engine} ),
            (r"/togglepreview", ToggleHandler, {'engine': engine} ),
            ]
        import kandu
        dirname = osp.dirname(kandu.__file__)
        template_path = osp.join(dirname, 'web', 'static')
        static_path = osp.join(dirname, 'web', 'static')
        s = {
            "template_path":template_path,
            "static_path":static_path,
            "compiled_template_cache":False,
            "debug": True
            }
        tornado.web.Application.__init__(self, handlers, autoescape=None, **s)

def main(args):
    ignorelist = [e.rstrip('\n') for e in open(args.ignorelist).readlines()]\
        if args.ignorelist else []

    engine = Engine(repository = args.repository,
                    jsonfile = args.jsonfile,
                    ignorelist = ignorelist,
                    maxitems = args.maxitems)
    http_server = tornado.httpserver.HTTPServer(Application(engine))
    http_server.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()

