class_name PioneerAudio
extends Node

var enabled = false
var ambience: AudioStreamPlayer
var steps: AudioStreamPlayer
var cue: AudioStreamPlayer
var voice: AudioStreamPlayer
var speech_enabled = true
var recordings: Dictionary = {}
var current_speaker = ""
var current_text = ""
var current_id = ""

func _ready() -> void:
	ambience = AudioStreamPlayer.new()
	ambience.stream = preload("res://assets/audio/ambience.wav")
	ambience.stream.loop_mode = AudioStreamWAV.LOOP_FORWARD
	ambience.stream.loop_end = int(ambience.stream.mix_rate * 8)
	ambience.volume_db = -11
	add_child(ambience)
	steps = AudioStreamPlayer.new()
	steps.stream = preload("res://assets/audio/step.wav")
	steps.volume_db = -13
	add_child(steps)
	cue = AudioStreamPlayer.new()
	cue.volume_db = -9
	add_child(cue)
	voice = AudioStreamPlayer.new()
	voice.volume_db = -1
	add_child(voice)
	var catalog_path = "res://assets/voices/catalog.json"
	if FileAccess.file_exists(catalog_path):
		var catalog = JSON.parse_string(FileAccess.get_file_as_string(catalog_path))
		if catalog is Dictionary and catalog.get("provider", "") == "ElevenLabs":
			recordings = catalog.get("clips", {})

func _process(delta: float) -> void:
	if ambience:
		ambience.volume_db = move_toward(ambience.volume_db, -23.0 if voice.playing else -11.0, delta * 35)
	if steps: steps.volume_db = -23.0 if voice.playing else -13.0

func has_recording(who: String, text: String) -> bool:
	var id = Conversations.line_id(who, text)
	if not recordings.has(id): return false
	var path = "res://assets/voices/" + str(recordings[id].get("file", ""))
	return ResourceLoader.exists(path)

func say(who: String, text: String) -> bool:
	stop_voice()
	current_speaker = who
	current_text = text
	current_id = Conversations.line_id(who, text)
	if not speech_enabled or not has_recording(who, text): return false
	voice.stream = load("res://assets/voices/" + str(recordings[current_id].file))
	voice.play()
	return true

func stop_voice() -> void:
	if voice: voice.stop()
	current_id = ""
	current_speaker = ""
	current_text = ""

func toggle_voice(who: String, text: String) -> void:
	speech_enabled = not speech_enabled
	if speech_enabled: say(who, text)
	else: stop_voice()

func update_sound() -> void:
	if enabled:
		if not ambience.playing:
			ambience.play()
	else:
		ambience.stop()
		steps.stop()
		cue.stop()

func set_room(room: String) -> void:
	if not ambience:
		return
	stop_voice()
	ambience.pitch_scale = 1.04 if room == "terminal" else (0.92 if room == "habitation" else 1.0)
	update_sound()

func step() -> void:
	if enabled:
		steps.pitch_scale = randf_range(0.9, 1.12)
		steps.play()

func launch(index: int) -> void:
	if not enabled:
		return
	if index == 1:
		cue.stream = preload("res://assets/audio/ignition.wav")
		cue.play()
	elif index == 3:
		cue.stop()
		cue.stream = preload("res://assets/audio/cutoff.wav")
		cue.play()
