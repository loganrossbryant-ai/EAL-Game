extends SceneTree

func _init() -> void:
	var image = Image.new()
	image.load_svg_from_string(FileAccess.get_file_as_string("res://assets/icon.svg"), 512.0 / 192)
	image.save_png("res://assets/icon512.png")
	quit()
