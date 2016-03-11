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

morphologist = { 'raw': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P=subject).(?P<extension>%s)'%image_extensions),
      'acpc': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P=subject).APC$'),
      'nobias': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'nobias_(?P=subject).(?P<extension>%s)'%image_extensions),
      'left_greywhite': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', '(?P<side>[L]?)grey_white_(?P=subject).(?P<extension>%s)'%image_extensions),
      'right_greywhite': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', '(?P<side>[R]?)grey_white_(?P=subject).(?P<extension>%s)'%image_extensions),
      'brainmask': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'brain_(?P=subject).(?P<extension>%s)'%image_extensions),
      'split': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'voronoi_(?P=subject).(?P<extension>%s)'%image_extensions),
      'left_white': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[L]?)white.(?P<extension>%s)'%mesh_extensions),
      'right_white': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[R]?)white.(?P<extension>%s)'%mesh_extensions),
      'left_hemi': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[L]?)hemi.(?P<extension>%s)'%mesh_extensions),
      'right_hemi': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[R]?)hemi.(?P<extension>%s)'%mesh_extensions),
      'left_sulci': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'folds', '(?P<graph_version>[\d.]+)', '(?P<side>[L]?)(?P=subject).arg'),
      'right_sulci': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'folds', '(?P<graph_version>[\d.]+)', '(?P<side>[R]?)(?P=subject).arg'),
      'spm_nobias': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'nobias_(?P=subject).(?P<extension>%s)'%image_extensions),
      'spm_greymap': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_greyProba.(?P<extension>%s)'%image_extensions),
      'spm_whitemap': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_whiteProba.(?P<extension>%s)'%image_extensions),
      'spm_csfmap': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_csfProba.(?P<extension>%s)'%image_extensions),
      'spm_greymap_warped': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_grey_probamap_warped.(?P<extension>%s)'%image_extensions),
      'spm_whitemap_warped': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_white_probamap_warped.(?P<extension>%s)'%image_extensions),
      'spm_csfmap_warped': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_csf_probamap_warped.(?P<extension>%s)'%image_extensions),
      'spm_greymap_modulated': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_grey_probamap_modulated.(?P<extension>%s)'%image_extensions),
      'spm_whitemap_modulated': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_white_probamap_modulated.(?P<extension>%s)'%image_extensions),
      'spm_csfmap_modulated': osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_csf_probamap_modulated.(?P<extension>%s)'%image_extensions),
      'spm_tiv_logfile' : osp.join('(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'whasa_(?P<whasa_analysis>[\w -]+)', 'segmentation','(?P=subject)_TIV_log_file.txt$'),
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
