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

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Engine():
    def __init__(self, repository, hierarchyjson, maxitems = 500):
        self.repository = osp.abspath(repository)
        self.hierarchy = {}
        self.jsonfile = osp.abspath(hierarchyjson)
        self.maxitems = maxitems

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


    def get_repository_section(self):
        html = '''<div class="btn-group">
                  <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Load preset <span class="caret"></span>
                  </button>
                  <ul class="dropdown-menu">
                    <li class="loadopenfmri"><a href="#">Load OpenfMRI</a></li>
                    <li class="loadfreesurfer"><a href="#">Load FreeSurfer</a></li>
                    <li class="loadmorpho"><a href="#">Load Morphologist</a></li>
                    <li class="loadjson"><a href="#">Load from %s</a></li>
                  </ul>
                </div>
                <br><br>
                '''%self.jsonfile
        j = self.get_n_first_files(self.repository, n=self.maxitems)
        html += ''.join(['<a data-path="%s" class="btn btn-default btn-xs" role="button">%s</a><br>'\
            %(fp, fp[len(self.repository)+1:]) for fp in j])
        html += '%s items max. displayed'%self.maxitems
        return html

    def get_n_first_files(self, repo, n=100):
        all_files = []

        for root, dirs, files in os.walk(repo):
            for f in files:
                all_files.append(osp.join(root, f))
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
        #return osp.join('(?P<database>[\w -/]+)', ''.join(bits))

    def bits_to_html(self):
        html = ''
        processed = []
        for each, r in zip(self.bits, self.rules):
            if each in ['/', '_']:
                html += ' %s '%each
            else:
                if r == '':
                    bit = each
                elif r != '':
                    bit = '%s=%s'%(r,each)
                html = html + ''' <div class="btn-group">
                          <button type="button" class="btn btn-danger">%s</button>
                          <button type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            <span class="caret"></span>
                            <span class="sr-only">Toggle Dropdown</span>
                          </button>
                          <ul class="dropdown-menu">
                            <li class="split"><a href="#">Split underscores</a></li>
                            <li class="assign"><a href="#">Set rule</a></li>
                          </ul>
                        </div>'''%bit
        return html

    def hierarchy_to_html(self, hierarchy=None):
        import tornado.escape
        if hierarchy is None:
            hierarchy = self.hierarchy
        html = '<div id="hierarchy" class="btn-group btn-xs" data-toggle="buttons">'
        for k, v in hierarchy.items():

            html += '''<label class="btn btn-primary rule btn-xs" data-rule="%s">
                  <input type="checkbox" autocomplete="off"> %s : %s</label><br>'''%(k, k, tornado.escape.xhtml_escape(v[len(self.repository)+1:]))
        html += '</div>'

        html += '''<br><br><button id="checkrules" type="button" class="btn btn-default">Check selected rules</button>
                <div class="btn-group">
                  <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Load preset <span class="caret"></span>
                  </button>
                  <ul class="dropdown-menu">
                    <li class="loadopenfmri"><a href="#">Load OpenfMRI</a></li>
                    <li class="loadfreesurfer"><a href="#">Load FreeSurfer</a></li>
                    <li class="loadmorpho"><a href="#">Load Morphologist</a></li>
                    <li class="loadjson"><a href="#">Load from %s</a></li>
                  </ul>
                </div><button id="validate" type="button" class="btn btn-default">Save and validate</button>
                '''%(self.jsonfile)
        return html


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, engine):
        self.engine = engine

class SplitHandler(BaseHandler):
    def post(self):
        i = self.get_argument('i')
        self.engine.underscore_split(string.atoi(i))
        path = self.engine.path
        html = '<span id="path">%s</span><br>%s'%(path, path[:len(self.engine.repository)])
        html += self.engine.bits_to_html()
        self.write(html);

class PresetHandler(BaseHandler):
    def post(self):
        preset = self.get_argument('p')
        if preset == 'openfmri':
            h = {'raw': os.path.join(self.engine.repository, '(?P<subject>\w+)', '(?P<session>\w+)', 'anatomy', '(?P=subject)_T1w.nii.gz$')}
            self.engine.hierarchy = h
        elif preset == 'json':
            self.engine.hierarchy = json.load(open(self.engine.jsonfile))
        elif preset == 'freesurfer':
            h = {
                  'nu' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'nu.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'nu_noneck' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'nu_noneck.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'norm' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'norm.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'brain' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'brain.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'brainmask' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'brainmask.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'aseg' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'aseg.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'orig' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'orig.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'filled' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'filled.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'wm' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'wm.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'ribbon' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'ribbon.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'T1' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'T1.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'wm.seg' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'wm.seg.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'wmparc' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'wmparc.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'left_ribbon' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', '(?P<side>[l]?)h.ribbon.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'right_ribbon' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', '(?P<side>[r]?)h.ribbon.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'aparc.a2009saseg': os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'aparc.a2009s+aseg.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
                  'talairachlta' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'transforms', 'talairach.lta$'), #image_extensions),
                  'talairachxfm' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'transforms', 'talairach.xfm$'), #image_extensions),
                  'talairachm3z' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'transforms', 'talairach.m3z$'), #image_extensions),
                  'talairachm3zinvmgz' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'transforms', 'talairach.m3z.inv(?P<param>[\w -]+).mgz$'), #image_extensions),

                  #mri/orig
                  'orig001' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'mri', 'orig', '001.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),

                  #stats
                  'aseg_stats' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'stats', 'aseg.stats$'),
                  'left_aparc_stats' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'stats', 'lh.aparc.stats$'),
                  'right_aparc_stats' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'stats', 'rh.aparc.stats$'),

                  #surfaces
                  'pial' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'surf', '(?P<side>[lr]?)h.pial$'), #image_extensions),
                  'white' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'surf', '(?P<side>[lr]?)h.white$'), #image_extensions),
                  'thickness' : os.path.join(self.engine.repository, '(?P<subject>\w+)', 'surf', '(?P<side>[lr]?)h.thickness$'), #image_extensions),
                 }
            self.engine.hierarchy = h
        elif preset == 'morphologist':
            image_extensions = '(nii.gz|nii|ima|ima.gz)$'
            mesh_extensions = '(gii|mesh)$'
            h = { 'raw': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P=subject).(?P<extension>%s)'%image_extensions),
                                 'acpc': os.path.join(self.engine.repository ,'(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P=subject).APC$'),
                                 'nobias': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'nobias_(?P=subject).(?P<extension>%s)'%image_extensions),
                                 'left_greywhite': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', '(?P<side>[L]?)grey_white_(?P=subject).(?P<extension>%s)'%image_extensions),
                                 'right_greywhite': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', '(?P<side>[R]?)grey_white_(?P=subject).(?P<extension>%s)'%image_extensions),
                                 'brainmask': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'brain_(?P=subject).(?P<extension>%s)'%image_extensions),
                                 'split': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'voronoi_(?P=subject).(?P<extension>%s)'%image_extensions),
                                 'left_white': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[L]?)white.(?P<extension>%s)'%mesh_extensions),
                                 'right_white': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[R]?)white.(?P<extension>%s)'%mesh_extensions),
                                 'left_hemi': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[L]?)hemi.(?P<extension>%s)'%mesh_extensions),
                                 'right_hemi': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[R]?)hemi.(?P<extension>%s)'%mesh_extensions),
                                 'left_sulci': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'folds', '(?P<graph_version>[\d.]+)', '(?P<side>[L]?)(?P=subject).arg'),
                                 'right_sulci': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'folds', '(?P<graph_version>[\d.]+)', '(?P<side>[R]?)(?P=subject).arg'),
                                 'spm_nobias': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'nobias_(?P=subject).(?P<extension>%s)'%image_extensions),
                                 'spm_greymap': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_greyProba.(?P<extension>%s)'%image_extensions),
                                 'spm_whitemap': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_whiteProba.(?P<extension>%s)'%image_extensions),
                                 'spm_csfmap': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_csfProba.(?P<extension>%s)'%image_extensions),
                                 'spm_greymap_warped': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_grey_probamap_warped.(?P<extension>%s)'%image_extensions),
                                 'spm_whitemap_warped': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_white_probamap_warped.(?P<extension>%s)'%image_extensions),
                                 'spm_csfmap_warped': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_csf_probamap_warped.(?P<extension>%s)'%image_extensions),
                                 'spm_greymap_modulated': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_grey_probamap_modulated.(?P<extension>%s)'%image_extensions),
                                 'spm_whitemap_modulated': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_white_probamap_modulated.(?P<extension>%s)'%image_extensions),
                                 'spm_csfmap_modulated': os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_csf_probamap_modulated.(?P<extension>%s)'%image_extensions),
                                 'spm_tiv_logfile' : os.path.join(self.engine.repository, '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'whasa_(?P<whasa_analysis>[\w -]+)', 'segmentation','(?P=subject)_TIV_log_file.txt$'),
                }
            self.engine.hierarchy = h
        html = self.engine.hierarchy_to_html()
        self.write(html)


class SetRuleHandler(BaseHandler):
    def post(self):
        i = self.get_argument('i')
        variable = self.get_argument('v')
        i = self.engine.correct_index(string.atoi(i))
        self.engine.rules[i] = variable

        path = self.engine.path
        html = '<span id="path">%s</span><br>%s'%(path, path[:len(self.engine.repository)])
        html += self.engine.bits_to_html()
        self.write(html);

class IdentifyHandler(BaseHandler):
    def post(self):
        path = self.get_argument('path')
        self.engine.path = path
        self.engine.slash_split(path)
        html = '<span id="path">%s</span><br>%s'%(path, path[:len(self.engine.repository)])
        html += self.engine.bits_to_html()
        self.write(html);

class SendTextHandler(BaseHandler):
    def post(self):

        if 'text' in self.request.arguments:
            rulename = self.get_argument('text')
            rule = self.engine.build_path_from_bits()
            print rule
            self.engine.hierarchy.update({rulename: rule})
            json.dump(self.engine.hierarchy, open(self.engine.jsonfile, 'w'))
            html = self.engine.hierarchy_to_html()
            self.write(html)


class MainHandler(BaseHandler):
    def get(self):
        html = self.engine.get_repository_section()
        self.render("html/index.html", repository = html)


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
            res = self.engine.check_repository()
            unknown, identified, labels = res['unknown'], res['identified'], res['labels']

            stats = len(identified.items()) / float((len(unknown) + len(identified.items()))) * 100.0
            html = '%.2f %% identified (%s over %s in total)<br><br>'%(stats, len(identified.items()), len(unknown) + len(identified.items()))
            html += "<div id='stats'><table class='table table-condensed'><tr><th>#</th><th>unknown filename</th></tr>"
            for i, each in enumerate(unknown):
                html += '<tr><td>%s</td><td>%s</td></tr>'%(i, each)
            html += "</table></div>"
            self.write(html)
            return

        res = {'valid':valid,
               'labels': labels,
               'repo': self.engine.get_repository_section()}
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
            ]
        dirname = '/'.join(__file__.split('/')[:-4])
        template_path = osp.join(dirname, 'web')
        static_path = osp.join(dirname, 'web')
        s = {
            "template_path":template_path,
            "static_path":static_path
            }
        tornado.web.Application.__init__(self, handlers, autoescape=None, **s)

def main(args):
    engine = Engine(args.repository, args.hierarchy, args.maxitems)
    http_server = tornado.httpserver.HTTPServer(Application(engine))
    http_server.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Runs the web server')
    parser.add_argument("--port", help="Port", default=8888, required=False)
    parser.add_argument("--max-preview", dest='maxitems', default=500, type=int, help="How many files to preview", required=False)
    parser.add_argument("--repository", dest='repository', type=str, help="Repository folder", required=True)
    parser.add_argument("--hierarchy", dest='hierarchy', type=str, help="Output hierarchy json", required=True)

    args = parser.parse_args()
    main(args)
