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
from kandu.web.engine import Engine

from tornado.options import define, options

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, engine):
        self.engine = engine

    def bits_to_html(self):
        html = ''
        processed = []
        for each, r in zip(self.engine.bits, self.engine.rules):
            if each in self.engine.separators: #['/', '_']:
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

    def get_preview_section(self):

        ignorelist = []
        ignorelist.extend(self.engine.ignorelist)
        if self.engine.unknown_only:
            ignorelist.extend(self.engine.hierarchy.keys())

        self.engine.n_first_files = self.engine.get_n_first_files(self.engine.repository, n=self.engine.maxitems, ignorelist=ignorelist)

        heading_info = ''
        if len(self.engine.ignorelist) != 0:
            heading_info += 'Files matching following rules are not displayed : %s<br><br>'%', '.join([e for e in self.engine.ignorelist if e in self.engine.hierarchy])
        if self.engine.unknown_only:
            heading_info += 'Files matching rules are not displayed<br><br>'
        files = ''.join(['<a data-path="%s" class="btn btn-default btn-xs" role="button">%s</a><br>'\
            %(fp, fp[len(self.engine.repository)+1:]) for fp in self.engine.n_first_files])
        closing_info = '%s items max. displayed'%self.engine.maxitems

        return self.render_string('html/preview_body.html', unknown_only = self.engine.unknown_only,
                     jsonfile = self.engine.jsonfile,
                     heading_info = heading_info,
                     files = files,
                     closing_info = closing_info)

class SplitHandler(BaseHandler):
    def post(self):
        i = self.get_argument('i')
        nbits = len(self.engine.bits)
        for sep in self.engine.separators:
           print 'splitting', sep
           if len(self.engine.bits) != nbits:
              break
           self.engine.oversplit(string.atoi(i), sep)
        html = '<span id="path">%s</span><br>'%(self.engine.path)
        html += self.engine.repository
        html += self.bits_to_html()
        self.write(html);

class PresetHandler(BaseHandler):
    def post(self):
        from kandu import patterns as p
        preset = self.get_argument('p')
        if preset == 'loadopenfmri':
            self.engine.hierarchy.update(p.set_repository(p.openfmri, self.engine.repository))
        elif preset == 'loadjson':
            print self.engine.jsonfile
            self.engine.hierarchy.update(p.set_repository(json.load(open(self.engine.jsonfile)), self.engine.repository))
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
        print path
        self.engine.slash_split(path)
        print self.engine.bits
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

class FilterHandler(BaseHandler):
    def post(self):

        if 'ext' in self.request.arguments:
            ext = self.get_argument('ext')
            rule = osp.join('^%s'%self.engine.repository, '.*.%s$'%ext)
            rulename = 'all_%s_files'%ext
            self.engine.hierarchy.update({rulename: rule})
            html = self.hierarchy_to_html()
            self.write(html)

class MainHandler(BaseHandler):
    def get(self):
        from kandu import patterns as p
        self.engine.hierarchy = p.set_repository(json.load(open(self.engine.jsonfile)), self.engine.repository)

        html = self.get_preview_section()
        h = self.hierarchy_to_html()
        self.render("html/index.html", repository = html, hierarchy = h)

class ToggleHandler(BaseHandler):
    def get(self):
        unknown_only = self.get_argument('unknown_only', '0')
        self.engine.unknown_only = {'0':False, '1':True}[unknown_only]
        html = self.get_preview_section()
        self.write(html)


class ValidateHandler(BaseHandler):
    def post(self):

        if 'files[]' in self.request.arguments:
            labels = []
            valid = []
            files = self.get_arguments('files[]')
            selected = self.get_arguments('selected[]')
            h = dict([(e, self.engine.hierarchy[e]) for e in selected])
            for fp in files:
                res = parsefilepath(fp, h)
                if not res is None:
                    valid.append(fp)
                    labels.append(res[0])
            res = {'valid':valid,
                  'labels': labels,
                  'repo': self.get_preview_section()}
            html = json.dumps(res)

            self.write(html);
            return

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
                from kandu import patterns as p
                json.dump(p.strip_repository(self.engine.hierarchy, self.engine.repository), open(self.engine.jsonfile, 'w'), indent=2)
            return


class Application(tornado.web.Application):
    def __init__(self, engine):
        handlers = [
            (r"/", MainHandler, {'engine': engine}),
            (r"/identify", IdentifyHandler,{'engine': engine}),
            (r"/split", SplitHandler,{'engine': engine}),
            (r"/setrule", SetRuleHandler,{'engine': engine}),
            (r"/validate", ValidateHandler, {'engine': engine} ),
            (r"/addrule", SendTextHandler, {'engine': engine} ),
            (r"/filterext", FilterHandler, {'engine': engine} ),
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
                    maxitems = args.maxitems,
                    separators = args.separators)
    http_server = tornado.httpserver.HTTPServer(Application(engine))
    http_server.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()

