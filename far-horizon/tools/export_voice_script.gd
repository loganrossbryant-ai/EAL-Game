extends SceneTree

func _initialize() -> void:
	var script_lines = Conversations.recording_script()
	var file = FileAccess.open("res://assets/voices/dialogue.json", FileAccess.WRITE)
	if not file:
		push_error("Could not write the authored NPC recording script.")
		quit(1)
		return
	file.store_string(JSON.stringify({"sessions": [1, 2, 3], "lines": script_lines}, "  ") + "\n")
	print("Exported ", script_lines.size(), " authored NPC lines. No student records included.")
	quit()
