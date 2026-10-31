class_name PioneerAudio
extends Node

var enabled = false
var ambience: AudioStreamPlayer
var steps: AudioStreamPlayer
var cue: AudioStreamPlayer

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
