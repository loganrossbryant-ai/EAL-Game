"""Original detailed Pioneer machinery: distinct silhouettes and articulated parts."""
import bpy,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fh_prop_geometry import *

def label(text,pos,size,material,parent):
 c=bpy.data.curves.new(text,'FONT');c.body=text;c.size=size;c.extrude=.0005;c.align_x='CENTER'
 o=bpy.data.objects.new('Unit marking '+text,c);bpy.context.collection.objects.link(o);o.location=pos;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(material)
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False)
 o.parent=parent;o.matrix_parent_inverse=parent.matrix_world.inverted();return o

def bolts(parent,pos,width,height,m):
 x,y,z=pos
 for sx in [-1,1]:
  for sz in [-1,1]:cyl('Hex fastener',(x+sx*width*.43,y,z+sz*height*.43),.012,.015,m,parent,(math.pi/2,0,0))

def vent(parent,pos,width,height,m):
 x,y,z=pos
 box('Vent gasket',(x,y,z),(width,.018,height),m,parent,.009)
 for i in range(7):box('Vent louvre',(x,y-.012,z-height*.38+i*height*.127),(width*.87,.014,.012),steel,parent,.003)

def optic(parent,pos,radius,color):
 x,y,z=pos
 cyl('Sensor outer bezel',pos,radius,.060,graphite,parent,(math.pi/2,0,0))
 cyl('Sensor steel ring',(x,y-.034,z),radius*.79,.016,steel,parent,(math.pi/2,0,0))
 sphere('Convex optical glass',(x,y-.051,z),(radius*.67,.027,radius*.67),glass,parent)
 cyl('Optical status lamp',(x,y-.081,z),radius*.23,.007,color,parent,(math.pi/2,0,0))

ivory=mat('Case Paint Worn',(.71,.69,.61),.38,.62)
steel=mat('Machined Steel',(.28,.34,.38),.85,.30)
graphite=mat('Carbon Housing',(.035,.051,.064),.64,.48)
rubber=mat('Rubber',(.014,.018,.021),.04,.90)
copper=mat('Copper',(.47,.21,.074),.81,.34)
glass=mat('Optical Glass',(.022,.078,.11),.55,.18)
cyan=mat('Cyan Emitter',(.08,.61,.79),.26,.3,True)
orange=mat('Amber Emitter',(.95,.36,.035),.28,.35,True)
yellow=mat('Loader Ochre',(.56,.32,.055),.48,.64)
medic=mat('Medical Porcelain',(.77,.81,.76),.25,.47)
teal=mat('Marine Teal',(.034,.15,.18),.46,.5)

# M-77: layered armor, real treads, hydraulic elbows, claw teeth, torch and harness.
reset();root=group('M77')
box('Suspended drive chassis',(0,0,.29),(.72,.69,.28),ivory,root,.065)
box('Recessed track frame',(0,0,.13),(.63,.67,.10),graphite,root)
for side in [-1,1]:
 x=side*.42
 for i in range(40):
  a=i/40*math.tau
  y=.29*math.sin(a);z=.22+.155*math.cos(a)
  link=box('Individual tread link',(x,y,z),(.19,.058,.029),rubber,root,.006);link.rotation_euler.x=-a
  if i%2==0:box('Raised tread grip',(x,y,z+.014),(.195,.024,.012),graphite,root,.002)
 for y in [-.22,0,.22]:
  wheel=group('Wheel_'+str(side)+'_'+str(y),(side*.524,y,.22),root)
  cyl('Road wheel',(side*.524,y,.22),.117,.028,graphite,wheel,(0,math.pi/2,0))
  cyl('Wheel hub',(side*.542,y,.22),.047,.018,steel,wheel,(0,math.pi/2,0))
  for i in range(6):cyl('Hub bolt',(side*.554,y+math.cos(i*math.tau/6)*.071,.22+math.sin(i*math.tau/6)*.071),.006,.006,copper,wheel,(0,math.pi/2,0))
box('Front drive armor',(0,-.37,.31),(.58,.055,.26),ivory,root,.025)
for i in range(5):
 stripe=box('Hazard stripe',(-.20+i*.095,-.402,.255),(.040,.006,.067),yellow if i%2 else graphite,root,.002);stripe.rotation_euler.y=.40
label('M-77',(0,-.408,.35),.075,graphite,root)
for side in [-1,1]:
 cyl('Suspension piston',(side*.20,0,.63),.040,.54,steel,root)
 cyl('Hydraulic seal',(side*.20,0,.72),.057,.12,graphite,root)
 hose('Braided drive line',[(side*.27,.17,.41),(side*.30,.23,.59),(side*.22,.21,.91)],.020,rubber,root)
box('Chest core',(0,0,1.11),(.58,.37,.59),graphite,root,.065)
box('Removable chest armor',(0,-.21,1.11),(.63,.060,.63),ivory,root,.032)
box('Side battery',(-.34,.045,1.08),(.10,.29,.38),ivory,root,.020)
vent(root,(.34,-.01,1.08),.095,.30,graphite)
bolts(root,(0,-.252,1.11),.60,.59,steel)
optic(root,(.06,-.267,1.20),.121,orange)
box('Designation plate',(-.085,-.255,.92),(.29,.018,.10),ivory,root,.005)
label('PIONEER',(-.085,-.269,.935),.038,graphite,root)
label('SERVICE UNIT',(-.085,-.269,.897),.020,graphite,root)
for i in range(4):box('Diagnostic port',(.22,-.255,.88+i*.033),(.052,.018,.016),graphite,root,.003)
for side in [-1,1]:
 shoulder_pos=(side*.385,0,1.25);shoulder=group('Shoulder_'+str(side),shoulder_pos,root)
 cyl('Rotary shoulder',shoulder_pos,.099,.13,steel,shoulder,(0,math.pi/2,0))
 box('Shoulder guard',(side*.39,.02,1.32),(.19,.22,.17),ivory,shoulder,.030)
 elbow_pos=(side*.62,-.035,1.42 if side<0 else .94)
 tube('Upper armored actuator',shoulder_pos,elbow_pos,.066,ivory,shoulder)
 tube('Piston rod',(side*.35,-.10,1.26),(side*.61,-.12,elbow_pos[2]),.017,steel,shoulder)
 elbow=group('Elbow_'+str(side),elbow_pos,shoulder)
 cyl('Elbow gear',elbow_pos,.087,.15,graphite,elbow,(math.pi/2,0,0))
 cyl('Gear center',(elbow_pos[0],elbow_pos[1]-.086,elbow_pos[2]),.040,.020,copper,elbow,(math.pi/2,0,0))
 end=(side*.79,-.26,1.63 if side<0 else .77)
 tube('Forearm casing',elbow_pos,end,.058,ivory,elbow)
 for off in [-.042,.042]:tube('Exposed forearm ram',(elbow_pos[0]+off,elbow_pos[1]-.03,elbow_pos[2]),(end[0]+off,end[1],end[2]),.010,steel,elbow)
 hose('Flex conduit',[(side*.37,.11,1.30),(side*.61,.13,elbow_pos[2]+.08),(end[0],end[1]+.06,end[2])],.018,rubber,shoulder)
 if side<0:
  box('Clamp crosshead',end,(.25,.14,.075),graphite,elbow,.018)
  for jaw in [-1,1]:
   a=(end[0]+jaw*.105,end[1],end[2]+.11);b=(end[0]+jaw*.11,end[1]-.08,end[2]+.24)
   tube('Clamp finger root',end,a,.036,ivory,elbow);tube('Clamp finger',a,b,.030,ivory,elbow)
   tube('Curved jaw tip',b,(b[0]-jaw*.07,b[1]-.04,b[2]+.045),.026,graphite,elbow)
   for i in range(4):box('Clamp gripping tooth',(b[0]-jaw*.021,b[1]-.02,b[2]-.07+i*.025),(.012,.024,.012),steel,elbow,.003)
 else:
  tube('Torch grip',end,(end[0],end[1]-.10,end[2]-.02),.043,rubber,elbow)
  tube('Copper arc torch',(end[0],end[1]-.10,end[2]-.02),(end[0]-.02,end[1]-.30,end[2]-.055),.022,copper,elbow)
  cyl('Arc tip',(end[0]-.02,end[1]-.305,end[2]-.055),.009,.023,cyan,elbow,(math.pi/2,0,0))
for i in range(6):hose('Rear service loom',[(-.23+i*.085,.20,.38),(-.27+i*.09,.30,.67),(-.24+i*.085,.26,1.23)],.008,rubber if i%2 else copper,root)
save('m77')

# Tall wheeled courier for the departure terminal.
reset();root=group('CourierBot')
box('Courier base',(0,0,.19),(.58,.44,.21),teal,root,.055)
for side in [-1,1]:
 for y in [-.15,.15]:cyl('Courier wheel',(side*.29,y,.14),.13,.065,rubber,root,(0,math.pi/2,0))
cyl('Telescopic trunk',(0,.02,.48),.075,.43,steel,root)
box('Cargo compartment',(0,.02,.70),(.42,.33,.34),teal,root,.055)
box('Parcel tray',(0,-.09,.90),(.56,.42,.055),ivory,root,.015)
box('Secured parcel',(0,.02,1.02),(.28,.22,.20),yellow,root,.020)
for x in [-.09,.09]:box('Cargo strap',(x,.02,1.125),(.019,.225,.016),graphite,root,.003)
head=group('CourierHead',(0,-.03,1.13),root)
box('Scanner head',(0,-.13,1.17),(.30,.16,.17),ivory,head,.035)
optic(head,(0,-.226,1.17),.054,cyan)
label('LOGISTICS',(0,-.174,.70),.037,ivory,root)
vent(root,(0,-.177,.54),.23,.10,graphite)
for side in [-1,1]:hose('Courier arm',[(side*.19,.02,.76),(side*.31,-.04,.65),(side*.30,-.14,.85)],.020,steel,root)
save('courier_bot')

# Low quadruped cargo loader: a contrasting, grounded silhouette.
reset();root=group('CargoLoader')
box('Load frame',(0,0,.51),(.80,.70,.24),yellow,root,.050)
box('Rubber cargo bed',(0,0,.65),(.88,.75,.065),graphite,root,.015)
for side in [-1,1]:
 for end in [-1,1]:
  start=(side*.36,end*.24,.49);hip=group('Hip_'+str(side)+'_'+str(end),start,root)
  knee=(side*.55,end*.33,.27);foot=(side*.61,end*.41,.08)
  cyl('Loader hip bearing',start,.09,.13,steel,hip,(0,math.pi/2,0))
  tube('Loader upper leg',start,knee,.055,yellow,hip);tube('Loader lower ram',knee,foot,.037,steel,hip)
  box('Magnetic foot',(foot[0],foot[1],.045),(.22,.20,.08),rubber,hip,.025)
  hose('Leg hydraulic line',[start,(side*.57,end*.26,.43),foot],.013,rubber,hip)
box('Supply crate',(-.14,.01,.88),(.43,.49,.41),ivory,root,.028)
box('Supply canister',(.26,.01,.83),(.24,.40,.31),teal,root,.035)
for x in [-.29,.01]:box('Crate restraint',(x,0,1.10),(.025,.51,.03),graphite,root,.003)
optic(root,(0,-.365,.54),.06,cyan);label('CARGO',(0,-.369,.44),.055,graphite,root)
save('cargo_loader')

# Medical skimmer: rounded porcelain shell, blue cross, articulated probe.
reset();root=group('MedicalSkimmer')
sphere('Medical hull',(0,0,0),(.34,.22,.16),medic,root)
box('Sealed instrument bay',(0,-.17,-.03),(.36,.10,.12),graphite,root,.035)
for side in [-1,1]:
 for y in [-.13,.13]:
  cyl('Induction duct',(side*.30,y,-.075),.065,.14,steel,root)
  cyl('Induction glow',(side*.30,y,-.15),.046,.013,cyan,root)
optic(root,(0,-.216,.018),.065,cyan)
box('Medical cross horizontal',(.15,-.18,.055),(.080,.012,.024),cyan,root,.003)
box('Medical cross vertical',(.15,-.18,.055),(.024,.012,.080),cyan,root,.003)
probe=group('MedicalProbe',(0,0,-.13),root)
tube('Medical articulated arm',(0,0,-.13),(.15,-.10,-.23),.018,steel,probe);tube('Probe shank',(.15,-.10,-.23),(.13,-.26,-.27),.013,medic,probe)
label('MED',(0,-.14,.139),.045,teal,root);save('medical_skimmer')

# Two minor repair units: an orb and a multi-legged tool drone, not recolors.
reset();root=group('SurveyOrb')
sphere('Survey spherical shell',(0,0,0),(.23,.23,.23),ivory,root)
for a in [-1,1]:
 box('Orb side fin',(a*.25,.02,-.02),(.12,.30,.045),graphite,root,.014)
 cyl('Orb induction pod',(a*.27,.03,-.07),.054,.13,steel,root)
 cyl('Orb thruster light',(a*.27,.03,-.138),.038,.012,orange,root)
optic(root,(0,-.215,.025),.086,orange)
for x in [-.10,0,.10]:box('Orb panel rib',(x,.12,.185),(.018,.20,.018),graphite,root,.004)
save('survey_orb')
reset();root=group('ToolSpider')
box('Tool spider core',(0,0,0),(.38,.26,.16),graphite,root,.040)
box('Tool spider armored back',(0,0,.09),(.28,.21,.055),teal,root,.018)
optic(root,(0,-.15,.012),.052,orange)
for side in [-1,1]:
 for i in range(3):
  y=-.10+i*.10;leg=group('LegPivot_'+str(side)+'_'+str(i),(side*.16,y,0),root)
  tube('Spider articulated strut',(side*.16,y,0),(side*.30,y+.025,-.07),.018,steel,leg)
  tube('Spider magnetic tool',(side*.30,y+.025,-.07),(side*.36,y+.02,-.20),.013,ivory,leg)
  sphere('Magnetic tool foot',(side*.36,y+.02,-.20),(.025,.026,.016),rubber,leg)
for x in [-.10,.10]:cyl('Spider induction emitter',(x,.06,-.10),.042,.08,cyan,root)
save('tool_spider')

# Holographic board-game table, used only in the recreation room.
reset();root=group('HoloTable')
cyl('Table central column',(0,0,.39),.11,.78,graphite,root)
for a in [0,2.094,4.189]:tube('Table splayed foot',(0,0,.12),(math.cos(a)*.43,math.sin(a)*.43,.045),.042,steel,root)
cyl('Table rim',(0,0,.80),.56,.08,teal,root)
cyl('Inset tabletop glass',(0,0,.85),.49,.018,glass,root)
for i in range(5):
 for axis in [0,1]:
  line=box('Holo board grid',((i-2)*.16 if axis==0 else 0,0 if axis==0 else(i-2)*.16,.87),(.006 if axis==0 else .66,.66 if axis==0 else .006,.006),cyan,root,.001)
for i in range(6):
 piece=group('HoloPiece_'+str(i),(-.24+(i%3)*.24,-.20+(i//3)*.40,.94),root)
 cyl('Game piece base',piece.location,.042,.035,cyan if i<3 else orange,piece)
 sphere('Game piece crystal',(piece.location.x,piece.location.y,1.005),(.036,.036,.065),cyan if i<3 else orange,piece)
save('holo_table')

# Door scanner and K-17 optical assembly have their own recognizable machinery.
reset();root=group('SecurityScanner')
box('Scanner wall plate',(0,.035,0),(.40,.10,.55),graphite,root,.030)
head=group('ScannerHead',(0,-.08,.06),root)
box('Angled sensor shroud',(0,-.10,.08),(.35,.24,.24),teal,head,.040)
optic(head,(0,-.24,.08),.070,cyan)
for i in range(3):box('Access status bar',(-.10+i*.10,-.025,-.17),(.048,.015,.012),orange,root,.002)
label('ACCESS',(0,-.025,-.24),.037,ivory,root);save('security_scanner')
reset();root=group('OpticalArray')
box('Optics mounting plinth',(0,0,.12),(.82,.64,.24),graphite,root,.035)
cyl('Azimuth bearing',(0,0,.34),.24,.22,steel,root)
assembly=group('OpticsGimbal',(0,0,.65),root)
box('Telescope chassis',(0,0,.74),(.36,.73,.34),ivory,assembly,.045)
for side in [-1,1]:
 tube('Optics trunnion',(side*.31,0,.38),(side*.31,0,.74),.045,steel,root)
 cyl('Trunnion bearing',(side*.30,0,.74),.10,.10,graphite,assembly,(0,math.pi/2,0))
for i in range(3):
 cyl('Optical barrel',(0,-.26-i*.12,.74),.16-i*.018,.17,graphite,assembly,(math.pi/2,0,0))
optic(assembly,(0,-.59,.74),.12,cyan)
for x in [-.17,.17]:tube('Focus slide',(x,-.02,.91),(x,-.50,.91),.015,steel,assembly)
vent(assembly,(0,.38,.74),.28,.24,graphite)
label('K-17',(0,-.335,.54),.065,teal,assembly);save('optical_array')
