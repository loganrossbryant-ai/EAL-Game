class_name IslandUI
extends RefCounted

const INK = Color("254e4a")
const TEAL = Color("217e76")
const CREAM = Color("fffaeb")
const GOLD = Color("edb847")
const CORAL = Color("cf654c")

static func box(fill: Color = CREAM, border: Color = Color("decba0"), radius: int = 24) -> StyleBoxFlat:
	var s = StyleBoxFlat.new()
	s.bg_color = fill
	s.border_color = border
	s.set_border_width_all(2)
	s.set_corner_radius_all(radius)
	s.content_margin_left = 20
	s.content_margin_right = 20
	s.shadow_color = Color(0.16, 0.19, 0.13, 0.18)
	s.shadow_size = 10
	s.shadow_offset = Vector2(0, 5)
	return s

static func theme() -> Theme:
	var t = Theme.new()
	var font = preload("res://assets/fonts/Body.ttf")
	font.fallbacks = [preload("res://assets/fonts/Chinese.otf")]
	t.default_font = font
	t.default_font_size = 34
	for type in ["Button", "Label", "CheckButton"]:
		t.set_color("font_color", type, INK)
	for type in ["Button", "CheckButton"]:
		t.set_stylebox("normal", type, box())
		t.set_stylebox("hover", type, box(Color("fff3cb"), TEAL))
		t.set_stylebox("pressed", type, box(Color("d5ece0"), TEAL))
		t.set_stylebox("focus", type, box(Color(0, 0, 0, 0), CORAL))
		t.set_stylebox("disabled", type, box(Color("d7e5db"), Color("8aac9c")))
		t.set_color("font_disabled_color", type, Color("58776c"))
	return t

static func panel(parent: Node, rect: Rect2, fill: Color = CREAM) -> Panel:
	var p = Panel.new()
	p.position = rect.position
	p.size = rect.size
	p.add_theme_stylebox_override("panel", box(fill))
	parent.add_child(p)
	return p

static func label(parent: Node, value: String, rect: Rect2, font_size: int = 34, color: Color = INK) -> Label:
	var l = Label.new()
	l.position = rect.position
	l.size = rect.size
	l.text = value
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	l.add_theme_color_override("font_color", color)
	l.add_theme_font_size_override("font_size", font_size)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(l)
	return l

static func button(parent: Node, value: String, rect: Rect2, fn: Callable, primary: bool = false, font_size: int = 34) -> Button:
	var b = Button.new()
	b.position = rect.position
	b.size = rect.size
	if b.size.y >= 100: b.size.y = maxf(110, b.size.y)
	b.text = value
	b.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	b.add_theme_font_size_override("font_size", font_size)
	b.focus_mode = Control.FOCUS_ALL
	if primary:
		b.add_theme_stylebox_override("normal", box(TEAL, Color("155c55")))
		b.add_theme_color_override("font_color", Color.WHITE)
	b.pressed.connect(fn)
	parent.add_child(b)
	return b

static func picture(parent: Node, texture: Texture2D, rect: Rect2) -> TextureRect:
	var t = TextureRect.new()
	t.position = rect.position
	t.size = rect.size
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	t.texture = texture
	t.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(t)
	return t
