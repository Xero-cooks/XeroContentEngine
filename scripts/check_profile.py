"""Validate structure and report local capability hints; never invoke a renderer."""
import argparse,json,pathlib,shutil
from common import load_json,validate_profile

def check(path):
 p=validate_profile(load_json(path));warnings=[]
 for group,key in [('tools','template_project'),('tools','renderer_executable'),('typography','font_file'),('backgrounds','directory')]:
  value=p[group].get(key)
  if not value:warnings.append(group+'.'+key+' is not configured')
  elif not pathlib.Path(value).expanduser().exists() and not (group=='tools' and key=='renderer_executable' and shutil.which(value)):warnings.append(group+'.'+key+' is unavailable')
 return {'profile_valid':True,'missing_or_unconfigured':warnings,'production_readiness':'requires supplied assets and actual renderer tests','render_performed':False,'publishing_authorized':False}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('profile',type=pathlib.Path);a=p.parse_args();print(json.dumps(check(a.profile),indent=2))
