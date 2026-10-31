class_name PioneerLivingDetails
extends Node2D

var room = "terminal"
var clock = 0.0
var effect = ""
var orbital = false
var stars: Array[Vector3] = []
var soft: GradientTexture2D
var windows: Array[PackedVector2Array] = []

func _ready() -> void:
	var rng = RandomNumberGenerator.new()
	rng.seed = 2412247
	for i in range(135): stars.append(Vector3(rng.randf_range(180, 1980), rng.randf_range(95, 405), rng.randf_range(0.4, 1.0)))
	soft = GradientTexture2D.new()
	soft.width = 64
	soft.height = 64
	soft.fill = GradientTexture2D.FILL_RADIAL
	soft.fill_from = Vector2(0.5, 0.5)
	soft.fill_to = Vector2(1.0, 0.5)
	var gradient = Gradient.new()
	gradient.set_color(0, Color(1, 1, 1, 0.7))
	gradient.set_color(1, Color(1, 1, 1, 0))
	soft.gradient = gradient

func configure(value: String) -> void:
	room = value
	windows.clear()
	if room in ["bridge", "ending"]:
		windows = [PackedVector2Array([Vector2(854, 112), Vector2(1312, 112), Vector2(1357, 402), Vector2(813, 402)]), PackedVector2Array([Vector2(1380, 120), Vector2(1775, 109), Vector2(1875, 400), Vector2(1420, 400)]), PackedVector2Array([Vector2(1855, 108), Vector2(1965, 108), Vector2(1907, 330)])]
	elif room == "launch":
		windows = [PackedVector2Array([Vector2(514, 102), Vector2(790, 102), Vector2(790, 400), Vector2(500, 400)]), PackedVector2Array([Vector2(850, 102), Vector2(1320, 102), Vector2(1320, 400), Vector2(850, 400)]), PackedVector2Array([Vector2(1380, 102), Vector2(1640, 102), Vector2(1670, 400), Vector2(1380, 400)])]
	queue_redraw()

func _starfield() -> void:
	for p in stars:
		var point = Vector2(180 + fposmod(p.x - 180 - clock * (1.6 + p.z), 1800), p.y)
		var in_window = false
		for glass in windows:
			if Geometry2D.is_point_in_polygon(point, glass):
				in_window = true
				break
		if not in_window: continue
		# Earth occupies the lower/left panes; points stay in the actual dark sky.
		if room in ["bridge", "ending"] and point.x < 1460 and point.y > 112 + (point.x - 850) * 0.40: continue
		var alpha = (0.42 + sin(clock * 0.7 + p.x) * 0.16) * p.z
		draw_circle(point, 0.65 + p.z * 0.75, Color(0.78, 0.9, 1, alpha), true, -1, true)
		if p.z > 0.94:
			draw_line(point - Vector2(3, 0), point + Vector2(3, 0), Color(0.73, 0.88, 1, alpha * 0.3), 0.7, true)

func _screen(rect: Rect2, seed_value: float) -> void:
	var color = Color(0.34, 0.84, 1, 0.38)
	var points = PackedVector2Array()
	for i in range(22):
		var x = float(i) / 21
		var y = 0.48 + sin(x * 13 + clock * 1.4 + seed_value) * 0.17 + sin(x * 27 - clock * 1.1) * 0.08
		points.append(rect.position + Vector2(x * rect.size.x, y * rect.size.y))
	draw_polyline(points, color, 0.8, true)
	var scan = fposmod(clock * 0.25 + seed_value, 1)
	draw_line(rect.position + Vector2(scan * rect.size.x, 1), rect.position + Vector2(scan * rect.size.x, rect.size.y - 1), Color(0.6, 0.95, 1, 0.18), 1, true)
	for i in range(4):
		var height = (0.25 + 0.5 * absf(sin(clock * 0.6 + i * 1.2 + seed_value))) * rect.size.y
		draw_rect(Rect2(rect.end.x - 15 + i * 4, rect.end.y - height, 2, height), Color(0.4, 0.9, 1, 0.24))

func _vapor(origin: Vector2, rise: float, drift: float, alpha: float, spread: float) -> void:
	if not soft: return
	for i in range(13):
		var age = fposmod(clock * 0.18 + i / 13.0, 1)
		var point = origin + Vector2(age * drift + sin(age * 7 + i) * 7, -age * rise)
		var size = Vector2(22 + age * spread, 10 + age * spread * 0.4)
		draw_texture_rect(soft, Rect2(point - size * 0.5, size), false, Color(0.85, 0.93, 1, sin(age * PI) * alpha))

func _draw() -> void:
	if room == "terminal":
		_vapor(Vector2(1500, 492), 91, 34, 0.15, 56)
		_vapor(Vector2(1745, 485), 70, -23, 0.12, 65)
		# A distant utility vehicle moves across the service apron beyond the glass.
		var x = 760 + fposmod(clock * 5, 160)
		draw_style_box(_cart_style(), Rect2(x, 444, 18, 6))
		draw_circle(Vector2(x + 4, 451), 2, Color("233642"), true, -1, true)
		draw_circle(Vector2(x + 14, 451), 2, Color("233642"), true, -1, true)
		draw_circle(Vector2(x + 18, 446), 1.1, Color(1, 0.82, 0.5, 0.75), true, -1, true)
		for point in [Vector2(1535, 257), Vector2(1869, 310)]:
			var pulse = pow(maxf(0, sin(clock * 2.7 + point.x)), 12)
			draw_circle(point, 1.6, Color(1, 0.62, 0.34, pulse * 0.8), true, -1, true)
	elif room == "launch":
		_screen(Rect2(1007, 439, 111, 35), 1.0)
		_screen(Rect2(775, 444, 44, 24), 2.0)
		_screen(Rect2(1269, 444, 55, 24), 3.0)
		if orbital: _starfield()
		else: _vapor(Vector2(1218, 388), 110, -42, 0.16, 95)
		for i in range(5):
			var on = fposmod(clock * 0.6 + i * 0.2, 1) < 0.72
			draw_circle(Vector2(982 + i * 8, 485), 1.7, Color(0.42, 0.88, 0.76, 0.7 if on else 0.08), true, -1, true)
	elif room == "habitation":
		_vapor(Vector2(308, 606), 125, 14, 0.045, 125)
		# Moving sunlight and air-borne motes remain warm and domestic.
		for i in range(14):
			var p = Vector2(770 + fposmod(i * 37 + clock * 3.7, 360), 202 + fposmod(i * 43 - clock * 2, 320))
			draw_circle(p, 0.9, Color(1, 0.88, 0.64, (0.23 + sin(clock * 0.8 + i) * 0.1)), true, -1, true)
		var light = PackedVector2Array([Vector2(778, 188), Vector2(861, 190), Vector2(1170, 610), Vector2(1002, 610)])
		draw_colored_polygon(light, Color(1, 0.83, 0.57, 0.015 + sin(clock * 0.24) * 0.005))
	elif room in ["bridge", "ending"]:
		_starfield()
		for i in range(3):
			_screen(Rect2(367 + i * 594, 426, 43, 20), i + 1.0)
			_screen(Rect2(506 + i * 594, 428, 30, 20), i + 4.0)
		# The navigation plot rotates independently of the static console housing.
		var center = Vector2(1080, 438)
		var tip = center + Vector2.from_angle(clock * 0.25) * Vector2(23, 11)
		draw_line(center, tip, Color(0.56, 0.9, 1, 0.38), 1, true)
		draw_circle(tip, 1.2, Color(0.7, 0.98, 1, 0.8), true, -1, true)
		_vapor(Vector2(1720, 643), 70, 48, 0.04, 130)

func _cart_style() -> StyleBoxFlat:
	var style = StyleBoxFlat.new()
	style.bg_color = Color("a8b8bd")
	style.border_color = Color("3c515a")
	style.set_border_width_all(1)
	style.set_corner_radius_all(1)
	return style
