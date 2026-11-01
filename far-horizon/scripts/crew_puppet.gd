class_name CrewPuppet
extends Node2D

const PARTS = ["body", "near_upper_arm", "near_forearm", "far_upper_arm", "far_forearm", "near_thigh", "near_shin", "near_boot", "far_thigh", "far_shin", "far_boot"]
const NAMES = ["flight", "science", "engineering", "colony"]
var pieces: Dictionary = {}
var regions: Dictionary = {}
var texture: Texture2D
var ready_rig = false
var hip_y = -104.5

func setup(department: int) -> bool:
	var base = "res://assets/art/rigs/" + NAMES[department]
	if not ResourceLoader.exists(base + ".png") or not FileAccess.file_exists(base + ".json"):
		return false
	var meta = JSON.parse_string(FileAccess.get_file_as_string(base + ".json"))
	if not meta is Dictionary or not meta.has("parts"):
		return false
	texture = load(base + ".png")
	regions = meta.parts
	for name in PARTS:
		if not regions.has(name): return false
		var mesh = Polygon2D.new()
		mesh.texture = load("res://assets/art/rigs/" + regions[name].texture) if regions[name].has("texture") else texture
		mesh.z_index = -3 if name.begins_with("far_") else (2 if "arm" in name else -1)
		if name == "body": mesh.z_index = 0
		if name.begins_with("far_"): mesh.color = Color(0.77, 0.81, 0.83, 1)
		pieces[name] = mesh
		add_child(mesh)
	ready_rig = true
	return true

func _region(name: String) -> Rect2:
	var r = regions[name].rect
	return Rect2(float(r[0]), float(r[1]), float(r[2]), float(r[3]))

func _limb(name: String, from: Vector2, to: Vector2, overlap_top: float = 3.0, overlap_bottom: float = 2.0) -> void:
	var r = _region(name)
	var direction = (to - from).normalized()
	var side = Vector2(direction.y, -direction.x)
	var scale_px = (from.distance_to(to) + overlap_top + overlap_bottom) / r.size.y
	var width_scale = 1.22 if "arm" in name else 1.0
	var a = from - direction * overlap_top
	var b = to + direction * overlap_bottom
	var anchor_a = float(regions[name].get("top_anchor", 0.5)) * r.size.x
	var anchor_b = float(regions[name].get("bottom_anchor", 0.5)) * r.size.x
	var mesh: Polygon2D = pieces[name]
	mesh.polygon = PackedVector2Array([a - side * anchor_a * scale_px * width_scale, a + side * (r.size.x - anchor_a) * scale_px * width_scale, b + side * (r.size.x - anchor_b) * scale_px * width_scale, b - side * anchor_b * scale_px * width_scale])
	mesh.uv = PackedVector2Array([r.position, r.position + Vector2(r.size.x, 0), r.end, r.position + Vector2(0, r.size.y)])

func _body(hip: Vector2, tilt: float) -> void:
	var r = _region("body")
	var pivot_x = float(regions.body.get("bottom_anchor", 0.63)) * r.size.x
	var source_rows = [0.0, 0.32, 0.47, 1.0]
	var target_rows = [-115.0, -85.0, -67.0, 0.0]
	var vertices = PackedVector2Array()
	var uvs = PackedVector2Array()
	for row in range(4):
		var width_scale = 0.86 if row == 0 else (0.93 if row == 1 else 1.0)
		for col in range(2):
			var x = (float(col) * r.size.x - pivot_x) * (115.0 / r.size.y) * width_scale
			vertices.append(hip + Vector2(x, target_rows[row]).rotated(tilt))
			uvs.append(r.position + Vector2(float(col) * r.size.x, source_rows[row] * r.size.y))
	var mesh: Polygon2D = pieces.body
	mesh.polygon = vertices
	mesh.uv = uvs
	mesh.polygons = [PackedInt32Array([0, 1, 3, 2]), PackedInt32Array([2, 3, 5, 4]), PackedInt32Array([4, 5, 7, 6])]

static func knee_for(hip: Vector2, foot: Vector2) -> Vector2:
	const THIGH = 50.0
	const SHIN = 42.0
	# Small leg extension handles reach without moving the pelvis up and down.
	var extension = clampf(hip.distance_to(foot) / (THIGH + SHIN - 0.1), 1.0, 1.11)
	var thigh = THIGH * extension
	var shin = SHIN * extension
	var d = clampf(hip.distance_to(foot), 10, thigh + shin - 0.05)
	var heading = (foot - hip).angle()
	var bend = acos(clampf((thigh * thigh + d * d - shin * shin) / (2.0 * thigh * d), -1, 1))
	return hip + Vector2.from_angle(heading - bend) * thigh

func _boot(name: String, sole: Vector2, lift: float) -> void:
	var r = _region(name)
	var height = 18.0
	var width = height * r.size.x / r.size.y
	var pivot = float(regions[name].top_anchor) * width
	var points = PackedVector2Array([Vector2(-pivot, -height), Vector2(width - pivot, -height), Vector2(width - pivot, 0), Vector2(-pivot, 0)])
	# A separate boot stays level on the floor instead of rotating with the shin.
	var pitch = -sin(clampf(-lift / 11.0, 0, 1) * PI * 0.7) * 0.12
	for i in range(points.size()): points[i] = sole + points[i].rotated(pitch)
	pieces[name].polygon = points
	pieces[name].uv = PackedVector2Array([r.position, r.position + Vector2(r.size.x, 0), r.end, r.position + Vector2(0, r.size.y)])

func pose(near_foot: Vector2, far_foot: Vector2, gait: float, weight: float, breath: float, lean: float) -> void:
	if not ready_rig: return
	var bob = sin(breath * 1.65) * 0.18 * (1 - weight) + sin(gait * TAU * 2) * 0.45 * weight
	hip_y = -104.5 + bob
	var hip = Vector2(0, hip_y)
	var far_hip = hip + Vector2(-3, -1)
	var near_hip = hip + Vector2(3, 0)
	var near_ankle = near_foot + Vector2(0, -14)
	var far_ankle = far_foot + Vector2(0, -14)
	var near_knee = knee_for(near_hip, near_ankle)
	var far_knee = knee_for(far_hip, far_ankle)
	_limb("far_thigh", far_hip, far_knee, 3, 4)
	_limb("far_shin", far_knee, far_ankle, 4, 3)
	_boot("far_boot", far_foot, far_foot.y)
	_limb("near_thigh", near_hip, near_knee, 3, 4)
	_limb("near_shin", near_knee, near_ankle, 4, 3)
	_boot("near_boot", near_foot, near_foot.y)
	_body(hip, lean + sin(gait * TAU) * 0.003 * weight)
	for near in [false, true]:
		var phase = gait * TAU + (0.0 if near else PI)
		var swing = cos(phase) * 0.30 * weight
		var r = _region("body")
		var shoulder_x = (float(regions.body.get("shoulder_x", 0.52)) - float(regions.body.get("bottom_anchor", 0.6))) * r.size.x * 115.0 / r.size.y
		var shoulder = hip + Vector2(shoulder_x if near else shoulder_x - 4, -68).rotated(lean)
		var elbow = shoulder + Vector2(0, 37).rotated(swing + lean)
		var wrist = elbow + Vector2(0, 39).rotated(swing - 0.12 - 0.10 * weight + lean)
		_limb("near_upper_arm" if near else "far_upper_arm", shoulder, elbow, 2.5, 3)
		_limb("near_forearm" if near else "far_forearm", elbow, wrist, 3, 0)
