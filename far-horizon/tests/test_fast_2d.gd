extends SceneTree
func _initialize() -> void:
	var scene=load("res://scenes/main.tscn").instantiate()
	root.add_child(scene)
	await process_frame
	await process_frame
	assert(root.find_children("*","Node3D",true,false).size()==0)
	assert(scene.party.size()==4)
	for member in scene.party:assert(member.has_rig and member.puppet.ready_rig)
	assert(scene.story.scenes.size()==3)
	assert(scene.story.clues.ticket.fields[2][1]=="TOMORROW 14:32")
	assert(scene.state.data.threats==[2,1,1])
	print("FAST_2D_NATIVE_PASS: four original 2D rigs, zero Node3D objects, three scenes, canon ticket/counters")
	quit()
