"""Apply inserted pauses to all provided cues with one explicit boundary rule.
At a pause boundary t, mapping returns the time AFTER that inserted pause.
No media is edited; cuts/time-stretch/forced alignment are outside this utility.
"""
import argparse,json,pathlib
from common import load_json,write_json,number

def retime(data):
 if not isinstance(data,dict) or not isinstance(data.get('pauses'),list) or not isinstance(data.get('cues'),list):raise ValueError('pauses and cues arrays required')
 pauses=[]
 for p in data['pauses']:
  if not isinstance(p,dict):raise ValueError('pause must be an object')
  pauses.append({'at':number(p.get('at'),'pause.at'),'duration':number(p.get('duration'),'pause.duration')})
 pauses.sort(key=lambda p:p['at'])
 def mapped(t):return round(t+sum(p['duration'] for p in pauses if p['at']<=t),9)
 cues=[];ids=set()
 for cue in data['cues']:
  if not isinstance(cue,dict) or not isinstance(cue.get('id'),str) or not cue['id'] or cue['id'] in ids:raise ValueError('each cue requires a unique nonempty id')
  ids.add(cue['id']);start=number(cue.get('source_start'),'source_start');end=number(cue.get('source_end'),'source_end')
  if end<start:raise ValueError('source_end before source_start')
  cues.append({**cue,'output_start':mapped(start),'output_end':mapped(end)})
 return {'mode':'inserted_pauses_only','boundary_rule':'pause.at <= source_time maps after pause','pauses':pauses,'cues':cues,'media_edited':False}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
 if a.output.exists():raise FileExistsError('output exists; refusing overwrite')
 write_json(a.output,retime(load_json(a.input)))
