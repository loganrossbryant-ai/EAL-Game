class_name PartyMember
extends CharacterBody2D

const STRIDE = 118.0
const STANCE = 0.61
var department = 0
var desired_speed = 0.0
var facing = 1.0
var selected = false
var attending = false
var breath = 0.0
var gait = 0.35
var motion_weight = 0.0
var lean = 0.0
var turn_time = 0.0
var turn_target = 1.0
var has_rig = false
var was_walking = false
var follow_side = 1.0
var feet: Array[Dictionary] = []
var puppet: CrewPuppet
var mirror: CrewPuppet
var walk_sprite: Sprite2D
var idle_sprite: Sprite2D
var visual: Node2D
var last_position = Vector2.ZERO
var render_puppet = true
signal footstep

func setup(index: int) -> void:
	department = index
	breath = index * 0.83
	collision_layer = 2
	collision_mask = 1
	var shape = CollisionShape2D.new()
	var capsule = CapsuleShape2D.new()
	capsule.radius = 15
	capsule.height = 175
	shape.shape = capsule
	shape.position.y = -88
	add_child(shape)
	visual = Node2D.new()
	add_child(visual)
	puppet = CrewPuppet.new()
	visual.add_child(puppet)
	has_rig = puppet.setup(index)
	mirror = CrewPuppet.new()
	mirror.scale.y = -0.32
	mirror.position.y = 1
	mirror.modulate = Color(0.6, 0.72, 0.8, 0.075)
	mirror.z_index = -8
	visual.add_child(mirror)
	if has_rig: mirror.setup(index)
	idle_sprite = Sprite2D.new()
	idle_sprite.texture = preload("res://assets/art/crew_idle.png")
	var standing = JSON.parse_string(FileAccess.get_file_as_string("res://assets/art/rigs/standing.json")).regions[index]
	idle_sprite.region_enabled = true
	idle_sprite.region_rect = Rect2(standing[0], standing[1], standing[2], standing[3])
	idle_sprite.scale = Vector2.ONE * (219.5 / float(standing[3]))
	idle_sprite.position.y = -109.75
	idle_sprite.modulate.a = 0
	add_child(idle_sprite)
	# Legacy observation/fallback only; hidden whenever the continuous rig exists.
	walk_sprite = Sprite2D.new()
	walk_sprite.texture = preload("res://assets/art/crew_walk.png")
	walk_sprite.hframes = 8
	walk_sprite.vframes = 4
	walk_sprite.frame = index * 8 + 2
	walk_sprite.scale = Vector2.ONE * 0.83
	walk_sprite.position.y = -98
	walk_sprite.visible = not has_rig
	add_child(walk_sprite)
	for i in range(2):
		feet.append({"world_x": 0.0, "height": 0.0, "start_x": 0.0, "target_x": 0.0, "stance": true, "phase": 0.0, "swing_start": STANCE, "contact": 0})

func reset_contacts() -> void:
	gait = fposmod(0.35 + department * 0.17, 1.0)
	for i in range(2):
		feet[i].world_x = global_position.x + (-7 if i == 0 else 8) * facing
		feet[i].start_x = feet[i].world_x
		feet[i].target_x = feet[i].world_x
		feet[i].height = 0.0
		feet[i].stance = true
		feet[i].contact += 1
	last_position = global_position

func _physics_process(delta: float) -> void:
	if global_position.distance_to(last_position) > 150 or last_position == Vector2.ZERO:
		reset_contacts()
	var target = desired_speed
	if absf(target) > 10 and signf(target) != facing and turn_time <= 0:
		if absf(velocity.x) > 12:
			target = 0
		else:
			turn_target = signf(target)
			turn_time = 0.20
	if turn_time > 0:
		turn_time = maxf(0, turn_time - delta)
		target = 0
		if turn_time < 0.10 and facing != turn_target:
			facing = turn_target
			reset_contacts()
	var acceleration = 430.0 if absf(target) > absf(velocity.x) else 640.0
	velocity.x = move_toward(velocity.x, target, acceleration * delta)
	velocity.y += 1000 * delta
	var old_x = global_position.x
	move_and_slide()
	var travel = absf(global_position.x - old_x)
	var walking = absf(velocity.x) >= 9 and turn_time <= 0
	if walking and not was_walking: reset_contacts()
	was_walking = walking
	breath += delta
	gait = fposmod(gait + travel / STRIDE, 1.0)
	motion_weight = move_toward(motion_weight, clampf(absf(velocity.x) / 85.0, 0, 1), delta * 6.0)
	lean = lerpf(lean, clampf(velocity.x / 145.0, -1, 1) * facing * 0.022, 1 - exp(-delta * 8))
	for i in range(2): _update_foot(i, delta)
	var near_foot = Vector2((feet[0].world_x - global_position.x) * facing, feet[0].height)
	var far_foot = Vector2((feet[1].world_x - global_position.x) * facing, feet[1].height)
	visual.scale.x = facing
	if has_rig and render_puppet:
		puppet.pose(near_foot, far_foot, gait, motion_weight, breath, lean)
		mirror.pose(near_foot, far_foot, gait, motion_weight, breath, lean)
	var turn_blend = sin(clampf(turn_time / 0.20, 0, 1) * PI) if turn_time > 0 else 0.0
	var front_target = maxf(turn_blend, 1.0 if attending and motion_weight < 0.05 else 0.0)
	idle_sprite.modulate.a = lerpf(idle_sprite.modulate.a, front_target, 1 - exp(-delta * 18))
	visual.modulate.a = 1.0 - idle_sprite.modulate.a
	idle_sprite.flip_h = facing < 0
	idle_sprite.position.y = -109.75 - sin(breath * 1.65) * 0.3
	walk_sprite.frame = department * 8 + int(gait * 8) % 8
	walk_sprite.flip_h = facing < 0
	last_position = global_position
	queue_redraw()

func _update_foot(index: int, delta: float) -> void:
	var foot = feet[index]
	var phase = fposmod(gait + index * 0.5, 1.0)
	if absf(velocity.x) < 9 or turn_time > 0:
		foot.world_x = lerpf(foot.world_x, global_position.x + (-7 if index == 0 else 8) * facing, 1 - exp(-delta * 12))
		foot.height = move_toward(foot.height, 0.0, delta * 65)
		foot.stance = true
		foot.phase = phase
		return
	var planted = phase < STANCE
	if planted:
		if not foot.stance:
			foot.world_x = foot.target_x
			foot.contact += 1
			footstep.emit()
		foot.height = 0.0
	else:
		if foot.stance:
			foot.start_x = foot.world_x
			foot.swing_start = phase
			foot.target_x = global_position.x + facing * ((1 - phase) * STRIDE + 32)
		var t = clampf((phase - float(foot.swing_start)) / maxf(0.01, 1 - float(foot.swing_start)), 0, 1)
		foot.world_x = lerpf(foot.start_x, foot.target_x, t * t * (3 - 2 * t))
		foot.height = -sin(t * PI) * 11.0
	foot.stance = planted
	foot.phase = phase

func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0, Vector2(1, 0.18))
	for i in range(5): draw_circle(Vector2.ZERO, 34 - i * 5, Color(0.01, 0.02, 0.03, 0.035))
	for foot in feet:
		var x = float(foot.world_x) - global_position.x
		draw_circle(Vector2(x, 0), 13, Color(0.01, 0.02, 0.03, 0.16 if foot.stance else 0.035))
	draw_set_transform(Vector2.ZERO)
	if selected:
		draw_arc(Vector2(0, 1), 24, 0.15, PI - 0.15, 20, Color(CrewState.COLORS[department], 0.75), 1.4, true)
