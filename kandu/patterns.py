import os
image_extensions = '(nii.gz|nii|ima|ima.gz)$'
mesh_extensions = '(gii|mesh)$'

freesurfers = {
      'nu' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'nu.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'nu_noneck' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'nu_noneck.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'norm' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'norm.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'brain' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'brain.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'brainmask' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'brainmask.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'aseg' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'aseg.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'orig' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'orig.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'filled' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'filled.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'wm' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'wm.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'ribbon' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'ribbon.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'T1' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'T1.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'wm.seg' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'wm.seg.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'wmparc' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'wmparc.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'left_ribbon' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', '(?P<side>[l]?)h.ribbon.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'right_ribbon' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', '(?P<side>[r]?)h.ribbon.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'aparc.a2009saseg': os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'aparc.a2009s+aseg.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),
      'talairachlta' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'transforms', 'talairach.lta$'), #image_extensions),
      'talairachxfm' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'transforms', 'talairach.xfm$'), #image_extensions),
      'talairachm3z' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'transforms', 'talairach.m3z$'), #image_extensions),
      'talairachm3zinvmgz' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'transforms', 'talairach.m3z.inv(?P<param>[\w -]+).mgz$'), #image_extensions),

      #mri/orig
      'orig001' : os.path.join("^%s", '(?P<subject>\w+)', 'mri', 'orig', '001.(?P<extension>%s)'%'[\w.]+$'), #image_extensions),

      #stats
      'aseg_stats' : os.path.join("^%s", '(?P<subject>\w+)', 'stats', 'aseg.stats$'),
      'left_aparc_stats' : os.path.join("^%s", '(?P<subject>\w+)', 'stats', 'lh.aparc.stats$'),
      'right_aparc_stats' : os.path.join("^%s", '(?P<subject>\w+)', 'stats', 'rh.aparc.stats$'),

      #surfaces
      'pial' : os.path.join("^%s", '(?P<subject>\w+)', 'surf', '(?P<side>[lr]?)h.pial$'), #image_extensions),
      'white' : os.path.join("^%s", '(?P<subject>\w+)', 'surf', '(?P<side>[lr]?)h.white$'), #image_extensions),
      'thickness' : os.path.join("^%s", '(?P<subject>\w+)', 'surf', '(?P<side>[lr]?)h.thickness$'), #image_extensions),
      }

morphologist = { 'raw': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P=subject).(?P<extension>%s)'%image_extensions),
      'acpc': os.path.join("^%s" ,'(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P=subject).APC$'),
      'nobias': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'nobias_(?P=subject).(?P<extension>%s)'%image_extensions),
      'left_greywhite': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', '(?P<side>[L]?)grey_white_(?P=subject).(?P<extension>%s)'%image_extensions),
      'right_greywhite': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', '(?P<side>[R]?)grey_white_(?P=subject).(?P<extension>%s)'%image_extensions),
      'brainmask': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'brain_(?P=subject).(?P<extension>%s)'%image_extensions),
      'split': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'voronoi_(?P=subject).(?P<extension>%s)'%image_extensions),
      'left_white': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[L]?)white.(?P<extension>%s)'%mesh_extensions),
      'right_white': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[R]?)white.(?P<extension>%s)'%mesh_extensions),
      'left_hemi': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[L]?)hemi.(?P<extension>%s)'%mesh_extensions),
      'right_hemi': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'segmentation', 'mesh', '(?P=subject)_(?P<side>[R]?)hemi.(?P<extension>%s)'%mesh_extensions),
      'left_sulci': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'folds', '(?P<graph_version>[\d.]+)', '(?P<side>[L]?)(?P=subject).arg'),
      'right_sulci': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', '(?P<analysis>[\w -]+)', 'folds', '(?P<graph_version>[\d.]+)', '(?P<side>[R]?)(?P=subject).arg'),
      'spm_nobias': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'nobias_(?P=subject).(?P<extension>%s)'%image_extensions),
      'spm_greymap': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_greyProba.(?P<extension>%s)'%image_extensions),
      'spm_whitemap': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_whiteProba.(?P<extension>%s)'%image_extensions),
      'spm_csfmap': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_csfProba.(?P<extension>%s)'%image_extensions),
      'spm_greymap_warped': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_Nat_grey_probamap_warped.(?P<extension>%s)'%image_extensions),
      'spm_whitemap_warped': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_white_probamap_warped.(?P<extension>%s)'%image_extensions),
      'spm_csfmap_warped': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_csf_probamap_warped.(?P<extension>%s)'%image_extensions),
      'spm_greymap_modulated': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_grey_probamap_modulated.(?P<extension>%s)'%image_extensions),
      'spm_whitemap_modulated': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_white_probamap_modulated.(?P<extension>%s)'%image_extensions),
      'spm_csfmap_modulated': os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'spm8_new_segment', 'segmentation','(?P=subject)_csf_probamap_modulated.(?P<extension>%s)'%image_extensions),
      'spm_tiv_logfile' : os.path.join("^%s", '(?P<group>[\w -]+)', '(?P<subject>\w+)', '(?P<modality>\w+)', '(?P<acquisition>[\w -]+)', 'whasa_(?P<whasa_analysis>[\w -]+)', 'segmentation','(?P=subject)_TIV_log_file.txt$'),
      }

def set_repository(d, repository):
   res = {}
   for k,v in d.items():
      res[k] = v%repository
   return res
