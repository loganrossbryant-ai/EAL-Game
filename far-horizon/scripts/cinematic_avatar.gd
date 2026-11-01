class_name CinematicAvatar
extends Node3D

var actor_id = "flight"
var model: Node3D
var animator: AnimationPlayer
var skeleton: Skeleton3D
var meshes: Array[MeshInstance3D] = []
var clock = 0.0
var speed = 0.0
var facing = 1.0
var npc = false
var using_device = false
var held = false
var current_animation = ""
var phase = 0.0
var look_x = 0.0
var gesture_time = 0.0
var paused_by_hold = false

func setup(id: String, is_npc: bool = false) -> void:
	actor_id = id
	npc = is_npc
	phase = float(id.hash() % 997) / 997.0
	var path = "res://assets/models/" + id + ".glb"
	if not ResourceLoader.exists(path): path = "res://assets/models/flight.glb"
	model = load(path).instantiate()
	add_child(model)
	_find_nodes(model)
	if animator:
		for name in animator.get_animation_list():
			if name in ["Idle", "Walk"]: animator.get_animation(name).loop_mode = Animation.LOOP_LINEAR
		_play("Idle")
		animator.seek(phase * 3.5, true)
	for mesh in meshes:
		for i in range(mesh.mesh.get_surface_count()):
			var material = mesh.get_active_material(i)
			if material is StandardMaterial3D:
				var m: StandardMaterial3D = material.duplicate()
				if m.resource_name.begins_with("Face") and ResourceLoader.exists("res://assets/art/crew_face_atlas.png"):
					var face = ShaderMaterial.new()
					face.shader = preload("res://shaders/crew_face.gdshader")
					face.set_shader_parameter("face_atlas",load("res://assets/art/crew_face_atlas.png"))
					var index = ["flight","science","engineering","colony","venn","juno","rhee","vale","okafor"].find(id)
					face.set_shader_parameter("cell",Vector2(index%3,index/3))
					face.set_shader_parameter("base_skin",m.albedo_color)
					if FileAccess.file_exists("res://data/face_fit.json"):
						var fits = JSON.parse_string(FileAccess.get_file_as_string("res://data/face_fit.json"))
						if fits.has(id):
							var fit = fits[id].fit
							face.set_shader_parameter("fit",Vector4(fit[0],fit[1],fit[2],fit[3]))
					mesh.set_surface_override_material(i,face)
					continue
				if (m.resource_name.begins_with("Uniform") or m.resource_name.begins_with("Pants")) and ResourceLoader.exists("res://assets/art/uniform_fabric.png"):
					m.albedo_texture = load("res://assets/art/uniform_fabric.png")
					m.uv1_scale = Vector3(8,8,1)
					m.roughness = 0.83
				mesh.set_surface_override_material(i,m)
	rotation.y = -0.18 if npc else PI / 2
	var shadow = MeshInstance3D.new()
	var plane = PlaneMesh.new()
	plane.size = Vector2(.48,.68)
	shadow.mesh = plane
	shadow.position.y = .003
	var texture = GradientTexture2D.new()
	texture.width = 64
	texture.height = 64
	texture.fill = GradientTexture2D.FILL_RADIAL
	texture.fill_from = Vector2(.5,.5)
	texture.fill_to = Vector2(1,.5)
	var gradient = Gradient.new()
	gradient.set_color(0,Color(0.005,0.009,0.012,.24))
	gradient.set_color(1,Color(0.005,0.009,0.012,0))
	texture.gradient = gradient
	var shade = StandardMaterial3D.new()
	shade.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	shade.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	shade.albedo_texture = texture
	shadow.material_override = shade
	shadow.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	add_child(shadow)

func _find_nodes(node: Node) -> void:
	if node is AnimationPlayer: animator = node
	if node is Skeleton3D: skeleton = node
	if node is MeshInstance3D: meshes.append(node)
	for child in node.get_children(): _find_nodes(child)

func _play(value: String) -> void:
	if not animator or not animator.has_animation(value) or current_animation == value: return
	current_animation = value
	animator.play(value,0.20)
	if value == "Walk": animator.seek(phase * animator.get_animation(value).length,false)

func begin_use() -> void:
	using_device = true
	_play("Use")
	if animator: animator.seek(0,true)

func end_use() -> void:
	using_device = false
	_play("Idle")

func gesture() -> void:
	gesture_time = 1.4
	_play("Use")
	if animator: animator.seek(0,true)

func _process(delta: float) -> void:
	if held:
		if animator: animator.pause()
		paused_by_hold=true
		return
	if paused_by_hold and animator:animator.play()
	paused_by_hold=false
	clock += delta
	gesture_time=maxf(0,gesture_time-delta)
	var target = PI if using_device else (clampf((look_x-global_position.x)*.09,-.38,.38) if npc else facing * PI / 2)
	rotation.y = lerp_angle(rotation.y,target,1 - exp(-delta * 8))
	if not using_device and gesture_time<=0:
		_play("Walk" if absf(speed) > 0.08 and not npc else "Idle")
		if animator:
			animator.speed_scale = absf(speed) / 0.80 if current_animation == "Walk" else 0.91 + phase * 0.15
			if not animator.is_playing(): animator.play()
	# The real eyelid morph moves face geometry over the fitted 3D eyeballs.
	var blink_phase = fposmod(clock + phase * 4.9,4.2 + phase * 1.7)
	var blink = sin(blink_phase / 0.16 * PI) if blink_phase < 0.16 else 0.0
	for mesh in meshes:
		var index = mesh.find_blend_shape_by_name("Blink")
		if index >= 0: mesh.set_blend_shape_value(index,blink)
