class_name GMState
extends RefCounted

const KEY = "far-horizon-gm-fast-2d-v1"
var data: Dictionary = {
	"version": 3, "layout_version": 3, "scene": "s2_malfunction", "cues": {}, "revealed": {},
	"leader": 0, "positions": {}, "routes": {}, "language": "zh", "clean": true,
	"seen": {}, "threats": [2, 1, 1], "sound": false, "voice": true
}
var storage_ok = true
var last_saved_value=""

func restore(story: GMStory) -> void:
	var raw = ""
	if OS.has_feature("web"):
		var value = JavaScriptBridge.eval("(function(){try{return localStorage.getItem('far-horizon-gm-fast-2d-v1')||'';}catch(e){return '';}})()", true)
		if value is String: raw = value
	elif FileAccess.file_exists("user://gm-fast-2d-v1.json"):
		raw = FileAccess.get_file_as_string("user://gm-fast-2d-v1.json")
	var parsed = JSON.parse_string(raw) if raw.strip_edges() != "" else null
	if parsed is Dictionary and parsed.get("version") == 3:
		for k in data:
			if parsed.has(k) and (typeof(parsed[k]) == typeof(data[k]) or (typeof(data[k]) in [TYPE_INT, TYPE_FLOAT] and typeof(parsed[k]) in [TYPE_INT, TYPE_FLOAT])):
				data[k] = parsed[k]
	if parsed is Dictionary and int(parsed.get("layout_version",0))<3:
		data.routes.clear()
	data.layout_version=3
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
	if value==last_saved_value:return
	if OS.has_feature("web"):
		storage_ok = bool(JavaScriptBridge.eval("(function(){try{localStorage.setItem('far-horizon-gm-fast-2d-v1'," + JSON.stringify(value) + ");return true;}catch(e){return false;}})()", true))
	else:
		var f = FileAccess.open("user://gm-fast-2d-v1.json.tmp", FileAccess.WRITE)
		storage_ok = f != null
		if f:
			f.store_string(value)
			f.close()
			storage_ok = DirAccess.rename_absolute("user://gm-fast-2d-v1.json.tmp", "user://gm-fast-2d-v1.json") == OK

	if storage_ok:last_saved_value=value
