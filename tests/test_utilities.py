import json,pathlib,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from common import load_json,validate_profile,episode_id
from init_profile import create as init_profile
from new_episode import create as new_episode
from retime import retime
from check_profile import check

class UtilityTests(unittest.TestCase):
 def test_both_profiles_valid(self):
  for name in ['orbit','neutral']:validate_profile(load_json(ROOT/'config/profiles'/(name+'.example.json')))
 def test_neutral_has_no_mascot(self):self.assertFalse(load_json(ROOT/'config/profiles/neutral.example.json')['character']['enabled'])
 def test_credentials_rejected(self):
  p=load_json(ROOT/'config/profiles/orbit.example.json');p['tools']['api_key']='test-only'
  with self.assertRaises(ValueError):validate_profile(p)
 def test_auto_spend_disallowed(self):
  p=load_json(ROOT/'config/profiles/orbit.example.json');p['audio']['paid_generation_default']=True
  with self.assertRaises(ValueError):validate_profile(p)
 def test_publish_approval_required(self):
  p=load_json(ROOT/'config/profiles/orbit.example.json');p['publishing']['require_explicit_approval']=False
  with self.assertRaises(ValueError):validate_profile(p)
 def test_bool_is_not_fps(self):
  p=load_json(ROOT/'config/profiles/orbit.example.json');p['video']['fps']=True
  with self.assertRaises(ValueError):validate_profile(p)
 def test_init_refuses_overwrite(self):
  with tempfile.TemporaryDirectory() as t:
   p=pathlib.Path(t)/'profile.json';init_profile('neutral',p)
   with self.assertRaises(FileExistsError):init_profile('orbit',p)
 def test_scaffold_and_overwrite_protection(self):
  with tempfile.TemporaryDirectory() as t:
   p=ROOT/'config/profiles/neutral.example.json';r=new_episode('demo_01',p,t)
   self.assertFalse(r['video_rendered']);self.assertTrue((pathlib.Path(t)/'demo_01/episode.json').exists())
   with self.assertRaises(FileExistsError):new_episode('demo_01',p,t)
 def test_native_template_copied_not_claimed_rendered(self):
  with tempfile.TemporaryDirectory() as t:
   t=pathlib.Path(t);src=t/'fixture.ecproj';src.write_text('SYNTHETIC TEST ONLY');p=load_json(ROOT/'config/profiles/neutral.example.json');p['tools']['template_project']=str(src);config=t/'p.json';config.write_text(json.dumps(p));r=new_episode('demo',config,t/'episodes');self.assertTrue(r['native_template_copied']);self.assertFalse(r['video_rendered'])
 def test_traversal_rejected(self):
  with self.assertRaises(ValueError):episode_id('../existing')
 def test_check_reports_missing_assets_not_fake_ready(self):
  r=check(ROOT/'config/profiles/orbit.example.json');self.assertTrue(r['missing_or_unconfigured']);self.assertFalse(r['render_performed'])
 def test_single_clock_boundary(self):
  r=retime(load_json(ROOT/'examples/inputs/timing.json'));self.assertEqual(r['cues'][1]['output_start'],2.2);self.assertEqual(r['cues'][2]['output_start'],6.5);self.assertFalse(r['media_edited'])
 def test_reversed_interval_rejected(self):
  with self.assertRaises(ValueError):retime({'pauses':[],'cues':[{'id':'a','source_start':2,'source_end':1}]})
 def test_nan_rejected(self):
  with self.assertRaises(ValueError):retime({'pauses':[{'at':float('nan'),'duration':1}],'cues':[]})
 def test_duplicate_cue_rejected(self):
  with self.assertRaises(ValueError):retime({'pauses':[],'cues':[{'id':'a','source_start':0,'source_end':1}]*2})
 def test_committed_retime_example_is_actual_output(self):self.assertEqual(retime(load_json(ROOT/'examples/inputs/timing.json')),load_json(ROOT/'examples/outputs/retimed.json'))
 def test_relative_markdown_links_exist(self):
  import re
  for p in ROOT.rglob('*.md'):
   for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
    if '://' not in link and not link.startswith('#'):self.assertTrue((p.parent/link.split('#')[0]).exists(),str(p)+':'+link)

if __name__=='__main__':unittest.main()
