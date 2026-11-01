class_name Conversations
extends RefCounted

static func line_id(who: String, text: String) -> String:
	return who.to_lower() + "_" + text.sha256_text().substr(0, 16)

# Recording and playback use the exact same authored campaign strings.
static func recording_script() -> Array[Dictionary]:
	var campaign: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign.json"))
	var unique: Dictionary = {}
	for who in campaign.characters:
		var person: Dictionary = campaign.characters[who]
		var lines: Array = [person.opening]
		for line in person.get("openings", {}).values(): lines.append(line)
		for reply in person.replies: lines.append(reply.text)
		for text in lines:
			var id = line_id(who, str(text))
			unique[id] = {"id":id,"speaker":who,"text":text}
	for scene in campaign.scenes:
		for cue in scene.cues:
			var who = str(cue.get("speaker", ""))
			if not campaign.characters.has(who): continue
			var id = line_id(who, str(cue.text))
			unique[id] = {"id":id,"speaker":who,"text":cue.text}
	var result: Array[Dictionary] = []
	for id in unique: result.append(unique[id])
	return result
