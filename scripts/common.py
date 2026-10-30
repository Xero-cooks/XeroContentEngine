"""Small standard-library helpers; no network, renderer or account side effects."""
from __future__ import annotations
import json,math,pathlib,re

ROOT=pathlib.Path(__file__).resolve().parents[1]

def load_json(path):
 p=pathlib.Path(path)
 if p.stat().st_size>1_000_000:raise ValueError('configuration exceeds 1MB ceiling')
 return json.loads(p.read_text(encoding='utf-8'))

def write_json(path,obj):
 p=pathlib.Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def number(value,name,minimum=0):
 if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value) or value<minimum:raise ValueError(name+' must be a finite number >= '+str(minimum))
 return value

def validate_profile(profile):
 if not isinstance(profile,dict) or profile.get('profile_version')!=1:raise ValueError('profile_version must be 1')
 for name in ['brand','character','typography','video','backgrounds','audio','tools','publishing','workspace']:
  if not isinstance(profile.get(name),dict):raise ValueError(name+' must be an object')
 for name in ['name','language']:
  if not isinstance(profile['brand'].get(name),str) or not profile['brand'][name].strip():raise ValueError('brand.'+name+' is required')
 for name in ['width','height','fps']:
  v=profile['video'].get(name);number(v,'video.'+name,1)
  if not isinstance(v,int):raise ValueError('video.'+name+' must be an integer')
 if not isinstance(profile['character'].get('enabled'),bool):raise ValueError('character.enabled must be boolean')
 if not isinstance(profile['publishing'].get('enabled'),bool):raise ValueError('publishing.enabled must be boolean')
 if profile['publishing'].get('require_explicit_approval') is not True:raise ValueError('publishing always requires explicit authorization')
 if profile['audio'].get('paid_generation_default') is not False:raise ValueError('paid generation is never authorized by a profile default')
 number(profile['audio'].get('sample_rate'),'audio.sample_rate',1)
 for key in ['target_lufs','true_peak_ceiling_dbtp']:
  v=profile['audio'].get(key)
  if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):raise ValueError('audio.'+key+' must be finite')
 def secrets(value):
  if isinstance(value,dict):
   for key,val in value.items():
    if key.lower() in {'api_key','password','access_token','refresh_token','client_secret','authorization','cookie'}:raise ValueError('credentials do not belong in profiles: '+key)
    secrets(val)
  elif isinstance(value,list):
   for item in value:secrets(item)
 secrets(profile)
 return profile

def episode_id(value):
 if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',value):raise ValueError('episode ID must be 1–64 lowercase letters/digits/underscores/hyphens, starting with a letter or digit')
 return value
