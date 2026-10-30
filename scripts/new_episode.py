"""Create an isolated episode scaffold. This does NOT align audio or render video."""
import argparse,json,pathlib,shutil
from common import ROOT,episode_id,load_json,validate_profile,write_json

def create(identifier,profile_path,output_root):
 identifier=episode_id(identifier);profile=validate_profile(load_json(profile_path));out=pathlib.Path(output_root).expanduser()/identifier
 if out.exists():raise FileExistsError('episode exists; refusing overwrite')
 out.mkdir(parents=True)
 for folder in ['audio','project','render','qa','delivery']:(out/folder).mkdir()
 write_json(out/'profile.effective.json',profile)
 project=profile['tools'].get('template_project');copied=False
 if project:
  source=pathlib.Path(project).expanduser()
  if source.is_file():shutil.copy2(source,out/'project'/source.name);copied=True
 write_json(out/'episode.json',{'episode_id':identifier,'video':profile['video'],'voice_path':'audio/voice-original.wav','pauses':[],'scenes':[],'caption_words':[],'impact_words':[],'sfx_cues':[],'status':'SCAFFOLD_NOT_RENDERED'})
 (out/'SCRIPT.md').write_text('# Approved script\n\nSupply the approved episode narration. No script or recording is inferred from the example.\n')
 (out/'STATE.md').write_text('# Episode state\n\nStatus: scaffold only; no rendering or posting performed.\nNext: supply approved script, original narration, alignment and actual assets; resolve native tooling, then plan/proof/draft/render/QA.\n')
 report={'episode_id':identifier,'status':'SCAFFOLD_NOT_RENDERED','native_template_copied':copied,'video_rendered':False,'publishing_performed':False,'directories':['audio','project','render','qa','delivery'],'files':['profile.effective.json','episode.json','SCRIPT.md','STATE.md'],'remaining':['approved script and narration','actual alignment','approved assets/native template','renderer preflight and production','audiovisual QA and actual delivery']};write_json(out/'scaffold-receipt.json',report);return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('episode_id');p.add_argument('--profile',type=pathlib.Path,default=ROOT/'config/profile.local.json');p.add_argument('--output-root',type=pathlib.Path,default=ROOT/'episodes');a=p.parse_args();print(json.dumps(create(a.episode_id,a.profile,a.output_root),indent=2))
