class_name GMStory
extends RefCounted

var data: Dictionary
var scenes: Array
var characters: Dictionary
var clues: Dictionary
var presentation: Dictionary
var cached_index: Array=[]

func _init() -> void:
	data = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign.json"))
	scenes = data.scenes
	characters = data.characters
	clues = data.clues
	presentation=JSON.parse_string(FileAccess.get_file_as_string("res://data/presentation.json"))
	for scene in scenes:cached_index.append({"id":scene.id,"session":scene.session,"title":scene.title,"cues":scene.cues.size()})

func find_scene(id: String) -> int:
	for i in range(scenes.size()):
		if scenes[i].id == id: return i
	return -1

func public_index() -> Array:
	return cached_index

func projected_line(text: String) -> String:
	return str(presentation.dialogue_captions.get(text,text))

func projected_cue(id: String,index: int) -> String:
	return str(presentation.scene_captions[id][index])

func projected_role(id: String) -> String:
	return str(presentation.role_labels.get(id,characters[id].role))
