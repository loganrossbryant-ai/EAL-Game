extends Node2D

const UI = preload("res://scripts/interface.gd")
const SPEED = 125.0
const WORLD_WIDTH = 2304.0
const FLOOR = 686.0
var story = GMStory.new()
var state = GMState.new()
var scene_index = 0
var scene: Dictionary
var scenery: PioneerScenery
var party: Array[PartyMember] = []
var camera: Camera2D
var world: Node2D
var audio: PioneerAudio
var npcs: Array[Dictionary] = []
var ui: Control
var chrome: Control
var overlay: Control
var modal: Control
var blackout: ColorRect
var cue_panel: Control
var scene_label: Label
var session_label: Label
var prompt: Label
var toast_label: Label
var leader_buttons: Array[Button] = []
var sound_button: Button
var next_button: Button
var cue_label: Label
var paused = false
var move_target = -1.0
var nearest = ""
var camera_lead = 0.0
var camera_focus = -1.0
var clock = 0.0
var publish_elapsed = 0.0
var bridge_elapsed = 0.0
var save_elapsed = 0.0
var current_clue = ""
var conversation = ""
var conversation_line = ""
var gallery = false
var stage: PioneerStage3D
var avatars: Array[CinematicAvatar] = []
var upper_route = false
var branch_pending = false
var physical_inspection = false
var member_routes: Array[bool] = [false,false,false,false]
var touch_direction = 0.0
var touch_until = 0
var phone_view = false
var presentation=false
var external_cover=false
var picture_quality="auto"
var actor_previous: Array[Vector3]=[]
var actor_next: Array[Vector3]=[]
var quality_grace=6.0
var slow_picture_time=0.0
var frame_average=1.0/60.0
var stage_container: SubViewportContainer
var stage_viewport: SubViewport

func _ready() -> void:
	if OS.is_debug_build() and OS.has_feature("web") and bool(JavaScriptBridge.eval("new URLSearchParams(location.search).get('preview')==='depth'",true)):
		get_tree().change_scene_to_file.call_deferred("res://scenes/depth_slice.tscn")
		return
	state.restore(story)
	if OS.has_feature("web"):
		phone_view=bool(JavaScriptBridge.eval("matchMedia('(pointer:coarse)').matches",true))
	_setup_input()
	_setup_bridge()
	_build_world()
	_build_ui()
	audio = PioneerAudio.new()
	add_child(audio)
	audio.enabled = bool(state.data.sound)
	audio.speech_enabled = bool(state.data.voice)
	for member in party:
		member.footstep.connect(func():
			if member.selected and not is_instance_valid(modal) and not paused: audio.step()
		)
	_enter_scene(story.find_scene(str(state.data.scene)), true)

func _setup_input() -> void:
	for action in {"walk_left": [KEY_A, KEY_LEFT], "walk_right": [KEY_D, KEY_RIGHT], "interact": [KEY_E]}:
		if not InputMap.has_action(action): InputMap.add_action(action)
		for code in {"walk_left": [KEY_A, KEY_LEFT], "walk_right": [KEY_D, KEY_RIGHT], "interact": [KEY_E]}[action]:
			var event = InputEventKey.new()
			event.physical_keycode = code
			InputMap.action_add_event(action, event)

func _setup_bridge() -> void:
	if OS.has_feature("web"):
		JavaScriptBridge.eval(FileAccess.get_file_as_string("res://web/bridge_bootstrap.js"), true)

func _build_world() -> void:
	world = Node2D.new()
	add_child(world)
	scenery = PioneerScenery.new()
	scenery.rendering_enabled=false
	world.add_child(scenery)
	var ground = StaticBody2D.new()
	ground.collision_layer = 1
	ground.collision_mask = 2
	var shape = CollisionShape2D.new()
	var rect = RectangleShape2D.new()
	rect.size = Vector2(WORLD_WIDTH + 400, 80)
	shape.shape = rect
	ground.position = Vector2(WORLD_WIDTH / 2, FLOOR + 40)
	ground.add_child(shape)
	world.add_child(ground)
	for x in [-10.0, WORLD_WIDTH + 10]:
		var wall = StaticBody2D.new()
		var cs = CollisionShape2D.new()
		var wr = RectangleShape2D.new()
		wr.size = Vector2(50, 1000)
		cs.shape = wr
		wall.add_child(cs)
		wall.position = Vector2(x, 400)
		wall.collision_layer = 1
		world.add_child(wall)
	for i in range(4):
		var member = PartyMember.new()
		member.setup(i,false)
		member.render_puppet=false
		member.position = Vector2(520 - i * 86, FLOOR)
		member.z_index = 5 + i
		party.append(member)
		world.add_child(member)
	camera = Camera2D.new()
	camera.position = Vector2(683, 384)
	camera.position_smoothing_enabled = false
	add_child(camera)
	# Retain the tested collision/follower controllers; render actual skinned
	# 3D people and geometry in a fixed viewport behind the presentation UI.
	world.visible = false
	scenery.set_process(false)
	var layer = CanvasLayer.new()
	layer.layer = -1
	add_child(layer)
	var container = SubViewportContainer.new()
	stage_container=container
	container.size = Vector2(1366,768)
	container.mouse_filter = Control.MOUSE_FILTER_IGNORE
	container.stretch = true
	container.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
	var edge_material=ShaderMaterial.new()
	edge_material.shader=load("res://shaders/edge_aa.gdshader")
	container.material=edge_material
	container.stretch_shrink=1
	layer.add_child(container)
	var viewport = SubViewport.new()
	stage_viewport=viewport
	viewport.size = Vector2i(1366,768)
	viewport.own_world_3d = true
	viewport.msaa_3d = Viewport.MSAA_DISABLED
	container.add_child(viewport)
	stage = PioneerStage3D.new()
	viewport.add_child(stage)
	_set_picture_quality("auto")
	for id in ["flight","science","engineering","colony"]:
		avatars.append(stage.add_actor(id))

func _build_ui() -> void:
	var layer = CanvasLayer.new()
	add_child(layer)
	ui = Control.new()
	ui.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	ui.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.theme = UI.theme()
	layer.add_child(ui)
	var film = ColorRect.new()
	film.size = Vector2(1366, 768)
	film.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var shader = Shader.new()
	shader.code = "shader_type canvas_item; render_mode unshaded; void fragment(){vec2 p=(UV-vec2(.5))*vec2(1.,.82);COLOR=vec4(.015,.028,.04,smoothstep(.32,.66,length(p))*.22);}"
	var material = ShaderMaterial.new()
	material.shader = shader
	film.material = material
	ui.add_child(film)
	blackout = ColorRect.new()
	blackout.size = Vector2(1366, 768)
	blackout.color = Color("02080d")
	blackout.mouse_filter = Control.MOUSE_FILTER_IGNORE
	blackout.visible = false
	ui.add_child(blackout)
	chrome = Control.new()
	chrome.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(chrome)
	var top = UI.panel(chrome, Rect2(24, 20, 1318, 80), 0.91)
	UI.title(top, "THE FAR HORIZON", Rect2(20, 10, 320, 32), 25)
	session_label = UI.label(top, "", Rect2(20, 46, 320, 20), 13, UI.AMBER)
	scene_label = UI.title(top, "", Rect2(350, 11, 590, 30), 23)
	cue_label = UI.label(top, "", Rect2(350, 47, 590, 20), 13, UI.MUTED)
	UI.button(top, "CLUES  [C]", Rect2(962, 15, 116, 48), _open_board, 14)
	UI.button(top, "GM DESK  [G]", Rect2(1090, 15, 203, 48), _open_gm, 15)
	for i in range(4):
		leader_buttons.append(UI.button(chrome, "", Rect2(28 + i * 169, 700, 159, 44), _select_leader.bind(i), 14))
	UI.button(chrome, "WORDS  [V]", Rect2(715, 700, 124, 44), _open_glossary, 13)
	sound_button = UI.button(chrome, "SFX OFF", Rect2(850, 700, 100, 44), _toggle_sound, 13)
	UI.button(chrome, "PREVIOUS", Rect2(961, 700, 135, 44), _previous, 13)
	next_button = UI.button(chrome, "NEXT  [↵]", Rect2(1107, 700, 230, 44), _next, 15)
	prompt = UI.label(chrome, "", Rect2(340, 646, 690, 36), 18)
	prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt.add_theme_color_override("font_shadow_color", Color.BLACK)
	prompt.add_theme_constant_override("shadow_outline_size", 5)
	toast_label = UI.label(chrome, "", Rect2(760, 110, 565, 65), 15, UI.AMBER)
	toast_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	overlay = Control.new()
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(overlay)

func _enter_scene(index: int, restoring: bool = false) -> void:
	if index < 0 or index >= story.scenes.size(): return
	if scene and not restoring:
		state.data.positions[scene.id] = party[int(state.data.leader)].position.x
		state.data.routes[scene.id] = upper_route
	_close_modal()
	move_target = -1
	touch_direction=0
	scene_index = index
	scene = story.scenes[index]
	state.data.scene = scene.id
	scenery.configure(str(scene.room))
	stage.configure(str(scene.room),str(scene.id))
	upper_route = bool(state.data.routes.get(scene.id,false)) and stage.has_route
	stage.restore_route(upper_route)
	actor_previous.clear()
	actor_next.clear()
	member_routes.fill(upper_route)
	branch_pending = false
	for person in stage.people.values():
		person.visible=false
		person.process_mode=Node.PROCESS_MODE_DISABLED
	for n in npcs:
		if is_instance_valid(n.node): n.node.queue_free()
	npcs.clear()
	var start = float(state.data.positions.get(scene.id, scene.start))
	var rank = 1
	for i in range(4):
		var offset = 0 if i == int(state.data.leader) else rank * 86
		if i != int(state.data.leader): rank += 1
		party[i].position = Vector2(clampf(start - offset, 65, WORLD_WIDTH - 65), FLOOR)
		party[i].velocity = Vector2.ZERO
		party[i].desired_speed = 0
		party[i].facing = 1
		party[i].turn_time = 0
		party[i].reset_contacts()
		party[i].visible = not scene.id in ["s1_route", "s3_packet"]
	for i in range(scene.npcs.size()):
		var spot=stage.npc_spot(i,str(scene.npcs[i]))
		_add_person(str(scene.npcs[i]),float(spot.x)*128.0,bool(spot.upper))
	if not scene.clues.is_empty():_add_station(str(scene.clues[0]),stage.device_x*128.0)
	camera.position = Vector2(clampf(start, 683, WORLD_WIDTH - 683), 384)
	camera_lead = 0
	stage.view_x = clampf(start/128.0,5.335,12.665)
	stage.reset_view(stage.view_x)
	audio.set_room(str(scene.room))
	_apply_cue(not restoring)

func _add_person(id: String, x: float,upper: bool=false) -> void:
	if not story.characters.has(id): return
	var p: Dictionary = story.characters[id]
	var node = Node2D.new()
	node.position = Vector2(x, FLOOR)
	node.z_index = 3
	world.add_child(node)
	if id=="iris":
		stage.place_iris(Vector3(x/128.0,stage.floor_point(x/128.0,upper).y+1.20,-1.8))
	elif id!="m77":
		var actor: CinematicAvatar = stage.people.get(id)
		if not actor:actor=stage.add_actor(id,true)
		actor.visible=true
		actor.process_mode=Node.PROCESS_MODE_INHERIT
		actor.position=stage.floor_point(x/128.0,upper)+Vector3(0,0,-.58)
		actor.gesture_time=0
		if not actor.has_node("Name"):
			var nameplate=Label3D.new()
			nameplate.name="Name"
			nameplate.text=str(p.name).to_upper()
			nameplate.position=Vector3(0,2.02,0)
			nameplate.font_size=27
			nameplate.pixel_size=.002
			nameplate.billboard=BaseMaterial3D.BILLBOARD_ENABLED
			nameplate.modulate=Color("cedddf")
			actor.add_child(nameplate)
	npcs.append({"kind":"person","id":id,"x":x,"node":node,"upper":upper})

func _add_station(id: String, x: float) -> void:
	var node = Node2D.new()
	node.position = Vector2(x, FLOOR)
	node.z_index = 1
	world.add_child(node)
	var plate = UI.panel(node, Rect2(-91, -171, 182, 69), 0.9)
	UI.label(plate, str(story.clues[id].title).to_upper(), Rect2(13, 11, 157, 52), 13, UI.PAPER)
	npcs.append({"kind": "clue", "id": id, "x": x, "node": node,"upper":stage.device_upper})
	stage.show_clue(story.clues[id])

func _cue_index() -> int:
	return int(state.data.cues.get(scene.id, 0))

func _apply_cue(play: bool = true) -> void:
	_close_modal()
	var cue: Dictionary = scene.cues[_cue_index()]
	state.data.seen[scene.id + ":" + str(_cue_index())] = true
	scenery.effect = str(cue.get("effect", ""))
	scenery.effect_time = 0
	stage.set_effect(scenery.effect)
	camera_focus = 1250.0 if scenery.effect == "round2" else -1.0
	blackout.visible = bool(cue.get("blackout", false))
	conversation_line = str(cue.text)
	conversation = str(cue.get("speaker", ""))
	_update_cue_panel()
	if cue.has("clue"):
		state.data.revealed[str(cue.clue)] = true
		_open_clue(str(cue.clue))
	if play and cue.has("sfx"): audio.launch(int(cue.sfx))
	var speaker = str(cue.get("speaker", ""))
	if play and story.characters.has(speaker): audio.say(speaker, str(cue.text))
	if stage.people.has(speaker):stage.people[speaker].gesture()
	_update_chrome()
	state.save()
	_publish()

func _update_cue_panel() -> void:
	if is_instance_valid(cue_panel):
		cue_panel.visible=false
		cue_panel.queue_free()
	var cue: Dictionary=scene.cues[_cue_index()]
	var rect=Rect2(24,618,1318,130) if presentation else Rect2(646 if stage.layout_key=="terminal" else 40,119,680,180)
	if blackout.visible:rect=Rect2(160,270,1046,224)
	cue_panel=UI.panel(ui,rect,.91)
	ui.move_child(cue_panel,ui.get_child_count()-1)
	ui.move_child(overlay,ui.get_child_count()-1)
	UI.label(cue_panel,str(cue.title).to_upper(),Rect2(18,8,rect.size.x-36,24),17,UI.AMBER)
	UI.label(cue_panel,story.projected_cue(str(scene.id),_cue_index()),Rect2(18,35,rect.size.x-36,rect.size.y-42),36 if presentation else 30)
	cue_panel.visible=not is_instance_valid(modal)

func _refresh_world_visibility() -> void:
	var covered=external_cover or (is_instance_valid(modal) and not physical_inspection)
	stage.process_mode=Node.PROCESS_MODE_DISABLED if covered else Node.PROCESS_MODE_INHERIT
	stage_viewport.render_target_update_mode=SubViewport.UPDATE_ONCE if covered else SubViewport.UPDATE_ALWAYS

func _set_presentation(enabled: bool) -> void:
	presentation=enabled
	stage.presentation=enabled
	_set_picture_quality(picture_quality)
	stage.camera_request_time=2.8
	_update_chrome()
	_update_cue_panel()
	_publish()

func _set_picture_quality(value: String) -> void:
	if not value in ["auto","sharp","smooth","balanced"]:return
	picture_quality=value
	var width=1366
	if value=="sharp":width=1920
	elif value=="smooth":width=960
	elif value=="auto":
		width=1280 if phone_view else 1600
		if OS.has_feature("web") and not phone_view:
			width=clampi(int(JavaScriptBridge.eval("Math.round(innerWidth*devicePixelRatio)",true)),1366,1920)
	quality_grace=6.0
	slow_picture_time=0.0
	_resize_picture(width)

func _resize_picture(width: int) -> void:
	var resolution=Vector2(width,roundi(width*768.0/1366.0))
	stage_container.size=resolution
	stage_container.scale=Vector2(1366,768)/resolution

func _process(delta: float) -> void:
	# Render between physics samples rather than stepping the 3D roots at 60 Hz.
	if actor_next.size()==avatars.size():
		var blend=Engine.get_physics_interpolation_fraction()
		for i in range(avatars.size()):
			avatars[i].position=actor_previous[i].lerp(actor_next[i],blend)
	# Auto can reduce only the world resolution after sustained slow frames.
	# Text and PPT portraits keep the display resolution; fixed choices stay fixed.
	if picture_quality!="auto" or paused or is_instance_valid(modal) or external_cover:
		quality_grace=maxf(quality_grace,1.5)
		return
	quality_grace=maxf(0,quality_grace-delta)
	frame_average=lerpf(frame_average,minf(delta,.15),minf(1,delta*1.5))
	if quality_grace>0:return
	if frame_average>1.0/42.0:slow_picture_time+=delta
	else:slow_picture_time=maxf(0,slow_picture_time-delta*2)
	if slow_picture_time>3.5 and stage_container.size.x>960:
		_resize_picture(maxi(960,roundi(stage_container.size.x*.82)))
		quality_grace=5.0
		slow_picture_time=0

func _update_chrome() -> void:
	session_label.text = "SESSION %02d  /  GM PRESENTATION" % int(scene.session)
	scene_label.text = str(scene.title)
	cue_label.text = "BEAT %d / %d   •   %s" % [_cue_index() + 1, scene.cues.size(), str(scene.focus)]
	chrome.visible = not bool(state.data.clean) and not presentation
	sound_button.text = "SFX ON" if audio.enabled else "SFX OFF"
	next_button.text = "NEXT SCENE  [↵]" if _cue_index() == scene.cues.size() - 1 else "NEXT BEAT  [↵]"
	for i in range(4):
		party[i].selected = i == int(state.data.leader)
		leader_buttons[i].text = str(i + 1) + "  " + CrewState.DEPARTMENTS[i].to_upper()
		leader_buttons[i].add_theme_color_override("font_color", CrewState.COLORS[i] if party[i].selected else UI.MUTED)

func _physics_process(delta: float) -> void:
	if not scene: return
	if not paused: clock += delta
	var held = paused or is_instance_valid(modal) or stage.route_transition
	var leader = party[int(state.data.leader)]
	for member in party:
		member.attending = is_instance_valid(modal)
		member.set_physics_process(not paused)
	var direction = 0.0 if held else Input.get_axis("walk_left", "walk_right")
	if not held and direction==0 and Time.get_ticks_msec()<touch_until:direction=touch_direction
	if branch_pending and not held:
		var junction = stage.route_junction_x*128.0
		var boarded=true
		if stage.layout_kind=="lift" and absf(leader.position.x-junction)<4:
			var slots=0
			for index in range(4):
				if index==int(state.data.leader):continue
				slots+=1
				if absf(party[index].position.x-(junction-slots*86))>10:boarded=false
		if absf(leader.position.x-junction)<4 and boarded:
			leader.position.x=junction
			leader.velocity.x=0
			upper_route=not upper_route
			member_routes[int(state.data.leader)]=upper_route
			stage.begin_route_change(upper_route)
			if stage.layout_kind=="lift":member_routes.fill(upper_route)
			branch_pending=false
			state.data.routes[scene.id]=upper_route
			state.save()
			direction=0
		else:direction=0 if absf(leader.position.x-junction)<4 else signf(junction-leader.position.x)
	if not held and move_target >= 0:
		if absf(leader.position.x - move_target) < 9 or direction != 0: move_target = -1
		else: direction = signf(move_target - leader.position.x)
	leader.desired_speed = direction * SPEED
	if direction != 0: camera_focus = -1
	var order: Array[int] = [int(state.data.leader)]
	for i in range(4):
		if i != state.data.leader: order.append(i)
	for rank in range(1, 4):
		var follower = party[order[rank]]
		var ahead = party[order[rank - 1]]
		var separation = ahead.position.x - follower.position.x
		if absf(separation) > 24: follower.follow_side = signf(separation)
		var error = separation - follower.follow_side * 86
		follower.desired_speed = clampf(ahead.velocity.x + error * 1.9, -SPEED * 1.08, SPEED * 1.08)
		# Signal a turn to the whole ensemble together instead of waiting for a
		# brake-turn-accelerate wave to reach the last member.
		if not held and direction != 0 and follower.facing != direction:
			follower.desired_speed = direction * SPEED
		if held or (absf(ahead.velocity.x) < 9 and absf(follower.desired_speed) < 9): follower.desired_speed = 0
		# Each follower crosses the junction before changing paths. This also
		# handles a leader reversing direction halfway up the access ramp.
		if member_routes[order[rank]]!=upper_route:
			var old_point=stage.floor_point(follower.position.x/128.0,member_routes[order[rank]])
			var new_point=stage.floor_point(follower.position.x/128.0,upper_route)
			if old_point.distance_to(new_point)<.08:member_routes[order[rank]]=upper_route
			elif not held:
				var error_to_junction=stage.route_junction_x*128.0-follower.position.x
				follower.desired_speed=signf(error_to_junction)*minf(SPEED,absf(error_to_junction)*2)
	if branch_pending and stage.layout_kind=="lift" and absf(leader.position.x-stage.route_junction_x*128)<4:
		for rank in range(1,4):
			var follower=party[order[rank]]
			var slot=stage.route_junction_x*128-rank*86
			var error_to_slot=slot-follower.position.x
			follower.desired_speed=signf(error_to_slot)*minf(SPEED,absf(error_to_slot)*2)
	if stage.layout_kind=="lift" and upper_route and not stage.route_transition:
		if leader.position.x>=8.95*128 and leader.desired_speed>0:leader.desired_speed=0
		if leader.position.x<.6*128 and leader.desired_speed<0:leader.desired_speed=0
	if upper_route and stage.layout_kind!="lift" and not stage.route_points.is_empty():
		var left_end=stage.route_points[0]
		if left_end.y>.1 and leader.position.x<(left_end.x+.10)*128 and leader.desired_speed<0:leader.desired_speed=0
	if not paused:
		camera_lead = lerpf(camera_lead, clampf(leader.velocity.x / SPEED, -1, 1) * 50, 1 - exp(-delta * 2.8))
		var goal = clampf(leader.position.x + camera_lead, 683, WORLD_WIDTH - 683)
		if camera_focus >= 0: goal = camera_focus
		camera.position.x = lerpf(camera.position.x, goal, 1 - exp(-delta * 3.8))
		camera.position.y = 384
		if scenery.effect in ["rumble", "ascent"]:
			camera.position += Vector2(sin(clock * 57) * 1.6, cos(clock * 49) * 1.1)
	scenery.camera_x = camera.position.x
	scenery.animating = not paused
	scenery.effect_time = stage.effect_time
	stage.view_x = camera.position.x/128.0
	stage.held = paused
	stage.active_actor = int(state.data.leader)
	for i in range(4):
		var place=stage.floor_point(party[i].position.x/128.0,member_routes[i],stage.route_transition)
		if actor_next.size()<=i:
			actor_previous.append(place)
			actor_next.append(place)
		else:
			actor_previous[i]=actor_next[i] if actor_next[i].distance_to(place)<2 else place
			actor_next[i]=place
		avatars[i].position=place
		avatars[i].speed = party[i].velocity.x/128.0
		avatars[i].facing = party[i].facing
		avatars[i].visible = party[i].visible
	for actor in stage.people.values():actor.look_x=leader.position.x/128.0
	nearest = ""
	var distance = 145.0
	for n in npcs:
		var contact=stage.floor_point(n.x/128.0,bool(n.get("upper",false)))
		var leader_place=avatars[int(state.data.leader)].position
		if Vector2(contact.y-leader_place.y,contact.z-leader_place.z).length()>.8:continue
		if absf(n.x - leader.position.x) < distance:
			distance = absf(n.x - leader.position.x)
			nearest = n.kind + ":" + n.id
	if stage.has_route and absf(leader.position.x-stage.route_junction_x*128.0)<76:nearest="route:change"
	elif leader.position.x>2180:nearest="travel:next"
	elif leader.position.x<110:nearest="travel:previous"
	var hint = ""
	if nearest != "" and not held:
		var parts = nearest.split(":")
		match parts[0]:
			"route":hint="[ E ]  RETURN TO MAIN DECK" if upper_route else "[ E ]  "+stage.route_name+"  ↗"
			"travel":hint="[ E ]  NEXT LOCATION" if parts[1]=="next" else "[ E ]  PREVIOUS LOCATION"
			"person":hint="[ E ]  "+str(story.characters[parts[1]].name)
			"clue":hint="[ E ]  USE "+str(story.clues[parts[1]].title).to_upper()
	if branch_pending:hint="APPROACHING THE ACCESS PATH"
	prompt.text = "PICTURE HELD  /  SPACE TO RESUME" if paused else hint
	save_elapsed += delta
	if save_elapsed > 2:
		save_elapsed = 0
		state.data.positions[scene.id] = leader.position.x
		state.data.routes[scene.id] = upper_route
		state.save()
	publish_elapsed += delta
	if publish_elapsed > 0.2:
		publish_elapsed = 0
		_publish()
	bridge_elapsed += delta
	if bridge_elapsed > 0.12 and OS.has_feature("web"):
		bridge_elapsed = 0
		var raw = JavaScriptBridge.eval("(function(){return window.fhGMBridge?JSON.stringify(window.fhGMBridge.queue.splice(0,20)):'[]';})()", true)
		var commands = JSON.parse_string(str(raw))
		if commands is Array:
			for command in commands:
				if command is Dictionary: _command(command)

func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		_close_modal()
		get_viewport().set_input_as_handled()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.physical_keycode:
			KEY_G: _open_gm()
			KEY_ENTER, KEY_PAGEDOWN: _next()
			KEY_PAGEUP: _previous()
			KEY_P: _toggle_clean()
			KEY_SPACE: _toggle_freeze()
			KEY_C: _open_board()
			KEY_V: _open_glossary()
			KEY_1, KEY_2, KEY_3, KEY_4:
				if not is_instance_valid(modal): _select_leader(event.physical_keycode - KEY_1)
			KEY_E:
				_interact_nearby()
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed and not is_instance_valid(modal) and not paused:
		var point = get_viewport().get_mouse_position()
		if point.y > 530 and point.y < 690: move_target = clampf(get_global_mouse_position().x, 65, WORLD_WIDTH - 65)

func _command(command: Dictionary) -> void:
	match str(command.get("action", "")):
		"cover":
			if typeof(command.get("enabled"))==TYPE_BOOL:
				external_cover=bool(command.enabled)
				_refresh_world_visibility()
		"presentation":
			if typeof(command.get("enabled"))==TYPE_BOOL:_set_presentation(bool(command.enabled))
		"quality":_set_picture_quality(str(command.get("value","auto")))
		"move":
			touch_direction=clampf(float(command.get("direction",0)),-1,1)
			touch_until=Time.get_ticks_msec()+800
			move_target=-1
		"interact":_interact_nearby()
		"reply":
			if conversation in story.characters:
				var choices=_dialogue_choices(conversation)
				var index=int(command.get("index",-1))
				if index>=0 and index<choices.size():_talk(conversation,str(choices[index].text))
		"jump": _enter_scene(story.find_scene(str(command.get("id", ""))))
		"cue":
			state.data.cues[scene.id] = clampi(int(command.get("index", 0)), 0, scene.cues.size() - 1)
			_apply_cue()
		"next": _next()
		"previous": _previous()
		"clue":
			var id = str(command.get("id", ""))
			if story.clues.has(id): _open_clue(id)
		"hide_clue":
			var id = str(command.get("id", ""))
			if story.clues.has(id):
				state.data.revealed[id] = false
				if current_clue == id: _close_modal()
				state.save()
		"close": _close_modal()
		"freeze": _toggle_freeze()
		"clean": _toggle_clean()
		"language":
			if str(command.get("value", "")) in ["zh", "ko", "ja"]:
				state.data.language = str(command.value)
				state.save()
				if conversation == "glossary": _open_glossary()
		"sound": _toggle_sound()
		"voice":
			audio.speech_enabled = not audio.speech_enabled
			state.data.voice = audio.speech_enabled
			if not audio.speech_enabled: audio.stop_voice()
			state.save()
		"replay": _apply_cue()
		"talk":
			var id = str(command.get("id", ""))
			if id in scene.npcs: _talk(id)
		"threat":
			var i = clampi(int(command.get("index", 0)), 0, 2)
			state.data.threats[i] = clampi(int(command.get("value", 0)), 0, 2 if i == 0 else 1)
			state.save()
		"board": _open_board()
		"glossary": _open_glossary()
		"export": _export_progress()
		"reset_session":
			var session = int(scene.session)
			for s in story.scenes:
				if int(s.session) == session:
					state.data.cues[s.id] = 0
					state.data.positions.erase(s.id)
					state.data.routes.erase(s.id)
			for id in story.clues:
				if int(story.clues[id].session) == session: state.data.revealed.erase(id)
			if session == 2: state.data.threats = [2, 1, 1]
			_enter_scene(scene_index,true)
	_publish()

func _interact_nearby() -> void:
	if paused or is_instance_valid(modal) or nearest=="":return
	var parts=nearest.split(":")
	if parts[0]=="person":_talk(parts[1])
	elif parts[0]=="clue":_inspect_world_clue(parts[1])
	elif parts[0]=="route":branch_pending=true
	elif parts[0]=="travel":_enter_scene(clampi(scene_index+(1 if parts[1]=="next" else -1),0,story.scenes.size()-1))

func _next() -> void:
	if _cue_index() + 1 < scene.cues.size():
		state.data.cues[scene.id] = _cue_index() + 1
		_apply_cue()
	elif scene_index + 1 < story.scenes.size():
		_enter_scene(scene_index + 1)
	else: _toast("End of Session 3. The packet stays sealed.")

func _previous() -> void:
	if _cue_index() > 0:
		state.data.cues[scene.id] = _cue_index() - 1
		_apply_cue()
	elif scene_index > 0: _enter_scene(scene_index - 1)

func _select_leader(index: int) -> void:
	state.data.leader = index
	upper_route=member_routes[index]
	move_target = -1
	branch_pending=false
	_update_chrome()
	state.save()

func _toggle_sound() -> void:
	audio.enabled = not audio.enabled
	audio.update_sound()
	state.data.sound = audio.enabled
	state.save()
	_update_chrome()

func _toggle_clean() -> void:
	state.data.clean = not state.data.clean
	_update_chrome()
	state.save()

func _toggle_freeze() -> void:
	paused = not paused
	move_target = -1
	scenery.animating = not paused

func _new_modal(rect: Rect2) -> Panel:
	_close_modal()
	move_target = -1
	touch_direction=0
	modal = Control.new()
	modal.mouse_filter = Control.MOUSE_FILTER_IGNORE
	overlay.add_child(modal)
	if is_instance_valid(cue_panel):cue_panel.visible=false
	var dim = ColorRect.new()
	dim.size = Vector2(1366, 768)
	dim.color = Color(0.004, 0.015, 0.025, 0.5)
	modal.add_child(dim)
	_refresh_world_visibility()
	return UI.panel(modal, rect, 0.98)

func _close_modal() -> void:
	if audio: audio.stop_voice()
	if is_instance_valid(modal):
		modal.visible=false
		modal.queue_free()
	modal = null
	current_clue = ""
	conversation = ""
	gallery = false
	if stage:stage.close_inspection()
	physical_inspection=false
	_refresh_world_visibility()
	if is_instance_valid(cue_panel):cue_panel.visible=true
	if chrome:chrome.visible=not bool(state.data.clean) and not presentation

func _inspect_world_clue(id: String) -> void:
	if not story.clues.has(id):return
	_close_modal()
	move_target=-1
	physical_inspection=true
	current_clue=id
	state.data.revealed[id]=true
	state.save()
	stage.active_actor=int(state.data.leader)
	stage.inspect(story.clues[id])
	modal=Control.new()
	modal.mouse_filter=Control.MOUSE_FILTER_IGNORE
	overlay.add_child(modal)
	chrome.visible=false
	cue_panel.visible=false
	UI.button(modal,"RETURN TO THE SCENE  [ESC]",Rect2(32,704,410,40),_close_modal,15)
	UI.button(modal,"READABLE TRANSCRIPT / SOURCE",Rect2(850,704,484,40),_open_clue.bind(id),15)
	var options: Array=scene.clues
	for i in range(options.size()):
		UI.button(modal,str(story.clues[options[i]].title),Rect2(32,22+i*43,300,36),_inspect_world_clue.bind(str(options[i])),13)
	_publish()

func _open_clue(id: String, image_only: bool = false) -> void:
	if not story.clues.has(id): return
	var clue: Dictionary = story.clues[id]
	if presentation and not image_only:
		var card=_new_modal(Rect2(20,20,1326,728))
		current_clue=id
		state.data.revealed[id]=true
		state.save()
		UI.label(card,str(clue.tag),Rect2(24,15,1140,28),20,UI.CYAN)
		UI.title(card,str(clue.title),Rect2(24,52,1250,60),40)
		var rows=ceili(clue.fields.size()/2.0)
		var row_height=minf(166,510.0/maxi(1,rows))
		for i in range(clue.fields.size()):
			var x=24+(i%2)*650
			var y=128+(i/2)*row_height
			UI.label(card,str(clue.fields[i][0]),Rect2(x,y,620,27),21,UI.CYAN)
			UI.label(card,str(clue.fields[i][1]),Rect2(x,y+32,620,row_height-35),34,UI.AMBER if id=="ticket" and str(clue.fields[i][0])=="COMPLETED" else UI.PAPER)
		UI.button(card,"Return to the scene  [Esc]",Rect2(24,670,1278,42),_close_modal,22)
		_publish()
		return
	var p = _new_modal(Rect2(65, 119, 1236, 555))
	if id == "ticket":
		var style = UI.box(Color("081d29"), UI.AMBER)
		style.set_corner_radius_all(14)
		style.set_border_width_all(2)
		p.add_theme_stylebox_override("panel", style)
	current_clue = id
	gallery = image_only
	state.data.revealed[id] = true
	state.save()
	UI.label(p, str(clue.tag), Rect2(24, 17, 1070, 22), 13, UI.CYAN)
	UI.title(p, str(clue.title), Rect2(24, 49, 1100, 42), 30)
	UI.button(p, "CLOSE  [ESC]", Rect2(1073, 15, 137, 37), _close_modal, 13)
	var has_image = str(clue.get("image", "")) != "" and ResourceLoader.exists("res://assets/props/" + str(clue.get("image", "")))
	if image_only and has_image:
		UI.portrait(p, load("res://assets/props/" + str(clue.image)), Rect2(26, 104, 1184, 384))
		UI.button(p, "READABLE TRANSCRIPT", Rect2(24, 502, 1186, 37), _open_clue.bind(id, false), 15)
		return
	var text_width = 916.0 if has_image else 1188.0
	var fields: Array = clue.fields
	var row_h = minf(74, 344.0 / maxf(1, fields.size()))
	for i in range(fields.size()):
		var y = 112 + i * row_h
		UI.label(p, str(fields[i][0]), Rect2(24, y + 3, 217, row_h - 7), 14, UI.CYAN)
		UI.label(p, str(fields[i][1]), Rect2(252, y, text_width - 250, row_h), 23 if fields.size() < 6 else 21, UI.AMBER if id == "ticket" and str(fields[i][0]) == "COMPLETED" else UI.PAPER)
	if has_image:
		UI.portrait(p, load("res://assets/props/" + str(clue.image)), Rect2(955, 107, 250, 342))
		UI.button(p, "ENLARGE PROP", Rect2(955, 459, 250, 35), _open_clue.bind(id, true), 13)
	UI.label(p, str(clue.note), Rect2(24, 463, text_width - 6, 72), 17, UI.AMBER)
	_publish()

func _open_board() -> void:
	var p = _new_modal(Rect2(81, 130, 1204, 517))
	conversation = "board"
	UI.title(p, "PIONEER / REVEALED EVIDENCE", Rect2(24, 18, 1100, 40), 28)
	UI.label(p, "Only evidence already revealed in this presentation appears here.", Rect2(24, 69, 1110, 31), 18, UI.MUTED)
	var visible: Array[String] = []
	for id in story.clues:
		if state.data.revealed.get(id, false): visible.append(id)
	for i in range(visible.size()):
		var id = visible[i]
		UI.button(p, str(story.clues[id].title), Rect2(24 + (i % 3) * 388, 124 + (i / 3) * 62, 372, 51), _open_clue.bind(id), 17)
	if visible.is_empty(): UI.label(p, "No clues have been revealed yet.", Rect2(24, 158, 1120, 55), 24)
	UI.button(p, "RETURN TO THE SCENE", Rect2(24, 460, 1156, 39), _close_modal, 16)

func _talk(who: String, reply: String = "") -> void:
	if not story.characters.has(who): return
	var data: Dictionary = story.characters[who]
	var line = str(data.opening) if reply == "" else reply
	if reply == "" and data.has("openings"): line = str(data.openings.get(str(int(scene.session)), line))
	var p = _new_modal(Rect2(0,0,1366,768))
	conversation=who
	conversation_line=line
	if stage.people.has(who):stage.people[who].gesture()
	stage.focus_person(who)
	var portrait_catalog=JSON.parse_string(FileAccess.get_file_as_string("res://data/portraits.json"))
	if portrait_catalog.has(who):
		var entry=portrait_catalog[who]
		var atlas=AtlasTexture.new()
		atlas.atlas=load("res://assets/portraits/"+str(entry.file))
		atlas.region=Rect2(entry.region[0],entry.region[1],entry.region[2],entry.region[3])
		var photo_frame=Control.new()
		photo_frame.size=Vector2(683,768)
		photo_frame.clip_contents=true
		p.add_child(photo_frame)
		var portrait=UI.portrait(photo_frame,atlas,Rect2(0,0,683,768))
		portrait.stretch_mode=TextureRect.STRETCH_KEEP_ASPECT_COVERED
	var side=UI.panel(p,Rect2(683,0,683,768),1)
	UI.title(side,str(data.name),Rect2(32,34,619,100),34)
	UI.label(side,story.projected_role(who),Rect2(32,134,619,38),21,UI.AMBER)
	UI.label(side,story.projected_line(line),Rect2(32,206,619,228),34)
	var choices: Array=_dialogue_choices(who)
	for i in range(mini(choices.size(),4)):
		UI.button(side,str(choices[i].question),Rect2(32,458+i*55,619,49),_talk.bind(who,str(choices[i].text)),23)
	UI.button(side,"Return to the scene  [Esc]",Rect2(32,708,619,42),_close_modal,20)
	audio.say(who, line)
	_publish()

func _dialogue_choices(who: String) -> Array:
	var choices: Array=[]
	for option in story.characters[who].replies:
		if int(scene.session)<int(option.get("min_session",1)):continue
		if int(scene.session)>int(option.get("max_session",3)):continue
		if str(option.get("requires",""))!="" and not state.data.revealed.get(str(option.requires),false):continue
		choices.append(option)
	return choices

func _open_glossary() -> void:
	var p = _new_modal(Rect2(145, 127, 1076, 545))
	conversation = "glossary"
	UI.title(p, "ACADEMIC WORDS / DRAMA & EVIDENCE", Rect2(24, 17, 1010, 35), 25)
	for i in range(3):
		var lang = ["zh", "ko", "ja"][i]
		UI.button(p, ["简体中文", "한국어", "日本語"][i], Rect2(24 + i * 344, 68, 330, 36), func():
			state.data.language = lang
			state.save()
			_open_glossary()
		, 16)
	for i in range(story.data.glossary.size()):
		var word: Dictionary = story.data.glossary[i]
		var x = 24 + (i % 3) * 344
		var y = 123 + (i / 3) * 52
		UI.label(p, str(word.term), Rect2(x, y, 330, 21), 15, UI.CYAN)
		var translated = UI.label(p, str(word[state.data.language]), Rect2(x, y + 22, 330, 26), 17)
		translated.language = str(state.data.language)
	UI.button(p, "RETURN TO THE SCENE", Rect2(24, 501, 1028, 33), _close_modal, 14)

func _open_gm() -> void:
	if OS.has_feature("web"):
		var ok = JavaScriptBridge.eval("window.fhGMBridge&&window.fhGMBridge.openDesk()", true)
		if not ok: _toast("Allow the GM Desk window, then press G again.")
		_publish()
	else:
		_toast("The separate GM Desk is available in the browser build. Page Up / Page Down navigate beats.")

func _export_progress() -> void:
	var bytes = JSON.stringify(state.data, "  ").to_utf8_buffer()
	if OS.has_feature("web"): JavaScriptBridge.download_buffer(bytes, "Far-Horizon-GM-Progress.json", "application/json")
	else:
		var f = FileAccess.open("user://Far-Horizon-GM-Progress.json", FileAccess.WRITE)
		if f: f.store_buffer(bytes)

func _toast(text: String) -> void:
	toast_label.text = text
	get_tree().create_timer(7).timeout.connect(func():
		if toast_label.text == text: toast_label.text = ""
	)

func _publish() -> void:
	if not scene or not audio: return
	var positions: Array = []
	for i in range(party.size()):
		var member=party[i]
		var item={"x":member.position.x,"y":member.position.y,"vx":member.velocity.x,"facing":member.facing,"rig":avatars[i].skeleton!=null}
		if OS.is_debug_build():
			item.gait=member.gait
			item.feet=member.feet
		positions.append(item)
	var subjects: Array = stage.animated_snapshot() if OS.is_debug_build() else []
	var payload = {
		"scene": scene.id, "scene_index": scene_index, "session": scene.session, "title": scene.title,
		"cue": _cue_index(), "cue_count": scene.cues.size(), "cue_title": scene.cues[_cue_index()].title,
		"cue_titles": scene.cues.map(func(c): return str(c.title)), "index": story.public_index(),
		"leader": state.data.leader, "party": positions, "nearest": nearest, "modal": is_instance_valid(modal),
		"clue": current_clue, "conversation": conversation, "line": conversation_line, "paused": paused,
		"clean": state.data.clean, "language": state.data.language, "revealed": state.data.revealed,
		"seen": state.data.seen, "threats": state.data.threats, "storage_ok": state.storage_ok,
		"sound": audio.enabled, "voice": audio.speech_enabled, "recordings": audio.recordings.size(),
		"voice_playing": audio.voice.playing, "clock": clock, "camera": camera.position.x
	}
	payload.upper_route=upper_route
	payload.branch_pending=branch_pending
	payload.physical_inspection=physical_inspection
	payload.stage_camera_size=stage.camera.size
	payload.stage_clock=stage.clock
	payload.volumetric=true
	payload.inspection_time=stage.inspection_time
	payload.render_fps=Engine.get_frames_per_second()
	payload.phone_view=phone_view
	payload.presentation=presentation
	payload.projected_role=story.projected_role(conversation) if conversation in story.characters else ""
	payload.world_covered=external_cover or (is_instance_valid(modal) and not physical_inspection)
	payload.picture_quality=picture_quality
	payload.world_resolution=[stage_viewport.size.x,stage_viewport.size.y]
	payload.projected_line=story.projected_line(conversation_line)
	payload.projected_caption=story.projected_cue(str(scene.id),_cue_index())
	payload.layout=stage.layout_key
	payload.layout_kind=stage.layout_kind
	payload.route_junction=stage.route_junction_x
	payload.device_x=stage.device_x
	payload.device_upper=stage.device_upper
	payload.route_transition=stage.route_transition
	if OS.is_debug_build():
		var rigs: Array=[]
		for actor in avatars:
			var hips=actor.skeleton.find_bone("pelvis")
			rigs.append({"x":actor.position.x,"y":actor.position.y,"z":actor.position.z,"yaw":actor.rotation.y,"animation":actor.current_animation,"time":actor.animator.current_animation_position,"hip_height":actor.skeleton.get_bone_global_pose(hips).origin.y if hips>=0 else -1})
		payload.avatars=rigs
		var poses: Dictionary={}
		for id in stage.people:
			var actor: CinematicAvatar=stage.people[id]
			if actor.visible:
				var head=actor.skeleton.find_bone("head")
				poses[id]={"yaw":actor.rotation.y,"time":actor.animator.current_animation_position,"head":actor.skeleton.get_bone_pose_rotation(head) if head>=0 else Quaternion.IDENTITY}
		payload.npc_poses=poses
	if OS.is_debug_build():
		payload.subjects = subjects
		payload.draw_calls=RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME)
		payload.effect = scenery.effect
		payload.effect_time = scenery.effect_time
		var issues: Array = []
		_collect_layout_issues(ui, issues)
		payload.layout_issues = issues
	if OS.has_feature("web"):
		var value = JSON.stringify(payload)
		JavaScriptBridge.eval("window.fhGMBridge&&window.fhGMBridge.publish(" + value + ")", true)
		if OS.is_debug_build(): JavaScriptBridge.eval("window.farHorizonTestState=" + value + ";", true)

func _collect_layout_issues(node: Node, issues: Array) -> void:
	if node.is_queued_for_deletion(): return
	if node is Label and node.is_visible_in_tree() and node.has_meta("designed_height"):
		var intended = float(node.get_meta("designed_height"))
		var content_height = node.get_line_count() * node.get_line_height()
		if content_height > intended + 4:
			issues.append({"text":node.text,"designed":intended,"actual":content_height})
	for child in node.get_children(): _collect_layout_issues(child, issues)
