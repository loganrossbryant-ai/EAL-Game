class_name IslandScenery
extends Node2D

var clock = 0.0
var festival = false
var delivered = false
var confetti = 0.0
var meal_texture: Texture2D
var album_texture: Texture2D

func _ready() -> void:
	var art = Sprite2D.new()
	art.texture = preload("res://assets/art/cafe.png")
	art.centered = false
	art.scale = Vector2(1440.0 / 1536, 960.0 / 1024)
	art.z_index = -10
	add_child(art)

func _process(delta: float) -> void:
	clock += delta
	confetti = maxf(confetti - delta, 0)
	queue_redraw()

func _draw() -> void:
	# Tiny sea sparkles, wind-borne petals and steam have independent motion.
	for i in range(24):
		var point = Vector2(25 + fposmod(i * 47.0, 700), 133 + fposmod(i * 13.0, 53))
		var alpha = pow(maxf(0, sin(clock * 1.8 + i * 2.4)), 6) * 0.65
		draw_line(point - Vector2(2, 0), point + Vector2(3, 0), Color(1, 1, 0.9, alpha), 1, true)
	for i in range(8):
		var p = Vector2(160 + fposmod(i * 147.0 + clock * 14, 1160), 400 + fposmod(i * 71.0 + clock * 7, 260))
		draw_circle(p, 2, Color(1, 0.79, 0.66, 0.45), true, -1, true)
	if delivered or festival:
		for i in range(12):
			var x = 252.0 + i * 18
			var y = 145 + sin(float(i) / 11 * PI) * 27
			draw_line(Vector2(x, y), Vector2(x + 18, 145 + sin(float(i + 1) / 11 * PI) * 27), Color("83613b"), 2)
			var points = PackedVector2Array([Vector2(x, y), Vector2(x + 15, y + 1), Vector2(x + 9 + sin(clock * 2 + i) * 2, y + 24)])
			draw_colored_polygon(points, [Color("54a5a0"), Color("f5bd51"), Color("ed9274")][i % 3])
		if meal_texture:
			draw_texture_rect(meal_texture, Rect2(305, 195, 58, 54), false)
	if festival:
		if album_texture: draw_texture_rect(album_texture, Rect2(369, 197, 53, 50), false)
		for i in range(8):
			var x = 258.0 + i * 26
			var y = 123 + sin(float(i) / 7 * PI) * 11
			draw_circle(Vector2(x, y), 4, Color(1, 0.9, 0.47, 0.85 + sin(clock * 1.2 + i) * 0.15), true, -1, true)
		for i in range(3):
			var p = Vector2(271 + i * 27 + sin(clock + i) * 5, 230 - i * 16)
			draw_line(p, Vector2(294, 287), Color("b79564"), 1.5, true)
			_ellipse(Rect2(p - Vector2(13, 18), Vector2(26, 34)), [Color("f1b94d"), Color("6abbb1"), Color("ed8e74")][i])
	if confetti > 0:
		for i in range(60):
			var p = Vector2(fposmod(i * 97.0 + sin(clock + i) * 60, 1440), fposmod(i * 43.0 + clock * 130, 960))
			draw_set_transform(p, clock * 2 + i)
			draw_rect(Rect2(-4, -2, 8, 4), [Color("f7d071"), Color("6abbb1"), Color("f29178")][i % 3])
			draw_set_transform(Vector2.ZERO)

func _ellipse(rect: Rect2, color: Color) -> void:
	draw_set_transform(rect.get_center(), 0, rect.size * 0.5)
	draw_circle(Vector2.ZERO, 1, color, true, -1, true)
	draw_set_transform(Vector2.ZERO)
