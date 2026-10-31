class_name CrewState
extends RefCounted

const WEB_KEY = "far-horizon-session1-v1"
const DEPARTMENTS = ["Flight", "Science", "Engineering", "Colony"]
const ROSTER = [
	["Orion Kade", "Lyra Seo", "Nova Lin", "Cai Mercer"],
	["Mira Volkov", "Jalen Rafiq", "Dax Ren", "Selene Park", "Theo Vale"],
	["Kai Mercer", "Elara Chen", "Vera Sol", "Milo Hart"],
	["Jae Orion", "Nia Rowan", "Zara Quinn", "Pax Rhee", "Luna Keung"]
]
const COLORS = [Color("8cdeef"), Color("b9dbc2"), Color("efbb70"), Color("e1a9b4")]
var data: Dictionary = {
	"version": 1, "scene": "terminal", "leader": 0, "position": 520.0,
	"representatives": ["Orion Kade", "Mira Volkov", "Kai Mercer", "Nia Rowan"],
	"records": {}, "paper": [false, false, false, false],
	"performed": [false, false, false, false], "deck_choices": {},
	"flags": {}, "transcript": [], "cue": 0, "script": {}, "script_paper": [false, false, false, false], "finished": false
}
var storage_ok = true

func restore() -> void:
	var serialized = ""
	if OS.has_feature("web"):
		var result = JavaScriptBridge.eval("(function(){try{return localStorage.getItem('" + WEB_KEY + "')||'';}catch(e){return '';}})()", true)
		if result is String:
			serialized = result
	elif FileAccess.file_exists("user://session-01.json"):
		serialized = FileAccess.get_file_as_string("user://session-01.json")
	if serialized.is_empty():
		return
	var loaded = JSON.parse_string(serialized)
	if not loaded is Dictionary or loaded.get("version") != 1:
		return
	for key in data:
		if loaded.has(key) and (typeof(loaded[key]) == typeof(data[key]) or (typeof(data[key]) in [TYPE_INT, TYPE_FLOAT] and typeof(loaded[key]) in [TYPE_INT, TYPE_FLOAT])):
			data[key] = loaded[key]
	if not data.scene in ["terminal", "launch", "habitation", "bridge", "ending"]:
		data.scene = "terminal"
	data.leader = clampi(int(data.leader), 0, 3)
	if data.representatives.size() != 4:
		data.representatives = ["Orion Kade", "Mira Volkov", "Kai Mercer", "Nia Rowan"]
	for i in range(4):
		if not data.representatives[i] in ROSTER[i]:
			data.representatives[i] = ROSTER[i][0]
	for key in ["paper", "performed", "script_paper"]:
		if data[key].size() != 4:
			data[key] = [false, false, false, false]
	data.cue = maxi(0, int(data.cue))
	data.position = clampf(float(data.position), 100.0, 2240.0)

func save() -> bool:
	var serialized = JSON.stringify(data)
	if OS.has_feature("web"):
		var result = JavaScriptBridge.eval("(function(){try{localStorage.setItem('" + WEB_KEY + "'," + JSON.stringify(serialized) + ");return true;}catch(e){return false;}})()", true)
		storage_ok = bool(result)
	else:
		var file = FileAccess.open("user://session-01.json.tmp", FileAccess.WRITE)
		storage_ok = file != null
		if file:
			file.store_string(serialized)
			file.close()
			storage_ok = DirAccess.rename_absolute("user://session-01.json.tmp", "user://session-01.json") == OK
	return storage_ok

func record_event(speaker: String, line: String) -> void:
	data.transcript.append({"scene": data.scene, "department": DEPARTMENTS[data.leader], "character": data.representatives[data.leader], "speaker": speaker, "line": line})
	if data.transcript.size() > 500:
		data.transcript.pop_front()
	save()

func ready_department(i: int) -> bool:
	if bool(data.paper[i]):
		return true
	for person in ROSTER[i]:
		var r = data.records.get(person, {})
		if r.get("reason", "").strip_edges().is_empty() or r.get("want", "").strip_edges().is_empty() or r.get("need", "").strip_edges().is_empty() or r.get("object", "").strip_edges().is_empty() or r.get("fear", "").strip_edges().is_empty():
			return false
	return true

func boarding_ready() -> bool:
	for i in range(4):
		if not ready_department(i) or not data.performed[i]:
			return false
	return data.flags.get("venn_address", false)

func script_ready() -> bool:
	for i in range(4):
		if data.script_paper[i]:
			continue
		for person in ROSTER[i]:
			var lines = data.script.get(person, {})
			if lines.get("action", "").is_empty() or lines.get("dialogue", "").is_empty() or lines.get("reaction", "").is_empty():
				return false
	return true
