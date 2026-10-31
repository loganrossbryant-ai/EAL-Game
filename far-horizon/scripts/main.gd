extends Node2D

const UI = preload("res://scripts/interface.gd")
const SPEED = 160.0
const WORLD_WIDTH = 2304.0
const FLOOR = 686.0
const LOCATIONS = {"terminal": "EARTH / DEPARTURE TERMINAL", "launch": "CSV-01 / LAUNCH CRADLE", "habitation": "PIONEER / STUDENT HABITATION", "bridge": "PIONEER / BRIDGE & OBSERVATION", "ending": "PIONEER / ROUTE LOG"}
var state = CrewState.new()
var scenery: PioneerScenery
var party: Array[PartyMember] = []
var camera: Camera2D
var world: Node2D
var npcs: Array[Dictionary] = []
var ui: Control
var hud: Control
var overlay: Control
var modal: Control
var message: Label
var prompt: Label
var objective: Label
var leader_labels: Array[Button] = []
var nearest = ""
var move_target = -1.0
var save_elapsed = 0.0
var snapshot_elapsed = 0.0
var paused = false
var transitioning = false
var conversation = ""
var conversation_line = ""
var title_card: Control
var editor_fields: Dictionary = {}
var editor_person = ""
var editor_feedback: Label
var clock = 0.0
var vignette: ColorRect
var audio: PioneerAudio
var sound_button: Button

func _ready() -> void:
	_setup_input()
	state.restore()
	_build_world()
	_build_ui()
	audio = PioneerAudio.new()
	add_child(audio)
	for member in party:
		member.footstep.connect(func():
			if member.selected and not is_instance_valid(modal) and not paused:
				audio.step()
		)
	_enter_room(state.data.scene, false)
	if state.data.scene == "terminal" and not state.data.flags.get("begun", false):
		_show_title()
	elif state.data.scene == "launch":
		_open_launch()
	elif state.data.scene == "ending":
		_show_ending()

func _setup_input() -> void:
	for action in {"walk_left": [KEY_A, KEY_LEFT], "walk_right": [KEY_D, KEY_RIGHT], "interact": [KEY_E]}:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		for code in {"walk_left": [KEY_A, KEY_LEFT], "walk_right": [KEY_D, KEY_RIGHT], "interact": [KEY_E]}[action]:
			var event = InputEventKey.new()
			event.physical_keycode = code
			InputMap.action_add_event(action, event)

func _build_world() -> void:
	world = Node2D.new()
	add_child(world)
	scenery = PioneerScenery.new()
	world.add_child(scenery)
	var ground = StaticBody2D.new()
	ground.collision_layer = 1
	ground.collision_mask = 2
	var shape = CollisionShape2D.new()
	var rect = RectangleShape2D.new()
	rect.size = Vector2(WORLD_WIDTH + 400, 80)
	shape.shape = rect
	ground.position = Vector2(WORLD_WIDTH / 2, FLOOR + 40)
	ground.add_child(shape)
	world.add_child(ground)
	for x in [-10.0, WORLD_WIDTH + 10]:
		var wall = StaticBody2D.new()
		var wall_shape = CollisionShape2D.new()
		var wall_rect = RectangleShape2D.new()
		wall_rect.size = Vector2(50, 1000)
		wall_shape.shape = wall_rect
		wall.add_child(wall_shape)
		wall.position = Vector2(x, 400)
		wall.collision_layer = 1
		world.add_child(wall)
	for i in range(4):
		var member = PartyMember.new()
		member.setup(i)
		member.position = Vector2(520 - i * 88, FLOOR)
		member.z_index = 5 + i
		party.append(member)
		world.add_child(member)
	camera = Camera2D.new()
	camera.position = Vector2(683, 384)
	camera.position_smoothing_enabled = false
	add_child(camera)

func _build_ui() -> void:
	var layer = CanvasLayer.new()
	add_child(layer)
	ui = Control.new()
	ui.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	ui.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.theme = UI.theme()
	layer.add_child(ui)
	vignette = ColorRect.new()
	vignette.size = Vector2(1366, 768)
	vignette.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var film_shader = Shader.new()
	film_shader.code = "shader_type canvas_item; render_mode unshaded; void fragment(){ vec2 p=(UV-vec2(0.5))*vec2(1.0,0.82); float edge=smoothstep(0.32,0.66,length(p)); COLOR=vec4(0.015,0.028,0.04,edge*0.24); }"
	var film_material = ShaderMaterial.new()
	film_material.shader = film_shader
	vignette.material = film_material
	ui.add_child(vignette)
	hud = Control.new()
	hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(hud)
	var top = UI.panel(hud, Rect2(26, 22, 1314, 76), 0.9)
	UI.title(top, "THE FAR HORIZON", Rect2(20, 11, 320, 30), 24)
	UI.label(top, "01   /   WELCOME TO PIONEER", Rect2(20, 42, 330, 22), 13, UI.AMBER)
	objective = UI.label(top, "", Rect2(365, 16, 530, 52), 16)
	sound_button = UI.button(top, "SOUND OFF", Rect2(826, 15, 118, 45), _toggle_sound, 13)
	UI.button(top, "CREW LOG  [L]", Rect2(955, 15, 157, 45), _open_log, 14)
	UI.button(top, "GM CUES  [G]", Rect2(1123, 15, 168, 45), _open_gm, 14)
	for i in range(4):
		var b = UI.button(hud, "", Rect2(28 + i * 184, 698, 174, 46), _select_leader.bind(i), 15)
		leader_labels.append(b)
	UI.label(hud, "A / D  or  ← / →   MOVE     E   INTERACT     SPACE   HOLD", Rect2(805, 716, 535, 24), 13, UI.PAPER)
	prompt = UI.label(hud, "", Rect2(350, 633, 666, 46), 18)
	prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt.add_theme_color_override("font_shadow_color", Color.BLACK)
	prompt.add_theme_constant_override("shadow_outline_size", 5)
	message = UI.label(hud, "", Rect2(770, 106, 557, 55), 16, UI.AMBER)
	message.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	overlay = Control.new()
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(overlay)
	_update_hud()

func _show_title() -> void:
	title_card = UI.panel(overlay, Rect2(55, 135, 547, 252), 0.89)
	UI.label(title_card, "2247  /  COHORT 01  /  CSV-01", Rect2(25, 20, 490, 25), 14, UI.CYAN)
	UI.title(title_card, "The last room on Earth", Rect2(25, 54, 500, 44), 31)
	UI.label(title_card, "Earth is not dying. That is what makes leaving harder.\nAhead waits Pioneer. Why does your character leave?", Rect2(25, 112, 490, 67), 18)
	UI.button(title_card, "ENTER THE TERMINAL", Rect2(25, 190, 292, 43), _begin)

func _begin() -> void:
	if is_instance_valid(title_card):
		title_card.queue_free()
	state.data.flags.begun = true
	state.save()
	_toast("Walk to the mission kiosk or speak with the crew. Click the floor to move.")

func _enter_room(room: String, reset_position: bool = true) -> void:
	state.data.scene = room
	scenery.configure(room)
	for n in npcs:
		if is_instance_valid(n.get("node")):
			n.node.queue_free()
	npcs.clear()
	if reset_position:
		state.data.position = 520.0
	var rank = 1
	for i in range(4):
		var offset = 0 if i == int(state.data.leader) else rank * 86
		if i != int(state.data.leader):
			rank += 1
		party[i].position = Vector2(clampf(float(state.data.position) - offset, 60, WORLD_WIDTH - 60), FLOOR)
		party[i].velocity = Vector2.ZERO
		party[i].desired_speed = 0
		party[i].visible = room != "ending"
	match room:
		"terminal":
			_add_station("briefing", "MISSION BRIEFING", 700)
			_add_person("juno", "JUNO REYES", 1110, 1)
			_add_person("venn", "CAPTAIN VENN", 1750, 0)
			_add_station("iris", "IRIS / CREW INTEGRATION", 1950)
			_add_station("gate", "BOARDING THRESHOLD", 2190)
		"launch":
			_add_station("launch_cue", "LAUNCH CONTROL", 1040)
		"habitation":
			_add_person("juno", "JUNO REYES", 1170, 1)
			_add_station("tour", "SIX-DECK ORIENTATION", 790)
			_add_station("bridge_door", "TO THE BRIDGE", 2170)
		"bridge":
			_add_person("venn", "CAPTAIN VENN", 1460, 0)
			_add_station("iris", "IRIS", 1110)
			_add_station("window", "OBSERVATION GLASS", 1880)
	_update_hud()
	if audio:
		audio.set_room(room)
	state.save()

func _add_person(id: String, person_name: String, x: float, half: int) -> void:
	var node = Node2D.new()
	node.position = Vector2(x, FLOOR)
	node.z_index = 3
	world.add_child(node)
	var shadow = Polygon2D.new()
	var points = PackedVector2Array()
	for i in range(32):
		points.append(Vector2(cos(i * TAU / 32.0) * 43, sin(i * TAU / 32.0) * 7))
	shadow.polygon = points
	shadow.color = Color(0, 0.02, 0.03, 0.22)
	node.add_child(shadow)
	var sprite = Sprite2D.new()
	sprite.texture = preload("res://assets/art/officers.png")
	sprite.hframes = 2
	sprite.frame = half
	sprite.scale = Vector2.ONE * 0.24
	sprite.position = Vector2(0, -120)
	node.add_child(sprite)
	var label = UI.label(node, person_name, Rect2(-112, -283, 224, 30), 14, UI.PAPER)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_color_override("font_shadow_color", Color("06131b"))
	label.add_theme_constant_override("shadow_outline_size", 5)
	npcs.append({"id": id, "x": x, "node": node, "sprite": sprite})

func _add_station(id: String, caption: String, x: float) -> void:
	var node = Node2D.new()
	node.position = Vector2(x, FLOOR)
	world.add_child(node)
	node.z_index = 1
	var plate = UI.panel(node, Rect2(-85, -175, 170, 76), 0.92)
	UI.label(plate, "P", Rect2(11, 14, 24, 30), 22, UI.CYAN)
	UI.label(plate, caption, Rect2(41, 10, 122, 55), 13, UI.PAPER)
	npcs.append({"id": id, "x": x, "node": node})

func _physics_process(delta: float) -> void:
	clock += delta
	var held = paused or is_instance_valid(modal) or transitioning
	for member in party:
		member.attending = is_instance_valid(modal)
	var leader: PartyMember = party[int(state.data.leader)]
	var direction = 0.0 if held else Input.get_axis("walk_left", "walk_right")
	if not held and move_target >= 0:
		if absf(leader.position.x - move_target) < 9 or direction != 0:
			move_target = -1
		else:
			direction = signf(move_target - leader.position.x)
	leader.desired_speed = direction * SPEED
	var order: Array[int] = [int(state.data.leader)]
	for i in range(4):
		if i != state.data.leader:
			order.append(i)
	for rank in range(1, 4):
		var follower = party[order[rank]]
		var ahead = party[order[rank - 1]]
		var separation = ahead.position.x - follower.position.x
		follower.desired_speed = clampf((separation - signf(separation) * 80) * 2.8, -SPEED * 1.06, SPEED * 1.06) if absf(separation) > 88 else 0.0
		if held:
			follower.desired_speed = 0
	var camera_goal = clampf(leader.position.x + 90 * leader.facing, 683, WORLD_WIDTH - 683)
	camera.position.x = lerpf(camera.position.x, camera_goal, 1 - exp(-delta * 3.8))
	camera.position.y = 384.0
	if scenery.effect in ["rumble", "ascent"] and not paused:
		camera.position += Vector2(sin(clock * 57) * 2.5, cos(clock * 49) * 1.7)
	scenery.camera_x = camera.position.x
	nearest = ""
	var distance = 150.0
	for n in npcs:
		if absf(n.x - leader.position.x) < distance:
			nearest = n.id
			distance = absf(n.x - leader.position.x)
		if n.has("sprite"):
			n.sprite.position.y = -120.0 - sin(clock * 1.5 + n.x) * 0.45
	prompt.text = "[ E ]  " + _interaction_name(nearest) if nearest != "" and not held else ("STORY HELD  /  SPACE TO RESUME" if paused else "")
	save_elapsed += delta
	if save_elapsed > 2:
		save_elapsed = 0
		state.data.position = leader.position.x
		state.save()
	snapshot_elapsed += delta
	if snapshot_elapsed > 0.2:
		snapshot_elapsed = 0
		_publish_snapshot()

func _input(event: InputEvent) -> void:
	# Escape must also work while a text field owns keyboard focus.
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		if is_instance_valid(modal):
			_close_modal()
		elif is_instance_valid(title_card):
			_begin()
		get_viewport().set_input_as_handled()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_ESCAPE:
			if is_instance_valid(modal):
				_close_modal()
			elif is_instance_valid(title_card):
				_begin()
			return
		if is_instance_valid(modal):
			return
		match event.physical_keycode:
			KEY_1, KEY_2, KEY_3, KEY_4:
				_select_leader(event.physical_keycode - KEY_1)
			KEY_L: _open_log()
			KEY_G: _open_gm()
			KEY_SPACE:
				paused = not paused
				move_target = -1
			KEY_E:
				if state.data.scene == "ending":
					_show_ending()
				elif not paused and nearest != "":
					_interact(nearest)
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed and not is_instance_valid(modal) and not paused:
		var screen_point = get_viewport().get_mouse_position()
		if screen_point.y > 545 and screen_point.y < 690:
			move_target = clampf(get_global_mouse_position().x, 65, WORLD_WIDTH - 65)

func _select_leader(index: int) -> void:
	if is_instance_valid(modal) or transitioning:
		return
	state.data.leader = index
	state.data.position = party[index].position.x
	move_target = -1
	_update_hud()
	state.save()

func _update_hud() -> void:
	if not objective:
		return
	var goal = "Find your reason to leave. Meet Captain Venn."
	match state.data.scene:
		"terminal":
			if state.data.flags.get("venn_address", false):
				goal = "Keep an Earth object. Perform the crossing. Board together."
		"launch": goal = "Take your places. The GM advances each launch beat."
		"habitation": goal = "Four departments. Six decks. Choose a place that matters."
		"bridge": goal = "Watch the observation glass. Record what you can see."
		"ending": goal = "Session 01 complete. Keep the question open."
	objective.text = LOCATIONS.get(state.data.scene, "PIONEER") + "\n" + goal
	objective.size.x = 450
	objective.add_theme_font_size_override("font_size", 15)
	for i in range(leader_labels.size()):
		party[i].selected = state.data.leader == i
		leader_labels[i].text = str(i + 1) + "  " + CrewState.DEPARTMENTS[i].to_upper()
		leader_labels[i].add_theme_color_override("font_color", CrewState.COLORS[i] if state.data.leader == i else UI.MUTED)
		leader_labels[i].add_theme_stylebox_override("normal", UI.box(Color("16333f") if state.data.leader == i else Color("081a24"), CrewState.COLORS[i] if state.data.leader == i else Color("3c505b")))

func _interaction_name(id: String) -> String:
	return {"venn": "SPEAK WITH CAPTAIN VENN", "juno": "SPEAK WITH JUNO", "iris": "SPEAK WITH IRIS", "briefing": "READ THE MISSION BRIEFING", "gate": "CROSS THE BOARDING THRESHOLD", "launch_cue": "TAKE YOUR LAUNCH POSITIONS", "tour": "OPEN THE DECK DIRECTORY", "bridge_door": "ENTER THE BRIDGE", "window": "LOOK THROUGH THE OBSERVATION GLASS"}.get(id, "")

func _interact(id: String) -> void:
	move_target = -1
	if id in ["venn", "juno", "iris"]:
		_open_conversation(id)
	elif id == "briefing":
		_open_briefing()
	elif id == "gate":
		_open_boarding()
	elif id == "launch_cue":
		_open_launch()
	elif id == "tour":
		_open_tour()
	elif id == "bridge_door":
		_bridge_gate()
	elif id == "window":
		_open_observation()

func _new_modal(rect: Rect2 = Rect2(55, 125, 1256, 550)) -> Panel:
	_close_modal()
	move_target = -1
	modal = Control.new()
	modal.mouse_filter = Control.MOUSE_FILTER_IGNORE
	overlay.add_child(modal)
	var shade = ColorRect.new()
	shade.size = Vector2(1366, 768)
	shade.color = Color(0.008, 0.02, 0.03, 0.33)
	modal.add_child(shade)
	return UI.panel(modal, rect, 0.98)

func _close_modal() -> void:
	if is_instance_valid(modal):
		modal.queue_free()
	modal = null
	conversation = ""
	editor_fields.clear()

func _open_conversation(who: String, reply: String = "") -> void:
	var aboard = state.data.scene != "terminal"
	var line = Conversations.opening(who, aboard) if reply.is_empty() else reply
	if who == "iris" and state.data.flags.get("anomaly", false) and reply.is_empty():
		line = "insufficient image duration for classification."
	var p = _new_modal(Rect2(38, 412, 1290, 326))
	conversation = who
	conversation_line = line
	var name_text = {"venn": "CAPTAIN MARA VENN", "juno": "JUNO REYES / STUDENT LIAISON", "iris": "IRIS / SHIP INTELLIGENCE"}[who]
	if who == "iris":
		var tex = AtlasTexture.new()
		tex.atlas = preload("res://assets/art/iris.jpeg")
		tex.region = Rect2(50, 160, 960, 1420)
		UI.portrait(p, tex, Rect2(18, 18, 170, 242))
	else:
		var tex = AtlasTexture.new()
		tex.atlas = preload("res://assets/art/officers.png")
		tex.region = Rect2(205 if who == "venn" else 970, 0, 405, 570)
		UI.portrait(p, tex, Rect2(17, 14, 180, 248))
	UI.label(p, name_text, Rect2(218, 16, 1000, 26), 16, UI.CYAN)
	UI.label(p, line, Rect2(218, 48, 1044, 100), 20)
	var options = Conversations.choices(who, aboard)
	var all_options: Array = options.duplicate()
	all_options.append(["Let the class speak in its own words…", "improv"])
	all_options.append(["Return to the scene", "close"])
	for i in range(all_options.size()):
		var option = all_options[i]
		UI.button(p, option[0], Rect2(218 + (i % 2) * 528, 157 + (i / 2) * 48, 516, 42), _choose_dialogue.bind(who, option[0], option[1]), 16)
	UI.label(p, "SPEAKING FOR " + CrewState.DEPARTMENTS[state.data.leader].to_upper() + " / " + state.data.representatives[state.data.leader], Rect2(218, 300, 1040, 20), 12, UI.MUTED)
	if reply.is_empty():
		state.record_event(name_text, line)
	if who == "venn" and not aboard:
		state.data.flags.venn_address = true
		state.save()
		_update_hud()

func _choose_dialogue(who: String, choice: String, reply: String) -> void:
	if reply == "close":
		_close_modal()
	elif reply == "improv":
		_open_improv(who)
	else:
		state.record_event(state.data.representatives[state.data.leader], choice)
		state.record_event(who, reply)
		_open_conversation(who, reply)

func _open_improv(who: String) -> void:
	var p = _new_modal(Rect2(160, 190, 1046, 440))
	UI.title(p, "The next words belong to your company", Rect2(28, 20, 980, 40), 27)
	UI.label(p, "Perform the exchange aloud. The GM plays the NPC. You can keep a short record below, or continue after the live performance.", Rect2(28, 77, 980, 65), 20)
	var field = TextEdit.new()
	field.position = Vector2(28, 157)
	field.size = Vector2(980, 158)
	field.placeholder_text = "Optional record of the company's words or decision…"
	field.wrap_mode = TextEdit.LINE_WRAPPING_BOUNDARY
	p.add_child(field)
	UI.button(p, "Keep the performance & continue", Rect2(28, 350, 470, 48), func():
		state.record_event(state.data.representatives[state.data.leader], field.text.strip_edges() if not field.text.strip_edges().is_empty() else "Live improvised exchange acknowledged by GM.")
		_open_conversation(who, "Take the time you need. We are listening.")
	)
	UI.button(p, "Back to the conversation", Rect2(515, 350, 493, 48), _open_conversation.bind(who))

func _open_briefing() -> void:
	var p = _new_modal()
	UI.portrait(p, preload("res://assets/art/briefing.jpeg"), Rect2(25, 20, 300, 490))
	UI.label(p, "PIONEER INITIATIVE / MISSION BRIEFING", Rect2(352, 25, 850, 28), 16, UI.CYAN)
	UI.title(p, "A beginning. Chosen together.", Rect2(352, 66, 850, 42), 30)
	UI.label(p, "2247. Earth is habitable. CSV-01 Pioneer carries Cohort 01 toward Asteria-4 to help establish a second civilization. This is a deliberate departure from a world that is still alive.\n\nFour departments travel together: Flight, Science, Engineering, and Colony. Nobody can build a home alone.\n\nBefore boarding: choose a reason to leave, a want, a possible need, a fear, and one object from Earth. Keep the object in your character's record.", Rect2(352, 130, 850, 245), 21)
	UI.button(p, "Open my character's crew log", Rect2(352, 440, 440, 55), _open_log)
	UI.button(p, "Return to the terminal", Rect2(809, 440, 393, 55), _close_modal)
	state.data.flags.briefing = true
	state.save()

func _open_log(person_override: String = "") -> void:
	var p = _new_modal(Rect2(55, 117, 1256, 563))
	editor_person = person_override if not person_override.is_empty() else state.data.representatives[state.data.leader]
	UI.title(p, "CREW LOG", Rect2(25, 20, 270, 38), 28)
	UI.label(p, "Fictional crew identities only. Saved on this browser.", Rect2(335, 26, 825, 28), 16, UI.MUTED)
	var select = OptionButton.new()
	select.position = Vector2(25, 82)
	select.size = Vector2(280, 46)
	var roster: Array[String] = []
	for i in range(4):
		for person in CrewState.ROSTER[i]:
			roster.append(person)
			select.add_item(CrewState.DEPARTMENTS[i] + " / " + person)
	select.select(roster.find(editor_person))
	select.item_selected.connect(func(index: int): _open_log(roster[index]))
	p.add_child(select)
	UI.label(p, "WANT / NEED\n\nA want: what the character tries to get.\n\nA need: what they may have to learn.\n\nWrite two different sentences. Keep one Earth object.", Rect2(25, 157, 275, 260), 18, UI.MUTED)
	var record = state.data.records.get(editor_person, {})
	var definitions = [["reason", "Why I am leaving Earth", "I am leaving because…"], ["want", "What my character WANTS", "My character wants…"], ["need", "What they may NEED to learn", "They may need to learn…"], ["fear", "What they fear losing", "They are afraid of losing…"], ["object", "One object from Earth / what it means", "They brought… because…"]]
	for i in range(definitions.size()):
		var definition = definitions[i]
		UI.label(p, definition[1], Rect2(335, 79 + i * 73, 870, 25), 15, UI.CYAN)
		var field = LineEdit.new()
		field.position = Vector2(335, 106 + i * 73)
		field.size = Vector2(893, 39)
		field.text = record.get(definition[0], "")
		field.placeholder_text = definition[2]
		field.max_length = 450
		p.add_child(field)
		editor_fields[definition[0]] = field
	editor_feedback = UI.label(p, "", Rect2(335, 453, 893, 30), 15, UI.AMBER)
	UI.button(p, "SAVE CHARACTER RECORD", Rect2(335, 495, 410, 46), _save_record, 16)
	UI.button(p, "Return to the scene", Rect2(762, 495, 466, 46), _close_modal, 16)
	UI.button(p, "Paper records / GM review", Rect2(25, 455, 280, 45), _open_gm, 15)

func _save_record() -> void:
	var record = {}
	for key in editor_fields:
		record[key] = editor_fields[key].text.strip_edges()
		if record[key].is_empty():
			editor_feedback.text = "Keep a reason, a want, a need, a fear, and your Earth object before saving."
			return
	if record.want.to_lower() == record.need.to_lower():
		editor_feedback.text = "Try a different sentence for NEED. What might the character have to learn?"
		return
	state.data.records[editor_person] = record
	var saved = state.save()
	editor_feedback.text = "Saved for " + editor_person + ". Share the want and need with your company." if saved else "Browser storage is unavailable. Export the session from GM Cues to keep this record."

func _open_gm() -> void:
	if state.data.scene != "terminal":
		_open_ship_cues()
		return
	var p = _new_modal(Rect2(48, 115, 1270, 568))
	UI.title(p, "SESSION 01 / GM CUES", Rect2(26, 18, 1100, 37), 27)
	UI.button(p, "CLOSE", Rect2(1135, 19, 108, 40), _close_modal, 14)
	UI.label(p, "Hold the screen while companies rehearse and perform. Paper and digital records are tracked separately. There is no real-time boarding countdown.", Rect2(26, 69, 1216, 58), 18, UI.MUTED)
	for i in range(4):
		var x = 26 + i * 307
		var card = UI.panel(p, Rect2(x, 141, 294, 195), 1)
		UI.title(card, CrewState.DEPARTMENTS[i].to_upper(), Rect2(14, 10, 266, 28), 20)
		var digital_count = 0
		for person in CrewState.ROSTER[i]:
			if state.data.records.has(person):
				digital_count += 1
		UI.label(card, str(digital_count) + " / " + str(CrewState.ROSTER[i].size()) + " digital records", Rect2(14, 47, 266, 25), 15, UI.MUTED)
		UI.button(card, ("✓  " if state.data.paper[i] else "○  ") + "Paper sheets reviewed", Rect2(12, 82, 270, 43), _toggle_paper.bind(i), 15)
		UI.button(card, ("✓  " if state.data.performed[i] else "○  ") + "Crossing performed", Rect2(12, 136, 270, 43), _toggle_performance.bind(i), 15)
	UI.label(p, "BOARDING SCORE", Rect2(26, 354, 1216, 25), 14, UI.CYAN)
	UI.label(p, "One person looks back. One moves first. One hides nerves. Someone notices something strange. Make a stage picture; physically cross a line.\nAudience: What did the group picture tell you before anyone spoke?", Rect2(26, 389, 1216, 75), 19)
	UI.button(p, "Hear Captain Venn's mission address", Rect2(26, 486, 475, 50), _open_conversation.bind("venn"), 17)
	UI.button(p, "Export session record", Rect2(518, 486, 354, 50), _export_record, 17)
	UI.button(p, "Return to the scene", Rect2(889, 486, 354, 50), _close_modal, 17)

func _toggle_paper(index: int) -> void:
	state.data.paper[index] = not bool(state.data.paper[index])
	state.save()
	_open_gm()

func _toggle_performance(index: int) -> void:
	state.data.performed[index] = not bool(state.data.performed[index])
	state.save()
	_open_gm()

func _open_boarding() -> void:
	var p = _new_modal(Rect2(190, 209, 986, 393))
	UI.label(p, "THE THRESHOLD / EARTH → PIONEER", Rect2(28, 22, 920, 25), 15, UI.AMBER)
	UI.title(p, "What do you take with you?", Rect2(28, 64, 920, 44), 32)
	var ready = state.boarding_ready()
	var body = "Your companies have performed the crossing and kept their reasons, wants, needs, fears, and Earth objects. When the class is ready, cross together."
	if not ready:
		body = "Before leaving: hear Venn's address, keep each character's crew record on paper or in the log, and perform all four companies' crossing scenes. The GM records the paper review and performances in GM Cues."
	UI.label(p, body, Rect2(28, 127, 925, 119), 21)
	if ready:
		UI.button(p, "CROSS TOGETHER / BOARD PIONEER", Rect2(28, 284, 605, 57), func(): _transition("launch"), 18)
	else:
		UI.button(p, "Review the companies / GM Cues", Rect2(28, 284, 605, 57), _open_gm, 18)
	UI.button(p, "One more moment", Rect2(651, 284, 302, 57), _close_modal, 18)

func _transition(room: String) -> void:
	_close_modal()
	transitioning = true
	move_target = -1
	var fade = ColorRect.new()
	fade.size = Vector2(1366, 768)
	fade.color = Color(0.01, 0.025, 0.035, 0)
	overlay.add_child(fade)
	var tween = create_tween()
	tween.tween_property(fade, "color:a", 1.0, 0.45)
	await tween.finished
	if room != state.data.scene:
		state.data.cue = 0
	scenery.effect = ""
	_enter_room(room)
	camera.position.x = 683
	tween = create_tween()
	tween.tween_property(fade, "color:a", 0.0, 0.6)
	await tween.finished
	fade.queue_free()
	transitioning = false
	if room == "launch":
		_open_launch()
	elif room == "ending":
		_show_ending()

func _open_launch() -> void:
	var beats = [
		["Take your places", "The restraints lock. Beyond the glass, the launch tower waits. Take one last breath of the world you know."],
		["Ignition", "For several seconds there is only vibration, pressure, and the impossible sight of Earth dropping beneath you."],
		["The tower falls away", "The cities are still lit. The oceans still move. Everything familiar grows smaller behind the glass."],
		["Engine cutoff", "Then the engines cut. A pen lifts from a console. Somebody laughs. Somebody else does not."],
		["One ship. One floor.", "Pioneer has become the only floor under your feet.\n\nCAPTAIN VENN: Welcome aboard Pioneer."]
	]
	var index = clampi(int(state.data.cue), 0, beats.size() - 1)
	var p = _new_modal(Rect2(135, 137, 1096, 255))
	UI.label(p, "LAUNCH / " + str(index + 1) + " OF 5 / GM-HELD", Rect2(24, 15, 1048, 24), 13, UI.AMBER)
	UI.title(p, beats[index][0], Rect2(24, 48, 1048, 40), 30)
	UI.label(p, beats[index][1], Rect2(24, 102, 1048, 80), 22)
	UI.button(p, "HOLD FOR THE CLASS", Rect2(24, 196, 330, 42), _close_modal, 15)
	UI.button(p, "REPLAY THIS BEAT", Rect2(371, 196, 330, 42), _replay_launch, 15)
	UI.button(p, "BEGIN THE SHIP TOUR" if index == 4 else "NEXT LAUNCH BEAT", Rect2(718, 196, 354, 42), _next_launch, 15)
	scenery.effect = "rumble" if index == 1 else ("ascent" if index == 2 else ("float" if index >= 3 else ""))
	state.save()

func _replay_launch() -> void:
	scenery.effect_time = 0
	if audio:
		audio.launch(int(state.data.cue))
	_open_launch()

func _next_launch() -> void:
	if state.data.cue >= 4:
		state.data.flags.launch_complete = true
		state.save()
		_transition("habitation")
	else:
		state.data.cue += 1
		scenery.effect_time = 0
		state.record_event("Launch", ["The restraints lock.", "Ignition.", "The tower falls away.", "The engines cut. A pen floats.", "Welcome aboard Pioneer."][state.data.cue])
		if audio:
			audio.launch(int(state.data.cue))
		_open_launch()

func _open_tour() -> void:
	var p = _new_modal(Rect2(62, 122, 1242, 553))
	UI.title(p, "PIONEER / SIX-DECK ORIENTATION", Rect2(24, 18, 1188, 38), 28)
	UI.label(p, "Choose one place your department expects to matter. Explain why. This is a quick tour; the class stays together.", Rect2(24, 67, 1188, 35), 18, UI.MUTED)
	for i in range(4):
		var choice = state.data.deck_choices.get(CrewState.DEPARTMENTS[i], {})
		var text = CrewState.DEPARTMENTS[i] + (" / chosen" if not choice.is_empty() else " / choose")
		var b = UI.button(p, text, Rect2(24 + i * 299, 116, 285, 41), _tour_department.bind(i), 16)
		b.add_theme_color_override("font_color", CrewState.COLORS[i])
	var areas = [
		["Bridge & observation", "Flight / a shared direction", "Venn: Speak plainly. Tell the crew what you see before you tell them what it means."],
		["Science & medical", "Science / questions and care", "Okafor: Your body is part of the mission equipment. Unlike the equipment, you are allowed to disagree with me."],
		["Student habitation", "Rest / a place to belong", "Juno: This is your ship too. What would make a room feel like yours?"],
		["Colony commons", "Colony / a community taking shape", "A ship needs shared routines as much as working machinery. What should people be able to count on?"],
		["Engineering", "Engineering / keeping a world working", "Rhee: Every ship is a collection of problems that have agreed not to happen at the same time."],
		["Cargo & boarding", "Resources / what we carry", "Every crate takes space. Every object comes from somewhere. What is essential—and who decides?"]
	]
	for i in range(areas.size()):
		var area = areas[i]
		var card = UI.panel(p, Rect2(24 + (i % 3) * 399, 180 + (i / 3) * 134, 385, 119), 1)
		UI.label(card, area[1], Rect2(13, 9, 359, 23), 13, UI.CYAN)
		UI.title(card, area[0], Rect2(13, 36, 359, 28), 20)
		UI.button(card, "Explore this idea", Rect2(13, 74, 359, 33), _choose_deck.bind(area), 15)
	UI.label(p, "Draft orientation layout / no room-by-room exploration", Rect2(24, 465, 720, 25), 13, UI.MUTED)
	UI.button(p, "Return to the gallery", Rect2(24, 499, 574, 37), _close_modal, 16)
	UI.button(p, "Continue to the bridge", Rect2(615, 499, 580, 37), _bridge_gate, 16)

func _tour_department(index: int) -> void:
	state.data.leader = index
	_update_hud()
	_open_tour()

func _choose_deck(area: Array) -> void:
	var p = _new_modal(Rect2(150, 162, 1066, 479))
	UI.label(p, CrewState.DEPARTMENTS[state.data.leader].to_upper() + " / A PLACE THAT MIGHT MATTER", Rect2(26, 20, 1000, 25), 15, UI.CYAN)
	UI.title(p, area[0], Rect2(26, 64, 1000, 43), 30)
	UI.label(p, area[2], Rect2(26, 123, 1000, 92), 22)
	UI.label(p, "We think this place will matter because…", Rect2(26, 233, 1000, 29), 18, UI.AMBER)
	var reason = LineEdit.new()
	reason.position = Vector2(26, 276)
	reason.size = Vector2(1012, 48)
	reason.max_length = 450
	reason.placeholder_text = "Optional written reason; the GM can acknowledge an oral response below."
	p.add_child(reason)
	var record = func():
		state.data.deck_choices[CrewState.DEPARTMENTS[state.data.leader]] = {"area": area[0], "reason": reason.text.strip_edges() if not reason.text.strip_edges().is_empty() else "Spoken reason acknowledged by GM.", "mode": "written" if not reason.text.strip_edges().is_empty() else "spoken"}
		state.record_event(state.data.representatives[state.data.leader], "We choose " + area[0] + ". " + state.data.deck_choices[CrewState.DEPARTMENTS[state.data.leader]].reason)
		_open_tour()
	UI.button(p, "Keep our reason / oral response heard", Rect2(26, 357, 625, 47), record, 17)
	UI.button(p, "Consider another place", Rect2(668, 357, 370, 47), _open_tour, 17)

func _bridge_gate() -> void:
	if state.data.deck_choices.size() < 4:
		_toast("Each department chooses one place and gives a reason before the observation scene.")
		_open_tour()
		return
	state.data.flags.tour_complete = true
	state.save()
	_transition("bridge")

func _open_observation() -> void:
	var p = _new_modal(Rect2(193, 165, 980, 358))
	UI.label(p, "OBSERVATION / WHAT CAN YOU ACTUALLY SEE?", Rect2(26, 22, 928, 25), 15, UI.CYAN)
	UI.title(p, "Beyond the glass", Rect2(26, 64, 928, 44), 32)
	var seen = bool(state.data.flags.get("anomaly", false))
	UI.label(p, "Something bent the starlight. Then it was gone. Describe the observation before you decide what it means." if seen else "The observation glass darkens. The stars brighten.\nLet the class watch in silence for a moment.", Rect2(26, 125, 928, 87), 23)
	UI.button(p, "Ask Iris what it was" if seen else "Watch the glass", Rect2(26, 244, 452, 46), _open_conversation.bind("iris") if seen else _play_anomaly, 17)
	UI.button(p, "Capture our three screenplay lines" if seen else "Hold the view", Rect2(498, 244, 456, 46), _open_script if seen else _close_modal, 17)
	UI.button(p, "Return to the bridge", Rect2(26, 305, 928, 34), _close_modal, 15)

func _play_anomaly() -> void:
	_close_modal()
	scenery.effect = "anomaly"
	scenery.effect_time = 0
	state.data.flags.anomaly = true
	state.record_event("Observation", "A brief lensing pattern interrupts the starlight. It is gone before it can be classified.")
	await get_tree().create_timer(2.0).timeout
	if state.data.scene == "bridge" and not is_instance_valid(modal):
		_open_observation()

func _open_script(person_override: String = "") -> void:
	var p = _new_modal(Rect2(71, 130, 1224, 536))
	editor_person = person_override if not person_override.is_empty() else state.data.representatives[state.data.leader]
	UI.title(p, "SCREENPLAY CAPTURE / THREE LINES", Rect2(25, 18, 1150, 36), 27)
	UI.label(p, "Write what the audience can SEE and HEAR. Keep the silent reaction visible. The teacher reviews the craft.", Rect2(25, 67, 1150, 48), 19, UI.MUTED)
	var people: Array[String] = []
	var select = OptionButton.new()
	select.position = Vector2(25, 126)
	select.size = Vector2(1174, 41)
	for department in CrewState.ROSTER:
		for person in department:
			people.append(person)
			select.add_item(person)
	select.select(people.find(editor_person))
	select.item_selected.connect(func(index: int): _open_script(people[index]))
	p.add_child(select)
	var saved = state.data.script.get(editor_person, {})
	var definitions = [["action", "1 / Action showing departure", "The launch tower falls away. A pen rises from the console."], ["dialogue", "2 / One line your character might say", "CHARACTER: …"], ["reaction", "3 / A silent, visible reaction", "A hand tightens around an Earth object. Nobody speaks."]]
	for i in range(3):
		UI.label(p, definitions[i][1], Rect2(25, 186 + i * 75, 1174, 24), 15, UI.CYAN)
		var field = LineEdit.new()
		field.position = Vector2(25, 212 + i * 75)
		field.size = Vector2(1174, 41)
		field.placeholder_text = definitions[i][2]
		field.text = saved.get(definitions[i][0], "")
		field.max_length = 650
		p.add_child(field)
		editor_fields[definitions[i][0]] = field
	editor_feedback = UI.label(p, "", Rect2(25, 441, 1174, 25), 15, UI.AMBER)
	UI.button(p, "Save these lines", Rect2(25, 480, 358, 40), _save_script, 16)
	UI.button(p, "Review paper scripts / finish session", Rect2(400, 480, 450, 40), _open_script_review, 16)
	UI.button(p, "Return to the bridge", Rect2(867, 480, 332, 40), _close_modal, 16)

func _save_script() -> void:
	var lines = {}
	for key in editor_fields:
		lines[key] = editor_fields[key].text.strip_edges()
		if lines[key].is_empty():
			editor_feedback.text = "Keep an action, a line of dialogue, and a visible silent reaction."
			return
	state.data.script[editor_person] = lines
	state.save()
	editor_feedback.text = "Saved for " + editor_person + ". Teacher review: can an audience see or hear each line?"

func _open_script_review() -> void:
	var p = _new_modal(Rect2(104, 176, 1158, 423))
	UI.title(p, "KEEP THE THREE-LINE SCRIPTS", Rect2(27, 23, 1100, 39), 29)
	UI.label(p, "Review the action line, dialogue, and silent reaction. If students wrote on paper, acknowledge each company's scripts below. Digital scripts stay attached to fictional crew names.", Rect2(27, 85, 1100, 91), 21)
	for i in range(4):
		UI.button(p, ("Reviewed / " if state.data.script_paper[i] else "Paper / ") + CrewState.DEPARTMENTS[i], Rect2(27 + i * 280, 206, 266, 55), _toggle_scripts.bind(i), 16)
	var ready = state.script_ready() and state.data.flags.get("anomaly", false)
	UI.label(p, "The observation is unresolved. End on the route log when the class is ready." if ready else "Keep all four companies' scripts and visit the observation glass before the cliffhanger.", Rect2(27, 282, 1100, 45), 18, UI.AMBER)
	UI.button(p, "END ON THE ROUTE LOG" if ready else "Return to the bridge", Rect2(27, 350, 1100, 48), _transition.bind("ending") if ready else _close_modal, 17)

func _toggle_scripts(index: int) -> void:
	state.data.script_paper[index] = not state.data.script_paper[index]
	state.save()
	_open_script_review()

func _open_ship_cues() -> void:
	var p = _new_modal(Rect2(105, 142, 1156, 489))
	UI.title(p, "GM / SESSION 01", Rect2(26, 20, 1100, 38), 28)
	UI.label(p, "Suggested class pace: launch & tour 32–55 min / observation 55–68 / scripts & ending 68–80. Hold, replay, and resume at your class's pace.", Rect2(26, 82, 1100, 75), 20, UI.MUTED)
	UI.button(p, "Resume launch cues" if state.data.scene == "launch" else "Open the deck directory", Rect2(26, 188, 537, 55), _open_launch if state.data.scene == "launch" else _open_tour, 18)
	UI.button(p, "Speak with Juno" if state.data.scene == "habitation" else "Speak with Captain Venn", Rect2(585, 188, 545, 55), _open_conversation.bind("juno" if state.data.scene == "habitation" else "venn"), 18)
	UI.button(p, "Screenplay capture", Rect2(26, 264, 537, 55), _open_script, 18)
	UI.button(p, "Review scripts / ending", Rect2(585, 264, 545, 55), _open_script_review, 18)
	UI.button(p, "Observation glass" if state.data.scene == "bridge" else "Where are we going? / Iris", Rect2(26, 340, 537, 55), _open_observation if state.data.scene == "bridge" else _open_conversation.bind("iris"), 18)
	UI.button(p, "Export session record", Rect2(585, 340, 545, 55), _export_record, 18)
	UI.button(p, "Return to the scene", Rect2(26, 419, 1104, 46), _close_modal, 17)

func _show_ending() -> void:
	hud.visible = false
	var p = _new_modal(Rect2(200, 421, 966, 270))
	var cue = int(state.data.cue)
	if cue >= 3:
		modal.get_child(0).color = Color("020609")
		state.data.finished = true
		state.save()
		UI.label(p, "SESSION 01 / COMPLETE", Rect2(27, 22, 912, 25), 15, UI.CYAN)
		UI.title(p, "Welcome to Pioneer", Rect2(27, 67, 912, 45), 36)
		UI.label(p, "Keep the Earth objects. Keep the question open.", Rect2(27, 132, 912, 42), 22)
		UI.button(p, "Export session record", Rect2(27, 205, 288, 43), _export_record, 16)
		UI.button(p, "Replay final exchange", Rect2(333, 205, 288, 43), func():
			state.data.cue = 0
			_show_ending()
		, 16)
		UI.button(p, "Start a new class", Rect2(639, 205, 300, 43), _confirm_new_class, 16)
		return
	var names = ["IRIS", "CAPTAIN MARA VENN", "IRIS"]
	var lines = ["Route correction accepted.", "Who entered that correction?", "No correction was entered."]
	conversation = "ending"
	conversation_line = lines[cue]
	UI.label(p, "ROUTE LOG / " + names[cue], Rect2(27, 25, 912, 25), 15, UI.CYAN)
	UI.title(p, "“" + lines[cue] + "”", Rect2(27, 84, 912, 75), 34)
	UI.button(p, "HOLD / LET THE CLASS REACT", Rect2(27, 207, 440, 42), func():
		_close_modal()
		_toast("Story held. Press E to return to the final exchange.")
	, 15)
	UI.button(p, "CUT / END SESSION" if cue == 2 else "CONTINUE", Rect2(486, 207, 453, 42), _next_ending, 16)
	state.record_event(names[cue], lines[cue])

func _next_ending() -> void:
	state.data.cue += 1
	state.save()
	_show_ending()

func _toggle_sound() -> void:
	audio.enabled = not audio.enabled
	audio.update_sound()
	sound_button.text = "SOUND ON" if audio.enabled else "SOUND OFF"

func _confirm_new_class() -> void:
	var p = _new_modal(Rect2(203, 200, 960, 365))
	UI.title(p, "A new Cohort 01", Rect2(26, 23, 908, 43), 32)
	UI.label(p, "Starting again replaces this browser's current Session 1 save. Export the current class record first if you want to keep it.", Rect2(26, 100, 908, 105), 23)
	UI.button(p, "Export current class", Rect2(26, 230, 440, 48), _export_record, 17)
	UI.button(p, "Replace save / start Session 1", Rect2(484, 230, 450, 48), _new_class, 17)
	UI.button(p, "Return to this class", Rect2(26, 296, 908, 40), _show_ending, 16)

func _new_class() -> void:
	_close_modal()
	state = CrewState.new()
	paused = false
	scenery.effect = ""
	state.save()
	hud.visible = true
	_enter_room("terminal")
	camera.position = Vector2(683, 384)
	_show_title()

func _export_record() -> void:
	var content = JSON.stringify(state.data, "  ").to_utf8_buffer()
	if OS.has_feature("web"):
		JavaScriptBridge.download_buffer(content, "Far-Horizon-Session-01.json", "application/json")
	else:
		var file = FileAccess.open("user://Far-Horizon-Session-01.json", FileAccess.WRITE)
		if file:
			file.store_buffer(content)
	_toast("Session record exported. It includes fictional crew records and dialogue choices.")

func _toast(value: String) -> void:
	message.text = value
	get_tree().create_timer(7).timeout.connect(func():
		if message.text == value:
			message.text = ""
	)

func _publish_snapshot() -> void:
	if not OS.has_feature("web") or not OS.is_debug_build():
		return
	var positions: Array = []
	for member in party:
		positions.append({"x": member.position.x, "y": member.position.y, "vx": member.velocity.x, "frame": member.walk_sprite.frame, "facing": member.facing})
	var editors = {}
	for key in editor_fields:
		if is_instance_valid(editor_fields[key]):
			editors[key] = editor_fields[key].text
	var snapshot = {"scene": state.data.scene, "leader": state.data.leader, "party": positions, "nearest": nearest, "modal": is_instance_valid(modal), "conversation": conversation, "line": conversation_line, "paused": paused, "camera": camera.position.x, "flags": state.data.flags, "records": state.data.records, "paper": state.data.paper, "performed": state.data.performed, "boarding_ready": state.boarding_ready(), "editors": editors, "storage_ok": state.storage_ok, "cue": state.data.cue, "deck_choices": state.data.deck_choices, "script": state.data.script, "script_paper": state.data.script_paper, "finished": state.data.finished, "sound": audio.enabled if audio else false}
	JavaScriptBridge.eval("window.farHorizonTestState=" + JSON.stringify(snapshot) + ";", true)
