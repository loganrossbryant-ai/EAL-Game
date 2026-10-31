class_name PartyMember
extends CharacterBody2D

var department = 0
var desired_speed = 0.0
var facing = 1.0
var selected = false
var walking_time = 0.0
var breath = 0.0
var turn_left = 0.0
var walk_sprite: Sprite2D
var idle_sprite: Sprite2D
var reflection: Sprite2D
var attending = false
var height_scale = 0.83
var step_distance = 0.0
signal footstep

func setup(index: int) -> void:
	department = index
	collision_layer = 2
	collision_mask = 1
	var shape = CollisionShape2D.new()
	var capsule = CapsuleShape2D.new()
	capsule.radius = 15
	capsule.height = 175
	shape.shape = capsule
	shape.position.y = -88
	add_child(shape)
	walk_sprite = Sprite2D.new()
	walk_sprite.texture = preload("res://assets/art/crew_walk.png")
	walk_sprite.hframes = 8
	walk_sprite.vframes = 4
	walk_sprite.position.y = -104
	walk_sprite.scale = Vector2.ONE * height_scale
	add_child(walk_sprite)
	if ResourceLoader.exists("res://assets/art/crew_idle.png"):
		idle_sprite = Sprite2D.new()
		idle_sprite.texture = load("res://assets/art/crew_idle.png")
		idle_sprite.hframes = 4
		idle_sprite.vframes = 2
		idle_sprite.scale = Vector2.ONE * 0.43
		idle_sprite.position.y = -108
		idle_sprite.frame = department
		add_child(idle_sprite)
	reflection = Sprite2D.new()
	reflection.texture = walk_sprite.texture
	reflection.hframes = 8
	reflection.vframes = 4
	reflection.flip_v = true
	reflection.modulate = Color(0.55, 0.71, 0.79, 0.09)
	reflection.z_index = -1
	add_child(reflection)
	set_anim(0)

func _physics_process(delta: float) -> void:
	velocity.x = move_toward(velocity.x, desired_speed, (700 if absf(desired_speed) > 0 else 1050) * delta)
	velocity.y += 1000 * delta
	var old_x = position.x
	move_and_slide()
	step_distance += absf(position.x - old_x)
	if step_distance > 65:
		step_distance = 0
		footstep.emit()
	breath += delta
	if absf(velocity.x) > 4:
		if signf(velocity.x) != facing:
			turn_left = 0.14
		facing = signf(velocity.x)
		walking_time += absf(velocity.x) * delta / 152.0
	else:
		walking_time = 0.0
	turn_left = maxf(0, turn_left - delta)
	set_anim(delta)
	queue_redraw()

func set_anim(_delta: float) -> void:
	if not walk_sprite:
		return
	var moving = absf(velocity.x) > 8
	var frame_index = int(walking_time * 10.0) % 8 if moving else 2
	walk_sprite.frame = department * 8 + frame_index
	walk_sprite.flip_h = facing < 0
	walk_sprite.position.y = -98.0 - (0.0 if moving else sin(breath * 1.7 + department) * 0.7)
	# Brief compression marks the change of weight when a character reverses direction.
	walk_sprite.scale.x = height_scale * (0.82 if turn_left > 0 else 1.0)
	if idle_sprite:
		idle_sprite.visible = not moving or turn_left > 0
		walk_sprite.visible = moving and turn_left <= 0
		idle_sprite.flip_h = facing < 0
		idle_sprite.position.y = -103.0 - sin(breath * 1.7 + department) * 0.7
		idle_sprite.frame = department + (4 if turn_left > 0 or attending else 0)
	if reflection:
		var source = idle_sprite if idle_sprite and idle_sprite.visible else walk_sprite
		reflection.texture = source.texture
		reflection.hframes = source.hframes
		reflection.vframes = source.vframes
		reflection.frame = source.frame
		reflection.flip_h = source.flip_h
		reflection.scale = Vector2(source.scale.x, source.scale.y * 0.4)
		reflection.position.y = -source.position.y * 0.4

func _draw() -> void:
	# Layered contact shadows anchor each actor to the actual collision floor.
	for i in range(6):
		draw_set_transform(Vector2.ZERO, 0, Vector2(1.0, 0.19))
		draw_circle(Vector2.ZERO, 40.0 - i * 5.0, Color(0.012, 0.022, 0.03, 0.035 + i * 0.008))
	draw_set_transform(Vector2.ZERO)
	if selected:
		draw_arc(Vector2(0, 1), 24, 0.15, PI - 0.15, 20, Color(CrewState.COLORS[department], 0.8), 1.5, true)
