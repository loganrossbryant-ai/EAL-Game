"""Verify the actual exported cast: skins, UV/tangents, morph and three clips."""
import hashlib,json,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/far-horizon-tests/performance-characters'
CAST=['flight','science','engineering','colony','venn','juno','rhee','vale','okafor']
def run():
 result=[]
 for name in CAST:
  path=ROOT/f'far-horizon/assets/models/{name}.glb';raw=path.read_bytes();size=struct.unpack_from('<I',raw,12)[0];doc=json.loads(raw[20:20+size]);meshes=doc['meshes']
  assert len(meshes)==2 and sum(len(m['primitives'])for m in meshes)==2,name
  nodes=[n for n in doc['nodes'] if 'mesh' in n];assert len(nodes)==2 and all('skin'in n for n in nodes),name
  for mesh in meshes:
   for primitive in mesh['primitives']:
    assert {'POSITION','NORMAL','TANGENT','TEXCOORD_0','JOINTS_0','WEIGHTS_0'}<=primitive['attributes'].keys(),(name,mesh['name'])
    assert 'TEXCOORD_1' not in primitive['attributes'],(name,'unexpected second UV')
  assert any('Blink'in m.get('extras',{}).get('targetNames',[])for m in meshes),name
  assert {a['name']for a in doc['animations']}=={'Idle','Walk','Use'},name
  for kind in ['albedo','normal','orm']:
   p=ROOT/f'far-horizon/assets/art/characters/{name}_{kind}.png';assert p.stat().st_size>10000
   imp=Path(str(p)+'.import');assert 'mipmaps/generate=true'in imp.read_text(),(name,kind,'missing mipmaps')
  result.append({'id':name,'surfaces':2,'clips':['Idle','Walk','Use'],'skinned_meshes':2,'blink':True,'uv_and_tangents':True,'mipmapped_maps':True,'glb_sha256':hashlib.sha256(raw).hexdigest()})
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'cast-assets.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'cast':len(result),'surfaces_per_character':2,'all_checks_passed':True}))
if __name__=='__main__':run()
