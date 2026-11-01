class_name IslandProgress
extends RefCounted

const SAVE_KEY = "alan-favorites-island-v1"
const SAVE_PATH = "user://alan-favorites-island-v1.json"
var data: Dictionary
var storage_ok = true

func defaults() -> Dictionary:
	return {"version": 1, "stage": 0, "target": "pizza", "carrying": "", "favorite": "", "festival": false, "festival_food": "", "completed_missions": [], "rounds_completed": 0, "words": {}, "patterns": {}, "tasks": [], "needs_practice": {}, "speaking_participation": 0, "practice_serial": 0, "topic_quests": {}, "festival_stamps": [], "cafe_translation_help": false, "settings": {"chinese": false, "voice": 0.85, "music": 0.24, "muted": false}}

func _init() -> void:
	data = defaults()
	var raw = ""
	if OS.has_feature("web"):
		var value = JavaScriptBridge.eval("(()=>{try{return localStorage.getItem('" + SAVE_KEY + "')||''}catch(e){return ''}})()")
		if value is String: raw = value
	elif FileAccess.file_exists(SAVE_PATH):
		raw = FileAccess.get_file_as_string(SAVE_PATH)
	var parsed = JSON.parse_string(raw) if not raw.is_empty() else null
	if parsed is Dictionary and parsed.get("version") == 1:
		for key in data:
			if not parsed.has(key): continue
			if typeof(data[key]) == TYPE_INT and typeof(parsed[key]) in [TYPE_INT, TYPE_FLOAT]:
				data[key] = int(parsed[key])
			elif typeof(parsed[key]) == typeof(data[key]): data[key] = parsed[key]
	data.stage = clampi(int(data.stage), 0, 6)
	var valid: Array = []
	for word_entry in JSON.parse_string(FileAccess.get_file_as_string("res://data/vocabulary.json")):
		if word_entry.topic == "food": valid.append(word_entry.en)
	if not data.target in valid: data.target = "pizza"
	if not data.favorite.is_empty() and not data.favorite in valid: data.favorite = ""
	if not data.carrying.is_empty() and not data.carrying in valid + ["noodles", "dumplings", "bread", "eggs"]: data.carrying = ""
	for key in defaults().settings:
		if not data.settings.has(key): data.settings[key] = defaults().settings[key]

func save() -> void:
	var json = JSON.stringify(data)
	if OS.has_feature("web"):
		storage_ok = bool(JavaScriptBridge.eval("(()=>{try{localStorage.setItem('" + SAVE_KEY + "'," + JSON.stringify(json) + ");return true}catch(e){return false}})()"))
	else:
		var f = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
		storage_ok = f != null
		if f: f.store_string(json)

func word(en: String, kind: String = "seen") -> void:
	if not data.words.has(en): data.words[en] = {"seen": 0, "heard": 0, "practised": 0}
	data.words[en][kind] = int(data.words[en].get(kind, 0)) + 1
	save()

func pattern(value: String) -> void:
	data.patterns[value] = int(data.patterns.get(value, 0)) + 1
	save()

func assess(task_id: String, kind: String, answer: String, expected: String, hinted: bool = false, practice_word: String = "") -> bool:
	var correct = answer == expected
	var prior = 0
	for task in data.tasks:
		if task.task_id == task_id: prior += 1
	data.tasks.append({"task_id": task_id, "kind": kind, "word": expected, "answer": answer, "correct": correct, "first_attempt": prior == 0, "hinted": hinted, "navigation_help": bool(data.settings.chinese), "translation_activity": kind.contains("translation") or kind.contains("meaning")})
	if not correct: data.needs_practice[expected] = true
	elif prior == 0 and data.needs_practice.has(expected): data.needs_practice.erase(expected)
	word(practice_word if not practice_word.is_empty() else (data.target if kind == "sentence_building" else expected), "practised")
	save()
	return correct

func first_attempt_stats() -> Vector2i:
	var stats = Vector2i.ZERO
	for task in data.tasks:
		if task.first_attempt:
			stats.y += 1
			if task.correct: stats.x += 1
	return stats

func export_summary() -> void:
	if OS.has_feature("web"):
		var json = JSON.stringify(data, "  ")
		JavaScriptBridge.eval("(()=>{const b=new Blob([" + JSON.stringify(json) + "],{type:'application/json'});const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='alan-island-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)})()")

func reset() -> void:
	data = defaults()
	save()
