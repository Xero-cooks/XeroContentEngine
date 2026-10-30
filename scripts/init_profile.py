"""Copy a clearly labeled example; never overwrite an existing local profile."""
import argparse,pathlib
from common import ROOT,load_json,validate_profile,write_json

def create(preset,output):
 p=pathlib.Path(output)
 if p.exists():raise FileExistsError('profile already exists; refusing overwrite')
 data=validate_profile(load_json(ROOT/'config/profiles'/(preset+'.example.json')));write_json(p,data)
 return {'profile_created':str(p),'preset':preset,'credentials_created':False,'publishing_authorized':False}

if __name__=='__main__':
 import json
 p=argparse.ArgumentParser();p.add_argument('--preset',choices=['orbit','neutral'],default='orbit');p.add_argument('--output',type=pathlib.Path,default=ROOT/'config/profile.local.json');a=p.parse_args();print(json.dumps(create(a.preset,a.output),indent=2))
