extends Node2D

const UI = preload("res://scripts/island_ui.gd")
const Progress = preload("res://scripts/progress.gd")
const Audio = preload("res://scripts/island_audio.gd")
const Actor = preload("res://scripts/actor.gd")
const Scenery = preload("res://scripts/scenery.gd")
const GROUPS = [["pizza", "rice", "sandwich", "ice cream"], ["apple", "banana", "orange", "strawberry"], ["noodles", "dumplings", "bread", "eggs"]]
const COUNTERS = [Vector2(577, 425), Vector2(788, 425), Vector2(987, 425)]
const WALK = [Vector2(275, 330), Vector2(440, 330), Vector2(495, 390), Vector2(1130, 390), Vector2(1195, 465), Vector2(1210, 540), Vector2(1240, 590), Vector2(1160, 745), Vector2(1100, 825), Vector2(1040, 916), Vector2(410, 916), Vector2(350, 810), Vector2(315, 695), Vector2(290, 610), Vector2(235, 550), Vector2(260, 440)]
const GOALS = ["Meet Mina at the café.", "Find Mina's favorite food.", "Build Mina's sentence.", "Say it with Pip.", "Choose your own favorite.", "Visit the festival table.", "The café is ready!"]
const GOALS_ZH = ["去咖啡馆认识米娜。", "找到米娜最喜欢的食物。", "拼出米娜说的句子。", "和皮普一起说。", "选你自己最喜欢的食物。", "去节日餐桌看看。", "咖啡馆准备好了！"]

var progress = Progress.new()
var sound: IslandAudio
var scenery: IslandScenery
var alan: IslandActor
var pip: IslandActor
var mina: IslandActor
var ui: Control
var hud: Control
var modal: Control
var modal_id = ""
var objective: Label
var objective_zh: Label
var tray: Label
var interact: Button
var zh_button: Button
var settings_button: Button
var overlay_replay: Button
var overlay_hint: Label
var feedback: Label
var vocabulary: Array = []
var foods: Dictionary = {}
var texture_cache: Dictionary = {}
var destination = Vector2(-1, -1)
var pending = ""
var nearest = ""
var started = false
var welcome_name = false
var clock = 0.0
var save_clock = 0.0
var joystick = Vector2.ZERO
var joystick_active = false
var last_face = 1.0
var selected_chunks: Array[String] = []
var sentence_label: Label
var chunk_buttons: Array[Button] = []
var favorite_page = 0
var practice_group = 0
var practice_kind = "word"
var practice_target = ""
var practice_id = ""
var practice_done = false
var hint_used = false
var toast: Label
var toast_time = 0.0

func _ready() -> void:
	vocabulary = JSON.parse_string(FileAccess.get_file_as_string("res://data/vocabulary.json"))
	for value in vocabulary:
		if value.topic == "food": foods[value.en] = value
	sound = Audio.new()
	sound.settings = progress.data.settings
	add_child(sound)
	scenery = Scenery.new()
	add_child(scenery)
	for kind in ["alan", "pip", "mina"]:
		var actor = Actor.new()
		actor.kind = kind
		add_child(actor)
		match kind:
			"alan": alan = actor
			"pip": pip = actor
			"mina": mina = actor
	alan.position = Vector2(720, 780)
	pip.position = Vector2(625, 800)
	mina.position = Vector2(1160, 550)
	var layer = CanvasLayer.new()
	add_child(layer)
	ui = Control.new()
	ui.theme = UI.theme()
	ui.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(ui)
	_build_hud()
	_refresh()
	welcome_name = progress.data.patterns.has("My name is Alan.")
	_welcome()

func _build_hud() -> void:
	hud = Control.new()
	hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(hud)
	var title = UI.panel(hud, Rect2(22, 20, 395, 114), Color("fff7de"))
	UI.label(title, "Favorites Island", Rect2(20, 3, 360, 66), 39)
	UI.label(title, "ALAN  +  PIP   /   SEASIDE CAFÉ", Rect2(22, 67, 354, 30), 21, UI.TEAL)
	var quest = UI.panel(hud, Rect2(430, 20, 535, 114), Color("fff7de"))
	objective = UI.label(quest, "", Rect2(20, 5, 496, 65), 33)
	objective_zh = UI.label(quest, "", Rect2(20, 72, 496, 30), 25, UI.TEAL)
	zh_button = UI.button(hud, "中文", Rect2(978, 20, 133, 114), _toggle_chinese, false, 34)
	UI.button(hud, "Album", Rect2(1121, 20, 144, 114), func(): _album(false), false, 31)
	settings_button = UI.button(hud, "Menu", Rect2(1275, 20, 143, 114), _settings, false, 31)
	for i in range(3):
		var value = ["Meals", "Fruit", "Bakery"][i]
		var rect = Rect2(COUNTERS[i].x - 90, 328, 180, 81)
		UI.button(hud, value, rect, _approach.bind("counter" + str(i)), false, 30)
	UI.button(hud, "Festival", Rect2(255, 256, 215, 83), _approach.bind("festival"), false, 30)
	UI.button(hud, "Mina", Rect2(1085, 208, 165, 84), _approach.bind("mina"), false, 32)
	var bottom = UI.panel(hud, Rect2(334, 824, 1084, 114), Color("fff7de"))
	tray = UI.label(bottom, "Tap the path to walk.", Rect2(22, 7, 470, 96), 32)
	interact = UI.button(bottom, "Meet Mina", Rect2(510, 6, 550, 102), _interact, true, 33)
	toast = UI.label(hud, "", Rect2(405, 718, 850, 86), 34, Color.WHITE)
	toast.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	toast.add_theme_color_override("font_shadow_color", Color("254e4a"))
	toast.add_theme_constant_override("shadow_outline_size", 8)

func _refresh() -> void:
	var stage = int(progress.data.stage)
	objective.text = GOALS[stage]
	objective_zh.text = GOALS_ZH[stage] if progress.data.settings.chinese else ""
	zh_button.text = "中文"
	zh_button.add_theme_stylebox_override("normal", UI.box(Color("d8eee1") if progress.data.settings.chinese else UI.CREAM))
	tray.text = "Carrying: " + progress.data.carrying if not progress.data.carrying.is_empty() else "Tap the path to walk."
	alan.carried_texture = _food_texture(progress.data.carrying) if not progress.data.carrying.is_empty() else null
	scenery.festival = progress.data.festival
	scenery.delivered = stage >= 2
	var displayed_food: String = progress.data.target if stage >= 2 else progress.data.festival_food
	scenery.meal_texture = _food_texture(displayed_food) if not displayed_food.is_empty() else null
	scenery.album_texture = _food_texture(progress.data.favorite) if not progress.data.favorite.is_empty() else null

func _food_texture(en: String) -> Texture2D:
	if not foods.has(en): return null
	if not texture_cache.has(en): texture_cache[en] = load("res://" + foods[en].illustration)
	return texture_cache[en]

func _sentence(en: String) -> String:
	return foods[en].sentence

func _hint(en: String, zh: String) -> String:
	return en + ("\n" + zh if progress.data.settings.chinese else "")

func _toggle_chinese() -> void:
	progress.data.settings.chinese = not progress.data.settings.chinese
	if is_instance_valid(modal): hint_used = true
	progress.save()
	_refresh()
	if not is_instance_valid(modal): return
	match modal_id:
		"welcome": _welcome()
		"name": _name_card()
		"resident": _resident()
		"sentence": _sentence_board()
		"speak": _speak()
		"album": _album(int(progress.data.stage) == 4)
		"favorite": _favorite_card()
		"festival": _festival_card()
		"menu": _counter(practice_group)
		"practice": _show_practice()
		_: pass

func _clear_modal() -> void:
	sound.stop()
	if is_instance_valid(modal):
		ui.remove_child(modal)
		modal.queue_free()
	modal = null
	modal_id = ""
	selected_chunks.clear()
	chunk_buttons.clear()
	joystick = Vector2.ZERO
	joystick_active = false

func _dialog(title: String, subtitle: String, kind: String) -> Panel:
	_clear_modal()
	modal_id = kind
	destination = Vector2(-1, -1)
	pending = ""
	modal = Control.new()
	ui.add_child(modal)
	var shade = ColorRect.new()
	shade.color = Color(0.04, 0.16, 0.16, 0.56)
	shade.size = Vector2(1440, 960)
	modal.add_child(shade)
	var panel = UI.panel(modal, Rect2(70, 156, 1300, 650), Color("fff9e8"))
	UI.label(panel, title, Rect2(32, 10, 865, 66), 43)
	overlay_hint = UI.label(panel, subtitle, Rect2(32, 80, 1050, 80), 31, UI.TEAL)
	UI.button(panel, "Close", Rect2(1110, 16, 162, 104), _clear_modal, false, 30)
	UI.button(panel, "中文 ✓" if progress.data.settings.chinese else "中文", Rect2(930, 16, 162, 104), _toggle_chinese, false, 30)
	feedback = UI.label(panel, "", Rect2(32, 494, 1210, 54), 31, UI.TEAL)
	return panel

func _voice_button(panel: Node, line: String, at: Rect2 = Rect2(32, 538, 245, 102)) -> void:
	if not sound.has_line(line): return
	UI.button(panel, "▶  Replay", at, func(): sound.say(line), false, 32)

func _welcome() -> void:
	var p = _dialog("Hello, Alan! I'm Pip.", _hint("Let's help Mina get ready for the Favorites Festival.", "帮米娜准备喜好节吧。"), "welcome")
	UI.picture(p, preload("res://assets/art/pip.png"), Rect2(70, 173, 230, 330))
	UI.label(p, "Walk. Listen. Help.\nFind what makes us smile.", Rect2(360, 191, 805, 170), 47)
	UI.label(p, _hint("Tap a path or use the arrow keys.", "点击小路，也可以用方向键移动。"), Rect2(360, 360, 800, 103), 33)
	_voice_button(p, "Hello, Allen! I am Pip. Let us explore the island together.")
	UI.button(p, "Let's go!", Rect2(850, 538, 410, 102), func():
		started = true
		sound.begin()
		progress.save()
		if not welcome_name:
			_name_card()
		else: _clear_modal()
	, true, 37)

func _name_card() -> void:
	welcome_name = true
	var p = _dialog("Alan meets Pip", _hint("Say hello together.", "一起打个招呼吧。"), "name")
	UI.picture(p, preload("res://assets/art/pip.png"), Rect2(54, 170, 205, 300))
	UI.label(p, "My name is Alan.", Rect2(330, 202, 880, 140), 58)
	if progress.data.settings.chinese: UI.label(p, "我叫艾伦。", Rect2(330, 345, 880, 62), 37, UI.TEAL)
	UI.label(p, _hint("Now let's meet Mina.", "现在去认识米娜。"), Rect2(330, 415, 880, 80), 32)
	UI.button(p, "We said it", Rect2(32, 538, 390, 102), func():
		progress.data.speaking_participation += 1
		progress.pattern("My name is Alan.")
		_clear_modal()
	, true, 36)
	UI.button(p, "Go explore", Rect2(850, 538, 410, 102), _clear_modal, false, 35)

func _approach(id: String) -> void:
	if is_instance_valid(modal): return
	pending = id
	match id:
		"mina": destination = Vector2(1080, 552)
		"festival": destination = Vector2(405, 355)
		_: destination = COUNTERS[int(id.right(1))] + Vector2(0, 50)

func _resident() -> void:
	var stage = int(progress.data.stage)
	if stage == 2:
		_sentence_board()
		return
	if stage == 3:
		_speak()
		return
	if stage == 4:
		_album(true)
		return
	if stage >= 5:
		var p = _dialog("Mina", _hint("Our festival table is waiting!", "节日餐桌在等我们！"), "resident")
		UI.picture(p, _food_texture(progress.data.target), Rect2(70, 175, 310, 270))
		UI.label(p, _sentence(progress.data.target), Rect2(430, 187, 760, 180), 48)
		_voice_button(p, _sentence(progress.data.target))
		UI.button(p, "To the festival table", Rect2(750, 538, 510, 102), func(): _clear_modal(); _approach("festival"), true)
		return
	var p = _dialog("Mina's festival order", _hint("Listen to Mina. Find her favorite.", "听米娜说，找到她最喜欢的食物。"), "resident")
	UI.label(p, _sentence(progress.data.target), Rect2(52, 190, 1180, 140), 50)
	if progress.data.settings.chinese: UI.label(p, foods[progress.data.target].meaning, Rect2(52, 347, 1180, 67), 35, UI.TEAL)
	_voice_button(p, _sentence(progress.data.target))
	if stage == 0:
		UI.button(p, "I'll find it!", Rect2(850, 538, 410, 102), func():
			progress.data.stage = 1
			progress.pattern("My favorite food is ___.")
			progress.word(progress.data.target, "heard")
			progress.save()
			_clear_modal()
			_refresh()
		, true, 37)
	elif progress.data.carrying.is_empty():
		UI.button(p, "Look at the food stalls", Rect2(700, 538, 560, 102), _clear_modal, true)
	else:
		UI.label(p, "Your tray: " + progress.data.carrying, Rect2(52, 424, 1180, 64), 36)
		UI.button(p, "Give " + progress.data.carrying, Rect2(700, 538, 560, 102), _deliver, true)
	sound.say(_sentence(progress.data.target))

func _deliver() -> void:
	var correct = progress.assess("delivery_" + str(progress.data.rounds_completed), "listen_and_deliver", progress.data.carrying, progress.data.target, hint_used)
	if not correct:
		feedback.text = _hint("Listen again. You can change your tray.", "再听一遍，可以换一种食物。")
		sound.say("Try again.")
		return
	progress.data.stage = 2
	progress.data.carrying = ""
	progress.save()
	_refresh()
	sound.chime()
	_sentence_board()

func _counter(index: int) -> void:
	practice_group = index
	var p = _dialog(["Mina's meal stall", "Mina's fruit stall", "Mina's bakery stall"][index], _hint("Pick something for your tray, or try a menu game.", "给托盘选食物，或者玩菜单游戏。"), "menu")
	for i in range(4):
		var en: String = GROUPS[index][i]
		var x = 30 + i * 311
		var b = UI.button(p, "", Rect2(x, 170, 295, 272), _pick_food.bind(en))
		b.set_meta("semantic", "food:" + en)
		UI.picture(b, _food_texture(en), Rect2(40, 7, 215, 145))
		var value = en + ("\n" + foods[en].zh if progress.data.settings.chinese else "")
		var l = UI.label(b, value, Rect2(8, 154, 279, 112), 38)
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		progress.word(en)
	UI.button(p, "Picture + word", Rect2(30, 538, 390, 102), _practice_start.bind(index, "word"), false, 32)
	UI.button(p, "中文 + English", Rect2(450, 538, 390, 102), _practice_start.bind(index, "meaning"), false, 31)
	if index != 2:
		UI.button(p, "Listen + find", Rect2(870, 538, 390, 102), _practice_start.bind(index, "listen"), true, 32)
	else:
		UI.label(p, _hint("Look, match, and say together.", "看一看，配一配，一起说。"), Rect2(870, 538, 390, 102), 29)

func _pick_food(en: String) -> void:
	progress.data.carrying = en
	progress.word(en, "practised")
	progress.save()
	_clear_modal()
	_refresh()
	_toast("On your tray: " + en)
	if sound.has_line(en): sound.say(en); progress.word(en, "heard")

func _sentence_board() -> void:
	var p = _dialog("Mina's order card", _hint("Build the sentence Mina said.", "拼出米娜说的句子。"), "sentence")
	UI.picture(p, _food_texture(progress.data.target), Rect2(30, 156, 190, 170))
	sentence_label = UI.label(p, "Tap the word pieces.", Rect2(245, 172, 1000, 127), 45)
	var choices = ["food", "My favorite", foods[progress.data.target].sentence_value + ".", "are", "is", "sport"]
	for i in range(choices.size()):
		var text: String = choices[i]
		var b = UI.button(p, text, Rect2(30 + (i % 3) * 416, 325 + (i / 3) * 94, 398, 86), _chunk.bind(text, i), false, 34)
		chunk_buttons.append(b)
	_voice_button(p, _sentence(progress.data.target), Rect2(30, 538, 310, 102))
	UI.button(p, "Start again", Rect2(373, 538, 335, 102), _reset_chunks, false, 33)
	UI.button(p, "Check sentence", Rect2(740, 538, 520, 102), _check_sentence, true, 35)
	sound.say(_sentence(progress.data.target))

func _chunk(value: String, index: int) -> void:
	if selected_chunks.size() >= 4: return
	selected_chunks.append(value)
	chunk_buttons[index].disabled = true
	sentence_label.text = " ".join(selected_chunks)
	feedback.text = ""

func _reset_chunks() -> void:
	selected_chunks.clear()
	for b in chunk_buttons: b.disabled = false
	sentence_label.text = "Tap the word pieces."
	feedback.text = ""

func _check_sentence() -> void:
	var answer = " ".join(selected_chunks)
	var correct = progress.assess("sentence_" + str(progress.data.rounds_completed), "sentence_building", answer, _sentence(progress.data.target), hint_used)
	if not correct:
		feedback.text = _hint("Listen, then try another order.", "听一听，再换个顺序试试。")
		sound.say("Try again.")
		return
	progress.data.stage = 3
	progress.pattern("My favorite food is ___.")
	progress.save()
	_refresh()
	sound.chime()
	_speak()

func _speak() -> void:
	var p = _dialog("Say it with Pip", _hint("Listen. Say the sentence together.", "听一听，一起说这句话。"), "speak")
	UI.picture(p, _food_texture(progress.data.target), Rect2(60, 185, 240, 260))
	UI.label(p, _sentence(progress.data.target), Rect2(360, 180, 845, 158), 47)
	if progress.data.settings.chinese: UI.label(p, foods[progress.data.target].meaning, Rect2(360, 350, 840, 80), 34, UI.TEAL)
	_voice_button(p, _sentence(progress.data.target))
	UI.button(p, "We said it", Rect2(850, 538, 410, 102), func():
		progress.data.speaking_participation += 1
		progress.data.stage = 4
		progress.save()
		_refresh()
		_album(true)
	, true, 36)
	sound.say(_sentence(progress.data.target))

func _album(_choosing: bool) -> void:
	var p = _dialog("My favorites album", _hint("What's your favorite food? Every choice is yours.", "你最喜欢什么食物？选你喜欢的，都可以。"), "album")
	var group: Array = GROUPS[favorite_page]
	for i in range(4):
		var en: String = group[i]
		var b = UI.button(p, "", Rect2(30 + i * 311, 170, 295, 272), _choose_favorite.bind(en))
		b.set_meta("semantic", "favorite:" + en)
		UI.picture(b, _food_texture(en), Rect2(40, 7, 215, 145))
		var l = UI.label(b, en + ("\n" + foods[en].zh if progress.data.settings.chinese else ""), Rect2(8, 154, 279, 112), 38)
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		if en == progress.data.favorite: b.add_theme_stylebox_override("normal", UI.box(Color("d8eee1"), UI.TEAL))
	_voice_button(p, "What's your favorite food?")
	UI.button(p, "More foods", Rect2(850, 538, 410, 102), func(): favorite_page = 1 - favorite_page; _album(false), false, 34)
	sound.say("What's your favorite food?")

func _choose_favorite(en: String) -> void:
	# Personal preference is never graded or entered as comprehension accuracy.
	progress.data.favorite = en
	progress.word(en, "practised")
	progress.pattern("My favorite food is ___.")
	if int(progress.data.stage) == 4: progress.data.stage = 5
	progress.save()
	_refresh()
	_favorite_card()

func _favorite_card() -> void:
	var en: String = progress.data.favorite
	var p = _dialog("Alan's favorite", _hint("Your choice belongs in the festival!", "把你喜欢的食物带到喜好节！"), "favorite")
	UI.picture(p, _food_texture(en), Rect2(55, 160, 280, 300))
	UI.label(p, _sentence(en), Rect2(380, 180, 825, 155), 48)
	if progress.data.settings.chinese: UI.label(p, foods[en].meaning, Rect2(380, 335, 825, 78), 34, UI.TEAL)
	if en == progress.data.target: UI.label(p, "That's my favorite, too!", Rect2(380, 420, 825, 65), 36, UI.CORAL)
	_voice_button(p, _sentence(en), Rect2(30, 538, 300, 102))
	UI.button(p, "Hear “I like…”", Rect2(355, 538, 390, 102), func():
		sound.say("I like " + foods[en].sentence_value + ".")
		progress.pattern("I like ___.")
	, false, 32)
	UI.button(p, "Ask Pip", Rect2(780, 538, 480, 102), _ask_pip, true, 36)
	sound.say(_sentence(en))
	progress.word(en, "heard")

func _ask_pip() -> void:
	var p = _dialog("Ask Pip", _hint("Ask together, then hear Pip's favorite.", "一起问，再听皮普最喜欢的食物。"), "ask")
	UI.label(p, "What's your favorite food?", Rect2(70, 178, 1150, 150), 52)
	_voice_button(p, "What's your favorite food?")
	UI.button(p, "We said it", Rect2(850, 538, 410, 102), func():
		progress.data.speaking_participation += 1
		progress.pattern("What's your favorite food?")
		var q = _dialog("Pip's favorite", _hint("Let's bring our favorites to the festival table.", "一起把喜欢的食物带到节日餐桌。"), "ask_answer")
		UI.picture(q, _food_texture(progress.data.target), Rect2(80, 166, 265, 295))
		UI.label(q, _sentence(progress.data.target), Rect2(400, 180, 800, 180), 48)
		_voice_button(q, _sentence(progress.data.target))
		UI.button(q, "Back to the island", Rect2(750, 538, 510, 102), _clear_modal, true)
		sound.say(_sentence(progress.data.target))
	, true, 36)
	sound.say("What's your favorite food?")

func _festival_card() -> void:
	if int(progress.data.stage) < 5:
		var q = _dialog("Favorites Festival", _hint("Help Mina fill this table with favorite foods.", "帮米娜把喜欢的食物摆上节日餐桌。"), "festival")
		UI.picture(q, preload("res://assets/art/pip.png"), Rect2(70, 176, 200, 300))
		UI.label(q, GOALS[int(progress.data.stage)], Rect2(360, 200, 830, 150), 49)
		UI.button(q, "Let's help Mina", Rect2(750, 538, 510, 102), func(): _clear_modal(); _approach("mina"), true)
		return
	if int(progress.data.stage) == 5:
		progress.data.stage = 6
		progress.data.festival = true
		progress.data.festival_food = progress.data.target
		if not "cafe" in progress.data.completed_missions: progress.data.completed_missions.append("cafe")
		progress.data.rounds_completed += 1
		progress.save()
		scenery.confetti = 5
		sound.chime()
	_refresh()
	var p = _dialog("The café is ready!", _hint("You helped Mina. Our festival table is full of favorites.", "你帮助了米娜，节日餐桌准备好了！"), "festival")
	UI.picture(p, _food_texture(progress.data.target), Rect2(90, 170, 290, 270))
	UI.picture(p, _food_texture(progress.data.favorite), Rect2(510, 170, 290, 270))
	UI.picture(p, preload("res://assets/art/pip.png"), Rect2(950, 160, 210, 310))
	UI.label(p, "Mina's favorite", Rect2(65, 438, 360, 55), 32)
	UI.label(p, "Alan's favorite", Rect2(490, 438, 360, 55), 32)
	UI.button(p, "See our table", Rect2(30, 538, 400, 102), _clear_modal, true, 34)
	UI.button(p, "Help Mina again", Rect2(820, 538, 440, 102), _new_round, false, 34)
	sound.say("Yes!")

func _new_round() -> void:
	var options: Array = GROUPS[0] + GROUPS[1]
	var previous: String = progress.data.target
	options.erase(previous)
	progress.data.target = options.pick_random()
	progress.data.stage = 0
	progress.data.carrying = ""
	hint_used = false
	progress.save()
	_clear_modal()
	_refresh()
	_approach("mina")

func _practice_start(index: int, kind: String) -> void:
	practice_group = index
	practice_kind = kind
	practice_target = GROUPS[index].pick_random()
	progress.data.practice_serial += 1
	practice_id = "menu_" + str(progress.data.practice_serial)
	practice_done = false
	hint_used = false
	progress.save()
	_show_practice()

func _show_practice() -> void:
	var prompt_text = {"word": "Which word matches?", "meaning": "Match the menu meaning.", "listen": "Listen and find."}[practice_kind]
	var p = _dialog("Mina's menu game", _hint(prompt_text, {"word": "哪个单词配这张图？", "meaning": "把中文和英文配起来。", "listen": "听一听，找到食物。"}[practice_kind]), "practice")
	var question = GROUPS[practice_group].duplicate()
	question.shuffle()
	if practice_kind == "word":
		UI.picture(p, _food_texture(practice_target), Rect2(70, 169, 300, 285))
	elif practice_kind == "meaning":
		UI.label(p, foods[practice_target].zh, Rect2(70, 200, 300, 190), 58)
	else:
		UI.picture(p, preload("res://assets/art/pip.png"), Rect2(110, 168, 215, 300))
	for i in range(4):
		var en: String = question[i]
		var rect = Rect2(420 + (i % 2) * 414, 173 + (i / 2) * 150, 395, 135)
		var b = UI.button(p, en if practice_kind != "listen" else "", rect, _practice_answer.bind(en), false, 35)
		if practice_kind == "listen": UI.picture(b, _food_texture(en), Rect2(120, 3, 155, 125))
	if practice_kind == "listen":
		_voice_button(p, "Find " + practice_target + ".")
		sound.say("Find " + practice_target + ".")
		progress.word(practice_target, "heard")
	UI.button(p, "Back to the stall", Rect2(750, 538, 510, 102), _counter.bind(practice_group), false, 34)
	if practice_done:
		feedback.text = _hint("Yes! They match.", "对了，配对成功！")
		UI.button(p, "Another menu game", Rect2(30, 538, 650, 102), _practice_start.bind(practice_group, practice_kind), true, 34)

func _practice_answer(en: String) -> void:
	if practice_done: return
	var correct = progress.assess(practice_id, practice_kind + "_matching", en, practice_target, hint_used)
	if correct:
		practice_done = true
		_show_practice()
		sound.chime()
		if sound.has_line(practice_target): sound.say(practice_target)
	else:
		feedback.text = _hint("Look again. You can try another.", "再看看，换一个试试。")
		sound.say("Try again.")

func _settings() -> void:
	var p = _dialog("Island menu", "", "settings")
	UI.label(p, "Jesse's voice", Rect2(40, 165, 400, 70), 37)
	UI.label(p, "Music", Rect2(40, 285, 400, 70), 37)
	for row in range(2):
		var slider = HSlider.new()
		slider.position = Vector2(440, 175 + row * 120)
		slider.size = Vector2(770, 80)
		slider.min_value = 0
		slider.max_value = 1
		slider.step = 0.05
		var key = "voice" if row == 0 else "music"
		slider.value = float(progress.data.settings[key])
		slider.value_changed.connect(func(value): progress.data.settings[key] = value; progress.save())
		p.add_child(slider)
	UI.button(p, "Unmute all" if progress.data.settings.muted else "Mute all", Rect2(40, 415, 360, 104), func():
		progress.data.settings.muted = not progress.data.settings.muted
		progress.save()
		_settings()
	, false, 32)
	UI.button(p, "Replay voice", Rect2(440, 415, 360, 104), func(): sound.say("What's your favorite food?"), false, 31)
	UI.button(p, "Teacher", Rect2(840, 415, 370, 104), _teacher, false, 33)
	UI.button(p, "Back to the island", Rect2(750, 538, 510, 102), _clear_modal, true)

func _teacher() -> void:
	var p = _dialog("Teacher summary", "Saved on this device only. No learner account.", "teacher")
	var stats = progress.first_attempt_stats()
	var summary = "Missions: %d     Café rounds: %d\nFirst attempts: %d / %d correct\nSpeaking participation: %d confirmations\n" % [progress.data.completed_missions.size(), progress.data.rounds_completed, stats.x, stats.y, progress.data.speaking_participation]
	summary += "Speaking is participation, not verified pronunciation.\n"
	summary += "Patterns: " + (", ".join(progress.data.patterns.keys()) if not progress.data.patterns.is_empty() else "None yet") + "\n"
	summary += "Further practice: " + (", ".join(progress.data.needs_practice.keys()) if not progress.data.needs_practice.is_empty() else "None recorded") + "\n"
	var words: Array[String] = []
	for en in progress.data.words:
		var value: Dictionary = progress.data.words[en]
		words.append(en + "  [seen %d / heard %d / practised %d]" % [value.seen, value.heard, value.practised])
	summary += "Words:\n" + "\n".join(words) + "\n\n"
	summary += "Personal favorites are never graded. Hints are logged separately.\n"
	summary += "12 food pictures; 8 fully voiced foods. Bakery words await Jesse sample approval.\n"
	summary += "Eight topics × 18 card-verified entries are in the data. Other island locations await café review.\n"
	if not progress.storage_ok: summary += "Storage is unavailable. This session cannot be saved.\n"
	var scroll = ScrollContainer.new()
	scroll.position = Vector2(32, 166)
	scroll.size = Vector2(1230, 353)
	p.add_child(scroll)
	var body = Label.new()
	body.text = summary
	body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	body.custom_minimum_size = Vector2(1170, 0)
	body.add_theme_font_size_override("font_size", 27)
	scroll.add_child(body)
	UI.button(p, "Export summary", Rect2(30, 538, 470, 102), progress.export_summary, false, 32)
	UI.button(p, "Reset progress", Rect2(790, 538, 470, 102), _reset_confirm, false, 32)

func _reset_confirm() -> void:
	var p = _dialog("Reset this device's progress?", "This clears missions, favorites, practice records and settings.", "reset")
	UI.label(p, "Start a new island visit?", Rect2(80, 190, 1140, 180), 54)
	UI.button(p, "Keep progress", Rect2(30, 538, 470, 102), _teacher, true, 34)
	UI.button(p, "Reset everything", Rect2(790, 538, 470, 102), func():
		progress.reset()
		sound.settings = progress.data.settings
		favorite_page = 0
		hint_used = false
		alan.position = Vector2(720, 780)
		pip.position = Vector2(625, 800)
		_refresh()
		_welcome()
	, false, 34)

func _interact() -> void:
	if is_instance_valid(modal): return
	if nearest.is_empty():
		_approach("festival" if int(progress.data.stage) >= 5 else "mina")
		return
	match nearest:
		"mina": _resident()
		"festival": _festival_card()
		_: _counter(int(nearest.right(1)))

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_ESCAPE:
			_clear_modal()
			get_viewport().set_input_as_handled()
		elif event.keycode in [KEY_E, KEY_ENTER] and not is_instance_valid(modal):
			_interact()
			get_viewport().set_input_as_handled()
	if is_instance_valid(modal): return
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed and event.position.distance_to(Vector2(165, 842)) < 106:
			joystick_active = true
			joystick = ((event.position - Vector2(165, 842)) / 65).limit_length()
			destination = Vector2(-1, -1)
			pending = ""
			get_viewport().set_input_as_handled()
		elif not event.pressed and joystick_active:
			joystick_active = false
			joystick = Vector2.ZERO
			get_viewport().set_input_as_handled()
	elif event is InputEventMouseMotion and joystick_active:
		joystick = ((event.position - Vector2(165, 842)) / 65).limit_length()
		get_viewport().set_input_as_handled()

func _unhandled_input(event: InputEvent) -> void:
	if is_instance_valid(modal): return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var point: Vector2 = event.position
		if point.distance_to(mina.position - Vector2(0, 100)) < 120:
			_approach("mina")
		elif point.x < 475 and point.y < 325:
			_approach("festival")
		elif Geometry2D.is_point_in_polygon(point, PackedVector2Array(WALK)):
			destination = point
			pending = ""

func _physics_process(delta: float) -> void:
	clock += delta
	var held = is_instance_valid(modal)
	var direction = Vector2.ZERO
	if not held:
		direction = Vector2(float(Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT)) - float(Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT)), float(Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN)) - float(Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP)))
		if direction.length() > 0: destination = Vector2(-1, -1); pending = ""
		elif joystick_active: direction = joystick
		elif destination.x >= 0:
			if alan.position.distance_to(destination) < 8:
				destination = Vector2(-1, -1)
				if not pending.is_empty():
					var action = pending
					pending = ""
					match action:
						"mina": _resident()
						"festival": _festival_card()
						_: _counter(int(action.right(1)))
			else: direction = (destination - alan.position).normalized()
	var step = direction.limit_length() * 235 * delta
	var next_position = alan.position + step
	if Geometry2D.is_point_in_polygon(next_position, PackedVector2Array(WALK)):
		alan.position = next_position
	else:
		# Sliding along a boundary preserves control without walking through furniture.
		if Geometry2D.is_point_in_polygon(alan.position + Vector2(step.x, 0), PackedVector2Array(WALK)): alan.position.x += step.x
		if Geometry2D.is_point_in_polygon(alan.position + Vector2(0, step.y), PackedVector2Array(WALK)): alan.position.y += step.y
	alan.speed = direction.length() * 235
	if absf(direction.x) > 0.05: alan.facing = signf(direction.x)
	var follow_goal = alan.position + Vector2(-80, 30)
	var follow_step = (follow_goal - pip.position) * (1 - exp(-delta * 3))
	if not held and Geometry2D.is_point_in_polygon(pip.position + follow_step, PackedVector2Array(WALK)):
		pip.position += follow_step
	for actor in [alan, pip, mina]: actor.z_index = int(actor.position.y)
	nearest = ""
	var distance = 120.0
	var targets = {"mina": Vector2(1080, 552), "festival": Vector2(405, 355), "counter0": COUNTERS[0] + Vector2(0, 50), "counter1": COUNTERS[1] + Vector2(0, 50), "counter2": COUNTERS[2] + Vector2(0, 50)}
	for id in targets:
		var d = alan.position.distance_to(targets[id])
		if d < distance: distance = d; nearest = id
	var title = "Talk to Mina"
	if nearest == "festival": title = "Visit festival table"
	elif nearest.begins_with("counter"): title = "Explore " + ["meals", "fruit", "bakery"][int(nearest.right(1))]
	elif nearest.is_empty() and int(progress.data.stage) >= 5: title = "To the festival table"
	interact.text = title
	toast_time = maxf(0, toast_time - delta)
	toast.visible = toast_time > 0 and not held
	save_clock += delta
	if save_clock > 0.25:
		save_clock = 0
		_publish_snapshot()
	queue_redraw()

func _draw() -> void:
	if not started or is_instance_valid(modal): return
	var base = Vector2(165, 842)
	draw_circle(base, 85, Color(1, 0.98, 0.88, 0.85), true, -1, true)
	draw_arc(base, 84, 0, TAU, 60, Color(0.17, 0.47, 0.42, 0.7), 3, true)
	for d in [Vector2(0, -1), Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0)]:
		draw_circle(base + d * 57, 6, Color("548a77"), true, -1, true)
	draw_circle(base + joystick * 44, 31, Color("297e72"), true, -1, true)
	if destination.x >= 0:
		draw_arc(destination, 16 + sin(clock * 5) * 3, 0, TAU, 32, Color(1, 0.96, 0.74, 0.8), 3, true)

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		joystick_active = false
		joystick = Vector2.ZERO
		destination = Vector2(-1, -1)
		pending = ""
		if sound: sound.stop()

func _toast(value: String) -> void:
	toast.text = value
	toast_time = 4

func _publish_snapshot() -> void:
	if not OS.has_feature("web") or not OS.is_debug_build(): return
	var buttons: Array = []
	for node in ui.find_children("*", "Button", true, false):
		if node.is_visible_in_tree():
			var r: Rect2 = node.get_global_rect()
			buttons.append({"text": node.text, "semantic": node.get_meta("semantic", ""), "rect": [r.position.x, r.position.y, r.size.x, r.size.y], "disabled": node.disabled})
	var snapshot = {"position": [alan.position.x, alan.position.y], "pip": [pip.position.x, pip.position.y], "modal": modal_id, "stage": progress.data.stage, "target": progress.data.target, "practice_target": practice_target, "voice_playing": sound.voice.playing, "voice_count": sound.played, "voice_volume": sound.voice.volume_db, "music_volume": sound.music.volume_db, "buttons": buttons, "festival": scenery.festival, "storage_ok": progress.storage_ok, "selected": selected_chunks}
	JavaScriptBridge.eval("window.__alanTest=" + JSON.stringify(snapshot))
