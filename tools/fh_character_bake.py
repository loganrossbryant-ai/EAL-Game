"""Original 3D material/UV baking for lightweight, detailed Pioneer characters.

Source images are unchanged AI material tiles. Blender bakes their appearance,
contact shading and tangent normals into ordinary UV texture maps. No portrait
projection or upstream program code is used.
"""
from pathlib import Path
import bpy,math,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'far-horizon/assets/art/characters'

def remove_hidden_body(body):
 """Discard skin-tight clothing underneath the real jacket and fitted boots."""
 old=body.data
 keep=[p for p in old.polygons if p.material_index not in [1,3]]
 coordinates=[v.co.copy() for v in old.vertices]
 group_names=[g.name for g in body.vertex_groups]
 weights=[[(g.group,g.weight) for g in v.groups] for v in old.vertices]
 keys=[]
 if old.shape_keys:
  keys=[(k.name,[v.co.copy() for v in k.data]) for k in old.shape_keys.key_blocks]
 mesh=bpy.data.meshes.new('Visible skin and trousers')
 mesh.from_pydata(coordinates,[],[list(p.vertices) for p in keep]);mesh.update()
 for m in old.materials:mesh.materials.append(m)
 loopmap=[]
 for new,source in zip(mesh.polygons,keep):
  new.material_index=source.material_index;new.use_smooth=True
  loopmap.extend(list(source.loop_indices))
 for source in old.uv_layers:
  dest=mesh.uv_layers.new(name=source.name)
  for i,j in enumerate(loopmap):dest.data[i].uv=source.data[j].uv
 for source in old.color_attributes:
  dest=mesh.color_attributes.new(name=source.name,type=source.data_type,domain=source.domain)
  mapping=loopmap if source.domain=='CORNER' else range(len(coordinates))
  for i,j in enumerate(mapping):dest.data[i].color=source.data[j].color
 body.data=mesh
 # Blender clears deform-group definitions when the replacement mesh has no
 # deform layer. Recreate the definitions in their original index order first.
 body.vertex_groups.clear()
 for name in group_names:body.vertex_groups.new(name=name)
 for index,groups in enumerate(weights):
  for group,weight in groups:body.vertex_groups[group].add([index],weight,"REPLACE")
 for name,values in keys:
  key=body.shape_key_add(name=name)
  for v,p in zip(key.data,values):v.co=p
 return len(old.polygons)-len(keep)

def shader_detail(material):
 if not material or not material.use_nodes:return
 nt=material.node_tree;n=nt.nodes;l=nt.links
 shader=next((x for x in n if x.type=='BSDF_PRINCIPLED'),None)
 if not shader:return
 name=material.name
 if name.startswith(('Skin','Face','Lips','Uniform','Pants')):
  skin=name.startswith(('Skin','Face','Lips'))
  source=ROOT/'far-horizon/assets/art'/('skin_microdetail.png' if skin else 'uniform_fabric.png')
  coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=32 if skin else 9
  l.new(coord.outputs['Object'],mapping.inputs[0])
  tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(source),check_existing=True);tex.projection='BOX';tex.projection_blend=.25;l.new(mapping.outputs[0],tex.inputs['Vector'])
  gray=n.new('ShaderNodeRGBToBW');l.new(tex.outputs['Color'],gray.inputs[0])
  scale=n.new('ShaderNodeMapRange');scale.inputs['From Min'].default_value=.10;scale.inputs['From Max'].default_value=.80;scale.inputs['To Min'].default_value=.93 if skin else .87;scale.inputs['To Max'].default_value=1.045 if skin else 1.06;l.new(gray.outputs[0],scale.inputs['Value'])
  multiply=n.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1
  base=shader.inputs['Base Color']
  if base.is_linked:l.new(base.links[0].from_socket,multiply.inputs[1])
  else:multiply.inputs[1].default_value=base.default_value
  l.new(scale.outputs['Result'],multiply.inputs[2]);l.new(multiply.outputs[0],base)
  micro=n.new('ShaderNodeBump');micro.inputs['Strength'].default_value=.33;micro.inputs['Distance'].default_value=.00018 if skin else .00055;l.new(gray.outputs[0],micro.inputs['Height'])
  if not skin:
   noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=22;noise.inputs['Detail'].default_value=2.5;noise.inputs['Roughness'].default_value=.6;l.new(coord.outputs['Object'],noise.inputs['Vector'])
   folds=n.new('ShaderNodeBump');folds.inputs['Strength'].default_value=.25;folds.inputs['Distance'].default_value=.0025;l.new(noise.outputs['Fac'],folds.inputs['Height']);l.new(folds.outputs['Normal'],micro.inputs['Normal'])
  l.new(micro.outputs['Normal'],shader.inputs['Normal'])
  shader.inputs['Roughness'].default_value=.56 if skin else .80
  shader.inputs['Specular IOR Level'].default_value=.34 if skin else .25
 elif name.startswith('Hair'):
  shader.inputs['Roughness'].default_value=.57
 return shader

def bake_appearance(name,body,arm):
 OUT.mkdir(parents=True,exist_ok=True)
 removed=remove_hidden_body(body)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
 materials=list({m for o in meshes for m in o.data.materials if m})
 for m in materials:shader_detail(m)
 # Eyes keep their fitted iris UV; source tiles use object-space coordinates.
 for m in materials:
  for n in m.node_tree.nodes:
   if n.type=='TEX_IMAGE' and n.image and n.image.name.startswith('brown_eye'):
    uv=m.node_tree.nodes.new('ShaderNodeUVMap');uv.uv_map='Iris UV';m.node_tree.links.new(uv.outputs['UV'],n.inputs['Vector'])
 for o in meshes:
  uv=o.data.uv_layers.new(name='Pioneer atlas UV');o.data.uv_layers.active=uv;uv.active_render=True
 bpy.ops.object.select_all(action='DESELECT')
 for o in meshes:o.select_set(True)
 bpy.context.view_layer.objects.active=body
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
 bpy.ops.uv.smart_project(angle_limit=1.15192,island_margin=.006,area_weight=.5,scale_to_bounds=False)
 bpy.ops.uv.pack_islands(rotate=True,margin=.008)
 bpy.ops.object.mode_set(mode='OBJECT')
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4
 scene.render.bake.margin=12;scene.render.bake.use_clear=True
 arm.data.pose_position='REST'
 source_outputs={};emission_nodes={};bake_targets={}
 for m in materials:
  nt=m.node_tree;output=next(x for x in nt.nodes if x.type=='OUTPUT_MATERIAL');source_outputs[m]=(output,output.inputs['Surface'].links[0].from_socket)
  emit=nt.nodes.new('ShaderNodeEmission');emission_nodes[m]=emit
  target=nt.nodes.new('ShaderNodeTexImage');bake_targets[m]=target
 def target_image(label,size,colorspace):
  im=bpy.data.images.new(name+' '+label,width=size,height=size,alpha=False)
  im.colorspace_settings.name=colorspace
  for m,node in bake_targets.items():node.image=im;m.node_tree.nodes.active=node
  return im
 def save(image,label):
  path=OUT/(name+'_'+label+'.png');image.filepath_raw=str(path);image.file_format='PNG';image.save();return path
 # Contact shading is baked once; it does not require extra live draw passes.
 albedo=target_image('albedo',2048,'sRGB')
 for m in materials:
  nt=m.node_tree;shader=next(x for x in nt.nodes if x.type=='BSDF_PRINCIPLED');base=shader.inputs['Base Color']
  ao=nt.nodes.new('ShaderNodeAmbientOcclusion');ao.inputs['Distance'].default_value=.085;ao.samples=8
  mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.48
  if base.is_linked:nt.links.new(base.links[0].from_socket,mix.inputs[1])
  else:mix.inputs[1].default_value=base.default_value
  nt.links.new(ao.outputs['Color'],mix.inputs[2]);nt.links.new(mix.outputs[0],emission_nodes[m].inputs['Color']);nt.links.new(emission_nodes[m].outputs[0],source_outputs[m][0].inputs['Surface'])
 bpy.ops.object.bake(type='EMIT');paths={'albedo':str(save(albedo,'albedo'))}
 # Restore the shading normals, including the fine cloth/skin bump treatment.
 for m,(output,socket) in source_outputs.items():m.node_tree.links.new(socket,output.inputs['Surface'])
 normal=target_image('normal',1024,'Non-Color');bpy.ops.object.bake(type='NORMAL',normal_space='TANGENT');paths['normal']=str(save(normal,'normal'))
 orm=target_image('orm',1024,'Non-Color')
 for m in materials:
  nt=m.node_tree;shader=next(x for x in nt.nodes if x.type=='BSDF_PRINCIPLED');combine=nt.nodes.new('ShaderNodeCombineColor');combine.mode='RGB';combine.inputs[0].default_value=1;combine.inputs[1].default_value=shader.inputs['Roughness'].default_value;combine.inputs[2].default_value=shader.inputs['Metallic'].default_value
  nt.links.new(combine.outputs[0],emission_nodes[m].inputs['Color']);nt.links.new(emission_nodes[m].outputs[0],source_outputs[m][0].inputs['Surface'])
 bpy.ops.object.bake(type='EMIT');paths['orm']=str(save(orm,'orm'))
 # One shared material across the two skinned meshes replaces many surfaces.
 material=bpy.data.materials.new('PioneerBakedAtlas');material.use_nodes=True
 shader=material.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(.65,.65,.65,1);shader.inputs['Roughness'].default_value=.65
 # A tiny placeholder keeps UVs/tangents in glTF without embedding the full
 # atlases twice. Godot binds the external maps to this material at runtime.
 placeholder=bpy.data.images.new('Atlas UV placeholder',width=1,height=1,alpha=False)
 placeholder.generated_color=(1,1,1,1)
 tex=material.node_tree.nodes.new('ShaderNodeTexImage');tex.image=placeholder
 material.node_tree.links.new(tex.outputs['Color'],shader.inputs['Base Color'])
 for o in meshes:
  o.data.materials.clear();o.data.materials.append(material)
  for p in o.data.polygons:p.material_index=0
  # RNA layer references shift after removal; retain names instead of wrappers.
  for old_name in [uv.name for uv in o.data.uv_layers if uv.name!='Pioneer atlas UV']:
   o.data.uv_layers.remove(o.data.uv_layers[old_name])
  o.data.uv_layers.active_index=0;o.data.uv_layers[0].active_render=True
  assert len(o.data.uv_layers)==1 and o.data.uv_layers[0].name=='Pioneer atlas UV'
  for attr in list(o.data.color_attributes):o.data.color_attributes.remove(attr)
 arm.data.pose_position='POSE'
 report={'name':name,'removed_hidden_faces':removed,'skinned_meshes':len(meshes),'surfaces':len(meshes),'albedo_pixels':[2048,2048],'normal_and_orm_pixels':[1024,1024],'maps':paths,'source_images_unchanged':True,'method':'3D UV material baking; no projected portrait'}
 (OUT/(name+'_bake.json')).write_text(json.dumps(report,indent=2)+'\n')
 print('FH_BAKED',json.dumps(report),flush=True)
