import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path as osp
import json

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    hierarchy = {}
    def initialize(self, repository):
        import os.path as osp
        self.repository = osp.abspath(repository)


class SplitHandler(BaseHandler):
    def post(self):
        value = self.get_argument('value')
        html = ''
        for each in value.split('_'): #path[len(self.repository)+1:].split('/'):
            html = html + ''' <div class="btn-group under%s">
                  <button type="button" class="btn btn-danger" data-rule="" data-value="%s">%s</button>
                  <button type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <span class="caret"></span>
                    <span class="sr-only">Toggle Dropdown</span>
                  </button>
                  <ul class="dropdown-menu">
                    <li><a href="#" class="split">Split '_'s</a></li>
                    <li ><a href="#">Another action</a></li>
                    <li><a href="#">Something else here</a></li>
                    <li role="separator" class="divider"></li>
                    <li><a href="#">Separated link</a></li>
                  </ul>
                </div> _ '''%(each, each, each)
        self.write(json.dumps([html[:-3], each] ))

class IdentifyHandler(BaseHandler):
    def post(self):
        path = self.get_argument('id')
        html = '<span id="path">%s</span><br>%s'%(path,path[:len(self.repository)])
        for each in path[len(self.repository)+1:].split('/'):
            html = html + ''' / <div class="btn-group slash%s">
                  <button type="button" class="btn btn-danger" data-rule="" data-value="%s">%s</button>
                  <button type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <span class="caret"></span>
                    <span class="sr-only">Toggle Dropdown</span>
                  </button>
                  <ul class="dropdown-menu">
                    <li><a href="#" class="split">Split '_'s</a></li>
                    <li ><a href="#">Another action</a></li>
                    <li><a href="#">Something else here</a></li>
                    <li role="separator" class="divider"></li>
                    <li><a href="#">Separated link</a></li>
                  </ul>
                </div>'''%(each, each, each)
        self.write(html);

class SendTextHandler(BaseHandler):
    def post(self):
        print self.request.arguments
        print self.request.body

        import os, os.path as osp
        import json
        from brainhack import tests as t
        from pluricent import checkbase as cb

        if 'text' in self.request.arguments:
            rule2 = self.get_arguments('rule[]')
            rulename = self.get_argument('text')
            rule = '(?P<database>[\w -/]+)'
            for each in rule2:
                print each
                if each.startswith('v@'):
                    each = each[2:]
                    rule = osp.join(rule, '(?P<%s>\w+)'%each)
                elif '@' in each:
                    bef, mid, aft = each.split('@')
                    rule = osp.join(rule, '%s(?P=%s)%s'%(bef,mid,aft))
                else:
                    rule = osp.join(rule, each)

            self.hierarchy.update({rulename: rule})
            json.dump(self.hierarchy, open('/tmp/hierarchy.json', 'w'))
            html = ''


class MainHandler(BaseHandler):
    def get(self):
        global nb_items
        j = get_json_from_repository(self.repository)
        html = get_repository_section(j[0])
        if nb_items==100:
            html += '100 items max. displayed'
        self.render("html/index.html", repository = html)

    def post(self):
        print self.request.arguments
        print self.request.body

        import os, os.path as osp
        import json
        from brainhack import tests as t
        from pluricent import checkbase as cb

        if 'validate' in self.request.arguments:
            tc = t.TestCheckbase(self.repository, '/tmp/hierarchy.json')
            valid = []
            for root, dirs, files in os.walk(self.repository):
                for f in files:
                    fp = osp.join(root, f)
                    res = cb.parsefilepath(fp, tc.patterns)
                    if not res is None:
                        valid.append(fp)
            html = json.dumps(valid)
        print html

        self.write(html);

class Application(tornado.web.Application):
    def __init__(self, repository):
        handlers = [
            (r"/", MainHandler, {'repository': repository}),
            (r"/identify", IdentifyHandler,{'repository': repository}),
            (r"/sendtext", SendTextHandler, {'repository': repository} ),
            (r"/split", SplitHandler, {'repository': repository} ),
        ]
        dirname = '/'.join(osp.split(osp.dirname(__file__))[:-3])
        print dirname
        template_path = osp.join(dirname, 'web')
        static_path = osp.join(dirname, 'web')
        s = {
            "template_path":template_path,
            "static_path":static_path,
            "repository" : repository
            }
        tornado.web.Application.__init__(self, handlers, autoescape=None, **s)

def get_json_from_repository(repository):
    import os,json
    os.system('tree %s -J > /tmp/repository.json'%repository)
    return json.load(open('/tmp/repository.json'))

global nb_items
nb_items = 0

def get_repository_section(j, depth=0, rootdir='.'):
    global nb_items
    import os.path as osp
    html = ''
    if nb_items < 100:
        nb_items += 1
        html = '<a style="margin-left:%spx" data-path="%s" class="btn btn-default" role="button">%s (%s-%s)</a><br>'\
        %(str(depth*20), osp.join(rootdir,j['name']), j['name'], j['type'], osp.join(rootdir,j['name']))
        for each in j.get('contents', []):
            html = html + get_repository_section(each, depth+1, osp.join(rootdir, j['name']))
    return html

def main(repository):
    print repository
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(repository))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    import sys
    print sys.argv[1]
    main(sys.argv[1])
