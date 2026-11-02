class_name PioneerStage3D
extends Node3D

const UI = preload("res://scripts/interface.gd")
const WIDTH = 18.0
var room = "terminal"
var presentation=false
var clock = 0.0
var camera: Camera3D
var background: Sprite3D
var geography: Node3D
var actors: Array[CinematicAvatar] = []
var people: Dictionary = {}
var devices: Node3D
var screen_view: SubViewport
var screen_ui: Control
var screen_center = Vector3(12.4,2.22,-1.85)
var inspection = false
var inspection_time = 0.0
var view_x = 5.335
var gallery = false
var drones: Array[Node3D] = []
var paint: StandardMaterial3D
var metal: StandardMaterial3D
var amber: StandardMaterial3D
var cyan: StandardMaterial3D
var flooring: StandardMaterial3D
var rounded_mesh: Mesh
var held = false
var avatar_fade = 0.0
var active_actor = 0
var route_rise = 1.05
var route_depth = -1.8
var route_end = 10.0
var route_name = "BOARDING GALLERY"
var effect = ""
var effect_time = 0.0
var subjects: Array[Dictionary] = []
var m77: Node3D
var iris: Node3D
var pen: Node3D
var orbit: Sprite3D
var lens: Node3D
var orbit_alpha = 0.0
var effect_camera_x = -1.0
var sparks: Array[MeshInstance3D] = []
var weld_light: OmniLight3D
var camera_request_time = 0.0
var layout: Dictionary
var layout_key = "terminal"
var layout_kind = "stairs"
var route_points: Array[Vector3]=[]
var route_junction_x=6.6
var has_route=true
var device_x=12.4
var device_upper=false
var device_style="boarding"
var lift_platform: Node3D
var lift_height=0.0
var lift_target=0.0
var route_transition=false
var device_screen_height=1.0
var conversation_focus: Node3D
var conversation_focus_height=1.1

func _ready() -> void:
	if ResourceLoader.exists("res://assets/models/rounded_box.glb"):
		var box_scene = load("res://assets/models/rounded_box.glb").instantiate()
		rounded_mesh = _first_mesh(box_scene)
		box_scene.free()
	paint = _material(Color("b8b5a8"),0.45,0.57)
	metal = _material(Color("24333b"),0.72,0.42)
	amber = _material(Color("e7ad65"),0.4,0.32,true)
	cyan = _material(Color("79cedd"),0.3,0.31,true)
	flooring = _material(Color("69767b"),0.62,0.48)
	if ResourceLoader.exists("res://assets/art/ship_alloy.png"):
		for mat in [paint,metal,flooring]:
			mat.albedo_texture = load("res://assets/art/ship_alloy.png")
			mat.uv1_scale = Vector3(3,3,1)
	var environment = WorldEnvironment.new()
	environment.environment = Environment.new()
	environment.environment.background_mode = Environment.BG_COLOR
	environment.environment.background_color = Color("08141d")
	environment.environment.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	environment.environment.ambient_light_color = Color("a2bacb")
	environment.environment.ambient_light_energy = 0.38
	add_child(environment)
	var key = DirectionalLight3D.new()
	key.rotation_degrees = Vector3(-48,-35,0)
	key.light_color = Color("fff3e7")
	key.light_energy = 1.12
	key.shadow_enabled = true
	key.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
	key.directional_shadow_max_distance = 25
	add_child(key)
	var rim = DirectionalLight3D.new()
	rim.rotation_degrees = Vector3(-22,145,0)
	rim.light_color = Color("91c5e4")
	rim.light_energy = 0.7
	add_child(rim)
	camera = Camera3D.new()
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 6
	camera.near = 0.1
	camera.far = 65
	add_child(camera)
	camera.current = true
	background = Sprite3D.new()
	background.shaded = false
	background.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(background)
	configure("terminal")

func _material(color: Color, metallic: float, roughness: float, emissive: bool = false) -> StandardMaterial3D:
	var m = StandardMaterial3D.new()
	m.albedo_color = color
	m.metallic = metallic
	m.roughness = roughness
	if emissive:
		m.emission_enabled = true
		m.emission = color
		m.emission_energy_multiplier = 0.6
	return m

func _box(parent: Node3D, pos: Vector3, size: Vector3, mat: Material) -> MeshInstance3D:
	var item = MeshInstance3D.new()
	if rounded_mesh:
		item.mesh = rounded_mesh
		item.scale = size
	else:
		var mesh = BoxMesh.new()
		mesh.size = size
		item.mesh = mesh
	item.material_override = mat
	item.position = pos
	parent.add_child(item)
	return item

func _first_mesh(node: Node) -> Mesh:
	if node is MeshInstance3D: return node.mesh
	for child in node.get_children():
		var found = _first_mesh(child)
		if found: return found
	return null

func _tube(parent: Node3D, a: Vector3, b: Vector3, radius: float, mat: Material) -> MeshInstance3D:
	var item = MeshInstance3D.new()
	var mesh = CylinderMesh.new()
	mesh.top_radius = radius
	mesh.bottom_radius = radius
	mesh.height = a.distance_to(b)
	mesh.radial_segments = 12
	item.mesh = mesh
	item.material_override = mat
	parent.add_child(item)
	item.position = (a+b)*0.5
	var y = (b-a).normalized()
	var x = Vector3.FORWARD.cross(y).normalized()
	if x.length() < 0.1: x = Vector3.RIGHT.cross(y).normalized()
	item.basis = Basis(x,y,x.cross(y).normalized())
	return item

func configure(value: String,scene_id: String="") -> void:
	room = value
	inspection = false
	conversation_focus=null
	inspection_time = 0
	avatar_fade = 0
	effect = ""
	effect_time = 0
	orbit_alpha = 0
	subjects.clear()
	sparks.clear()
	weld_light=null
	m77 = null
	iris = null
	pen = null
	orbit = null
	lens = null
	if geography:
		geography.visible=false
		geography.queue_free()
	geography = Node3D.new()
	add_child(geography)
	drones.clear()
	var plate = "corridor" if room == "restricted" else room
	var path = "res://assets/art/"+plate+".png"
	if not ResourceLoader.exists(path): path = "res://assets/art/terminal.png"
	background.texture = load(path)
	background.pixel_size = WIDTH / background.texture.get_width()
	background.position = Vector3(WIDTH/2,1.42,-5)
	var receiver = _material(Color.BLACK,0,1)
	receiver.shadow_to_opacity = true
	receiver.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	_box(geography,Vector3(9,-0.07,1.2),Vector3(WIDTH,0.12,4.6),receiver)
	layout_key="boarding" if scene_id=="s1_boarding" else room
	var catalog=JSON.parse_string(FileAccess.get_file_as_string("res://data/room_layouts.json"))
	layout=catalog[layout_key]
	layout_kind=str(layout.kind)
	has_route=layout_kind!="flat"
	route_junction_x=float(layout.junction)
	route_name=str(layout.route_name)
	route_points.clear()
	for point in layout.points:route_points.append(Vector3(point[0],point[1],point[2]))
	route_rise=0
	route_depth=0
	for point in route_points:
		route_rise=maxf(route_rise,point.y)
		route_depth=minf(route_depth,point.z)
	device_x=float(layout.device[0])
	device_upper=bool(layout.device[1])
	device_style=str(layout.device[2])
	lift_platform=null
	lift_height=0
	lift_target=0
	route_transition=false
	_build_route()
	_make_device()
	_room_subjects()
	_batch_static_geometry()

func _batch_static_geometry() -> void:
	# Railings, tread noses and fixture shells share a few material batches.
	# Animated assemblies and the live screen remain independent.
	var protected: Array[Node]=[devices]
	if lift_platform:protected.append(lift_platform)
	if m77:protected.append(m77)
	if pen:protected.append(pen)
	if orbit:protected.append(orbit)
	if lens:protected.append(lens)
	for spark in sparks:protected.append(spark)
	for item in subjects:protected.append(item.node)
	for item in drones:protected.append(item)
	var batches: Dictionary={}
	_collect_static_meshes(geography,protected,batches)
	for group in batches.values():
		var item=MeshInstance3D.new()
		item.mesh=group.tool.commit()
		item.material_override=group.material
		geography.add_child(item)

func _collect_static_meshes(node: Node,protected: Array[Node],batches: Dictionary) -> void:
	if node in protected:return
	if node is MeshInstance3D and node.mesh:
		for i in range(node.mesh.get_surface_count()):
			var material=node.get_active_material(i)
			if not material:continue
			var key=material.get_instance_id()
			if not batches.has(key):
				var surface=SurfaceTool.new()
				surface.begin(Mesh.PRIMITIVE_TRIANGLES)
				batches[key]={"tool":surface,"material":material}
			batches[key].tool.append_from(node.mesh,i,geography.global_transform.affine_inverse()*node.global_transform)
		node.visible=false
		node.queue_free()
		return
	for child in node.get_children():_collect_static_meshes(child,protected,batches)

func _build_route() -> void:
	if not has_route:return
	if layout_kind=="lift":
		# A left observation deck and a separate moving lift replace stairs here.
		_deck_segment(Vector3(0,1.25,-1.2),Vector3(6.35,1.25,-1.2),1.35,true)
		lift_platform=Node3D.new()
		geography.add_child(lift_platform)
		_box(lift_platform,Vector3(7.55,-.08,-.55),Vector3(3.3,.16,1.55),flooring)
		_box(lift_platform,Vector3(7.55,-.20,-.55),Vector3(3.4,.09,1.6),metal)
		for x in [5.85,9.25]:
			_box(geography,Vector3(x,1.7,-1.45),Vector3(.14,3.4,.18),metal)
			_box(geography,Vector3(x,1.7,-1.31),Vector3(.025,3.15,.025),cyan)
			_tube(lift_platform,Vector3(x+.1,0,-1.25),Vector3(x+.1,.90,-1.25),.025,paint)
		_tube(lift_platform,Vector3(5.95,.90,-1.25),Vector3(9.15,.90,-1.25),.025,paint)
		_route_marker(route_junction_x)
		return
	for i in range(route_points.size()-1):
		var a: Vector3=route_points[i]
		var b: Vector3=route_points[i+1]
		if layout_kind=="depth":
			_deck_segment(a,b,1.05,false)
		elif absf(a.y-b.y)<.01:
			_deck_segment(a,b,1.20,true)
		elif layout_kind=="ramp":
			var plank=_box(geography,(a+b)*.5-Vector3(0,.045,0),Vector3(a.distance_to(b),.09,1.15),flooring)
			plank.rotation.z=atan2(b.y-a.y,b.x-a.x)
			plank.rotation.y=-atan2(b.z-a.z,b.x-a.x)
		else:
			var count=maxi(3,ceili(absf(b.y-a.y)/.14))
			for step in range(count):
				var t=(step+.5)/count
				var p=a.lerp(b,t)
				var width=absf(b.x-a.x)/count
				_box(geography,p-Vector3(0,.055,0),Vector3(width,.11,1.10),flooring)
				_box(geography,p+Vector3(width*.43,.003,0),Vector3(.018,.007,1.10),amber)
			for z in [-.47,.47]:_tube(geography,a+Vector3(0,-.12,z),b+Vector3(0,-.12,z),.035,metal)
			_rail(a,b,-.58)
	_route_marker(route_junction_x)

func _deck_segment(a: Vector3,b: Vector3,width: float,railing: bool) -> void:
	var length=Vector2(b.x-a.x,b.z-a.z).length()
	var floor_panel=_box(geography,(a+b)*.5-Vector3(0,.07,0),Vector3(length,.14,width),flooring)
	floor_panel.rotation.y=-atan2(b.z-a.z,b.x-a.x)
	if maxf(a.y,b.y)>.1:
		_box(geography,(a+b)*.5-Vector3(0,.20,0),Vector3(absf(b.x-a.x),.10,width+.05),metal)
		for t in [.12,.52,.88]:
			var p=a.lerp(b,t)
			_box(geography,Vector3(p.x,p.y*.45,p.z),Vector3(.085,p.y*.9,.48),metal)
	if railing:_rail(a,b,-width*.5)
	for j in range(maxi(1,ceili(length/.8))):
		var p=a.lerp(b,(j+.5)/maxf(1,ceili(length/.8)))
		_box(geography,p+Vector3(0,.006,0),Vector3(.012,.008,width*.85),metal)

func _rail(a: Vector3,b: Vector3,z: float) -> void:
	_tube(geography,a+Vector3(0,.94,z),b+Vector3(0,.94,z),.023,paint)
	_tube(geography,a+Vector3(0,.42,z),b+Vector3(0,.42,z),.012,metal)
	var count=maxi(2,ceili(a.distance_to(b)/.85))
	for j in range(count+1):
		var p=a.lerp(b,float(j)/count)+Vector3(0,0,z)
		_tube(geography,p,p+Vector3(0,.94,0),.020,metal)
		_box(geography,p+Vector3(0,.025,0),Vector3(.105,.05,.09),paint)

func _route_marker(x: float) -> void:
	var marker=MeshInstance3D.new()
	var arrow=ImmediateMesh.new()
	arrow.surface_begin(Mesh.PRIMITIVE_TRIANGLES,amber)
	for p in [Vector3(-.16,0,.12),Vector3(.16,0,.12),Vector3(0,0,-.18)]:arrow.surface_add_vertex(p)
	arrow.surface_end()
	marker.mesh=arrow
	marker.position=Vector3(x,.012,.25)
	geography.add_child(marker)

func floor_point(x: float,upper: bool,rider: bool=false) -> Vector3:
	if not upper or not has_route:
		if rider and layout_kind=="lift":return Vector3(x,lift_height,-lift_height/1.25*1.2)
		return Vector3(x,0,0)
	if layout_kind=="lift":
		if rider:return Vector3(x,lift_height,-lift_height/1.25*1.2)
		return Vector3(x,1.25,-1.2)
	if x<route_points[0].x or x>route_points[-1].x:return Vector3(x,0,0)
	for i in range(route_points.size()-1):
		var a: Vector3=route_points[i]
		var b: Vector3=route_points[i+1]
		if x>=a.x and x<=b.x:
			return a.lerp(b,(x-a.x)/maxf(.001,b.x-a.x))
	return Vector3(x,0,0)

func begin_route_change(upper: bool) -> void:
	if layout_kind!="lift":return
	lift_target=1.25 if upper else 0.0
	route_transition=true

func restore_route(upper: bool) -> void:
	if layout_kind!="lift":return
	lift_height=1.25 if upper else 0.0
	lift_target=lift_height
	if lift_platform:lift_platform.position=Vector3(0,lift_height,-lift_height/1.25*.65)

func npc_spot(index: int,id: String) -> Dictionary:
	if id=="m77":return {"x":8.9,"upper":false}
	var spots: Array=layout.npc_positions
	var p: Array=spots[index%spots.size()]
	return {"x":float(p[0]),"upper":bool(p[1]) and has_route}

func add_actor(id: String, is_npc: bool = false) -> CinematicAvatar:
	var actor = CinematicAvatar.new()
	add_child(actor)
	actor.setup(id,is_npc)
	if is_npc: people[id] = actor
	else: actors.append(actor)
	return actor

func _make_device() -> void:
	devices=Node3D.new()
	geography.add_child(devices)
	var at=floor_point(device_x,device_upper)
	var y=at.y
	var z=at.z-.65
	var width={"boarding":1.32,"gate":1.10,"flight":1.48,"habitation":.96,"recreation":.94,"maintenance":1.26,"security":.92,"navigation":1.70,"science":1.35}.get(device_style,1.3)
	device_screen_height=width*.625
	var cy=y+1.20
	match device_style:
		"boarding", "gate":
			_box(devices,Vector3(device_x,y+.56,z-.08),Vector3(.46,1.12,.32),metal)
			_box(devices,Vector3(device_x,y+.09,z),Vector3(.74,.18,.65),paint)
			for i in range(6):_box(devices,Vector3(device_x-.13+i*.052,y+.55,z+.085),Vector3(.025,.25,.015),flooring)
		"flight", "navigation":
			# The monitor clears the desk's front edge instead of intersecting it.
			cy=y+1.45
			_box(devices,Vector3(device_x,y+.42,z),Vector3(width+.36,.84,.68),metal)
			_box(devices,Vector3(device_x,y+.79,z+.22),Vector3(width+.42,.10,.87),paint)
			_box(devices,Vector3(device_x,y+.99,z-.10),Vector3(.14,.38,.14),metal)
			for side in [-1,1]:
				_box(devices,Vector3(device_x+side*(width*.5+.11),y+.94,z+.3),Vector3(.12,.29,.32),metal)
				for i in range(3):_box(devices,Vector3(device_x+side*(width*.5+.11),y+.88+i*.07,z+.47),Vector3(.04,.032,.013),cyan if i!=1 else amber)
		"maintenance":
			_box(devices,Vector3(device_x,y+.40,z+.1),Vector3(2.1,.80,.72),metal)
			_box(devices,Vector3(device_x,y+.84,z+.12),Vector3(2.16,.10,.84),paint)
			for i in range(3):
				_box(devices,Vector3(device_x-.62,y+.19+i*.21,z+.48),Vector3(.60,.16,.027),flooring)
				_tube(devices,Vector3(device_x-.78,y+.19+i*.21,z+.51),Vector3(device_x-.47,y+.19+i*.21,z+.51),.012,metal)
			for i in range(4):_tube(devices,Vector3(device_x+.68+i*.08,y+.90,z+.16),Vector3(device_x+.68+i*.08,y+.90,z+.36),.014,metal)
		"habitation":
			_box(devices,Vector3(device_x,y+.41,z+.14),Vector3(.95,.09,.65),flooring)
			for x in [-.36,.36]:_tube(devices,Vector3(device_x+x,y,z+.12),Vector3(device_x+x,y+.4,z+.12),.027,metal)
			cy=y+.99
		"recreation":
			cy=y+1.12
			_box(devices,Vector3(device_x,y+.55,z-.08),Vector3(.70,1.10,.30),flooring)
			_box(devices,Vector3(device_x,y+.15,z+.12),Vector3(.84,.10,.56),metal)
		"security":
			cy=y+1.16
			_box(devices,Vector3(device_x,y+.55,z-.08),Vector3(.58,1.1,.32),metal)
			_box(devices,Vector3(device_x,y+.20,z+.13),Vector3(.72,.09,.48),flooring)
			for i in range(3):_box(devices,Vector3(device_x-.20+i*.20,y+.73,z+.11),Vector3(.06,.02,.03),amber)
		"science":
			cy=y+1.78
			_box(devices,Vector3(device_x,y+.59,z-.08),Vector3(.94,1.18,.48),metal)
			_box(devices,Vector3(device_x,y+1.29,z-.10),Vector3(.14,.26,.14),metal)
			for side in [-1,1]:
				_box(devices,Vector3(device_x+side*.55,y+.5,z),Vector3(.12,.85,.62),paint)
				for i in range(5):_box(devices,Vector3(device_x+side*.55,y+.25+i*.11,z+.33),Vector3(.065,.024,.018),cyan if i%2 else amber)
	_box(devices,Vector3(device_x,cy,z),Vector3(width+.16,device_screen_height+.16,.12),metal)
	_box(devices,Vector3(device_x,cy,z+.07),Vector3(width+.09,device_screen_height+.09,.025),paint)
	for x in [-1,1]:_box(devices,Vector3(device_x+x*(width*.5+.055),cy,z+.088),Vector3(.012,device_screen_height,.015),cyan)
	screen_center=Vector3(device_x,cy,z+.09)
	screen_view=SubViewport.new()
	screen_view.size=Vector2i(1280,800)
	screen_view.render_target_update_mode=SubViewport.UPDATE_ONCE
	devices.add_child(screen_view)
	screen_ui=Control.new()
	screen_ui.theme=UI.theme()
	screen_ui.size=Vector2(1280,800)
	screen_view.add_child(screen_ui)
	var quad=MeshInstance3D.new()
	var mesh=QuadMesh.new()
	mesh.size=Vector2(width,device_screen_height)
	quad.mesh=mesh
	var material=StandardMaterial3D.new()
	material.shading_mode=BaseMaterial3D.SHADING_MODE_UNSHADED
	material.albedo_texture=screen_view.get_texture()
	quad.material_override=material
	quad.position=screen_center
	devices.add_child(quad)
	var titles={"boarding":"Pioneer Initiative","gate":"Boarding control","flight":"Flight deck","habitation":"Crew commons","recreation":"Recreation deck","maintenance":"Local maintenance bus","security":"Access control","navigation":"Navigation","science":"Observation instruments"}
	show_clue({"title":titles[device_style],"tag":"CSV-01 / "+device_style.to_upper(),"fields":[["SYSTEM","LOCAL INTERFACE"],["CREW","COHORT 01"],["STATUS","STANDBY"]],"note":"Pioneer Initiative"})

func show_clue(clue: Dictionary) -> void:
	for child in screen_ui.get_children(): child.queue_free()
	var p = UI.panel(screen_ui,Rect2(0,0,1280,800),1)
	p.add_theme_stylebox_override("panel",UI.box(Color("081d29"),UI.AMBER))
	UI.label(p,str(clue.tag),Rect2(44,26,1190,34),20,UI.CYAN)
	UI.title(p,str(clue.title),Rect2(44,77,1190,66),43)
	var count = clue.fields.size()
	var row = minf(96,500.0/maxf(count,1))
	for i in range(count):
		UI.label(p,str(clue.fields[i][0]),Rect2(44,173+i*row,240,row),20,UI.CYAN)
		UI.label(p,str(clue.fields[i][1]),Rect2(304,169+i*row,928,row),29,UI.AMBER if str(clue.fields[i][0])=="COMPLETED" else UI.PAPER)
	UI.label(p,str(clue.note),Rect2(44,684,1190,94),23,UI.AMBER)
	screen_view.render_target_update_mode = SubViewport.UPDATE_ONCE

func inspect(clue: Dictionary) -> void:
	show_clue(clue)
	inspection = true
	inspection_time = 0
	camera_request_time = 2.8
	if not actors.is_empty(): actors[active_actor].begin_use()

func close_inspection() -> void:
	conversation_focus=null
	if inspection:camera_request_time=2.8
	inspection = false
	for actor in actors: actor.end_use()

func _drone(point: Vector3) -> void:
	var root = Node3D.new()
	root.position = point
	geography.add_child(root)
	if ResourceLoader.exists("res://assets/models/utility_drone.glb"):
		var machine = load("res://assets/models/utility_drone.glb").instantiate()
		root.add_child(machine)
		_prepare_machine_materials(machine)
		drones.append(root)
		return
	_box(root,Vector3.ZERO,Vector3(.58,.28,.31),paint)
	_box(root,Vector3(0,.15,0),Vector3(.41,.03,.25),metal)
	_box(root,Vector3(0,-.15,0),Vector3(.38,.035,.25),metal)
	for side in [-1,1]:
		_box(root,Vector3(side*.38,0,0),Vector3(.17,.19,.27),metal)
		_box(root,Vector3(side*.38,-.09,0),Vector3(.12,.012,.18),cyan)
		_tube(root,Vector3(side*.29,0,0),Vector3(side*.38,0,0),.032,paint)
	var eye = MeshInstance3D.new()
	var sphere = SphereMesh.new()
	sphere.radius = .075
	sphere.height = .15
	eye.mesh = sphere
	eye.material_override = cyan
	eye.position = Vector3(.13,.01,.17)
	root.add_child(eye)
	drones.append(root)

func _prepare_machine_materials(node: Node) -> void:
	if node is MeshInstance3D:
		for i in range(node.mesh.get_surface_count()):
			var material = node.get_active_material(i)
			if material is StandardMaterial3D:
				var m: StandardMaterial3D = material.duplicate()
				if m.resource_name.begins_with("Case Paint") and ResourceLoader.exists("res://assets/art/ship_alloy.png"):
					m.albedo_texture = load("res://assets/art/robot_enamel.png") if m.resource_name.contains("Worn") else load("res://assets/art/ship_alloy.png")
					m.uv1_scale = Vector3(2,2,1)
					node.set_surface_override_material(i,m)
	for child in node.get_children(): _prepare_machine_materials(child)

func _prop(kind: String, at: Vector3, factor: float = 1.0) -> Node3D:
	var root: Node3D = load("res://assets/models/"+kind+".glb").instantiate()
	geography.add_child(root)
	root.position = at
	root.scale = Vector3.ONE*factor
	_prepare_machine_materials(root)
	return root

func _sphere(parent: Node3D, at: Vector3, size: Vector3, mat: Material) -> MeshInstance3D:
	var mesh = SphereMesh.new()
	mesh.radius = .5
	mesh.height = 1
	mesh.radial_segments = 20
	mesh.rings = 10
	var item = MeshInstance3D.new()
	item.mesh = mesh
	item.material_override = mat
	item.scale = size
	item.position = at
	parent.add_child(item)
	return item

func _ring(parent: Node3D, at: Vector3, radius: float, mat: Material) -> MeshInstance3D:
	var mesh = TorusMesh.new()
	mesh.inner_radius = radius-.009
	mesh.outer_radius = radius+.009
	mesh.rings = 40
	mesh.ring_segments = 6
	var item = MeshInstance3D.new()
	item.mesh = mesh
	item.material_override = mat
	item.position = at
	parent.add_child(item)
	return item

func _moving(kind: String, node: Node3D, phase: float = 0.0) -> void:
	subjects.append({"kind":kind,"node":node,"home":node.position,"phase":phase,"scale":node.scale})

func _plant(at: Vector3, height: float = 1.0) -> void:
	var root = Node3D.new()
	root.position = at
	geography.add_child(root)
	_sphere(root,Vector3(0,.19,0),Vector3(.44,.42,.44),paint)
	var green = _material(Color("355d40"),0,.88)
	var stem = _material(Color("546346"),0,.9)
	for i in range(7):
		var pivot = Node3D.new()
		root.add_child(pivot)
		pivot.position.y = .29
		pivot.rotation.y = i*2.39
		var tip = Vector3(.12+sin(i*2.3)*.08,(.6+i*.08)*height,0)
		_tube(pivot,Vector3.ZERO,tip,.007,stem)
		var leaf = _sphere(pivot,tip,Vector3(.19,.038,.46),green)
		leaf.rotation = Vector3(.3+i*.06,.6,.2)
		_moving("living foliage",pivot,i*.8)

func _fan(at: Vector3) -> void:
	var cage = _ring(geography,at,.38,paint)
	cage.rotation.x = PI/2
	var rotor = Node3D.new()
	rotor.position = at
	geography.add_child(rotor)
	_sphere(rotor,Vector3.ZERO,Vector3(.13,.13,.09),metal)
	for i in range(5):
		var blade = _box(rotor,Vector3.ZERO,Vector3(.27,.09,.04),metal)
		blade.position = Vector3(cos(i*TAU/5),sin(i*TAU/5),0)*.20
		blade.rotation.z = i*TAU/5+.4
	_moving("air circulation",rotor)

func _room_subjects() -> void:
	match layout_key:
		"terminal":
			var courier=_prop("courier_bot",Vector3(10.1,0,-1.1),.88)
			_moving("courier bot",courier)
			var loader=_prop("cargo_loader",Vector3(15.7,0,-1.1),1.0)
			_moving("cargo loader",loader)
			var shuttle=_prop("shuttle",Vector3(5.5,3.6,-4),.58)
			_moving("departure traffic",shuttle)
		"boarding":
			_gate(Vector3(15.8,0,-1.2),true)
			_service_arm(Vector3(10.3,1.90,-1.8))
			for x in [7.0,8.5]:
				_box(geography,Vector3(x,.28,-1.1),Vector3(.72,.56,.50),flooring)
				_box(geography,Vector3(x,.58,-1.1),Vector3(.75,.05,.53),paint)
		"launch":
			orbit=Sprite3D.new()
			orbit.texture=load("res://assets/art/launch_orbit.png")
			orbit.pixel_size=WIDTH/orbit.texture.get_width()
			orbit.position=background.position+Vector3(0,0,.01)
			orbit.billboard=BaseMaterial3D.BILLBOARD_ENABLED
			orbit.shaded=false
			orbit.modulate.a=0
			geography.add_child(orbit)
			pen=Node3D.new()
			pen.position=Vector3(9,1.65,.15)
			geography.add_child(pen)
			_tube(pen,Vector3(0,-.12,0),Vector3(0,.12,0),.012,paint)
			_tube(pen,Vector3(0,.05,0),Vector3(0,.13,0),.014,cyan)
			pen.visible=false
			_service_arm(Vector3(9.0,2.28,-1.7))
			for x in [5.2,6.6,8.0]:_restraint_seat(Vector3(x,0,-1.25))
		"habitation":
			var skimmer=_prop("medical_skimmer",Vector3(9.0,2.10,-.20),1.10)
			_moving("medical skimmer",skimmer)
			_plant(Vector3(3.0,0,-.5),1.15)
			# Keep the upper-deck plant beside the console, clear of Okafor.
			_plant(Vector3(7.05,.68,-2.55),.65)
			for x in [15.0,16.0]:_box(geography,Vector3(x,.48,-1.3),Vector3(.70,.96,.36),flooring)
		"recreation":
			var table=_prop("holo_table",Vector3(10.2,0,-.95),1.15)
			_moving("holographic game table",table)
			_beverage_station(Vector3(14.2,0,-1.45))
			_lounge_seat(Vector3(7.3,0,-1.65),Color("516268"))
			_lounge_seat(Vector3(11.5,0,-1.65),Color("866a4c"))
		"corridor":
			_gate(Vector3(9.75,0,-1.65),false)
			m77=_prop("m77",Vector3(8.75,0,-.85),.95)
			m77.rotation.y=1.0
			var orb=_prop("survey_orb",Vector3(9.8,2.4,-.8),1.0)
			_moving("repair survey orb",orb)
			var spider=_prop("tool_spider",Vector3(11.3,1.90,-.45),1.10)
			_moving("repair tool spider",spider)
			for i in range(13):sparks.append(_sphere(geography,Vector3(9.6,.75,-1.24),Vector3(.012,.012,.04),amber))
			weld_light=OmniLight3D.new()
			weld_light.position=Vector3(9.58,.76,-1.19)
			weld_light.light_color=Color("9bd8f5")
			weld_light.omni_range=1.2
			geography.add_child(weld_light)
			_life_support(Vector3(11.6,0,-1.6))
		"restricted":
			_gate(Vector3(14.4,0,-1.7),false)
			var scanner=_prop("security_scanner",Vector3(10.5,2.05,-1.45),1.25)
			_moving("security scanner",scanner)
			_box(geography,Vector3(13.1,1.60,-1.55),Vector3(.12,3.2,.18),metal)
			_box(geography,Vector3(13.1,1.60,-1.42),Vector3(.022,2.6,.025),amber)
		"bridge":
			_navigation_globe(Vector3(9.1,1.6,-2.15))
			_lensing_geometry()
		"k17":
			var instrument=_prop("optical_array",Vector3(8.9,0,-1.6),1.25)
			_moving("K-17 optical array",instrument)
			_sample_rack(Vector3(6.7,0,-1.6))
			_lensing_geometry()
	iris=null

func _gate(at: Vector3,opens: bool) -> void:
	var root=Node3D.new()
	root.position=at
	geography.add_child(root)
	for side in [-1,1]:
		_box(root,Vector3(side*.94,1.25,0),Vector3(.14,2.5,.24),paint)
		_box(root,Vector3(side*.94,1.25,.15),Vector3(.025,2.20,.02),cyan if opens else amber)
		var panel=_box(root,Vector3(side*.43,1.20,-.04),Vector3(.84,2.40,.17),metal)
		if opens:_moving("boarding gate leaf",panel,side)
		_box(panel,Vector3.ZERO,Vector3(.7,.13,.015),paint)
	_box(root,Vector3(0,2.5,0),Vector3(2.08,.18,.24),metal)

func _service_arm(at: Vector3) -> void:
	var root=Node3D.new()
	root.position=at
	geography.add_child(root)
	_box(root,Vector3(0,0,-.13),Vector3(.32,.45,.30),metal)
	var joint=Node3D.new()
	root.add_child(joint)
	_tube(joint,Vector3.ZERO,Vector3(.44,-.25,0),.06,paint)
	_tube(joint,Vector3(.44,-.25,0),Vector3(.63,-.64,.1),.045,metal)
	_sphere(joint,Vector3(.44,-.25,0),Vector3(.17,.17,.17),flooring)
	_box(joint,Vector3(.63,-.65,.1),Vector3(.18,.09,.20),paint)
	_tube(joint,Vector3(.05,-.06,-.08),Vector3(.46,-.29,-.08),.015,metal)
	_moving("launch service arm",joint)

func _restraint_seat(at: Vector3) -> void:
	var root=Node3D.new()
	root.position=at
	geography.add_child(root)
	_box(root,Vector3(0,.36,0),Vector3(.56,.62,.46),metal)
	var pad=_sphere(root,Vector3(0,.82,-.13),Vector3(.55,1.02,.21),flooring)
	pad.rotation.x=.10
	_sphere(root,Vector3(0,.55,.09),Vector3(.56,.17,.51),flooring)
	for side in [-1,1]:
		_tube(root,Vector3(side*.23,.84,-.01),Vector3(side*.23,.52,.22),.028,paint)
		_box(root,Vector3(side*.16,.94,.0),Vector3(.025,.47,.025),metal)

func _lounge_seat(at: Vector3,color: Color) -> void:
	var mat=_material(color,.05,.89)
	mat.albedo_texture=load("res://assets/art/uniform_fabric.png")
	mat.uv1_scale=Vector3(6,6,1)
	_box(geography,at+Vector3(0,.43,0),Vector3(.82,.13,.74),metal)
	_box(geography,at+Vector3(0,.53,.02),Vector3(.72,.16,.66),mat)
	_box(geography,at+Vector3(0,.91,-.27),Vector3(.77,.71,.16),mat)
	for side in [-1,1]:
		_box(geography,at+Vector3(side*.38,.66,0),Vector3(.11,.24,.66),mat)
		for z in [-.24,.24]:_tube(geography,at+Vector3(side*.29,0,z+.04),at+Vector3(side*.29,.42,z),.022,metal)
		_tube(geography,at+Vector3(side*.31,.65,-.175),at+Vector3(side*.31,1.20,-.175),.0025,metal)
	_tube(geography,at+Vector3(-.31,1.20,-.175),at+Vector3(.31,1.20,-.175),.0025,metal)

func _beverage_station(at: Vector3) -> void:
	_box(geography,at+Vector3(0,.83,0),Vector3(.9,1.66,.55),metal)
	_box(geography,at+Vector3(0,1.00,.30),Vector3(.76,.65,.04),flooring)
	for i in range(3):
		var tube=_sphere(geography,at+Vector3(-.23+i*.23,1.18,.35),Vector3(.14,.39,.15),cyan if i!=1 else amber)
		_moving("refreshment indicator",tube,i*.8)
	_box(geography,at+Vector3(0,.55,.36),Vector3(.70,.07,.39),paint)

func _life_support(at: Vector3) -> void:
	for x in [-.35,.35]:
		_tube(geography,at+Vector3(x,0,0),at+Vector3(x,2.25,0),.055,metal)
		for y in [.35,.65,1.25,1.75]:_sphere(geography,at+Vector3(x,y,.03),Vector3(.15,.09,.15),paint)
	var rotor=_ring(geography,at+Vector3(0,1.1,.10),.19,amber)
	rotor.rotation.x=PI/2
	_moving("life support flow meter",rotor)

func _navigation_globe(at: Vector3) -> void:
	_box(geography,at-Vector3(0,.8,0),Vector3(.15,1.4,.15),metal)
	var globe=Node3D.new()
	globe.position=at
	geography.add_child(globe)
	_sphere(globe,Vector3.ZERO,Vector3(.50,.50,.50),_material(Color("31515e"),.35,.35))
	for i in range(4):
		var ring=_ring(globe,Vector3(0,(i-1.5)*.12,0),.25,cyan)
		ring.scale=Vector3(1-(absf(i-1.5)*.20),1,1-(absf(i-1.5)*.20))
	_moving("navigation globe",globe)

func _sample_rack(at: Vector3) -> void:
	_box(geography,at+Vector3(0,.45,0),Vector3(1.0,.9,.62),metal)
	_box(geography,at+Vector3(0,.94,0),Vector3(1.1,.08,.71),paint)
	for i in range(6):
		_sphere(geography,at+Vector3(-.4+i*.16,1.10,0),Vector3(.07,.28,.07),_material(Color("476874"),.25,.28))
		_box(geography,at+Vector3(-.4+i*.16,1.26,0),Vector3(.075,.035,.075),metal)

func place_iris(point: Vector3) -> void:
	if is_instance_valid(iris):iris.queue_free()
	iris=Node3D.new()
	iris.position=point
	geography.add_child(iris)
	_box(iris,Vector3(0,0,-.06),Vector3(.64,.88,.14),metal)
	for x in [-.33,.33]:_box(iris,Vector3(x,0,.025),Vector3(.018,.79,.025),cyan)
	var photo=AtlasTexture.new()
	var entry=JSON.parse_string(FileAccess.get_file_as_string("res://data/portraits.json")).iris
	photo.atlas=load("res://assets/portraits/"+str(entry.file))
	photo.region=Rect2(entry.region[0],entry.region[1],entry.region[2],entry.region[3])
	var face=MeshInstance3D.new()
	var mesh=QuadMesh.new()
	mesh.size=Vector2(.56,.78)
	face.mesh=mesh
	var material=StandardMaterial3D.new()
	material.shading_mode=BaseMaterial3D.SHADING_MODE_UNSHADED
	material.albedo_texture=photo
	face.material_override=material
	face.position.z=.025
	iris.add_child(face)
	var indicator=_sphere(iris,Vector3(.21,-.36,.05),Vector3(.018,.018,.015),cyan)
	_moving("Iris indicator",indicator)

func _lensing_geometry() -> void:
	lens = Node3D.new()
	geography.add_child(lens)
	lens.position = Vector3(10.0,2.85,-3.9)
	for j in range(5):
		var ring = Node3D.new()
		lens.add_child(ring)
		for i in range(15):
			var angle = -1.38+i*2.63/15
			var next_angle = angle+2.63/15
			var radius = .19+j*.08
			_tube(ring,Vector3(cos(angle)*radius,sin(angle)*radius,0),Vector3(cos(next_angle)*radius,sin(next_angle)*radius,0),.004,cyan)
		_moving("lensing caustic",ring,j*.4)
	lens.visible = false

func set_effect(value: String) -> void:
	effect = value
	effect_time = 0
	effect_camera_x = 9.8 if value=="round2" else -1.0
	camera_request_time=2.8
	if pen: pen.visible = value=="float"
	if lens:lens.visible = value in ["seed","recurrence"]

func reset_view(x: float) -> void:
	view_x=x
	camera.size=6
	camera.position=Vector3(x,4.98,14)
	camera.look_at(Vector3(x,2.36,0))

func focus_person(id: String) -> void:
	conversation_focus=people.get(id)
	conversation_focus_height=1.1
	if id=="m77":conversation_focus=m77
	if id=="iris":conversation_focus=iris
	if id=="m77":conversation_focus_height=.72
	if id=="iris":conversation_focus_height=0.0
	camera_request_time=2.8

func animated_snapshot() -> Array:
	var result: Array = []
	for item in subjects:
		var n: Node3D = item.node
		result.append({"kind":item.kind,"x":n.position.x,"y":n.position.y,"z":n.position.z,"rotation":n.rotation.length(),"assembly_motion":_assembly_signature(n)})
	for n in drones:result.append({"kind":"volumetric service drone","x":n.position.x,"y":n.position.y,"z":n.position.z,"rotation":n.rotation.length()})
	if m77: result.append({"kind":"articulated M-77","x":m77.position.x,"y":m77.position.y,"z":m77.position.z,"rotation":m77.rotation.length()})
	return result

func _assembly_signature(node: Node) -> float:
	var total=0.0
	if node is Node3D:total=node.rotation.dot(Vector3(1,1.7,2.3))+node.scale.dot(Vector3(.31,.43,.57))
	for child in node.get_children():total+=_assembly_signature(child)
	return total

func _process(delta: float) -> void:
	for actor in actors: actor.held=held
	for actor in people.values():actor.held=held
	if not held:
		clock += delta
		effect_time += delta
	var picture_delta = 0.0 if held else delta
	if route_transition and not held:
		lift_height=move_toward(lift_height,lift_target,delta*.75)
		if lift_platform:lift_platform.position=Vector3(0,lift_height,-lift_height/1.25*.65)
		for actor in actors:
			actor.position.y=lift_height
			actor.position.z=-lift_height/1.25*1.2
		if absf(lift_height-lift_target)<.001:route_transition=false
	for drone in drones:
		if not drone.has_meta("home_y"):drone.set_meta("home_y",drone.position.y)
		drone.position.y = float(drone.get_meta("home_y"))+sin(clock*1.1+drone.position.x)*.045
		drone.rotation = Vector3(sin(clock*.7)*.055,sin(clock*.25)*.23,sin(clock*.9)*.04)
		for eye in drone.find_children("*Gimbal*","Node3D",true,false):eye.rotation.y = sin(clock*.8)*.24
	for item in subjects:
		var node: Node3D = item.node
		var phase: float = item.phase
		match str(item.kind):
			"departure traffic":
				node.position.x = fposmod(clock*.23+4.2,23)-2
				node.rotation = Vector3(sin(clock*.4)*.025,-.25,sin(clock*.3)*.025)
			"living foliage":node.rotation.z = sin(clock*.55+phase)*.035
			"air circulation":node.rotation.z = clock*.64
			"orrery orbit", "navigation gimbal":node.rotation = Vector3(sin(clock*.15+phase)*.5,clock*(.10+phase*.03),phase)
			"Iris interface":node.rotation = Vector3(sin(clock*.7+phase)*.22,clock*.2,cos(clock*.4+phase)*.18)
			"lensing caustic":node.rotation.z = sin(clock*1.8+phase)*.15
			"Iris indicator":node.scale=item.scale*(.8+sin(clock*1.7)*.15)
	for item in subjects:
		var node: Node3D=item.node
		var home: Vector3=item.home
		var phase: float=item.phase
		match str(item.kind):
			"courier bot":
				node.position.x=home.x+sin(clock*.16)*.22
				for head in node.find_children("*CourierHead*","Node3D",true,false):head.rotation.y=sin(clock*.6)*.30
			"cargo loader":
				for hip in node.find_children("Hip*","Node3D",true,false):hip.rotation.y=sin(clock*.7+hip.position.x)*.025
			"medical skimmer", "repair survey orb", "repair tool spider":
				node.position.y=home.y+sin(clock*.9+home.x)*.045
				node.rotation=Vector3(sin(clock*.6+home.x)*.05,sin(clock*.31+home.x)*.2,cos(clock*.7)*.035)
				for joint in node.find_children("*LegPivot*","Node3D",true,false):joint.rotation.x=sin(clock*.9+joint.position.x)*.10
				for joint in node.find_children("*MedicalProbe*","Node3D",true,false):joint.rotation.x=sin(clock*.5)*.10
			"holographic game table":
				for piece in node.find_children("HoloPiece*","Node3D",true,false):piece.rotation.z=sin(clock*.8+piece.position.x)*.14
			"security scanner":
				for head in node.find_children("ScannerHead*","Node3D",true,false):head.rotation.z=sin(clock*.45)*.24
			"K-17 optical array":
				for head in node.find_children("OpticsGimbal*","Node3D",true,false):head.rotation.x=sin(clock*.16)*.045
			"launch service arm":node.rotation.z=sin(clock*.31)*.055
			"boarding gate leaf":node.position.x=home.x+phase*smoothstep(13.2,15.3,view_x+2)*.70
			"refreshment indicator":node.scale=item.scale*Vector3(1,1+sin(clock*.6+phase)*.025,1)
			"life support flow meter":node.rotation.z=clock*.10
			"navigation globe":node.rotation.y=clock*.13
	if m77:
		var active = effect in ["weld","encounter","round1","round2","round3"]
		m77.position.x = 8.75+sin(clock*.5)*(.025 if active else 0)
		for joint in m77.find_children("Shoulder*","Node3D",true,false):joint.rotation.x = sin(clock*.6+joint.position.x)*(.16 if active else .015)
		for joint in m77.find_children("Elbow*","Node3D",true,false):joint.rotation.y = sin(clock*.83+joint.position.x)*(.12 if active else .01)
		for wheel in m77.find_children("Wheel*","Node3D",true,false):wheel.rotation.x = sin(clock*.5)*(.5 if active else 0)
		for i in range(sparks.size()):
			var spark=sparks[i]
			spark.visible=active
			var t=fposmod(clock*1.8+i*.173,1)
			spark.position=Vector3(9.6,.75,-1.24)+Vector3(sin(i*12.9)*t*.32,t*.32-t*t*.55,cos(i*4.7)*t*.16)
			spark.scale=Vector3(.009,.009,.035)*(1-t)
		if weld_light:weld_light.light_energy=(.45+sin(clock*43)*.12) if active else 0
	if orbit:
		orbit_alpha = move_toward(orbit_alpha,1.0 if effect in ["ascent","float"] else 0.0,picture_delta*.45)
		orbit.modulate.a = orbit_alpha
	if pen:
		pen.position.y = 1.65+minf(effect_time,9)*.07
		pen.rotation = Vector3(.12+sin(clock*.6)*.1,clock*.09,-.4+clock*.05)
	if lens:lens.visible = effect in ["seed","recurrence"] and effect_time < (.65 if effect=="seed" else 1.65)
	# Explicit GM camera actions can finish while the world is held; otherwise
	# picture hold stops the camera as well as the animated geometry.
	if held and camera_request_time<=0:return
	camera_request_time=maxf(0,camera_request_time-delta)
	var target = Vector3(view_x,1.76 if presentation else 2.36,0)
	if effect_camera_x>=0:target.x=effect_camera_x
	var destination = target+Vector3(0,2.62,14)
	if effect in ["rumble","ascent"] and not held:destination += Vector3(sin(clock*57)*.009,cos(clock*49)*.007,0)
	var size = 6.0
	if is_instance_valid(conversation_focus):
		target=conversation_focus.global_position+Vector3(0,conversation_focus_height,0)
		target.x=clampf(target.x,4.10,WIDTH-4.10)
		destination=target+Vector3(0,1.95,10)
		size=4.5
	if inspection:
		inspection_time += delta
		if inspection_time > .60:
			target = screen_center
			destination = target+Vector3(0,0,.4)
			size = device_screen_height+.35
	var fade = smoothstep(.75,1.10,inspection_time) if inspection else 0.0
	avatar_fade = move_toward(avatar_fade,fade,delta*5)
	for actor in actors:
		for mesh in actor.meshes:mesh.transparency=avatar_fade
		actor.model.visible=not inspection or inspection_time<1.15
	for actor in people.values():actor.model.visible=not inspection or inspection_time<1.15
	camera.position = camera.position.lerp(destination,1-exp(-delta*4.2))
	camera.size = lerpf(camera.size,size,1-exp(-delta*4.2))
	var current_look = camera.position+(-camera.basis.z)*5
	camera.look_at(current_look.lerp(target,1-exp(-delta*5)),Vector3.UP)
