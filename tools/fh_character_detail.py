"""Original Pioneer character surfacing, hair and tailored clothing geometry.
Uses CC0 body topology as fitting data; no upstream program code is included.
"""
import bpy,math,random
from mathutils import Vector

def skin_paint(body,base,profile):
 colors=body.data.color_attributes.new(name='Complexion',type='BYTE_COLOR',domain='CORNER')
 def gauss(x,c,w):return math.exp(-((x-c)/w)**2)
 for polygon in body.data.polygons:
  for loop in polygon.loop_indices:
   i=body.data.loops[loop].vertex_index;p=base[i]
   if polygon.material_index not in [0,4,5]:color=(1,1,1,1)
   else:
    tint=list(profile['skin'][:3]);front=max(0,min(1,(p.z-.25)/.8))
    cheek=gauss(abs(p.x),.72,.31)*gauss(p.y,7.03,.27)*front
    eye=gauss(abs(p.x),.47,.25)*gauss(p.y,7.46,.12)*front
    nose=gauss(p.x,0,.32)*gauss(p.y,7.01,.21)*front
    shade=1-.14*eye
    if profile.get('stubble') and p.y<7.05 and p.z>.5:shade*=.80+.20*gauss(p.y,6.85,.18)*gauss(p.x,0,.4)
    grain=math.sin(p.x*69+p.y*51)*math.cos(p.z*47+p.y*37)*.012
    color=(tint[0]*(shade+grain)*(1+.055*cheek+.025*nose),tint[1]*(shade+grain)*(1-.055*cheek),tint[2]*(shade+grain)*(1-.045*nose),1)
    # Lips are a small continuous band; surrounding muzzle keeps skin color.
    lip=gauss(p.y,6.62,.055)*gauss(p.x,0,.25)*max(0,min(1,(p.z-1.4)/.12))
    color=(color[0]*(1-.09*lip),color[1]*(1-.24*lip),color[2]*(1-.20*lip),1)
   colors.data[loop].color=color
 for material in body.data.materials:
  if material and material.name.startswith(('Skin','Face','Lips')):
   shader=material.node_tree.nodes.get('Principled BSDF');node=material.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='Complexion'
   material.node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color']);shader.inputs['Roughness'].default_value=.77
   shader.inputs['Specular IOR Level'].default_value=.23

def sphere(name,pos,scale,mat,arm,bone):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1,location=pos);o=bpy.context.object;o.name=name;o.scale=scale
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
 vg=o.vertex_groups.new(name=bone);vg.add(list(range(len(o.data.vertices))),1,'REPLACE')
 mod=o.modifiers.new('Pioneer skeleton','ARMATURE');mod.object=arm;o.parent=arm
 return o

def text_mesh(label,pos,size,mat,arm,bone='spine_03'):
 c=bpy.data.curves.new('Embroidered '+label,'FONT');c.body=label;c.size=size;c.extrude=.00035;c.align_x='CENTER'
 o=bpy.data.objects.new('Stitched '+label,c);bpy.context.collection.objects.link(o);o.location=pos;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(mat)
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
 vg=o.vertex_groups.new(name=bone);vg.add(list(range(len(o.data.vertices))),1,'REPLACE');mod=o.modifiers.new('Pioneer skeleton','ARMATURE');mod.object=arm;o.parent=arm

def jacket(body,arm,base,weights,cloth,mesh_object,profile):
 faces=[list(p.vertices) for p in body.data.polygons if p.material_index==1]
 used=sorted({i for f in faces for i in f});mapping={i:j for j,i in enumerate(used)}
 coords=[body.data.vertices[i].co.copy() for i in used]
 neighbors=[set() for _ in coords];edge_counts={}
 for face in faces:
  for aa,bb in zip(face,face[1:]+face[:1]):
   a=mapping[aa];b=mapping[bb];neighbors[a].add(b);neighbors[b].add(a);edge=tuple(sorted((a,b)));edge_counts[edge]=edge_counts.get(edge,0)+1
 boundary={i for edge,count in edge_counts.items() if count==1 for i in edge}
 for _ in range(22):
  fresh=[p.copy() for p in coords]
  for i in range(len(coords)):
   if i not in boundary and neighbors[i]:fresh[i]=coords[i].lerp(sum((coords[j] for j in neighbors[i]),Vector())/len(neighbors[i]),.52)
  coords=fresh
 # Separate relaxed fabric from the fitted undershirt; suppress anatomical detail.
 for j,i in enumerate(used):
  p=coords[j];normal=body.data.vertices[i].normal
  torso=abs(base[i].x)<2.15
  ease=.022 if torso else .016
  p+=normal*ease
  if torso and 1.03<(base[i].y+8.4488)*.1<1.48 and p.y<-.04:
   p.y=min(p.y,-.18*math.sqrt(max(.1,1-(p.x/.245)**2)))
  if not torso:p+=normal*(math.sin(p.z*105+abs(p.x)*11)*.003)
 garment=mesh_object('Tailored Pioneer jacket',coords,[[mapping[i] for i in f] for f in faces],cloth)
 uvl=garment.data.uv_layers.new(name='Tailored cloth')
 source=[p for p in body.data.polygons if p.material_index==1]
 for p,q in zip(garment.data.polygons,source):
  for dst,src in zip(p.loop_indices,q.loop_indices):uvl.data[dst].uv=body.data.uv_layers.active.data[src].uv
 for bone,values in weights.items():
  group=garment.vertex_groups.new(name=bone)
  for i,w in values:
   if i in mapping:group.add([mapping[i]],w,'REPLACE')
 bpy.context.view_layer.objects.active=garment
 solid=garment.modifiers.new('Bound fabric edge','SOLIDIFY');solid.thickness=.004;solid.offset=-1
 bpy.ops.object.modifier_apply(modifier=solid.name)
 mod=garment.modifiers.new('Pioneer skeleton','ARMATURE');mod.object=arm;garment.parent=arm
 return garment

def hair_geometry(name,profile,arm,base,coords,normals,faces,hair,mesh_object,bind,curve,material):
 hair_faces=[]
 for face in faces:
  p=sum((base[i] for i in face),Vector())/len(face)
  backline=7.30 if profile['hair'] in ['bun','short'] else 6.96
  temple=7.40 if profile['hair'] in ['bun','short'] else 7.24
  if p.y>7.78 or (p.y>backline and p.z<.64) or (p.y>temple and abs(p.x)>.64 and p.z<1.03):hair_faces.append(face)
 offset=.007 if profile['hair']!='curl' else .010
 capcoords=[coords[i]+normals[i]*offset for i in range(len(coords))]
 cap=mesh_object('Continuous sculpted hair cap',capcoords,hair_faces,hair);bind(cap,arm,'head')
 highlight=material('Hair highlights',(.061,.035,.021,1),rough=.88)
 grey=material('Hair silver strands',(.16,.15,.13,1),rough=.88)
 choices=random.sample(hair_faces,min(115,len(hair_faces)))
 for index,face in enumerate(choices):
  p=sum((capcoords[i] for i in face),Vector())/len(face);n=sum((normals[i] for i in face),Vector()).normalized()
  tangent=Vector((.34 if name in ['venn','juno'] else -.30,.48,-.35));tangent=(tangent-n*tangent.dot(n)).normalized()
  points=[]
  if profile['hair']=='curl':
   u=n.cross(tangent).normalized()
   for j in range(9):
    a=j/8*math.tau*1.25;points.append(p+tangent*(math.cos(a)*.006)+u*(math.sin(a)*.006)+n*(.002+j/8*.004))
   radius=.0022
  else:
   length=.018 if profile['hair']=='short' else .026
   for j in range(6):
    t=j/5;wave=math.sin(t*math.pi)*.002
    points.append(p+tangent*length*t+n*wave)
   radius=.0016
  mat=grey if profile.get('stubble') and index%7==0 else (highlight if index%5==0 else hair)
  curve('Sculpted flowing hair lock',points,radius,mat,arm,'head')
 if profile['hair'] in ['wave','bob']:
  for i in range(10):
   desired=Vector((-.80+i*.16,7.90,1.00));k=min(range(len(base)),key=lambda j:(base[j]-desired).length_squared)
   p=coords[k]+normals[k]*.028
   curve('Swept fringe',[p,p+Vector((.015,-.008,.001)),p+Vector((.030,-.008,-.006)),p+Vector((.037,-.004,-.019))],.004,hair,arm,'head')
 scalp=[capcoords[i] for f in hair_faces for i in f]
 headtop=max(p.z for p in scalp)
 back=max(p.y for p in scalp)
 if profile['hair']=='bun':
  bun=Vector((0,max(p.y for p in scalp)+.025,max(p.z for p in scalp)-.11))
  sphere('Braided officer bun',bun,(.055,.040,.050),hair,arm,'head')
  for i in range(9):
   a=i/9*math.tau;points=[bun+Vector((math.cos(a)*.051,math.sin(a)*.038,0)),bun+Vector((math.cos(a+.5)*.052,math.sin(a+.5)*.038,.015)),bun+Vector((math.cos(a+1)*.048,math.sin(a+1)*.035,-.010))]
   curve('Bun braid',points,.002,highlight,arm,'head')
 if profile['hair']=='pony':
  for i in range(7):
   x=(i-3)*.008
   root=Vector((x,back+.015,headtop-.085))
   curve('Gathered ponytail',[root,root+Vector((.005,.035,-.025)),root+Vector((.012,.045,-.095)),root+Vector((.015,.035,-.19))],.008,hair,arm,'head')
 if profile['hair']=='bob':
  for side in [-1,1]:
   for i in range(9):
    a=(i/8)*2.0-1
    p=Vector((side*(.078+math.cos(a)*.006),.005+math.sin(a)*.055,headtop-.075))
    curve('Bob side lock',[p,p+Vector((side*.008,.006,-.04)),p+Vector((side*.010,.01,-.085)),p+Vector((side*.003,.009,-.13))],.006,hair,arm,'head')
 if profile.get('beard'):
  selected=[]
  for f in faces:
   p=sum((base[i] for i in f),Vector())/len(f)
   if 6.14<p.y<7.15 and p.z>.49 and (abs(p.x)>.35 or p.y<6.64):selected.append(f)
  beard=mesh_object('Short sculpted beard',[coords[i]+normals[i]*.007 for i in range(len(coords))],selected,hair);bind(beard,arm,'head')
  for f in random.sample(selected,min(85,len(selected))):
   p=sum((coords[i]+normals[i]*.010 for i in f),Vector())/len(f)
   curve('Beard lock',[p,p+Vector((.002,-.003,-.008)),p+Vector((.001,-.002,-.014))],.0028,hair,arm,'head')
 # Eyebrows follow the actual facial topology, including side views.
 for side in [-1,1]:
  brow=[]
  for i in range(6):
   u=i/5;desired=Vector((side*(.22+.49*u),7.58+math.sin(u*math.pi)*.10,1.20));k=min(range(len(base)),key=lambda j:(base[j]-desired).length_squared)
   brow.append(coords[k]+normals[k]*.004)
  curve('Fitted eyebrow',brow,.003,hair,arm,'head')

def outfit_details(name,profile,arm,body,base,cloth,trim,dark,glass,hair,mesh_object,bind,cube,curve,material):
 waist=arm.data.bones['pelvis'].head_local.z+.09
 chest=arm.data.bones['spine_03'].tail_local.z-.11
 neck=arm.data.bones['neck_01'].head_local.z-.025
 front=-.203
 # Fit the open collar to the mesh neckline, independently of rig joint origins.
 neckline=[body.data.vertices[i].co for i,p in enumerate(base) if 5.78<p.y<6.04 and abs(p.x)<.68]
 center=sum(neckline,Vector())/len(neckline)
 collar_z=center.z+.014
 vs=[];fs=[];steps=40
 for j in range(2):
  for i in range(steps):
   a=i/steps*math.tau
   vs.append((math.sin(a)*(.098-j*.010),center.y-math.cos(a)*(.090-j*.010),collar_z+(-.022 if j==0 else .033)))
 for i in range(steps):fs.append([i,(i+1)%steps,(i+1)%steps+steps,i+steps])
 band=mesh_object('Fitted standing collar',vs,fs,cloth);bind(band,arm,'neck_01')
 if name=='venn':
  curve('Officer gold collar piping',[(math.sin(i/40*math.tau)*.089,center.y-math.cos(i/40*math.tau)*.081,collar_z+.034) for i in range(41)],.0022,trim,arm,'neck_01')
 # Structured standing collar, lapels and a visible placket.
 for side in [-1,1]:
  curve('Structured jacket collar',[(side*.027,-.085,neck-.045),(side*.075,-.067,neck+.010),(side*.082,.025,neck+.027),(side*.035,.075,neck+.024)],.014,cloth,arm,'spine_03')
  if name in ['vale','okafor']:
   vs=[(side*.035,-.125,neck-.02),(side*.115,front+.015,chest+.06),(side*.055,front-.005,chest-.07)]
   lapel=mesh_object('Tailored lapel',vs,[[0,1,2],[2,1,0]],cloth);bind(lapel,arm,'spine_03')
 cube('Reinforced front closure',(0,front+.008,(waist+neck)*.5),(.010,.007,neck-waist-.03),dark,arm,'spine_03',.002)
 for side in [-1,1]:
  for i in range(3):cube('Closure stud',(side*.019,front-.006,chest-.05-i*.078),(.008,.005,.008),trim,arm,'spine_03',.002)
 # Asymmetrical, gusseted cloth pockets with seams and flap snaps.
 for side in [-1,1]:
  p=Vector((side*.106,front-.008,chest-.115+(0 if side>0 else .075)))
  cube('Gusseted field pocket',p,(.087,.025,.095),cloth,arm,'spine_03',.009)
  cube('Pocket flap',p+Vector((0,-.016,.035)),(.093,.010,.026),cloth,arm,'spine_03',.004)
  cube('Pocket snap',p+Vector((0,-.022,.027)),(.008,.004,.008),trim,arm,'spine_03',.002)
  curve('Pocket edge stitching',[p+Vector((-.039,-.016,.020)),p+Vector((-.039,-.017,-.041)),p+Vector((.039,-.017,-.041)),p+Vector((.039,-.016,.020))],.0014,trim,arm,'spine_03')
 cube('Identity patch',(-.102,front-.026,chest+.016),(.095,.008,.039),dark,arm,'spine_03',.004)
 text_mesh(('CMD' if name=='venn' else ('MED' if name=='okafor' else 'PIONEER')),(-.102,front-.031,chest+.006),.012,trim,arm)
 # Original double-chevron Pioneer emblem and department bars.
 for side in [-1,1]:curve('Pioneer chevron',[(.09+side*.025,front-.029,chest-.013),(.09,front-.030,chest+.032)],.003,trim,arm,'spine_03')
 for side in [-1,1]:
  suffix='l' if side>0 else 'r';shoulder=arm.data.bones['upperarm_'+suffix].head_local
  cube('Shoulder yoke',shoulder+Vector((side*.020,0,.014)),(.065,.18,.032),cloth,arm,'upperarm_'+suffix,.009)
  for i in range(3 if name=='venn' else 1):cube('Rank braid',shoulder+Vector((side*.020,-.052+i*.025,.034)),(.060,.010,.007),trim,arm,'upperarm_'+suffix,.002)
  wrist=arm.data.bones['hand_'+suffix].head_local
  cube('Layered sleeve cuff',wrist+Vector((0,.020,.020)),(.094,.115,.044),dark,arm,'lowerarm_'+suffix,.011)
  cube('Wrist tab',wrist+Vector((0,-.040,.022)),(.052,.010,.028),trim,arm,'lowerarm_'+suffix,.004)
 # A real belt wraps the hips instead of a solid rectangular block through them.
 pts=[Vector((math.sin(i/24*math.tau)*.164,-math.cos(i/24*math.tau)*.148,waist-.015)) for i in range(25)]
 curve('Woven utility belt',pts,.017,dark,arm,'pelvis')
 cube('Belt buckle',(0,-.168,waist-.015),(.053,.018,.032),trim,arm,'pelvis',.005)
 curve('Jacket hem seam',[Vector((math.sin(i/24*math.tau)*.182,-math.cos(i/24*math.tau)*.168,waist+.043)) for i in range(25)],.005,cloth,arm,'pelvis')
 if name in ['flight','science','colony','juno']:
  z=arm.data.bones['spine_03'].head_local.z+.04
  size={'flight':(.23,.115,.30),'science':(.19,.09,.25),'colony':(.25,.13,.24),'juno':(.22,.11,.32)}[name]
  cube('Soft field pack',(0,.19,z),size,cloth,arm,'spine_03',.040)
  cube('Pack flap',(0,.255,z+.08),(size[0]+.012,.035,.12),cloth,arm,'spine_03',.018)
  for side in [-1,1]:
   curve('Canvas shoulder strap',[(side*.074,.22,z+.12),(side*.13,.05,chest+.14),(side*.145,front-.014,chest+.015),(side*.12,front-.025,waist+.04),(side*.08,.21,z-.12)],.013,dark,arm,'spine_03')
   cube('Pack buckle',(side*.07,.281,z-.02),(.035,.018,.046),trim,arm,'spine_03',.004)
  if name=='juno':
   # Folded hood changes Juno's silhouette to match the PPT's civilian jacket.
   for i in range(4):
    a=i*.28
    curve('Folded hood seam',[(-.12,.14,neck-.05-a*.06),(-.09,.20+a*.02,neck-.10-a*.04),(0,.22+a*.02,neck-.14-a*.03),(.09,.20+a*.02,neck-.10-a*.04),(.12,.14,neck-.05-a*.06)],.017,cloth,arm,'spine_03')
 if name in ['engineering','rhee']:
  orange=material('Tool handle',(.46,.16,.035,1),rough=.70)
  for i in range(3):
   x=.16+i*.017
   cube('Belt tool pouch',(x,-.01,waist-.10),(.040,.075,.14),dark,arm,'pelvis',.009)
   cube('Insulated tool handle',(x,-.03,waist-.035),(.018,.032,.14),orange,arm,'pelvis',.006)
  curve('Service lanyard',[(.08,-.15,waist-.02),(.16,-.18,waist-.19),(.20,-.11,waist-.03)],.004,trim,arm,'pelvis')
 if profile.get('tablet'):
  hand=arm.data.bones['hand_l'].head_local
  cube('Field tablet case',hand+Vector((0,-.025,0)),(.17,.026,.235),dark,arm,'hand_l',.012)
  cube('Field tablet glass',hand+Vector((0,-.041,.003)),(.143,.008,.205),glass,arm,'hand_l',.006)
  for i in range(3):cube('Tablet status indicator',hand+Vector((-.04+i*.04,-.048,-.104)),(.014,.003,.004),trim,arm,'hand_l',.001)
 if name=='okafor':
  # Mid-thigh medical coat, with an open front and separate weighted skirt.
  vs=[];faces=[];segments=32;rings=6
  for j in range(rings):
   t=j/(rings-1);z=waist+.06-t*.30
   for i in range(segments+1):
    a=.22+i/segments*(math.tau-.44);vs.append((math.sin(a)*(.18+t*.055),-math.cos(a)*(.17+t*.07),z))
  for j in range(rings-1):
   for i in range(segments):a=j*(segments+1)+i;faces.append([a,a+1,a+segments+2,a+segments+1])
  skirt=mesh_object('Medical coat skirt',vs,faces,cloth);bind(skirt,arm,'pelvis')
  for side in [-1,1]:cube('Coat patch pocket',(side*.15,-.18,waist-.11),(.12,.018,.12),cloth,arm,'pelvis',.009)
