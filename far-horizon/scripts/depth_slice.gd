extends Node3D

const UI = preload("res://scripts/interface.gd")
var stage: PioneerStage3D
var party: Array[CinematicAvatar] = []
var leader_x = 4.0
var velocity = 0.0
var upper = false
var inspecting = false
var held = false
var prompt: Label
var location_label: Label
var clock = 0.0
var ui: Control
var story = GMStory.new()
var branch_pending = false
var dialogue: Control
var talking = ""
var dialogue_line = ""

func _ready() -> void:
	stage = PioneerStage3D.new()
	add_child(stage)
	for id in ["flight","science","engineering","colony"]:
		party.append(stage.add_actor(id))
	var venn = stage.add_actor("venn",true)
	venn.position = Vector3(14.7,1.05,-2.12)
	var juno = stage.add_actor("juno",true)
	juno.position = Vector3(8.6,0,-.45)
	stage.camera.position = Vector3(5.335,4.98,14)
	stage.camera.look_at(Vector3(5.335,2.36,0))
	var layer = CanvasLayer.new()
	add_child(layer)
	ui = Control.new()
	ui.theme = UI.theme()
	ui.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(ui)
	var top = UI.panel(ui,Rect2(32,24,630,75),.86)
	UI.title(top,"PIONEER / DEPARTURE CONCOURSE",Rect2(18,10,600,29),22)
	location_label = UI.label(top,"LOWER CONCOURSE",Rect2(18,47,590,22),13,UI.AMBER)
	prompt = UI.label(ui,"",Rect2(260,643,850,55),21)
	prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	prompt.add_theme_color_override("font_shadow_color",Color.BLACK)
	prompt.add_theme_constant_override("shadow_outline_size",4)
	UI.label(ui,"A / D  WALK     E  TRAVEL / USE     ESC  RETURN     SPACE  HOLD",Rect2(265,725,850,32),14,UI.CYAN)
	UI.button(ui,"GM DRAFT",Rect2(1165,28,165,45),func():
		if OS.has_feature("web"):JavaScriptBridge.eval("location.href=location.pathname",true)
	,14)

func _physics_process(delta: float) -> void:
	if not held:clock += delta
	var axis = 0.0
	if not inspecting and not held and talking == "":
		if Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT):axis+=1
		if Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT):axis-=1
	if branch_pending and not held:
		if absf(leader_x-6.2)<.025:
			leader_x=6.2
			upper=not upper
			branch_pending=false
			velocity=0
		else:axis=signf(6.2-leader_x)
	if not held:
		velocity = move_toward(velocity,axis*.84,delta*(3.4 if axis!=0 else 4.7))
		leader_x = clampf(leader_x+velocity*delta,.65,17.2)
	for i in range(party.size()):
		var actor = party[i]
		actor.position = stage.floor_point(clampf(leader_x-i*.66,.3,17.5),upper)
		actor.speed = velocity
		if absf(velocity)>.02:actor.facing=signf(velocity)
		actor.held=held
	stage.held=held
	for actor in stage.people.values():actor.look_x=party[0].global_position.x
	stage.view_x = clampf(leader_x+signf(velocity)*.3,5.335,12.665)
	location_label.text = "PIONEER / LAUNCH CHAMBER" if stage.room=="launch" else ("BOARDING GALLERY" if upper and leader_x>9.8 else ("ACCESS RAMP" if upper and leader_x>6.2 else "LOWER CONCOURSE"))
	if inspecting:prompt.text="ESC  /  RETURN TO THE CONCOURSE"
	elif talking!="":prompt.text=""
	elif branch_pending:prompt.text="APPROACHING THE ACCESS RAMP"
	elif stage.room=="terminal" and absf(leader_x-6.2)<.6:prompt.text="[ E ]  LOWER CONCOURSE" if upper else "[ E ]  BOARDING GALLERY  ↗"
	elif (upper or stage.room=="launch") and absf(leader_x-12.4)<.8:prompt.text="[ E ]  USE SHIP TERMINAL"
	elif stage.room=="terminal" and upper and absf(leader_x-14.7)<.8:prompt.text="[ E ]  CAPTAIN VENN"
	elif stage.room=="terminal" and not upper and absf(leader_x-8.6)<.8:prompt.text="[ E ]  JUNO REYES"
	elif stage.room=="terminal" and upper and leader_x>16.4:prompt.text="[ E ]  BOARD PIONEER"
	elif stage.room=="launch" and leader_x<1.1:prompt.text="[ E ]  RETURN TO THE BOARDING GALLERY"
	else:prompt.text=""
	if OS.has_feature("web") and OS.is_debug_build():
		var state={"x":leader_x,"upper":upper,"room":stage.room,"location":location_label.text,"inspecting":inspecting,"inspection_time":stage.inspection_time,"talking":talking,"line":dialogue_line,"branch_pending":branch_pending,"camera_size":stage.camera.size,"camera_position":stage.camera.position,"yaw":party[0].rotation.y,"speed":velocity,"clock":clock,"mesh_count":party[0].meshes.size(),"rigged":party[0].skeleton!=null,"fps":Engine.get_frames_per_second(),"party":party.map(func(a):return {"x":a.position.x,"y":a.position.y,"z":a.position.z,"animation":a.current_animation,"animation_time":a.animator.current_animation_position})}
		JavaScriptBridge.eval("window.farHorizonDepthTest="+JSON.stringify(state),true)

func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey and event.pressed and not event.echo):return
	match event.physical_keycode:
		KEY_E:
			if inspecting or talking!="":return
			if stage.room=="terminal" and absf(leader_x-6.2)<.6:branch_pending=true
			elif (upper or stage.room=="launch") and absf(leader_x-12.4)<.8:
				velocity=0
				inspecting=true
				stage.inspect(story.clues.mission)
			elif stage.room=="terminal" and upper and absf(leader_x-14.7)<.8:_talk("venn")
			elif stage.room=="terminal" and not upper and absf(leader_x-8.6)<.8:_talk("juno")
			elif stage.room=="terminal" and upper and leader_x>16.4:
				stage.configure("launch")
				upper=true
				leader_x=3.8
				for n in stage.people.values():n.visible=false
			elif stage.room=="launch" and leader_x<1.1:
				stage.configure("terminal")
				upper=true
				leader_x=16.6
				for n in stage.people.values():n.visible=true
		KEY_ESCAPE:
			_close_dialogue()
			inspecting=false
			stage.close_inspection()
		KEY_SPACE:held=not held

func _close_dialogue() -> void:
	if is_instance_valid(dialogue):dialogue.queue_free()
	dialogue=null
	talking=""

func _talk(who: String, line: String = "") -> void:
	_close_dialogue()
	talking=who
	if stage.people.has(who):stage.people[who].gesture()
	velocity=0
	dialogue=UI.panel(ui,Rect2(60,425,1246,288),.95)
	var person: Dictionary = story.characters[who]
	dialogue_line=str(person.opening) if line=="" else line
	UI.label(dialogue,str(person.name).to_upper(),Rect2(24,16,1180,28),17,UI.CYAN)
	UI.label(dialogue,dialogue_line,Rect2(24,58,1180,100),23)
	var choices: Array = []
	for option in person.replies:
		if int(option.get("min_session",1))>1 or option.has("requires"):continue
		choices.append(option)
	for i in range(mini(choices.size(),4)):
		UI.button(dialogue,str(choices[i].question),Rect2(24+(i%2)*603,163+(i/2)*47,588,40),_talk.bind(who,str(choices[i].text)),15)
