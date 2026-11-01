extends Node2D

const UI = preload("res://scripts/island_ui.gd")
const Actor = preload("res://scripts/actor.gd")
const Audio = preload("res://scripts/island_audio.gd")
const TOPICS = ["animals", "food", "sports", "entertainment", "people", "colors", "places", "activities"]
const ROOMS = {
	"sanctuary": {"title": "Animal sanctuary", "topics": ["animals"], "frame": 0, "npc": "Ari", "purpose": "Help Ari prepare the animal parade.", "map": Vector2(408, 344)},
	"park": {"title": "Sports park", "topics": ["sports", "activities"], "frame": 1, "npc": "Max", "purpose": "Help Max plan the festival games.", "map": Vector2(1090, 695)},
	"story": {"title": "Story square", "topics": ["entertainment", "people"], "frame": 2, "npc": "Luna", "purpose": "Help Luna fill the festival story wall.", "map": Vector2(365, 659)},
	"garden": {"title": "Art garden", "topics": ["colors", "places"], "frame": 3, "npc": "Zoe", "purpose": "Help Zoe decorate the festival map.", "map": Vector2(773, 462)},
	"cafe": {"title": "Seaside café", "topics": ["food"], "map": Vector2(1065, 318)}
}
const SEEDS = {"animals": "dolphin", "sports": "badminton", "activities": "drawing", "entertainment": "puppet show", "people": "firefighter", "colors": "silver", "places": "aquarium"}
const FLOOR = Rect2(290, 414, 906, 391)
const NPC_POS = Vector2(1100, 562)
const SHELF_POS = Vector2(610, 490)
var host: Node2D
var progress: IslandProgress
var sound: IslandAudio
var ui: Control
var hud: Control
var modal: Control
var modal_id = ""
var subtitle: Label
var feedback: Label
var objective: Label
var context_button: Button
var movement_hint: Label
var guide_button: Button
var scene: Sprite2D
var alan: IslandActor
var pip: IslandActor
var npc: Sprite2D
var room = ""
var topic = "animals"
var catalog: Dictionary = {}
var by_topic: Dictionary = {}
var textures: Dictionary = {}
var target_point = Vector2(-1, -1)
var pending = ""
var selected: Array[String] = []
var chunk_buttons: Array[Button] = []
var built_label: Label
var photo_page = -1
var practice_mode = "word"
var practice_target = ""
var practice_pool: Array = []
var practice_serial = 0
var practice_correct = false
var clock = 0.0
var snapshot_clock = 0.0
var joystick = Vector2.ZERO
var dragging = false
var celebration = 0.0
var last_request = ""

func _ready() -> void:
	for entry in JSON.parse_string(FileAccess.get_file_as_string("res://data/vocabulary.json")):
		catalog[entry.id] = entry
		if not by_topic.has(entry.topic): by_topic[entry.topic] = []
		by_topic[entry.topic].append(entry.id)
	if "cafe" in progress.data.completed_missions and not "food" in progress.data.festival_stamps:
		progress.data.festival_stamps.append("food")
	sound = Audio.new()
	sound.settings = progress.data.settings
	add_child(sound)
	sound.begin()
	scene = Sprite2D.new()
	scene.centered = false
	scene.z_index = -10
	add_child(scene)
	alan = Actor.new()
	alan.kind = "alan"
	add_child(alan)
	pip = Actor.new()
	pip.kind = "pip"
	add_child(pip)
	npc = Sprite2D.new()
	add_child(npc)
	var layer = CanvasLayer.new()
	add_child(layer)
	ui = Control.new()
	ui.theme = UI.theme()
	ui.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(ui)
	_enter_map()

func _quest() -> Dictionary:
	if not progress.data.topic_quests.has(topic):
		progress.data.topic_quests[topic] = {"round": 0, "stage": 0, "target": "", "carrying": "", "favorite": "", "completed": [], "translation_help": false}
	var q: Dictionary = progress.data.topic_quests[topic]
	if q.target.is_empty():
		var ids: Array = by_topic[topic]
		var seed = 0
		for i in range(ids.size()):
			if catalog[ids[i]].en == SEEDS.get(topic, ""): seed = i
		q.target = ids[(seed + int(q.round)) % ids.size()]
		progress.save()
	return q

func _texture(id: String) -> Texture2D:
	if not textures.has(id): textures[id] = load("res://" + catalog[id].illustration)
	return textures[id]

func _pool() -> Array:
	var q = _quest()
	var ids: Array = by_topic[topic]
	var start = ids.find(q.target)
	var result: Array = []
	for i in range(4): result.append(ids[(start + i) % ids.size()])
	return result

func _help(en: String, instruction: String) -> String:
	return en + ("\n" + instruction if progress.data.settings.chinese else "")

func _clear() -> void:
	sound.stop()
	if is_instance_valid(modal):
		ui.remove_child(modal)
		modal.queue_free()
	modal = null
	modal_id = ""
	selected.clear()
	chunk_buttons.clear()
	dragging = false
	joystick = Vector2.ZERO

func _dialog(title: String, hint: String, kind: String) -> Panel:
	_clear()
	modal_id = kind
	target_point = Vector2(-1, -1)
	pending = ""
	modal = Control.new()
	ui.add_child(modal)
	var shade = ColorRect.new()
	shade.size = Vector2(1440, 960)
	shade.color = Color(0.04, 0.16, 0.16, 0.56)
	modal.add_child(shade)
	var panel = UI.panel(modal, Rect2(70, 156, 1300, 650), Color("fff9e8"))
	UI.label(panel, title, Rect2(30, 7, 865, 68), 42)
	subtitle = UI.label(panel, hint, Rect2(30, 81, 1050, 84), 30, UI.TEAL)
	UI.button(panel, "操作", Rect2(930, 16, 162, 110), _toggle_help, false, 31)
	UI.button(panel, "Close", Rect2(1110, 16, 162, 110), _clear, false, 31)
	feedback = UI.label(panel, "", Rect2(30, 487, 1220, 55), 31, UI.TEAL)
	return panel

func _toggle_help() -> void:
	progress.data.settings.chinese = not progress.data.settings.chinese
	progress.save()
	var keep = selected.duplicate()
	match modal_id:
		"request": _request()
		"shelf": _shelf()
		"build":
			_build_sentence()
			for value in keep:
				for i in range(chunk_buttons.size()):
					if chunk_buttons[i].text == value and not chunk_buttons[i].disabled: _chunk(value, i); break
		"personal": _personal()
		"speaking": _speaking()
		"word", "translation": _practice_panel()
		"passport": _passport()
		_: pass
	_refresh()

func _replay(panel: Node, line: String, rect: Rect2 = Rect2(30, 538, 285, 110)) -> void:
	if not sound.has_line(line): return
	UI.button(panel, "▶ Replay", rect, func(): sound.say(line), false, 32)

func _reset_hud() -> void:
	if is_instance_valid(hud):
		ui.remove_child(hud)
		hud.queue_free()
	hud = Control.new()
	hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(hud)
	var title = UI.panel(hud, Rect2(22, 20, 470, 114))
	UI.label(title, "Favorites Island" if room.is_empty() else ROOMS[room].title, Rect2(20, 5, 430, 59), 39)
	UI.label(title, "ALAN + PIP  /  FAVORITES FESTIVAL", Rect2(20, 70, 430, 31), 22, UI.TEAL)
	var goal = UI.panel(hud, Rect2(507, 20, 455, 114))
	objective = UI.label(goal, "", Rect2(18, 3, 420, 105), 31)
	guide_button = UI.button(hud, "操作", Rect2(978, 20, 133, 114), _toggle_help)
	UI.button(hud, "Stamps", Rect2(1121, 20, 154, 114), _passport, false, 28)
	UI.button(hud, "Café", Rect2(1285, 20, 133, 114), _return_cafe, false, 29)
	var bottom = UI.panel(hud, Rect2(334, 824, 1084, 114))
	movement_hint = UI.label(bottom, "Tap the path to walk.", Rect2(20, 8, 430, 95), 30)
	context_button = UI.button(bottom, "", Rect2(470, 4, 590, 110), _context, true, 32)
	if room.is_empty():
		for key in ROOMS:
			var info: Dictionary = ROOMS[key]
			UI.button(hud, info.title, Rect2(info.map - Vector2(132, 80), Vector2(264, 92)), _approach.bind(key), false, 29)
	else:
		UI.button(hud, "Island path", Rect2(24, 164, 240, 110), _approach.bind("map"), false, 30)
		UI.button(hud, ROOMS[room].npc, Rect2(1030, 164, 175, 100), _approach.bind("npc"), false, 33)
		UI.button(hud, "Picture shelf", Rect2(490, 272, 245, 102), _approach.bind("shelf"), false, 30)
		var topics: Array = ROOMS[room].topics
		for i in range(topics.size()):
			var key: String = topics[i]
			UI.button(hud, key.capitalize(), Rect2(24, 300 + i * 112, 240, 100), _choose_topic.bind(key), false, 29)
	_refresh()

func _enter_map() -> void:
	_clear()
	room = ""
	scene.texture = preload("res://assets/art/island.webp")
	scene.scale = Vector2(1440.0 / 1536, 960.0 / 1024)
	alan.scale = Vector2.ONE * 0.72
	pip.scale = Vector2.ONE * 0.72
	alan.position = Vector2(735, 690)
	pip.position = Vector2(668, 715)
	npc.hide()
	_reset_hud()

func _enter_room(key: String) -> void:
	if key == "cafe": _return_cafe(); return
	_clear()
	room = key
	topic = ROOMS[room].topics[0]
	var frame: int = ROOMS[room].frame
	var atlas = AtlasTexture.new()
	atlas.atlas = preload("res://assets/art/festival-rooms.png")
	atlas.region = Rect2((frame % 2) * 768, (frame / 2) * 512, 768, 512)
	scene.texture = atlas
	scene.scale = Vector2(1440.0 / 768, 960.0 / 512)
	alan.scale = Vector2.ONE
	pip.scale = Vector2.ONE
	alan.position = Vector2(745, 745)
	pip.position = Vector2(660, 780)
	var portrait = AtlasTexture.new()
	portrait.atlas = preload("res://assets/art/residents.png")
	portrait.region = Rect2(frame * 384, 0, 384, 1024)
	npc.texture = portrait
	npc.position = NPC_POS - Vector2(0, 123)
	npc.scale = Vector2.ONE * 0.24
	npc.z_index = int(NPC_POS.y)
	npc.show()
	photo_page = -1
	_quest()
	_reset_hud()

func _choose_topic(value: String) -> void:
	if is_instance_valid(modal): return
	topic = value
	photo_page = -1
	_quest()
	_refresh()
	_approach("npc")

func _refresh() -> void:
	if not is_instance_valid(objective): return
	movement_hint.text = _help("Tap the path to walk.", "点小路走动，点人物接任务。")
	guide_button.add_theme_stylebox_override("normal", UI.box(Color("d8eee1") if progress.data.settings.chinese else UI.CREAM))
	if room.is_empty():
		objective.text = "Visit a resident.\nFestival teams: %d / 8" % progress.data.festival_stamps.size()
		context_button.text = "Choose a path above"
		alan.carried_texture = null
		return
	var q = _quest()
	var actions = ["Meet " + ROOMS[room].npc + ".", "Bring the requested picture.", "Build the sentence.", "Choose your favorite.", "Say it together.", "Your display is ready!"]
	objective.text = topic.capitalize() + "  /  " + actions[int(q.stage)]
	context_button.text = "Talk to " + ROOMS[room].npc
	alan.carried_texture = _texture(q.carrying) if not q.carrying.is_empty() else null

func _approach(id: String) -> void:
	if is_instance_valid(modal): return
	pending = id
	if room.is_empty(): target_point = ROOMS[id].map + Vector2(0, 32)
	elif id == "map": target_point = Vector2(350, 650)
	elif id == "shelf": target_point = SHELF_POS
	else: target_point = NPC_POS - Vector2(70, 0)

func _context() -> void:
	if room.is_empty(): return
	if alan.position.distance_to(SHELF_POS) < 120: _shelf()
	elif alan.position.distance_to(Vector2(350, 650)) < 110: _enter_map()
	else: _approach("npc")

func _request() -> void:
	var q = _quest()
	if int(q.stage) == 2: _build_sentence(); return
	if int(q.stage) == 3: _personal(); return
	if int(q.stage) == 4: _speaking(); return
	if int(q.stage) == 5: _finished(); return
	var entry: Dictionary = catalog[q.target]
	var p = _dialog(ROOMS[room].npc + "'s festival note", _help(ROOMS[room].purpose, "看便条，到架子选图，再带回来。"), "request")
	UI.label(p, entry.sentence, Rect2(50, 182, 1180, 145), 48)
	UI.label(p, "Bring a picture for our display.", Rect2(50, 364, 1180, 85), 37)
	_replay(p, entry.sentence)
	if int(q.stage) == 0:
		UI.button(p, "I'll help!", Rect2(850, 538, 410, 110), func(): q.stage = 1; progress.save(); _clear(); _refresh(), true, 36)
	elif q.carrying.is_empty():
		UI.button(p, "Go to the picture shelf", Rect2(685, 538, 575, 110), func(): _clear(); _approach("shelf"), true, 33)
	else:
		UI.label(p, "Your picture: " + catalog[q.carrying].en, Rect2(50, 447, 1180, 50), 32)
		UI.button(p, "Give the picture", Rect2(750, 538, 510, 110), _deliver, true)
	if sound.say(entry.sentence): progress.word(entry.id, "heard")

func _deliver() -> void:
	var q = _quest()
	if not progress.assess("trail_" + topic + "_delivery_" + str(q.round), "resident_delivery", q.carrying, q.target, bool(q.get("translation_help", false)), q.target):
		feedback.text = _help("Read the note again. You can change your picture.", "再看便条，可以回去换一张。")
		sound.say("Try again.")
		return
	q.stage = 2
	q.carrying = ""
	progress.save()
	_refresh()
	sound.chime()
	_build_sentence()

func _card(panel: Node, id: String, x: float, fn: Callable, semantic: String) -> void:
	var b = UI.button(panel, "", Rect2(x, 168, 294, 310), fn)
	b.set_meta("semantic", semantic + ":" + id)
	UI.picture(b, _texture(id), Rect2(28, 6, 238, 199))
	var text = UI.label(b, catalog[id].en, Rect2(9, 208, 276, 97), 35)
	text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	progress.word(id, "seen")

func _shelf() -> void:
	var p = _dialog(ROOMS[room].npc + "'s picture shelf", _help("Choose a picture to carry, or practise with the cards.", "点一张图带走；也可以先做配对练习。"), "shelf")
	var ids: Array = by_topic[topic]
	var visible: Array = _pool() if photo_page < 0 else ids.slice(photo_page * 4, mini(photo_page * 4 + 4, ids.size()))
	for i in range(visible.size()):
		var id: String = visible[i]
		_card(p, id, 30 + i * 311, _pickup.bind(id), "collect")
	UI.button(p, "Picture + word", Rect2(30, 538, 390, 110), _start_practice.bind("word"), false, 31)
	UI.button(p, "Translation game", Rect2(450, 538, 390, 110), _start_practice.bind("translation"), false, 29)
	UI.button(p, "More pictures", Rect2(870, 538, 390, 110), func(): photo_page = ((photo_page + 2) % 6) - 1; _shelf(), true, 31)

func _pickup(id: String) -> void:
	_quest().carrying = id
	progress.word(id, "practised")
	progress.save()
	_clear()
	_refresh()
	if sound.say(catalog[id].en): progress.word(id, "heard")

func _build_sentence() -> void:
	var q = _quest()
	var entry: Dictionary = catalog[q.target]
	var p = _dialog("Make the festival label", _help("Build the sentence from the note.", "点词块排顺序，再点检查；不会扣分。"), "build")
	UI.picture(p, _texture(q.target), Rect2(30, 161, 190, 165))
	built_label = UI.label(p, "Tap the word pieces.", Rect2(244, 168, 1000, 131), 43)
	var parts: Array = entry.chunks.duplicate()
	parts.append("are" if "is" in parts else "likes")
	parts.shuffle()
	for i in range(parts.size()):
		var value: String = parts[i]
		var b = UI.button(p, value, Rect2(30 + (i % 3) * 416, 325 + (i / 3) * 94, 398, 86), _chunk.bind(value, i), false, 31)
		chunk_buttons.append(b)
	_replay(p, entry.sentence, Rect2(30, 538, 310, 110))
	UI.button(p, "Start again", Rect2(373, 538, 335, 110), _reset_parts, false, 32)
	UI.button(p, "Check sentence", Rect2(740, 538, 520, 110), _check_parts, true, 34)

func _chunk(value: String, index: int) -> void:
	if selected.size() >= catalog[_quest().target].chunks.size(): return
	selected.append(value)
	chunk_buttons[index].disabled = true
	built_label.text = " ".join(selected)

func _reset_parts() -> void:
	selected.clear()
	for b in chunk_buttons: b.disabled = false
	built_label.text = "Tap the word pieces."

func _check_parts() -> void:
	var q = _quest()
	var entry: Dictionary = catalog[q.target]
	if not progress.assess("trail_" + topic + "_sentence_" + str(q.round), "trail_sentence", " ".join(selected), entry.sentence, bool(q.get("translation_help", false)), q.target):
		feedback.text = _help("Try another order. Read the note again.", "换个顺序试试，也可以再看便条。")
		return
	q.stage = 3
	progress.pattern(entry.sentence)
	progress.save()
	_refresh()
	_personal()

func _personal() -> void:
	var p = _dialog("My " + topic + " page", _help(catalog[_quest().target].question + " Your choice is yours.", "点选你自己的图片，不计对错。"), "personal")
	var ids: Array = by_topic[topic]
	var visible: Array = _pool() if photo_page < 0 else ids.slice(photo_page * 4, mini(photo_page * 4 + 4, ids.size()))
	for i in range(visible.size()):
		var id: String = visible[i]
		_card(p, id, 30 + i * 311, _personal_choice.bind(id), "favorite")
	_replay(p, catalog[_quest().target].question)
	UI.button(p, "More choices", Rect2(850, 538, 410, 110), func(): photo_page = ((photo_page + 2) % 6) - 1; _personal(), false, 33)

func _personal_choice(id: String) -> void:
	_quest().favorite = id
	_quest().stage = 4
	progress.word(id, "practised")
	progress.save()
	_refresh()
	_speaking()

func _speaking() -> void:
	var entry: Dictionary = catalog[_quest().favorite]
	var p = _dialog("Say it together", _help("Tell Pip your choice. Ask someone about theirs.", "看词卡，和大人一起说。说完后请大人确认。"), "speaking")
	UI.picture(p, _texture(entry.id), Rect2(45, 169, 270, 285))
	UI.label(p, entry.sentence, Rect2(365, 175, 850, 168), 44)
	UI.label(p, entry.question, Rect2(365, 365, 850, 100), 37, UI.TEAL)
	_replay(p, entry.sentence)
	UI.button(p, "We said it", Rect2(850, 538, 410, 110), _confirm_speaking, true, 36)
	if sound.say(entry.sentence): progress.word(entry.id, "heard")

func _confirm_speaking() -> void:
	var q = _quest()
	q.stage = 5
	progress.data.speaking_participation += 1
	progress.pattern(catalog[q.favorite].question)
	if not q.target in q.completed: q.completed.append(q.target)
	if not topic in progress.data.festival_stamps: progress.data.festival_stamps.append(topic)
	if not ("festival_" + topic) in progress.data.completed_missions: progress.data.completed_missions.append("festival_" + topic)
	progress.save()
	celebration = 4
	sound.chime()
	_refresh()
	_finished()

func _finished() -> void:
	var q = _quest()
	var p = _dialog("The display is ready!", _help("Your pictures helped the festival.", "完成了！可以继续接任务，或去别的地方。"), "finished")
	UI.picture(p, _texture(q.target), Rect2(110, 177, 300, 288))
	UI.picture(p, _texture(q.favorite), Rect2(740, 177, 300, 288))
	UI.label(p, ROOMS[room].npc + "'s picture", Rect2(70, 448, 430, 50), 31)
	UI.label(p, "My picture", Rect2(740, 448, 430, 50), 31)
	UI.button(p, "See the display", Rect2(30, 538, 400, 110), _clear, true, 32)
	UI.button(p, "Another request", Rect2(820, 538, 440, 110), _next_request, false, 32)

func _next_request() -> void:
	var q = _quest()
	q.round = int(q.round) + 1
	q.target = ""
	q.carrying = ""
	q.stage = 0
	q.translation_help = false
	photo_page = -1
	_quest()
	progress.save()
	_refresh()
	_request()

func _start_practice(mode: String) -> void:
	practice_mode = mode
	if mode == "translation": _quest().translation_help = true
	practice_correct = false
	practice_target = _quest().target
	practice_pool = _pool()
	practice_pool.shuffle()
	progress.data.practice_serial += 1
	practice_serial = int(progress.data.practice_serial)
	progress.save()
	_practice_panel()

func _practice_panel() -> void:
	var translate = practice_mode == "translation"
	var p = _dialog("Translation game" if translate else "Match the display label", _help("Chinese → English" if translate else "Choose the English word for this picture.", "这是翻译配对：看中文，选英文。" if translate else "看图，点选英文词卡。"), "translation" if translate else "word")
	# This is the ONLY target-language Chinese renderer in the festival trail.
	if translate: UI.label(p, catalog[practice_target].zh, Rect2(40, 184, 335, 243), 47)
	else: UI.picture(p, _texture(practice_target), Rect2(45, 170, 310, 285))
	for i in range(practice_pool.size()):
		var id: String = practice_pool[i]
		var b = UI.button(p, catalog[id].en, Rect2(420 + (i % 2) * 414, 172 + (i / 2) * 151, 395, 138), _answer.bind(id), false, 33)
		b.set_meta("semantic", "answer:" + id)
	UI.button(p, "Back to the shelf", Rect2(750, 538, 510, 110), _shelf, false, 32)
	if practice_correct: feedback.text = _help("Yes! They match.", "配对成功！返回后可以继续任务。")

func _answer(id: String) -> void:
	if practice_correct: return
	if progress.assess("trail_practice_" + str(practice_serial), practice_mode, id, practice_target, false, practice_target):
		practice_correct = true
		_practice_panel()
		sound.chime()
		if sound.say(catalog[id].en): progress.word(id, "heard")
	else:
		feedback.text = _help("Try another card.", "再选一张试试。")
		sound.say("Try again.")

func _passport() -> void:
	var p = _dialog("My festival passport", _help("One helpful mission for each festival team.", "每帮一组完成任务，就能盖一个章。"), "passport")
	for i in range(TOPICS.size()):
		var key: String = TOPICS[i]
		var done = key in progress.data.festival_stamps
		var row = UI.panel(p, Rect2(35 + (i % 2) * 620, 170 + (i / 2) * 78, 590, 66), Color("d8eee1") if done else UI.CREAM)
		UI.label(row, ("✓  " if done else "○  ") + key.capitalize(), Rect2(18, 0, 560, 65), 33)
	if progress.data.festival_stamps.size() == 8:
		feedback.text = "All eight festival teams are ready!"
	UI.button(p, "Back to exploring", Rect2(750, 538, 510, 110), _clear, true, 33)

func _return_cafe() -> void:
	_clear()
	sound.stop()
	sound.music.stop()
	host.show()
	host.ui.show()
	host.set_physics_process(true)
	host.set_process_input(true)
	host.set_process_unhandled_input(true)
	host._refresh()
	host.sound.begin()
	queue_free()

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_ESCAPE: _clear(); get_viewport().set_input_as_handled()
		elif event.keycode in [KEY_E, KEY_ENTER] and not is_instance_valid(modal): _context(); get_viewport().set_input_as_handled()
	if is_instance_valid(modal): return
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed and event.position.distance_to(Vector2(165, 842)) < 100:
			dragging = true
			target_point = Vector2(-1, -1)
			pending = ""
			joystick = ((event.position - Vector2(165, 842)) / 65).limit_length()
			get_viewport().set_input_as_handled()
		elif not event.pressed and dragging:
			dragging = false
			joystick = Vector2.ZERO
			get_viewport().set_input_as_handled()
	elif event is InputEventMouseMotion and dragging:
		joystick = ((event.position - Vector2(165, 842)) / 65).limit_length()
		get_viewport().set_input_as_handled()

func _unhandled_input(event: InputEvent) -> void:
	if is_instance_valid(modal): return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var bounds = Rect2(350, 250, 780, 540) if room.is_empty() else FLOOR
		if bounds.has_point(event.position): target_point = event.position; pending = ""

func _physics_process(delta: float) -> void:
	clock += delta
	celebration = maxf(0, celebration - delta)
	var direction = Vector2.ZERO
	if not is_instance_valid(modal):
		direction = Vector2(float(Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT)) - float(Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT)), float(Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN)) - float(Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP)))
		if direction.length() > 0: target_point = Vector2(-1, -1); pending = ""
		elif dragging: direction = joystick
		elif target_point.x >= 0:
			if alan.position.distance_to(target_point) < 8:
				target_point = Vector2(-1, -1)
				var action = pending
				pending = ""
				if not action.is_empty():
					if room.is_empty(): _enter_room(action)
					elif action == "map": _enter_map()
					elif action == "shelf": _shelf()
					else: _request()
			else: direction = (target_point - alan.position).normalized()
	var point = alan.position + direction.limit_length() * 260 * delta
	var bounds = Rect2(290, 240, 940, 565) if room.is_empty() else FLOOR
	alan.position = point.clamp(bounds.position, bounds.end)
	alan.speed = direction.length() * 260
	if absf(direction.x) > 0.05: alan.facing = signf(direction.x)
	if not is_instance_valid(modal): pip.position = pip.position.lerp(alan.position + Vector2(-72, 25), 1 - exp(-delta * 3))
	alan.z_index = int(alan.position.y)
	pip.z_index = int(pip.position.y)
	if npc.visible: npc.scale.y = 0.24 + sin(clock * 1.8) * 0.0007
	if not room.is_empty() and is_instance_valid(context_button):
		context_button.text = "Explore the picture shelf" if alan.position.distance_to(SHELF_POS) < 120 else "Talk to " + ROOMS[room].npc
	snapshot_clock += delta
	if snapshot_clock > 0.20: snapshot_clock = 0; _snapshot()
	queue_redraw()

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		dragging = false
		joystick = Vector2.ZERO
		target_point = Vector2(-1, -1)
		pending = ""
		if sound: sound.stop()

func _draw() -> void:
	if not is_instance_valid(alan): return
	if not is_instance_valid(modal):
		draw_circle(Vector2(165, 842), 85, Color(1, 0.98, 0.88, 0.85), true, -1, true)
		draw_circle(Vector2(165, 842) + joystick * 44, 31, UI.TEAL, true, -1, true)
	if not room.is_empty():
		var q = _quest()
		var completed: Array = q.completed
		for i in range(mini(completed.size(), 4)):
			draw_style_box(UI.box(UI.CREAM, UI.GOLD, 7), Rect2(292 + i * 90, 252, 84, 81))
			draw_texture_rect(_texture(completed[i]), Rect2(296 + i * 90, 257, 76, 70), false)
		if topic in progress.data.festival_stamps:
			for i in range(10):
				var x = 280 + i * 31
				var y = 215 + sin(float(i) / 9 * PI) * 20
				draw_colored_polygon(PackedVector2Array([Vector2(x, y), Vector2(x + 24, y), Vector2(x + 12 + sin(clock + i) * 2, y + 26)]), [UI.TEAL, UI.CORAL, UI.GOLD][i % 3])
	if celebration > 0:
		for i in range(40):
			draw_rect(Rect2(fposmod(i * 97 + sin(clock + i) * 30, 1440), fposmod(i * 79 + clock * 120, 960), 7, 5), [UI.GOLD, UI.CORAL, UI.TEAL][i % 3])

func _snapshot() -> void:
	if not OS.has_feature("web") or not OS.is_debug_build(): return
	var buttons: Array = []
	var labels: Array = []
	for node in ui.find_children("*", "Button", true, false):
		if node.is_visible_in_tree():
			var rect: Rect2 = node.get_global_rect()
			buttons.append({"text": node.text, "semantic": node.get_meta("semantic", ""), "disabled": node.disabled, "rect": [rect.position.x, rect.position.y, rect.size.x, rect.size.y]})
	for node in ui.find_children("*", "Label", true, false):
		if node.is_visible_in_tree(): labels.append(node.text)
	var data = {"tick": clock, "mode": "trail", "room": room, "topic": topic, "modal": modal_id, "position": [alan.position.x, alan.position.y], "buttons": buttons, "labels": labels, "quest": _quest() if not room.is_empty() else {}, "practice_target": practice_target, "voice_playing": sound.voice.playing, "stamps": progress.data.festival_stamps}
	JavaScriptBridge.eval("window.__alanTest=" + JSON.stringify(data))
