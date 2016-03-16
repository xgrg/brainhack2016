import os.path as osp
image_extensions = '(nii.gz|nii|ima|ima.gz)$'
mesh_extensions = '(gii|mesh)$'

def parsefilepath(filepath, patterns):
  ''' Matches a filepath with a set of regex given as a dictionary named patterns.
  Returns the key name of the successfully matched pattern, and the identified attributes'''
  import re
  for datatype, path in patterns.items():
    m = re.match(r"%s"%path, filepath)
    if m:
       return datatype, m.groupdict()

openfmri = {'raw': osp.join('(?P<subject>\w+)', '(?P<session>\w+)', 'anatomy', '(?P=subject)_T1w.nii.gz$')}

freesurfer = {
      'nu' : osp.join('(?P<subject>\w+)', 'mri', 'nu.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'nu_noneck' : osp.join('(?P<subject>\w+)', 'mri', 'nu_noneck.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'norm' : osp.join('(?P<subject>\w+)', 'mri', 'norm.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'brain' : osp.join('(?P<subject>\w+)', 'mri', 'brain.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'brainmask' : osp.join('(?P<subject>\w+)', 'mri', 'brainmask.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'aseg' : osp.join('(?P<subject>\w+)', 'mri', 'aseg.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'orig' : osp.join('(?P<subject>\w+)', 'mri', 'orig.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'filled' : osp.join('(?P<subject>\w+)', 'mri', 'filled.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'wm' : osp.join('(?P<subject>\w+)', 'mri', 'wm.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'ribbon' : osp.join('(?P<subject>\w+)', 'mri', 'ribbon.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'T1' : osp.join('(?P<subject>\w+)', 'mri', 'T1.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'wm.seg' : osp.join('(?P<subject>\w+)', 'mri', 'wm.seg.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'wmparc' : osp.join('(?P<subject>\w+)', 'mri', 'wmparc.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'left_ribbon' : osp.join('(?P<subject>\w+)', 'mri', '(?P<side>[l]?)h.ribbon.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'right_ribbon' : osp.join('(?P<subject>\w+)', 'mri', '(?P<side>[r]?)h.ribbon.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'aparc.a2009saseg': osp.join('(?P<subject>\w+)', 'mri', 'aparc.a2009s+aseg.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'talairachlta' : osp.join('(?P<subject>\w+)', 'mri', 'transforms', 'talairach.lta$'), #image_extensions),
      'talairachxfm' : osp.join('(?P<subject>\w+)', 'mri', 'transforms', 'talairach.xfm$'), #image_extensions),
      'talairachm3z' : osp.join('(?P<subject>\w+)', 'mri', 'transforms', 'talairach.m3z$'), #image_extensions),
      'talairachm3zinvmgz' : osp.join('(?P<subject>\w+)', 'mri', 'transforms', 'talairach.m3z.inv(?P<param>[\w -]+).mgz$'), #image_extensions),

      #mri/orig
      'orig001' : osp.join('(?P<subject>\w+)', 'mri', 'orig', '001.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),

      #stats
      'aseg_stats' : osp.join('(?P<subject>\w+)', 'stats', 'aseg.stats$'),
      'left_aparc_stats' : osp.join('(?P<subject>\w+)', 'stats', 'lh.aparc.stats$'),
      'right_aparc_stats' : osp.join('(?P<subject>\w+)', 'stats', 'rh.aparc.stats$'),

      #surfaces
      'pial' : osp.join('(?P<subject>\w+)', 'surf', '(?P<side>[lr]?)h.pial$'), #image_extensions),
      'white' : osp.join('(?P<subject>\w+)', 'surf', '(?P<side>[lr]?)h.white$'), #image_extensions),
      'thickness' : osp.join('(?P<subject>\w+)', 'surf', '(?P<side>[lr]?)h.thickness$'), #image_extensions),
      }


morphologist = {
  "t1mri": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P=subject).(?P<extension>%s)"%image_extensions),
  "normalized_spm": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "normalized_SPM_(?P=subject).(?P<extension>%s)"%image_extensions),
  "sn_mat": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P=subject)_sn.mat$"),
  "APC": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P=subject).APC$"),
  "edges": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "edges_(?P=subject).(?P<extension>%s)"%image_extensions),
  "variance": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "variance_(?P=subject).(?P<extension>%s)"%image_extensions),
  "whiteridge": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "whiteridge_(?P=subject).(?P<extension>%s)"%image_extensions),
  "hfiltered": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "hfiltered_(?P=subject).(?P<extension>%s)"%image_extensions),
  "skull_stripped": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "skull_stripped_(?P=subject).(?P<extension>%s)"%image_extensions),
  "nobias": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "default_analysis/nobias_(?P=subject).(?P<extension>%s)"%image_extensions),
  "nobias_his": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "nobias_(?P=subject).his$"),
  "nobias_han": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "nobias_(?P=subject).han$"),
  "brain": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "brain_(?P=subject).(?P<extension>%s)"%image_extensions),
  "voronoi": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "voronoi_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Lgrey_white": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "Lgrey_white_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Rgrey_white": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "Rgrey_white_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Lcortex": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "Lcortex_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Rcortex": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "Rcortex_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Lskeleton": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "Lskeleton_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Rskeleton": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "Rskeleton_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Lroots": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "Lroots_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Rroots": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "Rroots_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Lgw_interface": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "Lgw_interface_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Rgw_interface": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "Rgw_interface_(?P=subject).(?P<extension>%s)"%image_extensions),
  "Lwhite": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "mesh", "(?P=subject)_Lwhite.(?P<extension>%s)"%mesh_extensions),
  "Rwhite": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "mesh", "(?P=subject)_Rwhite.(?P<extension>%s)"%mesh_extensions),
  "Lhemi": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "mesh", "(?P=subject)_Lhemi.(?P<extension>%s)"%mesh_extensions),
  "Rhemi": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "mesh", "(?P=subject)_Rhemi.(?P<extension>%s)"%mesh_extensions),
  "head": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "segmentation", "mesh", "(?P=subject)_head.(?P<extension>%s)"%mesh_extensions),
  "folds": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "(?P<analysis>[^/]+)", "folds", ".*$"),
  "spm_new_segment": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "spm_new_segment", ".*$"),
  "spm8_new_segment": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "spm8_new_segment", ".*$"),
  "registration": osp.join("(?P<group>[^/]+)", "(?P<subject>[^/]+)", "(?P<modality>[^/]+)", "(?P<acquisition>[^/]+)", "registration", ".*$"),
  "snapshot": osp.join('snapshots', "(?P<acquisition>[^/]+)", "(?P<software>[^/]+)", "(?P<type>[^/]+)", "snapshot_.*_(?P<subject>[^/]+)_(?P=acquisition).png$"),
  "table": osp.join('tables', "(?P<acquisition>[^/]+)", "(?P<filename>[^/]+).(csv|txt)$"),
  "all_minf_files": ".*.minf$",
  "database": "database.*$",
  "history_book" : osp.join("history_book", ".*$")
}

def set_repository(d, repository):
   res = {}
   for k,v in d.items():
      res[k] = osp.join('^%s'%repository, v)
   return res

def strip_repository(d, repository):
   res = {}
   for k,v in d.items():
      res[k] = v.split('^%s'%repository + '/')[1]
   return res

def lower(d):
    res = {}
    first_att = set([osp.split(each)[0] for each in d.values()])
    if (len(first_att) != 1):
        raise Exception('The rules do not share the same attribute : %s'%' '.join(first_att))
    for k,v in d.items():
        res[k] = '/'.join(v.split('/')[1:])
    return res

def add_level(d, parent):
    res = {}
    for k,v in d.items():
        res[k] = osp.join(parent, v)
    return res
