class_name PioneerProps
extends Node2D

# Independent world actors. Their clocks stop with the GM's picture-hold control.
var room = "terminal"
var clock = 0.0
var effect = ""
var effect_time = 0.0
var actors: Array[Dictionary] = []
var drone_texture = load("res://assets/art/utility_drone.png")
var ship_texture = load("res://assets/art/shuttle.png")
var unit_texture = load("res://assets/art/m77.png")

func configure(value: String) -> void:
	room = value
	for child in get_children(): child.queue_free()
	actors.clear()
	if room == "terminal":
		var glass = Polygon2D.new()
		glass.polygon = PackedVector2Array([Vector2(525,112),Vector2(1670,112),Vector2(1670,175),Vector2(525,248)])
		glass.clip_children = CanvasItem.CLIP_CHILDREN_ONLY
		add_child(glass)
		_add("shuttle", ship_texture, Vector2(890,178), 205, glass)
		_add("drone", drone_texture, Vector2(1190,411), 126)
	elif room == "launch":
		_add("drone", drone_texture, Vector2(1110,359), 100)
	elif room == "habitation":
		_add("drone", drone_texture, Vector2(1130,401), 116)
	elif room == "recreation":
		_add("orrery", null, Vector2(1195,351), 76)
	elif room in ["corridor", "restricted"]:
		if room == "corridor":
			_add("m77", unit_texture, Vector2(1040,686), 257)
			_add("minor1", drone_texture, Vector2(650,416), 92)
			_add("minor2", drone_texture, Vector2(1670,403), 92)
		else:
			_add("drone", drone_texture, Vector2(1190,389), 105)
	elif room in ["bridge", "k17"]:
		_add("drone", drone_texture, Vector2(1160,377), 89)
	update_picture()

func _add(kind: String, texture: Texture2D, point: Vector2, width: float, parent: Node = self) -> void:
	var sprite = Sprite2D.new()
	sprite.texture = texture
	if texture:sprite.scale = Vector2.ONE * width / texture.get_width()
	if kind == "m77": sprite.offset.y = -texture.get_height() * 0.5
	parent.add_child(sprite)
	actors.append({"kind":kind,"sprite":sprite,"base":point,"width":width})

func update_picture() -> void:
	for actor in actors:
		var sprite: Sprite2D = actor.sprite
		var base: Vector2 = actor.base
		var kind: String = actor.kind
		if kind == "shuttle":
			var phase = fposmod(clock / 32.0, 1)
			sprite.position = Vector2(565 + phase * 1070, 173 - sin(phase * PI) * 18)
			sprite.rotation = -0.018
		elif kind == "orrery":
			sprite.position = base + Vector2(0,sin(clock * 0.8) * 2.5)
			sprite.rotation = clock * 0.45
		elif kind == "m77":
			var travel = sin(clock * 0.16) * 26 if effect != "contained" else 0.0
			sprite.position = base + Vector2(travel, 0)
			sprite.rotation = sin(clock * 0.8) * 0.002 if effect != "contained" else 0.0
			sprite.modulate = Color(0.65,0.72,0.75) if effect == "contained" else Color.WHITE
		else:
			var phase = base.x * 0.01
			var radius = 21.0 if kind.begins_with("minor") else 57.0
			sprite.position = base + Vector2(sin(clock * 0.24 + phase) * radius, sin(clock * 1.17 + phase) * 6)
			sprite.rotation = sin(clock * 0.73 + phase) * 0.026
			sprite.modulate = Color(0.55,0.65,0.68) if effect == "contained" and kind.begins_with("minor") else Color.WHITE
	queue_redraw()

func _draw() -> void:
	for actor in actors:
		if actor.kind == "shuttle": continue
		var sprite: Sprite2D = actor.sprite
		var point = sprite.position
		if actor.kind == "orrery":
			_orrery(point,sprite.rotation)
			continue
		# Soft contact/hover shadows anchor the subjects to the scenic floor.
		var shadow_y = 686.0 if actor.kind == "m77" else 655.0
		draw_set_transform(Vector2(point.x,shadow_y),0,Vector2(1,0.12))
		for i in range(7): draw_circle(Vector2.ZERO, actor.width * (0.25 + i * 0.028),Color(0.005,0.013,0.019,0.034),true,-1,true)
		draw_set_transform(Vector2.ZERO)
		if actor.kind != "m77":
			var radius = actor.width * 0.022
			var light = point + Vector2(actor.width * 0.2, -actor.width * 0.01)
			for i in range(4): draw_circle(light, radius + i * 1.7,Color(0.28,0.86,1,0.11 / (i + 1)),true,-1,true)
	if room == "corridor" and effect in ["weld","round1","round2","round3"]:
		var origin = Vector2(642,435) if effect in ["weld","round1"] else Vector2(1687,403)
		var target = Vector2(670,426) if effect in ["weld","round1"] else Vector2(1651,354)
		var pulse = 0.65 + 0.35 * sin(clock * 47)
		draw_line(origin,target,Color(0.25,0.78,1,0.4),7,true)
		draw_line(origin,target,Color(0.88,0.97,1,pulse),1.8,true)
		for i in range(12):
			var age = fposmod(clock * 1.8 + i / 12.0,1)
			var angle = -2.7 + i * 0.27
			var p = target + Vector2.from_angle(angle) * age * 58 + Vector2(0,age * age * 70)
			draw_line(p,p - Vector2.from_angle(angle) * 4,Color(1,0.62 + 0.3 * (1-age),0.25,1-age),1.6,true)
		for i in range(4): draw_circle(target,3 + i * 5,Color(0.5,0.8,1,pulse * 0.12 / (i+1)),true,-1,true)
	if room == "restricted":
		var alpha = 0.35 + sin(clock * 1.3) * 0.12
		draw_line(Vector2(1760,315),Vector2(1760,613),Color(1,0.28,0.15,alpha),2,true)
		draw_line(Vector2(1780,315),Vector2(1780,613),Color(1,0.28,0.15,alpha * 0.5),1,true)

func _orrery(center: Vector2, angle: float) -> void:
	# A recreational tabletop star model, suspended above the pool-table end.
	var base = Vector2(center.x,420)
	draw_colored_polygon(PackedVector2Array([base + Vector2(-8,0),base + Vector2(8,0),center + Vector2(29,0),center + Vector2(-29,0)]),Color(0.26,0.79,1,0.035))
	draw_set_transform(base,0,Vector2(1,0.2))
	draw_circle(Vector2.ZERO,12,Color(0.4,0.86,1,0.48),false,1.4,true)
	draw_set_transform(Vector2.ZERO)
	draw_circle(center,32,Color(0.2,0.7,1,0.055),true,-1,true)
	for i in range(-2,3):
		var latitude = float(i) * 0.34
		var radius = sqrt(1 - latitude * latitude) * 31
		var points = PackedVector2Array()
		for j in range(49):
			var phase = j / 48.0 * TAU
			points.append(center + Vector2(cos(phase) * radius,latitude * 28 + sin(phase) * radius * 0.27))
		draw_polyline(points,Color(0.42,0.84,1,0.29),0.85,true)
	for i in range(5):
		var turn = angle + i / 5.0 * PI
		var points = PackedVector2Array()
		for j in range(49):
			var phase = j / 48.0 * TAU
			points.append(center + Vector2(cos(phase) * cos(turn) * 31,sin(phase) * 29 + cos(phase) * sin(turn) * 8))
		draw_polyline(points,Color(0.53,0.89,1,0.39),0.85,true)
	for i in range(3):
		var phase = angle * (1 + i * 0.37) + i * 2.1
		var radius = 44 + i * 8
		var points = PackedVector2Array()
		for j in range(65):
			var arc = j / 64.0 * TAU
			points.append(center + Vector2(cos(arc) * radius,sin(arc) * radius * 0.37).rotated(-0.25))
		draw_polyline(points,Color(0.66,0.86,1,0.18),0.7,true)
		var moon = center + Vector2(cos(phase) * radius,sin(phase) * radius * 0.37).rotated(-0.25)
		draw_circle(moon,2.2,Color(1,0.82,0.52,0.85),true,-1,true)
