class_name Conversations
extends RefCounted

static func opening(who: String, aboard: bool) -> String:
	match who:
		"venn":
			if aboard:
				return "Welcome aboard Pioneer. The ship has six decks. Each department should choose one place it thinks will matter most—and tell us why."
			return "Cohort 01, you were selected because this mission requires people who can adapt for decades, not simply survive a launch. Asteria is not a rescue. It is a beginning. If you board, you are agreeing to help decide what that beginning becomes."
		"juno":
			if aboard:
				return "This is your ship too. Find somewhere you can imagine belonging. A bunk, a table, a view. What would make a room feel like yours?"
			return "If you forgot to say goodbye to someone, you have about forty seconds to decide whether that matters. Take a breath. Who are you leaving behind?"
		"iris": return "Cohort 01 biometric integration complete. Department credentials recognized. How may I assist?"
	return "Pioneer Initiative. People. Worlds. Possibilities."

static func choices(who: String, aboard: bool) -> Array:
	match who:
		"venn":
			if aboard:
				return [["What does a captain need from us?", "We will disagree. When we do, speak plainly, listen closely, and make your reasons visible to one another."], ["How will we decide what matters?", "Start with the people who depend on your work. Explain your choice. Another department may see a need you have missed."], ["I'm not sure I belong here.", "You do not have to know who you will become before you board. We will need more than one kind of courage."]]
			return [["Why leave a world that is still alive?", "Because humanity should never have only one home. Earth is not dying. We are choosing to build a second civilization on Asteria-4."], ["What if we are afraid?", "You do not have to know who you will become before you board. Fear can travel with you. It does not have to make the decision."], ["What are we agreeing to?", "To adapt for decades, work across departments, and help decide what this beginning becomes. The mission needs people who can change."], ["I am not ready to say goodbye.", "Then take this moment. What would staying cost your character? What might leaving make possible? The choice should mean something."]]
		"juno":
			if aboard:
				return [["What did you bring from Earth?", "Something small enough to carry and large enough to remind me. What is your object? Tell us what it holds that the ship cannot replace."], ["I want a fresh start.", "A fresh start still has you in it. What do you want here—and what might you need to learn before you can have it?"], ["Can we choose how to use this space?", "Begin with one detail. A shared routine, a plant, a place to sit. Tell your company what you would change and why."]]
			return [["I'm trying not to look nervous.", "Then give your character something to do with their hands. We can see a tightened strap or a folded note. We cannot see a thought."], ["I want to look back once.", "Then look. Let the others decide whether to wait or keep walking. That picture can tell us something before anybody speaks."], ["What if our company wants different things?", "Show us. Who crosses first? Who hangs back? Who notices? You can disagree and still cross the same line."], ["What should we put in our crew log?", "Why you are leaving, what you want, what you might need to learn, what you fear losing, and one object from Earth. Use your fictional character's name."]]
		"iris":
			return [["Confirm our destination.", "CSV-01 Pioneer. Destination: Asteria-4. Mission: establish a deliberate second civilization. Earth remains habitable."], ["What is my department's role?", "Flight navigates. Science investigates. Engineering maintains the ship. Colony helps a community take shape. Each department depends on the others."], ["What does our badge do?", "A badge connects a crew identity to a department. The person behind that identity still chooses what to say and do."]]
	return []
