"""Build original clothed Pioneer characters from CC0 MakeHuman mesh/rig data.

Run with Blender 4.3+: blender -b --factory-startup --python tools/build_fh_crew3d.py -- --only flight,venn,juno
Only upstream asset data is read. No MakeHuman/MPFB application code is executed.
"""
import argparse, json, math, random, struct, sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector, Quaternion, Matrix
from mathutils.geometry import convex_hull_2d
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fh_character_detail import skin_paint,jacket,hair_geometry,outfit_details,sphere
from fh_character_bake import bake_appearance

ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('/workspace/reference-review/makehuman')
OUT=ROOT/'far-horizon/assets/models'
NAMES={
 'flight':dict(sex='male',race='caucasian',age=.03,skin=(.63,.40,.27,1),cloth=(.065,.14,.22,1),accent=(.28,.69,.83,1),hair='short',height=1.79,crew=True),
 'science':dict(sex='female',race='asian',age=.02,skin=(.61,.42,.30,1),cloth=(.57,.60,.58,1),accent=(.64,.82,.81,1),hair='pony',height=1.68,crew=True),
 'engineering':dict(sex='male',race='asian',age=.08,skin=(.56,.37,.23,1),cloth=(.13,.18,.16,1),accent=(.88,.53,.16,1),hair='short',height=1.77,crew=True),
 'colony':dict(sex='female',race='african',age=.02,skin=(.20,.095,.055,1),cloth=(.27,.08,.10,1),accent=(.78,.68,.49,1),hair='curl',height=1.69,crew=True),
 'venn':dict(sex='female',race='caucasian',age=.27,skin=(.63,.41,.29,1),cloth=(.012,.026,.052,1),accent=(.83,.60,.28,1),hair='bun',height=1.73),
 'juno':dict(sex='female',race='asian',age=.18,skin=(.54,.32,.20,1),cloth=(.065,.074,.078,1),accent=(.60,.33,.13,1),hair='pony',height=1.66),
 'rhee':dict(sex='male',race='asian',age=.43,skin=(.52,.32,.20,1),cloth=(.09,.11,.12,1),accent=(.85,.51,.16,1),hair='wave',height=1.74,tablet=True,stubble=True),
 'vale':dict(sex='male',race='caucasian',age=.23,skin=(.58,.35,.22,1),cloth=(.12,.20,.25,1),accent=(.44,.65,.71,1),hair='wave',height=1.80,tablet=True,beard=True),
 'okafor':dict(sex='female',race='african',age=.20,skin=(.23,.105,.059,1),cloth=(.72,.73,.68,1),accent=(.36,.66,.66,1),hair='curl',height=1.70,tablet=True),
}

def obj_data(path):
 vs=[]; uv=[]; faces=[]; faceuv=[]; groups={};group=''
 for line in path.read_text().splitlines():
  a=line.split()
  if not a:continue
  if a[0]=='v':vs.append(Vector(tuple(map(float,a[1:4]))))
  elif a[0]=='vt':uv.append(tuple(map(float,a[1:3])))
  elif a[0]=='g':group=a[1];groups.setdefault(group,[])
  elif a[0]=='f':
   ids=[int(v.split('/')[0])-1 for v in a[1:]];uvs=[int(v.split('/')[1])-1 if '/' in v and v.split('/')[1] else 0 for v in a[1:]]
   groups.setdefault(group,[]).extend(ids)
   if group=='body' or not any(g=='body' for g in groups):faces.append(ids);faceuv.append(uvs)
 return vs,uv,faces,faceuv,{k:sorted(set(v)) for k,v in groups.items()}

BASE,UV,FACES,FUV,GROUPS=obj_data(SOURCE/'makehuman/data/3dobjs/base.obj')
RIG=json.loads((SOURCE/'game-rig/rig.game_engine.json').read_text())
WEIGHTS=json.loads((SOURCE/'game-rig/weights.game_engine.json').read_text())['weights']


def target(path):
 result={}
 if path.exists():
  for line in path.read_text().splitlines():
   a=line.split()
   if len(a)==4 and not line.startswith('#'):result[int(a[0])]=Vector(tuple(map(float,a[1:])))
 return result


def material(name,color,metal=0,rough=.65):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=color
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 return m


def mesh_object(name,vs,faces,mat):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],faces);mesh.update()
 o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o)
 if mat:o.data.materials.append(mat)
 for p in mesh.polygons:p.use_smooth=True
 return o


def bind(o,arm,bone):
 vg=o.vertex_groups.new(name=bone);vg.add(list(range(len(o.data.vertices))),1,'REPLACE')
 mod=o.modifiers.new('Pioneer skeleton','ARMATURE');mod.object=arm;o.parent=arm


def cube(name,loc,size,mat,arm=None,bone='spine_03',bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Machined rounded edges','BEVEL');mod.width=bevel;mod.segments=3
  bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
 if arm:
  # Armature skinning uses mesh-space coordinates; bake the object's translation.
  bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);bind(o,arm,bone)
 return o


def curve(name,points,radius,mat,arm=None,bone='head'):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=3;c.bevel_depth=radius;c.bevel_resolution=1
 s=c.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
 for p,co in zip(s.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False)
 if arm:bind(o,arm,bone)
 return o


def pole_angle(base,end,pole):
 normal=(end.tail-base.head).cross(pole-base.head)
 axis=normal.cross(base.tail-base.head).normalized()
 a=base.x_axis.angle(axis)
 return -a if base.x_axis.cross(axis).dot(base.y_axis)<0 else a


def set_world_bone(arm,name,point,direction):
 pb=arm.pose.bones[name];rest=pb.bone.matrix_local.to_quaternion()
 turn=(rest@Vector((0,1,0))).rotation_difference(direction.normalized())
 mat=(turn@rest).to_matrix().to_4x4();mat.translation=point;pb.matrix=mat


def solve_limb(arm,upper,lower,target,pole):
 first=arm.pose.bones[upper];second=arm.pose.bones[lower];start=first.head.copy()
 length1=first.bone.length;length2=second.bone.length
 delta=target-start;distance=min(delta.length,length1+length2-.0001)
 direction=delta.normalized();axial=(length1*length1-length2*length2+distance*distance)/(2*distance)
 across=(pole-direction*direction.dot(pole)).normalized()
 bend=math.sqrt(max(0,length1*length1-axial*axial))
 joint=start+direction*axial+across*bend
 end=start+direction*distance
 set_world_bone(arm,upper,start,joint-start);bpy.context.view_layer.update()
 set_world_bone(arm,lower,joint,end-joint);bpy.context.view_layer.update()
 return end


def animate(arm,profile,factor):
 animations=[]
 for label,count in [('Idle',97),('Walk',25),('Use',33)]:
  arm.animation_data_create();action=bpy.data.actions.new(label);arm.animation_data.action=action
  for frame in range(1,count+1):
   bpy.context.scene.frame_set(frame)
   for pb in arm.pose.bones:
    pb.location=(0,0,0);pb.rotation_mode='QUATERNION';pb.rotation_quaternion=(1,0,0,0);pb.scale=(1,1,1)
   t=(frame-1)/(count-1);phase=t*math.tau
   for pb in arm.pose.bones:
    if pb.name.startswith(('index_','middle_','ring_','pinky_')):pb.rotation_quaternion=Quaternion(Vector((1,0,0)),.17)
    if pb.name.startswith('thumb_'):pb.rotation_quaternion=Quaternion(Vector((0,0,1)),.12)
   pelvis=arm.pose.bones['pelvis']
   drop=.030 if label=='Walk' else .004
   pelvis.location=pelvis.bone.matrix_local.inverted().to_3x3()@Vector((math.sin(phase)*.002/factor,0,-drop/factor))
   for name,axis,angle in [('spine_03',Vector((0,1,0)),math.sin(phase)*.004),('head',Vector((0,0,1)),math.sin(phase)*.027),('neck_01',Vector((1,0,0)),math.sin(phase)*.005)]:
    pb=arm.pose.bones[name];local=pb.bone.matrix_local.inverted().to_3x3()@axis;pb.rotation_quaternion=Quaternion(local,angle)
   bpy.context.view_layer.update()
   for suffix,side in [('l',1),('r',-1)]:
    foot=arm.pose.bones['foot_'+suffix].bone.head_local.copy()
    if label=='Walk':
     p=(t+(0 if side==1 else .5))%1
     if p<.61:forward=(.305-p)*.80/factor;lift=0
     else:
      u=(p-.61)/.39;forward=(-.305+.61*(u*u*(3-2*u)))*.80/factor;lift=math.sin(u*math.pi)*.065/factor
     target=Vector((side*.135/factor,foot.y-forward,foot.z+lift))
    else:target=foot.copy()
    ankle=solve_limb(arm,'thigh_'+suffix,'calf_'+suffix,target,Vector((0,-1,0)))
    mat=arm.pose.bones['foot_'+suffix].bone.matrix_local.copy();mat.translation=ankle;arm.pose.bones['foot_'+suffix].matrix=mat
    bpy.context.view_layer.update()
    shoulder=arm.pose.bones['upperarm_'+suffix].head.copy()
    length=arm.pose.bones['upperarm_'+suffix].bone.length+arm.pose.bones['lowerarm_'+suffix].bone.length
    hand=shoulder+Vector((side*.035/factor,-.015/factor,-length*.985))
    if profile.get('tablet') and suffix=='l':hand=shoulder+Vector((-.015/factor,-.18/factor,-length*.52))
    if label=='Walk':hand.y+=math.cos(phase+(0 if side==1 else math.pi))*.075/factor;hand.z+=.008/factor
    elif label=='Use' and suffix=='r':
     reach=math.sin(min(1,t/.78)*math.pi) if t<.78 else 0
     hand=hand.lerp(shoulder+Vector((.015/factor,-.40/factor,-.12/factor)),reach)
    else:hand.y+=math.sin(phase+side)*.002/factor
    wrist=solve_limb(arm,'upperarm_'+suffix,'lowerarm_'+suffix,hand,Vector((side*.15,1,0)))
    arm.pose.bones['hand_'+suffix].location=(0,0,0)
   bpy.context.view_layer.update()
   for pb in arm.pose.bones:
    pb.keyframe_insert('location',frame=frame);pb.keyframe_insert('rotation_quaternion',frame=frame);pb.keyframe_insert('scale',frame=frame)
  action.use_fake_user=True;animations.append(action)
 arm.animation_data.action=animations[0];bpy.context.scene.frame_set(1)
 return animations


def build(name,profile,bake=False):
 random.seed(2247+sum(map(ord,name)));bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 for action in list(bpy.data.actions):bpy.data.actions.remove(action)
 verts=[v.copy() for v in BASE]
 for age,factor in [('young',1-profile['age']),('old',profile['age'])]:
  changes=target(SOURCE/'makehuman/data/targets/macrodetails'/f"{profile['race']}-{profile['sex']}-{age}.target")
  for i,d in changes.items():verts[i]+=d*factor
 body_used=set(i for face in FACES for i in face)
 ground=min(verts[i].y for i in body_used)
 def cv(v):return Vector((v.x*.1,-v.z*.1,(v.y-ground)*.1))
 coords=[cv(v) for v in verts]
 skin=material('Skin',profile['skin'],rough=.59)
 face_material=material('Face',profile['skin'],rough=.63)
 cloth=material('Uniform',profile['cloth'],rough=.81)
 pants=material('Pants',(.07,.085,.095,1),rough=.84)
 boots=material('Boots',(.028,.034,.039,1),metal=.1,rough=.48)
 lipcolor=tuple(profile['skin'][i]*([.86,.70,.71][i]) for i in range(3))+(1,)
 lips=material('Lips',lipcolor,rough=.56)
 hair=material('Hair',(.031,.019,.012,1) if profile['hair']!='curl' else (.014,.009,.007,1),rough=.82)
 trim=material('Trim',profile['accent'],metal=.42,rough=.39)
 dark=material('Equipment',(.035,.047,.055,1),metal=.31,rough=.46)
 glass=material('Screen',(.05,.39,.46,1),metal=.25,rough=.27)
 armdata=bpy.data.armatures.new('PioneerSkeleton');arm=bpy.data.objects.new('PioneerSkeleton',armdata);bpy.context.collection.objects.link(arm);bpy.context.view_layer.objects.active=arm;arm.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
 def point(definition):
  ids=definition.get('vertex_indices') if definition['strategy']=='MEAN' else GROUPS[definition['cube_name']]
  return sum((coords[i] for i in ids),Vector())/len(ids)
 for key,d in RIG.items():
  b=armdata.edit_bones.new(key);b.head=point(d['head']);b.tail=point(d['tail']);b.roll=d['roll']
  if (b.tail-b.head).length<.001:b.tail=b.head+Vector((0,0,.01))
 for key,d in RIG.items():
  if d['parent']:armdata.edit_bones[key].parent=armdata.edit_bones[d['parent']]
 bpy.ops.object.mode_set(mode='OBJECT')
 body=mesh_object('Crew uniform and face',coords,FACES,None)
 for m in [skin,cloth,pants,boots,lips,face_material]:body.data.materials.append(m)
 # Mask by location and real hand weights; only the face/neck/hands remain skin.
 hand_weights=[0.0]*len(verts)
 for key,weights in WEIGHTS.items():
  if key.startswith(('hand_','thumb_','index_','middle_','ring_','pinky_')):
   for i,w in weights:hand_weights[i]+=w
 for p,face in zip(body.data.polygons,FACES):
  avg=sum((BASE[i] for i in face),Vector())/len(face);height=(avg.y+8.4488)*.1
  is_skin=avg.y>5.92 or sum(hand_weights[i] for i in face)/len(face)>.65
  p.material_index=0 if is_skin else (3 if height<.17 else (2 if height<.91 else 1))
  # Complexion is continuous across the face; the vertex paint defines lips.
 uv=body.data.uv_layers.new(name='Pioneer UV')
 for poly,faceuv,face in zip(body.data.polygons,FUV,FACES):
  for loop,idx,vertex in zip(poly.loop_indices,faceuv,face):
   uv.data[loop].uv=UV[idx]
 # Slight, continuous garment ease rather than a painted-on body silhouette.
 body.data.update()
 normals=[v.normal.copy() for v in body.data.vertices]
 for i,v in enumerate(body.data.vertices):
  h=(BASE[i].y+8.4488)*.1
  if BASE[i].y<5.92 and hand_weights[i]<.65:
   ease=.023 if h>.9 else .022
   v.co+=normals[i]*ease
   if .70<h<1.0 and abs(v.co.x)<.105 and v.co.y<-.05:v.co.y=min(v.co.y,-.105)
 # Structured workwear smooths small anatomical detail beneath the cloth.
 neighbors=[set() for _ in coords]
 for face in FACES:
  for a,b in zip(face,face[1:]+face[:1]):neighbors[a].add(b);neighbors[b].add(a)
 cloth_ids=[i for i in body_used if 1.05<(BASE[i].y+8.4488)*.1<1.44 and abs(BASE[i].x)<2.4 and BASE[i].z>.15]
 for _ in range(12):
  smoothed={i:sum((body.data.vertices[j].co for j in neighbors[i]),Vector())/len(neighbors[i]) for i in cloth_ids if neighbors[i]}
  for i,p in smoothed.items():body.data.vertices[i].co=body.data.vertices[i].co.lerp(p,.55)
 body.shape_key_add(name='Basis')
 blink=body.shape_key_add(name='Blink')
 for side in ['left','right']:
  for i,delta in target(SOURCE/'makehuman/data/targets/expression/units'/profile['race']/f'eye-{side}-closure.target').items():blink.data[i].co+=Vector((delta.x,-delta.z,delta.y))*.1
 for key,weights in WEIGHTS.items():
  vg=body.vertex_groups.new(name=key)
  for i,w in weights:
   if w>0:vg.add([i],w,'REPLACE')
 mod=body.modifiers.new('Pioneer skeleton','ARMATURE');mod.object=arm;body.parent=arm
 skin_paint(body,BASE,profile)
 jacket(body,arm,BASE,WEIGHTS,cloth,mesh_object,profile)
 hair_geometry(name,profile,arm,BASE,coords,normals,FACES,hair,mesh_object,bind,curve,material)
 # Real eyeballs, using the CC0 eye mesh and iris texture if available.
 eye_path=SOURCE/'makehuman/data/eyes/high-poly/high-poly.obj'
 if eye_path.exists():
  ev,eu,ef,euf,eg=obj_data(eye_path)
  # Official barycentric proxy data fits the eyeballs to each morphed head.
  fitted=[];reading=False;scales=Vector((1,1,1))
  for line in eye_path.with_suffix('.mhclo').read_text().splitlines():
   a=line.split()
   if not a or a[0].startswith('#'):continue
   if a[0] in ['x_scale','y_scale','z_scale']:
    axis={'x_scale':0,'y_scale':1,'z_scale':2}[a[0]]
    scales[axis]=abs(verts[int(a[1])][axis]-verts[int(a[2])][axis])/float(a[3])
   elif a[0]=='verts':reading=True
   elif reading and len(a)==9:
    pos=sum((verts[int(a[i])]*float(a[3+i]) for i in range(3)),Vector())
    pos+=Vector(tuple(float(a[6+i])*scales[i] for i in range(3)))
    fitted.append(cv(pos))
  if len(fitted)!=len(ev):raise ValueError('Eye proxy vertex count mismatch')
  eye=mesh_object('Eyes',fitted,ef,material('Eyes',(.78,.76,.68,1),rough=.24))
  tex=SOURCE/'makehuman/data/eyes/materials/brown_eye.png'
  if tex.exists():
   im=bpy.data.images.load(str(tex));m=eye.data.materials[0];n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=im;m.node_tree.links.new(n.outputs['Color'],m.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
   uvl=eye.data.uv_layers.new(name='Iris UV')
   for poly,faceuv in zip(eye.data.polygons,euf):
    for loop,idx in zip(poly.loop_indices,faceuv):uvl.data[loop].uv=eu[idx]
  bind(eye,arm,'head')
  iris=material('Iris brown',(.064,.025,.010,1),rough=.33)
  pupil=material('Pupil',(.003,.004,.005,1),rough=.20)
  glint=material('Corneal highlight',(.76,.83,.86,1),rough=.12)
  for side in [-1,1]:
   half=[v for v in fitted if v.x*side>0]
   cx=(min(v.x for v in half)+max(v.x for v in half))*.5
   cz=(min(v.z for v in half)+max(v.z for v in half))*.5
   front=min(v.y for v in half)-.0004
   sphere('Iris lens',(cx,front,cz),(.0082,.0018,.0082),iris,arm,'head')
   sphere('Round pupil',(cx,front-.0017,cz),(.0038,.0007,.0038),pupil,arm,'head')
   sphere('Eye catchlight',(cx-.0022,front-.0025,cz+.0029),(.0010,.0003,.0010),glint,arm,'head')
 outfit_details(name,profile,arm,body,BASE,cloth,trim,dark,glass,hair,mesh_object,bind,cube,curve,material)
 for side in ['l','r']:
  weights={i:w for bone in ['foot_'+side,'ball_'+side] for i,w in WEIGHTS[bone]}
  ids=[i for i in body_used if weights.get(i,0)>.15 and BASE[i].y< -6.3]
  points=[coords[i]+normals[i]*.008 for i in ids]
  bm=bmesh.new();points_bm=[bm.verts.new(p) for p in points];bmesh.ops.convex_hull(bm,input=points_bm)
  mesh=bpy.data.meshes.new('Fitted boot');bm.to_mesh(mesh);bm.free()
  shoe=bpy.data.objects.new('Fitted safety boot',mesh);bpy.context.collection.objects.link(shoe);shoe.data.materials.append(boots)
  for face in mesh.polygons:face.use_smooth=True
  bind(shoe,arm,'foot_'+side)
  outline=convex_hull_2d([Vector((p.x,p.y)) for p in points])
  if len(outline)>30:outline=outline[::2]
  z=min(p.z for p in points)-.003
  solepoints=[Vector((points[i].x,points[i].y,z+h)) for h in [0,.019] for i in outline]
  n=len(outline);faces=[list(reversed(range(n))),list(range(n,2*n))]
  faces += [[i,(i+1)%n,(i+1)%n+n,i+n] for i in range(n)]
  sole=mesh_object('Shaped boot sole',solepoints,faces,dark);bind(sole,arm,'foot_'+side)
 # Join rigid details by one skinned mesh to keep browser draw calls modest.
 details=[o for o in bpy.context.scene.objects if o.type=='MESH' and o!=body]
 if details:
  bpy.ops.object.select_all(action='DESELECT')
  for o in details:o.select_set(True)
  bpy.context.view_layer.objects.active=details[0];bpy.ops.object.join();bpy.context.object.name='Hair eyes and uniform equipment'
  # Boot-sole end caps are n-gons; tangent export requires tris or quads.
  detail=bpy.context.object
  triangulate=detail.modifiers.new('Tangent-ready sole caps','TRIANGULATE');triangulate.min_vertices=5
  bpy.ops.object.modifier_apply(modifier=triangulate.name)
 if bake:bake_appearance(name,body,arm)
 # Normalize target distances as well as the mesh for each morphed stature.
 top=max(coords[i].z for i in body_used)
 factor=profile['height']/top
 actions=animate(arm,profile,factor)
 arm.scale=(factor,)*3
 for o in bpy.context.scene.objects:o.select_set(o.type in {'MESH','ARMATURE'})
 bpy.context.view_layer.objects.active=arm
 OUT.mkdir(parents=True,exist_ok=True)
 path=OUT/(name+'.glb')
 bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='ACTIONS',export_force_sampling=True,export_frame_range=False,export_skins=True,export_morph=True,export_extras=True,export_yup=True,export_texcoords=True,export_tangents=True)
 print('FH_MODEL',name,path.stat().st_size,flush=True)


def main():
 p=argparse.ArgumentParser();p.add_argument('--only',default='flight,venn,juno');p.add_argument('--bake',action='store_true');args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--'in sys.argv else [])
 for name in args.only.split(','):build(name,NAMES[name],args.bake)
 (OUT/'SOURCES.json').write_text(json.dumps({'assets':'MakeHuman / MPFB base mesh, morph targets and game-engine rig','license':'CC0 1.0 Universal','sources':['https://github.com/makehumancommunity/makehuman','https://github.com/makehumancommunity/mpfb2'],'adaptation':'Original Pioneer uniforms, hair meshes, accessories, IK-baked idle/walk/use animation; no upstream program code distributed.'},indent=2)+'\n')

if __name__=='__main__':main()
