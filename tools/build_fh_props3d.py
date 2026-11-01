"""Original articulated Pioneer machines; generated geometry, not billboard art."""
import bpy, math
from pathlib import Path
from mathutils import Vector
OUT=Path(__file__).resolve().parents[1]/'far-horizon/assets/models'

def mat(name,color,metal=.4,rough=.45,emission=False):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if emission:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=.8
 return m

def reset():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)

def group(name,location=(0,0,0),parent=None):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.location=location
 if parent:o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted()
 bpy.context.view_layer.update();return o

def finish(o,name,m,parent=None,bevel=0):
 o.name=name;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Machined edge radius','BEVEL');mod.width=bevel;mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in o.data.polygons:p.use_smooth=True
 n=o.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL');n.keep_sharp=True;bpy.ops.object.modifier_apply(modifier=n.name)
 o.data.materials.append(m)
 if parent:o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted()
 return o

def box(name,pos,size,m,parent=None,r=.014):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.scale=size
 return finish(o,name,m,parent,min(r,min(size)*.25))

def cyl(name,pos,radius,depth,m,parent=None,rotation=(0,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=radius,depth=depth,location=pos,rotation=rotation)
 return finish(bpy.context.object,name,m,parent,min(.006,radius*.15))

def sphere(name,pos,scale,m,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=1,location=pos);o=bpy.context.object;o.scale=scale
 return finish(o,name,m,parent)

def tube(name,a,b,r,m,parent=None):
 delta=Vector(b)-Vector(a);o=cyl(name,(Vector(a)+Vector(b))/2,r,delta.length,m,parent)
 o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();return o

def hose(name,points,r,m,parent=None):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=8;c.bevel_depth=r;c.bevel_resolution=2
 s=c.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
 for p,co in zip(s.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(m);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False)
 if parent:o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted()
 return o

def save(name):
 # A few independent articulated subassemblies, each internally batched.
 parents={o.parent for o in bpy.context.scene.objects if o.type=='MESH'}
 for parent in parents:
  members=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==parent]
  if len(members)>1:
   bpy.ops.object.select_all(action='DESELECT')
   for o in members:o.select_set(True)
   bpy.context.view_layer.objects.active=members[0];bpy.ops.object.join();bpy.context.object.name=(parent.name if parent else name)+'_mesh'
 bpy.ops.object.select_all(action='SELECT');OUT.mkdir(parents=True,exist_ok=True)
 bpy.ops.export_scene.gltf(filepath=str(OUT/(name+'.glb')),export_format='GLB',use_selection=True,export_yup=True,export_extras=True,export_animations=False)
 print('FH_PROP',name,flush=True)

ivory=mat('Case Paint',(.67,.65,.58),.32,.49)
graphite=mat('Metal',(.07,.095,.11),.75,.36)
steel=mat('Steel',(.37,.43,.46),.88,.27)
rubber=mat('Rubber',(.022,.026,.030),.04,.84)
blue=mat('Optic',(.015,.09,.14),.65,.13)
cyan=mat('Emitter',(.13,.67,.83),.35,.25,True)
orange=mat('Amber',(.9,.39,.06),.4,.32,True)

reset();box('Rounded unit box',(0,0,0),(1,1,1),ivory,r=.024);save('rounded_box')

reset();root=group('UtilityDrone')
box('Maintenance hull',(0,0,0),(.58,.34,.30),ivory,root,.045)
box('Upper armored cover',(0,.005,.153),(.45,.28,.04),graphite,root,.02)
box('Underside frame',(0,.012,-.15),(.43,.27,.035),graphite,root)
for side in [-1,1]:
 cyl('Hydraulic connector',(side*.335,0,0),.041,.13,steel,root,(0,math.pi/2,0))
 box('Thruster pod',(side*.425,0,-.005),(.19,.26,.18),ivory,root,.037)
 box('Pod housing',(side*.425,.015,-.100),(.145,.20,.025),graphite,root)
 for i in range(5):box('Cooling slit',(side*.425,-.135,-.055+i*.023),(.12,.008,.008),graphite,root,.002)
 box('Pod running light',(side*.425,-.139,.052),(.06,.008,.014),orange,root,.003)
 cyl('Induction ring',(side*.425,0,-.12),.051,.018,cyan,root)
for x in [-.23,.23]:
 for y in [-.105,.105]:cyl('Fastener',(x,y,.179),.009,.007,steel,root)
gimbal=group('OpticGimbal',(0,-.194,.012),root)
cyl('Optic bezel',(0,-.192,.012),.096,.044,graphite,gimbal,(math.pi/2,0,0))
cyl('Optic inner ring',(0,-.220,.012),.073,.014,steel,gimbal,(math.pi/2,0,0))
sphere('Curved optical lens',(0,-.230,.012),(.064,.026,.064),blue,gimbal)
cyl('Cyan sensor',(0,-.257,.012),.017,.005,cyan,gimbal,(math.pi/2,0,0))
box('Status strip',(0,-.174,-.114),(.21,.012,.008),cyan,root,.002)
hose('Service line',[(-.21,.13,-.13),(-.18,.20,-.04),(.06,.20,.04),(.20,.12,.12)],.011,rubber,root)
save('utility_drone')

reset();root=group('M77')
box('Base chassis',(0,0,.26),(.72,.67,.28),ivory,root,.055)
box('Recessed base',(0,0,.41),(.53,.53,.08),graphite,root)
for side in [-1,1]:
 box('Track belt',(side*.39,0,.21),(.18,.79,.34),rubber,root,.075)
 for i in range(7):
  y=-.32+i*.107
  for z in [.06,.36]:box('Track shoe',(side*.39,y,z),(.19,.076,.033),graphite,root,.006)
 for y in [-.28,0,.28]:
  wheel=group('Wheel',(side*.488,y,.205),root)
  cyl('Drive wheel',(side*.488,y,.205),.109,.035,graphite,wheel,(0,math.pi/2,0))
  cyl('Wheel axle',(side*.51,y,.205),.039,.009,steel,wheel,(0,math.pi/2,0))
cyl('Spine piston',(0,0,.62),.11,.45,steel,root)
box('Torso',(0,0,1.02),(.63,.42,.61),ivory,root,.035)
box('Torso lower shield',(0,-.03,.715),(.49,.44,.06),graphite,root)
for x in [-.26,.26]:
 for z in [.78,1.26]:cyl('Torso bolt',(x,-.22,z),.017,.014,steel,root,(math.pi/2,0,0))
cyl('Central iris',(0,-.23,1.10),.135,.05,graphite,root,(math.pi/2,0,0))
sphere('Amber objective lens',(0,-.27,1.10),(.105,.03,.105),blue,root)
cyl('Objective light',(0,-.30,1.10),.052,.01,orange,root,(math.pi/2,0,0))
for side in [-1,1]:
 shoulder=group('Shoulder_'+('L'if side<0 else'R'),(side*.38,0,1.17),root)
 cyl('Shoulder bearing',(side*.38,0,1.17),.092,.12,steel,shoulder,(0,math.pi/2,0))
 elbow_pos=(side*.65,-.02,1.38 if side<0 else .88)
 tube('Upper actuator',(side*.39,0,1.17),elbow_pos,.072,ivory,shoulder)
 elbow=group('Elbow_'+str(side),elbow_pos,shoulder)
 cyl('Elbow bearing',elbow_pos,.078,.15,graphite,elbow,(math.pi/2,0,0))
 end=(side*.82,-.27,1.62 if side<0 else .75)
 tube('Forearm',elbow_pos,end,.055,ivory,elbow)
 hose('Hydraulic line',[(side*.35,.1,1.19),(side*.58,.14,1.36),(side*.78,-.05,end[2])],.016,rubber,shoulder)
 if side<0:
  for direction in [-1,1]:
   tip=(end[0]+direction*.08,end[1]-.035,end[2]+.18)
   tube('Clamp finger',end,tip,.025,graphite,elbow)
   tube('Clamp jaw',tip,(tip[0]-direction*.04,tip[1]-.07,tip[2]+.08),.023,ivory,elbow)
 else:
  tube('Welder nozzle',end,(end[0]-.02,end[1]-.25,end[2]-.055),.020,steel,elbow)
  cyl('Weld emitter',(end[0]-.02,end[1]-.26,end[2]-.055),.008,.02,cyan,elbow,(math.pi/2,0,0))
hose('Main conduit',[(-.20,.21,.46),(-.29,.30,.67),(-.25,.29,1.24)],.025,rubber,root)
save('m77')

reset();root=group('Shuttle')
box('Transport fuselage',(0,0,0),(2.0,.51,.44),ivory,root,.14)
sphere('Nose',(.94,0,.015),(.50,.25,.21),ivory,root)
box('Cockpit',(.64,-.25,.084),(.55,.025,.23),blue,root,.04)
box('Lower keel',(-.11,0,-.23),(1.65,.34,.065),graphite,root,.025)
for side in [-1,1]:
 box('Wing',(-.3,side*.40,-.08),(1.25,.48,.035),graphite,root,.008)
 cyl('Engine',(-.80,side*.39,-.02),.13,.64,steel,root,(0,math.pi/2,0))
 cyl('Exhaust',(-1.13,side*.39,-.02),.095,.026,cyan,root,(0,math.pi/2,0))
 box('Navigation strip',(.03,side*.51,-.055),(.40,.014,.012),cyan,root,.003)
for x in [-.60,-.30,0,.3]:box('Hull seam',(x,-.259,-.08),(.008,.009,.20),graphite,root,.001)
save('shuttle')
