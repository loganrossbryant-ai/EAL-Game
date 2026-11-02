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

