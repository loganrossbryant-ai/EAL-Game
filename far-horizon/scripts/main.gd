extends Node2D

const UI = preload("res://scripts/interface.gd")
const SPEED = 520.0
const WORLD_WIDTH = 2304.0
const FLOOR = 686.0
var story = GMStory.new()
var state = GMState.new()
var scene_index = 0
var scene: Dictionary
var scenery: PioneerScenery
var party: Array[PartyMember] = []
var camera: Camera2D
var world: Node2D
var audio: PioneerAudio
var npcs: Array[Dictionary] = []
var ui: Control
var chrome: Control
var overlay: Control
var modal: Control
var blackout: ColorRect
var cue_panel: Control
var scene_label: Label
var session_label: Label
var prompt: Label
var toast_label: Label
var leader_buttons: Array[Button] = []
var sound_button: Button
var next_button: Button
var cue_label: Label
var paused = false
var move_target = -1.0
var nearest = ""
var camera_lead = 0.0
var camera_focus = -1.0
var clock = 0.0
var publish_elapsed = 0.0
var bridge_elapsed = 0.0
var save_elapsed = 0.0
var current_clue = ""
var conversation = ""
var conversation_line = ""
var gallery = false
var presentation=false
var external_cover=false
var phone_view=false
var touch_direction=0.0
var touch_until=0
var engine_callback: JavaScriptObject
var portrait_catalog: Dictionary
var command_count=0

func _ready() -> void:
	state.restore(story)
	portrait_catalog=JSON.parse_string(FileAccess.get_file_as_string("res://data/portraits.json"))
	if OS.has_feature("web"):phone_view=bool(JavaScriptBridge.eval("matchMedia('(pointer:coarse)').matches",true))
	_setup_input()
	_setup_bridge()
	_build_world()
	_build_ui()
	audio = PioneerAudio.new()
	add_child(audio)
	audio.enabled = bool(state.data.sound)
	audio.speech_enabled = bool(state.data.voice)
	for member in party:
		member.footstep.connect(func():
			if member.selected and not is_instance_valid(modal) and not paused: audio.step()
		)
	# Warm only the three portraits used by this short encounter.
	for entry in portrait_catalog.values():load("res://assets/portraits/"+str(entry.file))
	_enter_scene(story.find_scene(str(state.data.scene)), true)

func _setup_input() -> void:
	for action in {"walk_left": [KEY_A, KEY_LEFT], "walk_right": [KEY_D, KEY_RIGHT], "interact": [KEY_E]}:
		if not InputMap.has_action(action): InputMap.add_action(action)
		for code in {"walk_left": [KEY_A, KEY_LEFT], "walk_right": [KEY_D, KEY_RIGHT], "interact": [KEY_E]}[action]:
			var event = InputEventKey.new()
			event.physical_keycode = code
			InputMap.action_add_event(action, event)

func _setup_bridge() -> void:
	if OS.has_feature("web"):
		JavaScriptBridge.eval(FileAccess.get_file_as_string("res://web/bridge_bootstrap.js"), true)
		engine_callback=JavaScriptBridge.create_callback(_browser_command)
		JavaScriptBridge.get_interface("fhGMBridge").commandCallback=engine_callback

func _build_world() -> void:
	world = Node2D.new()
	add_child(world)
	scenery = PioneerScenery.new()
	scenery.room="corridor"
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
		var cs = CollisionShape2D.new()
		var wr = RectangleShape2D.new()
		wr.size = Vector2(50, 1000)
		cs.shape = wr
		wall.add_child(cs)
		wall.position = Vector2(x, 400)
		wall.collision_layer = 1
		world.add_child(wall)
	for i in range(4):
		var member = PartyMember.new()
		member.setup(i)
		member.position = Vector2(520 - i * 86, FLOOR)
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
	blackout = ColorRect.new()
	blackout.size = Vector2(1366, 768)
	blackout.color = Color("02080d")
	blackout.mouse_filter = Control.MOUSE_FILTER_IGNORE
	blackout.visible = false
	ui.add_child(blackout)
	chrome = Control.new()
	chrome.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(chrome)
	var top = UI.panel(chrome, Rect2(24, 20, 1318, 80), 0.91)
	UI.title(top, "THE FAR HORIZON", Rect2(20, 10, 320, 32), 25)
	session_label = UI.label(top, "", Rect2(20, 46, 320, 20), 13, UI.AMBER)
	scene_label = UI.title(top, "", Rect2(350, 11, 590, 30), 23)
	cue_label = UI.label(top, "", Rect2(350, 47, 590, 20), 13, UI.MUTED)
	UI.button(top, "CLUES  [C]", Rect2(962, 15, 116, 48), _open_board, 14)
	UI.button(top, "GM DESK  [G]", Rect2(1090, 15, 203, 48), _open_gm, 15)
	for i in range(4):
		leader_buttons.append(UI.button(chrome, "", Rect2(28 + i * 169, 700, 159, 44), _select_leader.bind(i), 14))
	UI.button(chrome, "WORDS  [V]", Rect2(715, 700, 124, 44), _open_glossary, 13)
	sound_button = UI.button(chrome, "SFX OFF", Rect2(850, 700, 100, 44), _toggle_sound, 13)
	UI.button(chrome, "PREVIOUS", Rect2(961, 700, 135, 44), _previous, 13)
	next_button = UI.button(chrome, "NEXT  [↵]", Rect2(1107, 700, 230, 44), _next, 15)
	prompt = UI.label(chrome, "", Rect2(340, 646, 690, 36), 18)
	prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt.add_theme_color_override("font_shadow_color", Color.BLACK)
	prompt.add_theme_constant_override("shadow_outline_size", 5)
	toast_label = UI.label(chrome, "", Rect2(760, 110, 565, 65), 15, UI.AMBER)
	toast_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	overlay = Control.new()
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(overlay)

func _enter_scene(index: int, restoring: bool = false) -> void:
	if index < 0 or index >= story.scenes.size(): return
	if scene and not restoring:
		state.data.positions[scene.id] = party[int(state.data.leader)].position.x
	_close_modal()
	move_target = -1
	scene_index = index
	scene = story.scenes[index]
	state.data.scene = scene.id
	scenery.configure(str(scene.room))
	for n in npcs:
		if is_instance_valid(n.node): n.node.queue_free()
	npcs.clear()
	var start = float(state.data.positions.get(scene.id, scene.start))
	var rank = 1
	for i in range(4):
		var offset = 0 if i == int(state.data.leader) else rank * 86
		if i != int(state.data.leader): rank += 1
		party[i].position = Vector2(clampf(start - offset, 65, WORLD_WIDTH - 65), FLOOR)
		party[i].velocity = Vector2.ZERO
		party[i].desired_speed = 0
		party[i].facing = 1
		party[i].turn_time = 0
		party[i].reset_contacts()
		party[i].visible = not scene.id in ["s1_route", "s3_packet"]
	for i in range(scene.npcs.size()):
		var x = 1060 + i * 330
		if scene.room == "corridor": x = 1660 if str(scene.npcs[i]) != "m77" else 1040
		_add_person(str(scene.npcs[i]), x)
	if not scene.clues.is_empty(): _add_station(str(scene.clues[0]), 2060)
	camera.position = Vector2(clampf(start, 683, WORLD_WIDTH - 683), 384)
	camera_lead = 0
	audio.set_room(str(scene.room))
	_apply_cue(not restoring)

func _add_person(id: String, x: float) -> void:
	if not story.characters.has(id): return
	var p: Dictionary = story.characters[id]
	var node = Node2D.new()
	node.position = Vector2(x, FLOOR)
	node.z_index = 3
	world.add_child(node)
	if id != "iris" and id != "m77":
		var spr = Sprite2D.new()
		var path = "res://assets/art/" + str(p.sheet)
		if ResourceLoader.exists(path):
			spr.texture = load(path)
			var parts = 3 if p.sheet == "officers_s23.png" else 2
			spr.hframes = parts
			spr.frame = int(p.region)
			spr.scale = Vector2.ONE * (235.0 / spr.texture.get_height())
			spr.position.y = -117.5
			node.add_child(spr)
			npcs.append({"kind": "person", "id": id, "x": x, "node": node, "sprite": spr})
		else:
			npcs.append({"kind": "person", "id": id, "x": x, "node": node})
	elif id == "iris":
		var sign = UI.panel(node, Rect2(-90, -153, 180, 61), 0.9)
		UI.label(sign, "IRIS / VOICE LINK", Rect2(12, 15, 160, 40), 13, UI.CYAN)
		npcs.append({"kind": "person", "id": id, "x": x, "node": node})
	else:
		npcs.append({"kind": "person", "id": id, "x": x, "node": node})
	var label = UI.label(node, str(p.name).to_upper(), Rect2(-135, -277, 270, 32), 13)
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_color_override("font_shadow_color", Color("06131b"))
	label.add_theme_constant_override("shadow_outline_size", 5)

func _add_station(id: String, x: float) -> void:
	var node = Node2D.new()
	node.position = Vector2(x, FLOOR)
	node.z_index = 1
	world.add_child(node)
	var plate = UI.panel(node, Rect2(-91, -171, 182, 69), 0.9)
	UI.label(plate, str(story.clues[id].title).to_upper(), Rect2(13, 11, 157, 52), 13, UI.PAPER)
	npcs.append({"kind": "clue", "id": id, "x": x, "node": node})

func _cue_index() -> int:
	return int(state.data.cues.get(scene.id, 0))

func _apply_cue(play: bool = true) -> void:
	_close_modal()
	var cue: Dictionary = scene.cues[_cue_index()]
	state.data.seen[scene.id + ":" + str(_cue_index())] = true
	scenery.effect = str(cue.get("effect", ""))
	scenery.effect_time = 0
	camera_focus = 1250.0 if scenery.effect == "round2" else -1.0
	blackout.visible = bool(cue.get("blackout", false))
	conversation_line = str(cue.text)
	conversation = str(cue.get("speaker", ""))
	_update_cue_panel()
	if cue.has("clue"):
		state.data.revealed[str(cue.clue)] = true
		_open_clue(str(cue.clue))
	if play and cue.has("sfx"): audio.launch(int(cue.sfx))
	var speaker = str(cue.get("speaker", ""))
	if play and story.characters.has(speaker): audio.say(speaker, str(cue.text))
	_update_chrome()
	state.save()
	_publish()

func _update_cue_panel() -> void:
	if is_instance_valid(cue_panel):
		cue_panel.visible=false
		cue_panel.queue_free()
	cue_panel=UI.panel(ui,Rect2(24,700,1318,62),.94)
	UI.label(cue_panel,story.projected_cue(str(scene.id),_cue_index()),Rect2(18,6,1282,52),30)
	cue_panel.visible=not is_instance_valid(modal)
	ui.move_child(overlay,ui.get_child_count()-1)

func _update_chrome() -> void:
	session_label.text = "SESSION %02d  /  GM PRESENTATION" % int(scene.session)
	scene_label.text = str(scene.title)
	cue_label.text = "BEAT %d / %d   •   %s" % [_cue_index() + 1, scene.cues.size(), str(scene.focus)]
	chrome.visible = not bool(state.data.clean) and not presentation
	sound_button.text = "SFX ON" if audio.enabled else "SFX OFF"
	next_button.text = "NEXT SCENE  [↵]" if _cue_index() == scene.cues.size() - 1 else "NEXT BEAT  [↵]"
	for i in range(4):
		party[i].selected = i == int(state.data.leader)
		leader_buttons[i].text = str(i + 1) + "  " + CrewState.DEPARTMENTS[i].to_upper()
		leader_buttons[i].add_theme_color_override("font_color", CrewState.COLORS[i] if party[i].selected else UI.MUTED)

func _physics_process(delta: float) -> void:
	if not scene: return
	if not paused: clock += delta
	var held = paused or is_instance_valid(modal) or external_cover
	var leader = party[int(state.data.leader)]
	for member in party:
		member.attending = is_instance_valid(modal)
		member.set_physics_process(not held)
	var direction = 0.0 if held else Input.get_axis("walk_left", "walk_right")
	if not held and direction==0 and Time.get_ticks_msec()<touch_until:direction=touch_direction
	if not held and move_target >= 0:
		if absf(leader.position.x - move_target) < 9 or direction != 0: move_target = -1
		else: direction = signf(move_target - leader.position.x)
	leader.desired_speed = direction * SPEED
	if direction != 0: camera_focus = -1
	var order: Array[int] = [int(state.data.leader)]
	for i in range(4):
		if i != state.data.leader: order.append(i)
	for rank in range(1, 4):
		var follower = party[order[rank]]
		var ahead = party[order[rank - 1]]
		var separation = ahead.position.x - follower.position.x
		if absf(separation) > 24: follower.follow_side = signf(separation)
		var error = separation - follower.follow_side * 86
		follower.desired_speed = clampf(ahead.velocity.x + error * 1.9, -SPEED * 1.08, SPEED * 1.08)
		# Signal a turn to the whole ensemble together instead of waiting for a
		# brake-turn-accelerate wave to reach the last member.
		if not held and direction != 0 and follower.facing != direction:
			follower.desired_speed = direction * SPEED
		if held or (absf(ahead.velocity.x) < 9 and absf(follower.desired_speed) < 9): follower.desired_speed = 0
	if not paused:
		camera_lead = lerpf(camera_lead, clampf(leader.velocity.x / SPEED, -1, 1) * 50, 1 - exp(-delta * 2.8))
		var goal = clampf(leader.position.x + camera_lead, 683, WORLD_WIDTH - 683)
		if camera_focus >= 0: goal = camera_focus
		camera.position.x = lerpf(camera.position.x, goal, 1 - exp(-delta * 3.8))
		camera.position.y = 384
		if scenery.effect in ["rumble", "ascent"]:
			camera.position += Vector2(sin(clock * 57) * 1.6, cos(clock * 49) * 1.1)
	scenery.camera_x = camera.position.x
	scenery.animating = not paused
	nearest = ""
	var distance = 145.0
	for n in npcs:
		if absf(n.x - leader.position.x) < distance:
			distance = absf(n.x - leader.position.x)
			nearest = n.kind + ":" + n.id
		if n.has("sprite"):
			n.sprite.position.y = -117.5 - sin(clock * 1.3 + n.x) * 0.25
	var hint = ""
	if nearest != "" and not held:
		var parts = nearest.split(":")
		hint = "[ E ]  " + (str(story.characters[parts[1]].name) if parts[0] == "person" else str(story.clues[parts[1]].title))
	prompt.text = "PICTURE HELD  /  SPACE TO RESUME" if paused else hint
	save_elapsed += delta
	if save_elapsed > 2:
		save_elapsed = 0
		state.data.positions[scene.id] = leader.position.x
		state.save()
	publish_elapsed += delta
	if publish_elapsed > 0.25:
		publish_elapsed = 0
		_publish()

func _browser_command(args: Array) -> void:
	if args.is_empty() or not args[0] is String:return
	var command=JSON.parse_string(args[0])
	if command is Dictionary:_command(command)


func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		_close_modal()
		_publish()
		get_viewport().set_input_as_handled()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.physical_keycode:
			KEY_R: _talk("rhee")
			KEY_M:
				if "m77" in scene.npcs:_talk("m77")
			KEY_T: _open_clue("ticket")
			KEY_F: _focus_door()
			KEY_G: _open_gm()
			KEY_ENTER, KEY_PAGEDOWN: _next()
			KEY_PAGEUP: _previous()
			KEY_P: _toggle_clean()
			KEY_SPACE: _toggle_freeze()
			KEY_C: _open_board()
			KEY_V: _open_glossary()
			KEY_1, KEY_2, KEY_3, KEY_4:
				if not is_instance_valid(modal): _select_leader(event.physical_keycode - KEY_1)
			KEY_E:
				if not paused and not is_instance_valid(modal) and nearest != "":
					var parts = nearest.split(":")
					if parts[0] == "person": _talk(parts[1])
					else: _open_clue(parts[1])
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed and not is_instance_valid(modal) and not paused:
		var point = get_viewport().get_mouse_position()
		if point.y > 530 and point.y < 690: move_target = clampf(get_global_mouse_position().x, 65, WORLD_WIDTH - 65)

func _command(command: Dictionary) -> void:
	command_count+=1
	match str(command.get("action", "")):
		"cover":
			external_cover=bool(command.get("enabled",false))
			world.visible=not external_cover and not is_instance_valid(modal)
		"presentation":
			presentation=bool(command.get("enabled",false))
			_update_chrome()
		"move":
			touch_direction=clampf(float(command.get("direction",0)),-1,1)
			touch_until=Time.get_ticks_msec()+650
			move_target=-1
		"focus":_focus_door()
		"interact":
			if nearest!="":
				var target=nearest.split(":")
				if target[0]=="person":_talk(target[1])
				else:_open_clue(target[1])
		"reply":
			if conversation in story.characters:
				var options=_dialogue_choices(conversation)
				var index=int(command.get("index",-1))
				if index>=0 and index<options.size():_talk(conversation,str(options[index].text))
		"jump": _enter_scene(story.find_scene(str(command.get("id", ""))))
		"cue":
			state.data.cues[scene.id] = clampi(int(command.get("index", 0)), 0, scene.cues.size() - 1)
			_apply_cue()
		"next": _next()
		"previous": _previous()
		"clue":
			var id = str(command.get("id", ""))
			if story.clues.has(id): _open_clue(id)
		"hide_clue":
			var id = str(command.get("id", ""))
			if story.clues.has(id):
				state.data.revealed[id] = false
				if current_clue == id: _close_modal()
				state.save()
		"close": _close_modal()
		"freeze": _toggle_freeze()
		"clean": _toggle_clean()
		"language":
			if str(command.get("value", "")) in ["zh", "ko", "ja"]:
				state.data.language = str(command.value)
				state.save()
				if conversation == "glossary": _open_glossary()
		"sound": _toggle_sound()
		"voice":
			audio.speech_enabled = not audio.speech_enabled
			state.data.voice = audio.speech_enabled
			if not audio.speech_enabled: audio.stop_voice()
			state.save()
		"replay": _apply_cue()
		"talk":
			var id = str(command.get("id", ""))
			if id in scene.npcs: _talk(id)
		"threat":
			var i = clampi(int(command.get("index", 0)), 0, 2)
			state.data.threats[i] = clampi(int(command.get("value", 0)), 0, 2 if i == 0 else 1)
			state.save()
		"board": _open_board()
		"glossary": _open_glossary()
		"export": _export_progress()
		"reset_session":
			var session = int(scene.session)
			for s in story.scenes:
				if int(s.session) == session:
					state.data.cues[s.id] = 0
					state.data.positions.erase(s.id)
			for id in story.clues:
				if int(story.clues[id].session) == session: state.data.revealed.erase(id)
			if session == 2: state.data.threats = [2, 1, 1]
			_enter_scene(scene_index)
	_publish()

func _next() -> void:
	if _cue_index() + 1 < scene.cues.size():
		state.data.cues[scene.id] = _cue_index() + 1
		_apply_cue()
	elif scene_index + 1 < story.scenes.size():
		_enter_scene(scene_index + 1)
	else: _toast("End of the M-77 test. Page Up returns to earlier beats.")

func _previous() -> void:
	if _cue_index() > 0:
		state.data.cues[scene.id] = _cue_index() - 1
		_apply_cue()
	elif scene_index > 0: _enter_scene(scene_index - 1)

func _select_leader(index: int) -> void:
	state.data.leader = index
	move_target = -1
	_update_chrome()
	state.save()

func _toggle_sound() -> void:
	audio.enabled = not audio.enabled
	audio.update_sound()
	state.data.sound = audio.enabled
	state.save()
	_update_chrome()

func _toggle_clean() -> void:
	state.data.clean = not state.data.clean
	_update_chrome()
	state.save()

func _toggle_freeze() -> void:
	paused = not paused
	move_target = -1
	scenery.animating = not paused

func _new_modal(rect: Rect2) -> Panel:
	_close_modal()
	move_target = -1
	modal = Control.new()
	modal.mouse_filter = Control.MOUSE_FILTER_IGNORE
	overlay.add_child(modal)
	world.visible=false
	world.process_mode=Node.PROCESS_MODE_DISABLED
	if cue_panel:cue_panel.visible=false
	var dim = ColorRect.new()
	dim.size = Vector2(1366, 768)
	dim.color = Color(0.004, 0.015, 0.025, 0.5)
	modal.add_child(dim)
	return UI.panel(modal, rect, 0.98)

func _close_modal() -> void:
	if audio: audio.stop_voice()
	if is_instance_valid(modal):
		modal.visible=false
		modal.queue_free()
	modal = null
	current_clue = ""
	conversation = ""
	gallery = false
	if world:
		world.visible=not external_cover
		world.process_mode=Node.PROCESS_MODE_INHERIT
	if cue_panel:cue_panel.visible=true

func _open_clue(id: String, image_only: bool = false) -> void:
	if not story.clues.has(id): return
	var clue: Dictionary = story.clues[id]
	if not image_only:
		var card=_new_modal(Rect2(20,20,1326,728))
		current_clue=id
		state.data.revealed[id]=true
		state.save()
		UI.label(card,str(clue.tag),Rect2(24,15,1140,28),20,UI.CYAN)
		UI.title(card,str(clue.title),Rect2(24,52,1250,60),40)
		var rows=ceili(clue.fields.size()/2.0)
		var row_height=minf(166,510.0/maxi(1,rows))
		for i in range(clue.fields.size()):
			var x=24+(i%2)*650
			var y=128+(i/2)*row_height
			UI.label(card,str(clue.fields[i][0]),Rect2(x,y,620,35),21,UI.CYAN)
			UI.label(card,str(clue.fields[i][1]),Rect2(x,y+38,620,row_height-41),34,UI.AMBER if id=="ticket" and str(clue.fields[i][0])=="COMPLETED" else UI.PAPER)
		UI.button(card,"Return to the scene  [Esc]",Rect2(24,670,1278,42),_close_modal,22)
		_publish()
		return
	var p = _new_modal(Rect2(65, 119, 1236, 555))
	if id == "ticket":
		var style = UI.box(Color("081d29"), UI.AMBER)
		style.set_corner_radius_all(14)
		style.set_border_width_all(2)
		p.add_theme_stylebox_override("panel", style)
	current_clue = id
	gallery = image_only
	state.data.revealed[id] = true
	state.save()
	UI.label(p, str(clue.tag), Rect2(24, 17, 1070, 22), 13, UI.CYAN)
	UI.title(p, str(clue.title), Rect2(24, 49, 1100, 42), 30)
	UI.button(p, "CLOSE  [ESC]", Rect2(1073, 15, 137, 37), _close_modal, 13)
	var has_image = str(clue.get("image", "")) != "" and ResourceLoader.exists("res://assets/props/" + str(clue.get("image", "")))
	if image_only and has_image:
		UI.portrait(p, load("res://assets/props/" + str(clue.image)), Rect2(26, 104, 1184, 384))
		UI.button(p, "READABLE TRANSCRIPT", Rect2(24, 502, 1186, 37), _open_clue.bind(id, false), 15)
		return
	var text_width = 916.0 if has_image else 1188.0
	var fields: Array = clue.fields
	var row_h = minf(74, 344.0 / maxf(1, fields.size()))
	for i in range(fields.size()):
		var y = 112 + i * row_h
		UI.label(p, str(fields[i][0]), Rect2(24, y + 3, 217, row_h - 7), 14, UI.CYAN)
		UI.label(p, str(fields[i][1]), Rect2(252, y, text_width - 250, row_h), 23 if fields.size() < 6 else 21, UI.AMBER if id == "ticket" and str(fields[i][0]) == "COMPLETED" else UI.PAPER)
	if has_image:
		UI.portrait(p, load("res://assets/props/" + str(clue.image)), Rect2(955, 107, 250, 342))
		UI.button(p, "ENLARGE PROP", Rect2(955, 459, 250, 35), _open_clue.bind(id, true), 13)
	UI.label(p, str(clue.note), Rect2(24, 463, text_width - 6, 72), 17, UI.AMBER)
	_publish()

func _open_board() -> void:
	var p = _new_modal(Rect2(81, 130, 1204, 517))
	conversation = "board"
	UI.title(p, "PIONEER / REVEALED EVIDENCE", Rect2(24, 18, 1100, 40), 28)
	UI.label(p, "Only evidence already revealed in this presentation appears here.", Rect2(24, 69, 1110, 31), 18, UI.MUTED)
	var visible: Array[String] = []
	for id in story.clues:
		if state.data.revealed.get(id, false): visible.append(id)
	for i in range(visible.size()):
		var id = visible[i]
		UI.button(p, str(story.clues[id].title), Rect2(24 + (i % 3) * 388, 124 + (i / 3) * 62, 372, 51), _open_clue.bind(id), 17)
	if visible.is_empty(): UI.label(p, "No clues have been revealed yet.", Rect2(24, 158, 1120, 55), 24)
	UI.button(p, "RETURN TO THE SCENE", Rect2(24, 460, 1156, 39), _close_modal, 16)

func _talk(who: String, reply: String = "") -> void:
	if not story.characters.has(who): return
	var data: Dictionary = story.characters[who]
	var line = str(data.opening) if reply == "" else reply
	if reply == "" and data.has("openings"): line = str(data.openings.get(str(int(scene.session)), line))
	var p = _new_modal(Rect2(0,0,1366,768))
	conversation=who
	conversation_line=line
	if portrait_catalog.has(who):
		var entry=portrait_catalog[who]
		var atlas=AtlasTexture.new()
		atlas.atlas=load("res://assets/portraits/"+str(entry.file))
		atlas.region=Rect2(entry.region[0],entry.region[1],entry.region[2],entry.region[3])
		var photo_frame=Control.new()
		photo_frame.size=Vector2(683,768)
		photo_frame.clip_contents=true
		p.add_child(photo_frame)
		var portrait=UI.portrait(photo_frame,atlas,Rect2(0,0,683,768))
		portrait.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_COVERED
	var side=UI.panel(p,Rect2(683,0,683,768),1)
	UI.title(side,str(data.name),Rect2(32,34,619,100),34)
	UI.label(side,story.projected_role(who),Rect2(32,134,619,38),21,UI.AMBER)
	UI.label(side,story.projected_line(line),Rect2(32,206,619,228),34)
	var choices: Array=_dialogue_choices(who)
	for i in range(mini(choices.size(),4)):
		UI.button(side,str(choices[i].question),Rect2(32,458+i*55,619,49),_talk.bind(who,str(choices[i].text)),23)
	UI.button(side,"Return to the scene  [Esc]",Rect2(32,708,619,42),_close_modal,20)
	audio.say(who, line)
	_publish()

func _dialogue_choices(who: String) -> Array:
	var choices: Array=[]
	for option in story.characters[who].replies:
		if int(scene.session)<int(option.get("min_session",1)):continue
		if int(scene.session)>int(option.get("max_session",3)):continue
		if str(option.get("requires",""))!="" and not state.data.revealed.get(str(option.requires),false):continue
		choices.append(option)
	return choices

func _open_glossary() -> void:
	var p = _new_modal(Rect2(145, 127, 1076, 545))
	conversation = "glossary"
	UI.title(p, "ACADEMIC WORDS / DRAMA & EVIDENCE", Rect2(24, 17, 1010, 35), 25)
	for i in range(3):
		var lang = ["zh", "ko", "ja"][i]
		UI.button(p, ["简体中文", "한국어", "日本語"][i], Rect2(24 + i * 344, 68, 330, 36), func():
			state.data.language = lang
			state.save()
			_open_glossary()
		, 16)
	for i in range(story.data.glossary.size()):
		var word: Dictionary = story.data.glossary[i]
		var x = 24 + (i % 3) * 344
		var y = 123 + (i / 3) * 52
		UI.label(p, str(word.term), Rect2(x, y, 330, 21), 15, UI.CYAN)
		var translated = UI.label(p, str(word[state.data.language]), Rect2(x, y + 22, 330, 26), 17)
		translated.language = str(state.data.language)
	UI.button(p, "RETURN TO THE SCENE", Rect2(24, 501, 1028, 33), _close_modal, 14)

func _open_gm() -> void:
	if OS.has_feature("web"):
		var ok = JavaScriptBridge.eval("window.fhGMBridge&&window.fhGMBridge.openDesk()", true)
		if not ok: _toast("Allow the GM Desk window, then press G again.")
		_publish()
	else:
		_toast("The separate GM Desk is available in the browser build. Page Up / Page Down navigate beats.")

func _export_progress() -> void:
	var bytes = JSON.stringify(state.data, "  ").to_utf8_buffer()
	if OS.has_feature("web"): JavaScriptBridge.download_buffer(bytes, "Far-Horizon-GM-Progress.json", "application/json")
	else:
		var f = FileAccess.open("user://Far-Horizon-GM-Progress.json", FileAccess.WRITE)
		if f: f.store_buffer(bytes)

func _toast(text: String) -> void:
	toast_label.text = text
	get_tree().create_timer(7).timeout.connect(func():
		if toast_label.text == text: toast_label.text = ""
	)

func _publish() -> void:
	if not scene or not audio: return
	var positions: Array = []
	for member in party:
		positions.append({"x":member.position.x,"y":member.position.y,"vx":member.velocity.x,"facing":member.facing,"rig":member.has_rig})
	var subjects: Array = []
	for actor in scenery.props.actors:
		subjects.append({"kind":actor.kind,"x":actor.sprite.position.x,"y":actor.sprite.position.y,"rotation":actor.sprite.rotation})
	var payload = {
		"scene": scene.id, "scene_index": scene_index, "session": scene.session, "title": scene.title,
		"cue": _cue_index(), "cue_count": scene.cues.size(), "cue_title": scene.cues[_cue_index()].title,
		"cue_titles": scene.cues.map(func(c): return str(c.title)), "index": story.public_index(),
		"leader": state.data.leader, "party": positions, "nearest": nearest, "modal": is_instance_valid(modal),
		"clue": current_clue, "conversation": conversation, "line": conversation_line, "paused": paused,
		"clean": state.data.clean, "language": state.data.language, "revealed": state.data.revealed,
		"seen": state.data.seen, "threats": state.data.threats, "storage_ok": state.storage_ok,
		"sound": audio.enabled, "voice": audio.speech_enabled, "recordings": audio.recordings.size(),
		"voice_playing": audio.voice.playing, "clock": clock, "camera": camera.position.x
	}
	payload.phone_view=phone_view
	payload.presentation=presentation
	payload.projected_line=story.projected_line(conversation_line)
	payload.projected_caption=story.projected_cue(str(scene.id),_cue_index())
	payload.projected_role=story.projected_role(conversation) if conversation in story.characters else ""
	payload.physical_inspection=false
	payload.fast_2d=true
	payload.command_count=command_count
	payload.render_fps=Engine.get_frames_per_second()
	payload.world_covered=is_instance_valid(modal) or external_cover
	if OS.is_debug_build():
		payload.subjects = subjects
		payload.effect = scenery.effect
		payload.effect_time = scenery.effect_time
		var issues: Array = []
		_collect_layout_issues(ui, issues)
		payload.layout_issues = issues
	if OS.has_feature("web"):
		var value = JSON.stringify(payload)
		JavaScriptBridge.eval("window.fhGMBridge&&window.fhGMBridge.publish(" + value + ")", true)
		if OS.is_debug_build(): JavaScriptBridge.eval("window.farHorizonTestState=" + value + ";", true)

func _collect_layout_issues(node: Node, issues: Array) -> void:
	if node.is_queued_for_deletion(): return
	if node is Label and node.is_visible_in_tree() and node.has_meta("designed_height"):
		var intended = float(node.get_meta("designed_height"))
		var content_height = node.get_line_count() * node.get_line_height()
		if content_height > intended + 4:
			issues.append({"text":node.text,"designed":intended,"actual":content_height})
	for child in node.get_children(): _collect_layout_issues(child, issues)

func _focus_door() -> void:
	_close_modal()
	move_target=-1
	touch_direction=0
	var lead=int(state.data.leader)
	var order=[lead]
	for i in range(4):
		if i!=lead:order.append(i)
	for rank in range(4):
		var member=party[order[rank]]
		member.position=Vector2(910-rank*86,FLOOR)
		member.velocity=Vector2.ZERO
		member.desired_speed=0
		member.reset_contacts()
	camera.position=Vector2(1152,384)
	camera_focus=1152
	camera_lead=0
	_publish()
