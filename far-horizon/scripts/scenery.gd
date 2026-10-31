class_name PioneerScenery
extends Node2D

var room = "terminal"
var world_width = 2304.0
var floor_y = 686.0
var clock = 0.0
var camera_x = 683.0
var effect = ""
var effect_time = 0.0
var art: Sprite2D
var orbit_plate: Sprite2D
var foreground: Sprite2D
var dust: Array[Vector3] = []

func _ready() -> void:
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
	configure(room)

func configure(value: String) -> void:
	room = value
	if not art:
		return
	var path = "res://assets/art/terminal.png"
	if room == "launch" and ResourceLoader.exists("res://assets/art/launch.png"):
		path = "res://assets/art/launch.png"
	elif room in ["bridge", "ending"] and ResourceLoader.exists("res://assets/art/bridge.png"):
		path = "res://assets/art/bridge.png"
	elif room == "habitation" and ResourceLoader.exists("res://assets/art/habitation.png"):
		path = "res://assets/art/habitation.png"
	art.texture = load(path)
	art.scale = Vector2(world_width / art.texture.get_width(), 768.0 / art.texture.get_height())
	art.position = Vector2.ZERO
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

func _process(delta: float) -> void:
	clock += delta
	effect_time += delta
	# Tiny independent drift on the far layer gives the camera a physical sense of depth.
	art.position.x = (camera_x - 1152.0) * 0.014
	orbit_plate.position = art.position
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
	if effect == "anomaly" and effect_time < 0.65:
		var alpha = sin(effect_time / 0.65 * PI) * 0.24
		for i in range(4):
			draw_arc(Vector2(1260 + i * 3, 260), 30 + i * 12, -1.5, 1.7, 30, Color(0.7, 0.87, 0.96, alpha / (i + 1)), 1, true)
