class_name PioneerScenery
extends Node2D

var rendering_enabled = true

var room = "terminal"
var world_width = 2304.0
var floor_y = 686.0
var clock = 0.0
var camera_x = 683.0
var effect = ""
var effect_time = 0.0
var animating = true
var art: Sprite2D
var orbit_plate: Sprite2D
var foreground: Sprite2D
var dust: Array[Vector3] = []
var living: PioneerLivingDetails
var props: PioneerProps
var moving_sky: Array[Polygon2D] = []
var plants: Array[Polygon2D] = []

func _ready() -> void:
	if not rendering_enabled:
		set_process(false)
		return
	var rng = RandomNumberGenerator.new()
	rng.seed = 2247
	for i in range(44):
		dust.append(Vector3(rng.randf_range(0, 2400), rng.randf_range(100, 640), rng.randf_range(0.5, 1.8)))
	art = Sprite2D.new()
	art.centered = false
	add_child(art)
	art.z_index = -15
	orbit_plate = Sprite2D.new()
	orbit_plate.centered = false
	orbit_plate.z_index = -14
	orbit_plate.visible = false
	add_child(orbit_plate)
	living = PioneerLivingDetails.new()
	living.z_index = -10
	living.scale = Vector2(world_width / 2172.0, 768.0 / 724.0)
	add_child(living)
	props = PioneerProps.new()
	props.z_index = 2
	add_child(props)
	configure(room)

func configure(value: String) -> void:
	room = value
	if not art:
		return
	var plate = "corridor" if room == "restricted" else room
	var path = "res://assets/art/" + plate + ".png"
	if not ResourceLoader.exists(path): path = "res://assets/art/terminal.png"
	art.texture = load(path)
	art.scale = Vector2(world_width / art.texture.get_width(), 768.0 / art.texture.get_height())
	art.position = Vector2.ZERO
	for item in moving_sky: item.queue_free()
	for item in plants: item.queue_free()
	moving_sky.clear()
	plants.clear()
	living.configure(room)
	props.configure(room)
	if room == "terminal":
		_sky_patch(PackedVector2Array([Vector2(489, 103), Vector2(652, 103), Vector2(652, 233), Vector2(489, 233)]), 0.24)
		_sky_patch(PackedVector2Array([Vector2(716, 103), Vector2(1012, 103), Vector2(1012, 238), Vector2(716, 238)]), 0.24)
		_sky_patch(PackedVector2Array([Vector2(1070, 103), Vector2(1577, 103), Vector2(1577, 163), Vector2(1070, 205)]), 0.20)
		_plant(Vector2(82, 753), 0.19, 0.0)
		_plant(Vector2(2290, 755), 0.17, 2.0)
	elif room == "habitation":
		_plant(Vector2(105, 756), 0.20, 0.4)
		_plant(Vector2(2035, 756), 0.18, 2.4)
	elif room == "recreation":
		_plant(Vector2(2170, 760), 0.16, 1.3)
	elif room == "launch":
		_sky_patch(PackedVector2Array([Vector2(517, 105), Vector2(790, 105), Vector2(790, 236), Vector2(505, 246)]), 0.14)
		_sky_patch(PackedVector2Array([Vector2(853, 105), Vector2(1150, 105), Vector2(1150, 230), Vector2(853, 230)]), 0.13)
	if foreground:
		foreground.queue_free()
	foreground = Sprite2D.new()
	var floor_trim = AtlasTexture.new()
	floor_trim.atlas = art.texture
	floor_trim.region = Rect2(0, art.texture.get_height() - 22, art.texture.get_width(), 22)
	foreground.texture = floor_trim
	foreground.centered = false
	foreground.scale = Vector2((world_width + 90) / art.texture.get_width(), 1.25)
	foreground.position = Vector2(-40, 746)
	foreground.z_index = 20
	add_child(foreground)
	orbit_plate.visible = room == "launch" and ResourceLoader.exists("res://assets/art/launch_orbit.png")
	if orbit_plate.visible:
		orbit_plate.texture = load("res://assets/art/launch_orbit.png")
		orbit_plate.scale = Vector2(world_width / orbit_plate.texture.get_width(), 768.0 / orbit_plate.texture.get_height())
	orbit_plate.modulate.a = 0
	queue_redraw()

func _sky_patch(points: PackedVector2Array, strength: float) -> void:
	var cloud = Polygon2D.new()
	cloud.polygon = points
	cloud.scale = Vector2(world_width / 2172.0, 768.0 / 724.0)
	cloud.z_index = -11
	var material = ShaderMaterial.new()
	material.shader = preload("res://shaders/sky_motion.gdshader")
	material.set_shader_parameter("strength", strength)
	var bounds = Rect2(points[0], Vector2.ZERO)
	for point in points: bounds = bounds.expand(point)
	material.set_shader_parameter("mask_bounds", Vector4(bounds.position.x, bounds.position.y, bounds.end.x, bounds.end.y))
	cloud.material = material
	add_child(cloud)
	moving_sky.append(cloud)

func _plant(point: Vector2, size: float, phase: float) -> void:
	var plant = Polygon2D.new()
	plant.texture = preload("res://assets/art/foreground_plant.png")
	var w = float(plant.texture.get_width())
	var h = float(plant.texture.get_height())
	var vertices = PackedVector2Array()
	var uv = PackedVector2Array()
	var cells: Array[PackedInt32Array] = []
	for y in range(17):
		for x in range(9):
			var pixel = Vector2(w * x / 8, h * y / 16)
			vertices.append(pixel - Vector2(w / 2, h))
			uv.append(pixel)
	for y in range(16):
		for x in range(8):
			var i = y * 9 + x
			cells.append(PackedInt32Array([i, i + 1, i + 10, i + 9]))
	plant.polygon = vertices
	plant.uv = uv
	plant.polygons = cells
	plant.position = point
	plant.scale = Vector2.ONE * size
	plant.z_index = 22
	var material = ShaderMaterial.new()
	material.shader = preload("res://shaders/leaf_wind.gdshader")
	material.set_shader_parameter("phase", phase)
	plant.material = material
	add_child(plant)
	plants.append(plant)

func _process(delta: float) -> void:
	if not animating: delta = 0
	clock += delta
	effect_time += delta
	# Tiny independent drift on the far layer gives the camera a physical sense of depth.
	art.position.x = (camera_x - 1152.0) * 0.014
	orbit_plate.position = art.position
	living.position = art.position
	living.clock = clock
	living.effect = effect
	living.orbital = orbit_plate.visible and orbit_plate.modulate.a > 0.8
	living.queue_redraw()
	props.clock = clock
	props.effect = effect
	props.effect_time = effect_time
	props.update_picture()
	for cloud in moving_sky:
		cloud.position = art.position
		cloud.material.set_shader_parameter("clock", clock)
		cloud.modulate.a = 1.0 - orbit_plate.modulate.a if room == "launch" else 1.0
	for plant in plants:
		plant.material.set_shader_parameter("clock", clock)
		plant.offset.x = -(camera_x - 1152) * 0.055
	if foreground:
		foreground.position.x = -40 - (camera_x - 1152) * 0.055
	if orbit_plate.visible:
		var target_alpha = 1.0 if effect in ["ascent", "float"] else 0.0
		orbit_plate.modulate.a = move_toward(orbit_plate.modulate.a, target_alpha, delta * 0.45)
	queue_redraw()

func _draw() -> void:
	if not art:
		return
	# Atmospheric light pools, independently animated from the scenic painting.
	for p in dust:
		var px = fposmod(p.x + clock * (2.0 + p.z * 2), world_width)
		var py = p.y + sin(clock * 0.28 + p.x) * 8
		draw_circle(Vector2(px, py), p.z * 0.65, Color(0.9, 0.94, 0.9, 0.14), false, 0.8, true)
	if room == "terminal":
		var light = PackedVector2Array([Vector2(390, 120), Vector2(450, 120), Vector2(1120, 690), Vector2(690, 690)])
		draw_colored_polygon(light, Color(1, 0.85, 0.61, 0.025 + sin(clock * 0.15) * 0.005))
		# Boarding threshold is an actual world-space strip at the door, not a HUD button.
		draw_line(Vector2(2150, 669), Vector2(2240, 698), Color("e9b86d"), 4, true)
		draw_line(Vector2(2150, 676), Vector2(2240, 705), Color(0.8, 0.92, 0.94, 0.32), 1, true)
	if effect == "float":
		var pen = Vector2(910 + sin(clock * 0.6) * 10, 472 - minf(effect_time, 9) * 10)
		draw_set_transform(pen, -0.5 + clock * 0.09)
		draw_line(Vector2(-2, -24), Vector2(2, 24), Color("c9d9df"), 4, true)
		draw_line(Vector2(-2, -24), Vector2(0, -14), Color("5dbfd2"), 5, true)
		draw_set_transform(Vector2.ZERO)
	if effect in ["seed", "recurrence"]:
		var duration = 0.65 if effect == "seed" else 1.65
		if effect_time < duration:
			var alpha = sin(effect_time / duration * PI) * 0.68
			# A fleeting, asymmetric lens caustic; never a confirmed person or creature.
			var center = Vector2(1255, 277)
			for i in range(5):
				draw_arc(center + Vector2(i * 3, i * 5), 26 + i * 13, -1.38, 1.25, 40, Color(0.7, 0.87, 0.96, alpha / (i + 1)), 1.6, true)
			var caustic = PackedVector2Array([center + Vector2(-7,-49),center + Vector2(-20,-14),center + Vector2(10,19),center + Vector2(-3,70)])
			draw_polyline(caustic, Color(0.88,0.94,1,alpha * 0.65), 2.2, true)
