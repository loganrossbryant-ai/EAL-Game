class_name IslandActor
extends Node2D

var kind = "alan"
var clock = 0.0
var travel = 0.0
var speed = 0.0
var facing = 1.0
var body: Sprite2D
var left_leg: Sprite2D
var right_leg: Sprite2D
var carried_texture: Texture2D

func _ready() -> void:
	if kind == "pip":
		body = Sprite2D.new()
		body.texture = preload("res://assets/art/pip.png")
		body.scale = Vector2.ONE * 0.085
		body.position.y = -61
		add_child(body)
	elif kind == "mina":
		body = _piece(Rect2(950, 15, 390, 985), Vector2(0, -120), 0.245)
	else:
		# Separate leg cutouts swing continuously; the upper body has a small gait sway.
		left_leg = _piece(Rect2(240, 788, 135, 212), Vector2(-14, -26), 0.245)
		right_leg = _piece(Rect2(385, 788, 170, 210), Vector2(17, -26), 0.245)
		body = _piece(Rect2(235, 230, 320, 568), Vector2(0, -120), 0.245)
	queue_redraw()

func _piece(region: Rect2, at: Vector2, factor: float) -> Sprite2D:
	var sprite = Sprite2D.new()
	var atlas = AtlasTexture.new()
	atlas.atlas = preload("res://assets/art/characters.png")
	atlas.region = region
	sprite.texture = atlas
	sprite.scale = Vector2.ONE * factor
	sprite.position = at
	add_child(sprite)
	return sprite

func _process(delta: float) -> void:
	clock += delta
	travel += speed * delta * 0.048
	var weight = clampf(speed / 230.0, 0, 1)
	if kind == "alan":
		body.position.y = -120 - absf(sin(travel)) * 2.3 * weight - sin(clock * 1.6) * 0.45
		body.rotation = sin(travel) * 0.018 * weight
		left_leg.position = Vector2(-14, -26 - maxf(0, sin(travel)) * 8 * weight)
		right_leg.position = Vector2(17, -26 - maxf(0, -sin(travel)) * 8 * weight)
		left_leg.rotation = sin(travel) * 0.12 * weight
		right_leg.rotation = -sin(travel) * 0.12 * weight
		for sprite in [body, left_leg, right_leg]: sprite.flip_h = facing < 0
	elif kind == "pip":
		body.position.y = -61 + sin(clock * 2.4) * 5
		body.rotation = sin(clock * 1.4) * 0.025
	else:
		body.scale.y = 0.245 + sin(clock * 1.8) * 0.001
	queue_redraw()

func _draw() -> void:
	draw_set_transform(Vector2.ZERO, 0, Vector2(1, 0.24))
	draw_circle(Vector2.ZERO, 34 if kind != "pip" else 28, Color(0.17, 0.21, 0.15, 0.24), true, -1, true)
	draw_set_transform(Vector2.ZERO)
	if carried_texture:
		draw_circle(Vector2(48, -87), 34, Color("fff9e8"), true, -1, true)
		draw_texture_rect(carried_texture, Rect2(17, -118, 62, 62), false)
