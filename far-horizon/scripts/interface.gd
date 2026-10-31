class_name PioneerUI
extends RefCounted

const INK = Color("07141e")
const PAPER = Color("eaf0ed")
const MUTED = Color("a8bdc5")
const CYAN = Color("82d5df")
const AMBER = Color("edbd7e")

static func theme() -> Theme:
	var t = Theme.new()
	var body_font = preload("res://assets/fonts/Body.ttf")
	body_font.fallbacks = [preload("res://assets/fonts/Symbols.ttf")]
	t.default_font = body_font
	t.default_font_size = 18
	for type in ["Label", "Button", "LineEdit", "TextEdit", "OptionButton", "CheckButton"]:
		t.set_color("font_color", type, PAPER)
		t.set_color("font_hover_color", type, Color.WHITE)
		t.set_color("font_focus_color", type, Color.WHITE)
	for type in ["Button", "OptionButton"]:
		t.set_stylebox("normal", type, box(Color("132b37"), Color("43606b")))
		t.set_stylebox("hover", type, box(Color("22414d"), CYAN))
		t.set_stylebox("pressed", type, box(Color("2b4d59"), AMBER))
		t.set_stylebox("focus", type, box(Color(0, 0, 0, 0), AMBER))
		t.set_stylebox("disabled", type, box(Color("11222b"), Color("283e47")))
	for type in ["TextEdit", "LineEdit"]:
		t.set_stylebox("normal", type, box(Color("0a1e29"), Color("3d5964")))
		t.set_stylebox("focus", type, box(Color("102a36"), CYAN))
		t.set_color("caret_color", type, AMBER)
		t.set_color("font_placeholder_color", type, MUTED)
	t.set_stylebox("panel", "PopupMenu", box(Color("0d2430"), CYAN))
	t.set_color("font_color", "PopupMenu", PAPER)
	t.set_color("font_hover_color", "PopupMenu", Color.WHITE)
	return t

static func box(fill: Color, border: Color = Color("42616d")) -> StyleBoxFlat:
	var b = StyleBoxFlat.new()
	b.bg_color = fill
	b.border_color = border
	b.set_border_width_all(1)
	b.set_corner_radius_all(3)
	b.content_margin_left = 14
	b.content_margin_right = 14
	b.content_margin_top = 8
	b.content_margin_bottom = 8
	return b

static func panel(parent: Node, rect: Rect2, opacity: float = 0.96) -> Panel:
	var p = Panel.new()
	p.position = rect.position
	p.size = rect.size
	p.add_theme_stylebox_override("panel", box(Color(0.022, 0.062, 0.089, opacity)))
	parent.add_child(p)
	return p

static func label(parent: Node, value: String, rect: Rect2, font_size: int = 18, color: Color = PAPER) -> Label:
	var l = Label.new()
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.add_theme_font_size_override("font_size", font_size)
	l.add_theme_color_override("font_color", color)
	l.text = value
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(l)
	l.position = rect.position
	l.size = rect.size
	return l

static func title(parent: Node, value: String, rect: Rect2, font_size: int = 28) -> Label:
	var l = label(parent, value, rect, font_size)
	l.add_theme_font_override("font", preload("res://assets/fonts/Heading.ttf"))
	return l

static func button(parent: Node, value: String, rect: Rect2, action: Callable, font_size: int = 17) -> Button:
	var b = Button.new()
	b.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	b.add_theme_font_size_override("font_size", font_size)
	b.text = value
	b.focus_mode = Control.FOCUS_NONE
	b.pressed.connect(action)
	parent.add_child(b)
	b.position = rect.position
	b.size = rect.size
	return b

static func portrait(parent: Node, texture: Texture2D, rect: Rect2) -> TextureRect:
	var t = TextureRect.new()
	t.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	t.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	t.texture = texture
	t.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(t)
	t.position = rect.position
	t.size = rect.size
	return t
