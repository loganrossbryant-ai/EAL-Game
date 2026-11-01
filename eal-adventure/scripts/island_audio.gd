class_name IslandAudio
extends Node

var voice = AudioStreamPlayer.new()
var music = AudioStreamPlayer.new()
var effects = AudioStreamPlayer.new()
var recordings: Dictionary = {}
var settings: Dictionary
var last_line = ""
var played = 0

func _ready() -> void:
	add_child(voice)
	add_child(music)
	add_child(effects)
	recordings = JSON.parse_string(FileAccess.get_file_as_string("res://data/voice.json"))
	music.stream = preload("res://assets/music.wav")
	music.finished.connect(func(): music.play())

func begin() -> void:
	if not music.playing: music.play()

func has_line(line: String) -> bool:
	return recordings.has(line)

func say(line: String) -> bool:
	stop()
	last_line = line
	if not has_line(line) or settings.muted or float(settings.voice) <= 0: return false
	voice.stream = load("res://" + recordings[line])
	voice.play()
	played += 1
	return true

func stop() -> void:
	voice.stop()

func chime() -> void:
	if settings.muted: return
	effects.stream = preload("res://assets/chime.wav")
	effects.play()

func _process(_delta: float) -> void:
	if settings == null or settings.is_empty(): return
	voice.volume_db = -80 if settings.muted else linear_to_db(maxf(float(settings.voice), 0.0001))
	music.volume_db = -80 if settings.muted else linear_to_db(maxf(float(settings.music) * (0.28 if voice.playing else 1.0), 0.0001))
	effects.volume_db = -80 if settings.muted else -15
