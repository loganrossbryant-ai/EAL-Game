class_name GMStory
extends RefCounted

var data: Dictionary
var scenes: Array
var characters: Dictionary
var clues: Dictionary

func _init() -> void:
	data = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign.json"))
	scenes = data.scenes
	characters = data.characters
	clues = data.clues

func find_scene(id: String) -> int:
	for i in range(scenes.size()):
		if scenes[i].id == id: return i
	return -1

func public_index() -> Array:
	var result: Array = []
	for s in scenes:
		result.append({"id": s.id, "session": s.session, "title": s.title, "cues": s.cues.size()})
	return result
