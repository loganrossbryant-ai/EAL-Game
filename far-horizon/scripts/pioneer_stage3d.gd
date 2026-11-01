class_name PioneerStage3D
extends Node3D

const UI = preload("res://scripts/interface.gd")
const WIDTH = 18.0
var room = "terminal"
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

func configure(value: String) -> void:
	room = value
	inspection = false
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
	if geography: geography.queue_free()
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
	var spec = {"terminal":[1.05,-1.8,"BOARDING GALLERY"],"launch":[.48,-1.3,"FLIGHT ACCESS"],"habitation":[.62,-1.4,"CREW QUARTERS"],"recreation":[0.0,-2.1,"OBSERVATION LOUNGE"],"corridor":[.65,-1.5,"SERVICE WALKWAY"],"restricted":[.65,-1.5,"SECURITY LANDING"],"bridge":[.72,-1.55,"OBSERVATION GALLERY"],"k17":[.72,-1.55,"INSTRUMENT GALLERY"]}.get(room,[.65,-1.5,"UPPER WALKWAY"])
	route_rise = spec[0]
	route_depth = spec[1]
	route_name = spec[2]
	route_end = 10.0
	_gallery()
	_make_device()
	_room_subjects()

func _gallery() -> void:
	_box(geography,Vector3(14,route_rise-.07,route_depth),Vector3(8,.14,1.3),flooring)
	_box(geography,Vector3(14,route_rise-.19,route_depth),Vector3(8,.10,1.35),metal)
	_box(geography,Vector3(14,route_rise-.20,route_depth+.69),Vector3(7.8,.018,.02),amber)
	var a = Vector3(6.2,0,0)
	var b = Vector3(10,route_rise,route_depth)
	if route_rise>.1:
		for z in [-.48,.48]:_tube(geography,a+Vector3(0,-.10,z),b+Vector3(0,-.10,z),.035,metal)
		for x in [11.0,14.0,17.0]:
			_box(geography,Vector3(x,route_rise*.45,route_depth),Vector3(.085,route_rise*.9,.55),metal)
	for i in range(20):
		var t = (i+.5)/20.0
		var point = a.lerp(b,t)
		_box(geography,point-Vector3(0,.045,0),Vector3(.203,.09,1.28),flooring)
		_box(geography,point+Vector3(.098,.003,0),Vector3(.014,.006,1.28),metal)
	for z in [-.65,.65]:
		var offset = Vector3(0,.77,z)
		_tube(geography,a+offset,b+offset,.016,paint)
		for i in range(9):
			var point = a.lerp(b,i/8.0)+Vector3(0,0,z)
			_tube(geography,point,point+Vector3(0,.77,0),.012,metal)
	for z in [route_depth-.64,route_depth+.64]:
		_tube(geography,Vector3(10,route_rise+.77,z),Vector3(18,route_rise+.77,z),.016,paint)
		for i in range(12):
			var point = Vector3(10+i*.70,route_rise,z)
			_tube(geography,point,point+Vector3(0,.77,0),.012,metal)
	var marker = MeshInstance3D.new()
	var arrow = ImmediateMesh.new()
	arrow.surface_begin(Mesh.PRIMITIVE_TRIANGLES,amber)
	for p in [Vector3(-.16,0,.12),Vector3(.16,0,.12),Vector3(0,0,-.18)]:arrow.surface_add_vertex(p)
	arrow.surface_end()
	marker.mesh=arrow
	marker.position=Vector3(6.2,.012,.30)
	geography.add_child(marker)

func floor_point(x: float, upper: bool) -> Vector3:
	if not upper: return Vector3(x,0,0)
	var t = clampf((x-6.2)/3.8,0,1)
	return Vector3(x,t*route_rise,t*route_depth)

func add_actor(id: String, is_npc: bool = false) -> CinematicAvatar:
	var actor = CinematicAvatar.new()
	add_child(actor)
	actor.setup(id,is_npc)
	if is_npc: people[id] = actor
	else: actors.append(actor)
	return actor

func _make_device() -> void:
	devices = Node3D.new()
	geography.add_child(devices)
	var y = route_rise
	var z = route_depth-.6
	_box(devices,Vector3(12.4,y+.7,z-.12),Vector3(.72,1.4,.44),metal)
	_box(devices,Vector3(12.4,y+1.28,z),Vector3(2.12,1.52,.19),metal)
	_box(devices,Vector3(12.4,y+1.28,z+.105),Vector3(2.01,1.39,.025),paint)
	_box(devices,Vector3(12.4,y+.48,z+.15),Vector3(1.30,.08,.55),paint)
	for x in [11.39,13.41]:_box(devices,Vector3(x,y+1.29,z+.13),Vector3(.012,1.26,.012),cyan)
	screen_center = Vector3(12.4,y+1.28,z+.14)
	screen_view = SubViewport.new()
	screen_view.size = Vector2i(1280,800)
	screen_view.render_target_update_mode = SubViewport.UPDATE_ONCE
	devices.add_child(screen_view)
	screen_ui = Control.new()
	screen_ui.theme = UI.theme()
	screen_ui.size = Vector2(1280,800)
	screen_view.add_child(screen_ui)
	var quad = MeshInstance3D.new()
	var mesh = QuadMesh.new()
	mesh.size = Vector2(1.94,1.2125)
	quad.mesh = mesh
	var mat = StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.albedo_texture = screen_view.get_texture()
	quad.material_override = mat
	quad.position = screen_center
	devices.add_child(quad)
	show_clue({"title":"Pioneer Initiative","tag":"CSV-01 / BOARDING GALLERY","fields":[["DESTINATION","Asteria-4"],["COHORT","01"],["STATUS","READY TO BOARD"]],"note":"People. Worlds. Possibilities."})

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
					m.albedo_texture = load("res://assets/art/ship_alloy.png")
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
	subjects.append({"kind":kind,"node":node,"home":node.position,"phase":phase})

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
	match room:
		"terminal":
			_drone(Vector3(9.1,2.05,-.3))
			var shuttle = _prop("shuttle",Vector3(5.5,3.6,-4),.58)
			_moving("departure traffic",shuttle)
		"launch":
			orbit = Sprite3D.new()
			orbit.texture = load("res://assets/art/launch_orbit.png")
			orbit.pixel_size = WIDTH/orbit.texture.get_width()
			orbit.position = background.position+Vector3(0,0,.01)
			orbit.billboard = BaseMaterial3D.BILLBOARD_ENABLED
			orbit.shaded = false
			orbit.modulate.a = 0
			geography.add_child(orbit)
			pen = Node3D.new()
			pen.position = Vector3(9,1.65,.15)
			geography.add_child(pen)
			_tube(pen,Vector3(0,-.12,0),Vector3(0,.12,0),.012,paint)
			_tube(pen,Vector3(0,.05,0),Vector3(0,.13,0),.014,cyan)
			pen.visible = false
			_fan(Vector3(8.9,2.3,-1.0))
		"habitation":
			_plant(Vector3(7.2,0,.5),1.1)
			_plant(Vector3(15.2,route_rise,route_depth-.3),.9)
			_fan(Vector3(9.0,2.3,-.8))
		"recreation":
			var orrery = Node3D.new()
			orrery.position = Vector3(9.5,1.6,-1)
			geography.add_child(orrery)
			_box(geography,Vector3(9.5,.45,-1),Vector3(1.25,.9,.85),metal)
			_sphere(orrery,Vector3.ZERO,Vector3(.30,.30,.30),amber)
			for i in range(3):
				var ring = _ring(orrery,Vector3.ZERO,.35+i*.23,cyan)
				ring.rotation = Vector3(i*.28,0,i*.34)
				_sphere(ring,Vector3(.35+i*.23,0,0),Vector3(.08,.08,.08),paint)
				_moving("orrery orbit",ring,i*.8)
			_plant(Vector3(15.8,0,.3),1.2)
		"corridor", "restricted":
			var door = Vector3(9.7,1.1,-.85)
			_box(geography,door,Vector3(1.7,2.2,.18),metal)
			for x in [8.82,10.58]:
				_box(geography,Vector3(x,1.14,-.7),Vector3(.1,2.28,.18),paint)
				_box(geography,Vector3(x,1.14,-.59),Vector3(.02,1.96,.02),amber)
			_fan(Vector3(9.4,2.45,-.4))
			if room == "corridor":
				m77 = _prop("m77",Vector3(8.75,0,-.10),.95)
				m77.rotation.y = 1.0
				for i in range(13):
					var spark = _sphere(geography,Vector3(9.6,.75,-.49),Vector3(.012,.012,.04),amber)
					sparks.append(spark)
				weld_light=OmniLight3D.new()
				weld_light.position=Vector3(9.58,.76,-.44)
				weld_light.light_color=Color("9bd8f5")
				weld_light.omni_range=1.2
				geography.add_child(weld_light)
				_drone(Vector3(9.4,2.1,-.5))
				_drone(Vector3(14.4,2.25,-.9))
		"bridge", "k17":
			var mount = Vector3(9.7,1.9,-2.6)
			_box(geography,mount-Vector3(0,.8,0),Vector3(.22,1.4,.22),metal)
			var instrument = Node3D.new()
			geography.add_child(instrument)
			instrument.position = mount
			_sphere(instrument,Vector3.ZERO,Vector3(.28,.28,.28),metal)
			for i in range(3):
				var ring = _ring(instrument,Vector3.ZERO,.38+i*.1,paint if i==0 else cyan)
				ring.rotation.z = i*.8
				_moving("navigation gimbal",ring,i*.7)
			_lensing_geometry()
	# A projected ship interface has actual intersecting rings and a solid emitter.
	iris = Node3D.new()
	iris.position = Vector3(15.7,route_rise+.9,route_depth-.15)
	geography.add_child(iris)
	_box(geography,iris.position-Vector3(0,.85,0),Vector3(.42,.14,.42),metal)
	for i in range(4):
		var ring = _ring(iris,Vector3(0,i*.12,0),.18+sin(i*.8)*.07,cyan)
		_moving("Iris interface",ring,i*.6)

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

func animated_snapshot() -> Array:
	var result: Array = []
	for item in subjects:
		var n: Node3D = item.node
		result.append({"kind":item.kind,"x":n.position.x,"y":n.position.y,"z":n.position.z,"rotation":n.rotation.length()})
	for n in drones:result.append({"kind":"volumetric service drone","x":n.position.x,"y":n.position.y,"z":n.position.z,"rotation":n.rotation.length()})
	if m77: result.append({"kind":"articulated M-77","x":m77.position.x,"y":m77.position.y,"z":m77.position.z,"rotation":m77.rotation.length()})
	return result

func _process(delta: float) -> void:
	for actor in actors: actor.held=held
	for actor in people.values():actor.held=held
	if not held:
		clock += delta
		effect_time += delta
	var picture_delta = 0.0 if held else delta
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
			spark.position=Vector3(9.6,.75,-.49)+Vector3(sin(i*12.9)*t*.32,t*.32-t*t*.55,cos(i*4.7)*t*.16)
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
	var target = Vector3(view_x,2.36,0)
	if effect_camera_x>=0:target.x=effect_camera_x
	var destination = target+Vector3(0,2.62,14)
	if effect in ["rumble","ascent"] and not held:destination += Vector3(sin(clock*57)*.009,cos(clock*49)*.007,0)
	var size = 6.0
	if inspection:
		inspection_time += delta
		if inspection_time > .60:
			target = screen_center
			destination = target+Vector3(0,0,.4)
			size = 1.62
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
