class_name GMState
extends RefCounted

const KEY = "far-horizon-gm-v2"
var data: Dictionary = {
	"version": 2, "scene": "s1_terminal", "cues": {}, "revealed": {},
	"leader": 0, "positions": {}, "language": "zh", "clean": false,
	"seen": {}, "threats": [2, 1, 1], "sound": false, "voice": true
}
var storage_ok = true

func restore(story: GMStory) -> void:
	var raw = ""
	if OS.has_feature("web"):
		var value = JavaScriptBridge.eval("(function(){try{return localStorage.getItem('far-horizon-gm-v2')||'';}catch(e){return '';}})()", true)
		if value is String: raw = value
	elif FileAccess.file_exists("user://gm-visual-aid.json"):
		raw = FileAccess.get_file_as_string("user://gm-visual-aid.json")
	var parsed = JSON.parse_string(raw) if raw.strip_edges() != "" else null
	if parsed is Dictionary and parsed.get("version") == 2:
		for k in data:
			if parsed.has(k) and (typeof(parsed[k]) == typeof(data[k]) or (typeof(data[k]) in [TYPE_INT, TYPE_FLOAT] and typeof(parsed[k]) in [TYPE_INT, TYPE_FLOAT])):
				data[k] = parsed[k]
	if story.find_scene(str(data.scene)) < 0: data.scene = story.scenes[0].id
	data.leader = clampi(int(data.leader), 0, 3)
	if not data.language in ["zh", "ko", "ja"]: data.language = "zh"
	if data.threats.size() != 3: data.threats = [2, 1, 1]
	for i in range(3): data.threats[i] = clampi(int(data.threats[i]), 0, 2 if i == 0 else 1)
	for s in story.scenes:
		data.cues[s.id] = clampi(int(data.cues.get(s.id, 0)), 0, s.cues.size() - 1)
	for id in data.revealed.keys():
		if not story.clues.has(id): data.revealed.erase(id)

func save() -> void:
	var value = JSON.stringify(data)
	if OS.has_feature("web"):
		storage_ok = bool(JavaScriptBridge.eval("(function(){try{localStorage.setItem('far-horizon-gm-v2'," + JSON.stringify(value) + ");return true;}catch(e){return false;}})()", true))
	else:
		var f = FileAccess.open("user://gm-visual-aid.json.tmp", FileAccess.WRITE)
		storage_ok = f != null
		if f:
			f.store_string(value)
			f.close()
			storage_ok = DirAccess.rename_absolute("user://gm-visual-aid.json.tmp", "user://gm-visual-aid.json") == OK
