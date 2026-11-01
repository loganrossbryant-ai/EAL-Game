"""Author the GM-only Sessions 1–3 aid from Bible v12 and visual deck v14.

This is source data, not a student-response service. The chronology and M-77
ticket choices below were explicitly confirmed by the teacher in this chat.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "far-horizon/data"


def cue(title, text, speaker="", **kw):
    return dict(title=title, text=text, speaker=speaker, **kw)


def person(name, role, sheet, region, opening, replies):
    return dict(name=name, role=role, sheet=sheet, region=region, opening=opening,
                replies=[dict(question=q, text=t) for q, t in replies])


def scene(id, session, title, room, cues, *, npcs=None, clues=None, notes="", focus="", start=520):
    return dict(id=id, session=session, title=title, room=room, cues=cues,
                npcs=npcs or [], clues=clues or [], gm=notes, focus=focus, start=start)


people = {
    "venn": person("Captain Mara Venn", "Captain / CSV-01 Pioneer", "officers.png", 0,
        "Cohort 01, you were selected because this mission requires people who can adapt for decades, not simply survive a launch. Asteria is not a rescue. It is a beginning.", [
        ("Why leave a healthy Earth?", "Because humanity should never have only one home. Earth is not dying. We are choosing to build a second civilization on Asteria-4."),
        ("What do you need from the crew?", "We will disagree. When we do, speak plainly, listen closely, and make your reasons visible to one another."),
        ("What if we are afraid?", "You do not have to know who you will become before you board."),
        ("What should happen to the maintenance record?", "Nobody deletes the record.")]),
    "juno": person("Juno Reyes", "Student liaison", "officers.png", 1,
        "If you forgot to say goodbye to someone, you have about forty seconds to decide whether that matters.", [
        ("I am trying to hide my nervousness.", "Then give your character something to do with their hands. We can see a tightened strap or a folded note. We cannot see a thought."),
        ("What if we want different things?", "Who crosses first? Who hangs back? Who notices? You can disagree and still cross the same line."),
        ("How do we make this ship ours?", "This is your ship too. What would make a room feel like yours?"),
        ("The recreation booking has become an argument.", "Start with what each person wants right now. Then show us what they do to get it.")]),
    "iris": person("Iris", "Ship intelligence", "iris.jpeg", 0,
        "Cohort 01 biometric integration complete.", [
        ("Confirm the destination.", "CSV-01 Pioneer. Destination: Asteria-4. Mission: establish a deliberate second civilization. Earth remains habitable."),
        ("Explain the departments.", "Flight navigates. Science investigates. Engineering maintains the ship. Colony helps a community take shape. Each department depends on the others."),
        ("Can you classify the brief lensing pattern?", "insufficient image duration for classification."),
        ("Why was the unit allowed to do that?", "The unit is operating within maintenance authority.")]),
    "rhee": person("Chief Tomas Rhee", "Chief engineer", "officers_s23.png", 0,
        "Every ship is a collection of problems that have agreed not to happen at the same time.", [
        ("What is that maintenance unit doing?", "That unit is either malfunctioning or developing artistic opinions. Both are unacceptable."),
        ("How should we stop it?", "Shut it down, trap it, redirect it, or cut its power. Protect the ship and the people first."),
        ("Can we trust the repair record?", "Machines lie less often than people. That does not mean they never lie."),
        ("What is wrong with the clocks?", "Four correct clocks can still make one impossible system.")]),
    "vale": person("Dr Elias Vale", "Astrophysicist", "officers_s23.png", 1,
        "If the instrument is wrong, tell me how. If physics is wrong, I need a longer lunch.", [
        ("What do the K-17 readings show?", "The mass and lensing readings cannot be reconciled under normal physics."),
        ("Have we proved an explanation?", "Keep the observation separate from the explanation. Tell us what you measured, then tell us what you think it means."),
        ("Could this be an ordinary relativistic effect?", "Test that model. The magnitude and pattern do not fit ordinary relativistic effects.")]),
    "okafor": person("Dr Nia Okafor", "Chief medical officer", "officers_s23.png", 2,
        "Your body is part of the mission equipment. Unlike the equipment, you are allowed to disagree with me.", [
        ("Why are the biological readings different?", "Your cells do not know they are supposed to agree with the ship clock."),
        ("Should we let the unit repair us?", "Before anyone volunteers to be repaired, come see me."),
        ("Do we know what causes the timing drift?", "The difference is an observation. It is not yet an explanation.")]),
    "m77": person("Maintenance unit M-77", "Automated service unit", "m77.png", 0,
        "OBSTRUCTION DETECTED. REPAIRING OBSTRUCTION.", [
        ("Stop the repair.", "OBSTRUCTION DETECTED. REPAIRING OBSTRUCTION."),
        ("What repair are you talking about?", "PLEASE DO NOT INTERFERE WITH YOUR PREVIOUS REPAIR.")]),
}

# Dialogue follows what the class has actually learned, even after a direct GM jump.
people["venn"]["openings"] = {"2": "Nobody deletes the record.", "3": "Speak plainly. Tell the crew what you see before you tell them what it means."}
people["juno"]["openings"] = {"2": "This is your ship too. What would make a room feel like yours?"}
people["iris"]["openings"] = {"2": "Maintenance authority is active. How may I assist?", "3": "The navigation estimates are available. State your question."}
people["rhee"]["openings"] = {"2": "That unit is either malfunctioning or developing artistic opinions. Both are unacceptable.", "3": "Four correct clocks can still make one impossible system."}
people["okafor"]["openings"] = {"3": "Your cells do not know they are supposed to agree with the ship clock."}
people["venn"]["replies"][3]["requires"] = "ticket"
people["juno"]["replies"][3]["min_session"] = 2
people["iris"]["replies"][2]["requires"] = "frame"
people["iris"]["replies"][3].update(min_session=2, max_session=2)
for i in (0, 1): people["rhee"]["replies"][i].update(min_session=2,max_session=2)
people["rhee"]["replies"][2]["requires"] = "ticket"
people["rhee"]["replies"][3]["requires"] = "clocks"
people["okafor"]["replies"][0]["requires"] = "biometric"
people["okafor"]["replies"][1].update(min_session=2,max_session=2,requires="ticket")
people["okafor"]["replies"][2]["requires"] = "biometric"
people["m77"]["replies"][1]["requires"] = "ticket"
people["okafor"]["replies"].append(dict(question="How can we look after one another?",text="Make time to rest. Speak up when something feels wrong. Looking after a community begins with noticing one another."))
people["rhee"]["replies"].append(dict(question="What should a new engineer remember?",text="Notice what changes. Check before you act. A good question can prevent a very expensive repair."))

clues = {
    "mission": dict(session=1, title="Mission briefing", tag="PIONEER INITIATIVE / 2247", image="mission.jpg", fields=[
        ["VESSEL", "CSV-01 Pioneer"], ["CREW", "Cohort 01"], ["DESTINATION", "Asteria-4"],
        ["MISSION", "Establish humanity’s first truly independent second civilization."],
        ["EARTH", "Still habitable. This is a deliberate beginning, not an evacuation."]],
        note="Why does your character leave a world that is still alive?"),
    "badges": dict(session=1, title="Crew credentials", tag="IDENTITY / DEPARTMENT", image="badges.jpg", fields=[
        ["FLIGHT", "Navigation and a shared direction"], ["SCIENCE", "Questions, investigation and care"],
        ["ENGINEERING", "Keeping the ship working"], ["COLONY", "Helping a community take shape"]],
        note="The badge names a responsibility. The character still chooses how to carry it."),
    "directory": dict(session=1, title="Pioneer orientation", tag="SIX WORKING AREAS", image="", fields=[
        ["BRIDGE & OBSERVATION", "A shared direction"], ["SCIENCE & MEDICAL", "Questions and care"],
        ["STUDENT HABITATION", "Rest and belonging"], ["COLONY COMMONS", "A community taking shape"],
        ["ENGINEERING", "Keeping a world working"], ["CARGO & BOARDING", "What we carry"]],
        note="Each department chooses one place it expects to matter and explains why."),
    "frame": dict(session=1, title="One impossible frame", tag="OBSERVATION / UNCLASSIFIED", image="", fields=[
        ["DURATION", "Less than a second"], ["OBSERVATION", "A bent-light pattern briefly interrupts the starlight."],
        ["IRIS", "insufficient image duration for classification."]],
        note="Describe what you could actually see before deciding what it means."),
    "route": dict(session=1, title="Route log", tag="CSV-01 / ROUTE CONTROL", image="", fields=[
        ["IRIS", "Route correction accepted."], ["VENN", "Who entered that correction?"],
        ["IRIS", "No correction was entered."]], note="Keep the question open."),
    "ticket": dict(session=2, title="Maintenance ticket", tag="M-77 / HAB DECK", image="", fields=[
        ["UNIT", "M-77 / HAB DECK"], ["STATUS", "REPAIRED"], ["COMPLETED", "TOMORROW 14:32"],
        ["TECHNICIAN", "COHORT 01"], ["NOTE", "Collision with unrecorded passenger resolved."]],
        note="The record names a repair the crew has not yet performed. The timestamp is the essential contradiction."),
    "restricted": dict(session=2, title="Restricted access notice", tag="PIONEER / SHIP SECURITY", image="restricted.jpg", fields=[
        ["ACCESS", "RESTRICTED"], ["NOTICE", "Unauthorized access is a violation of ship security protocols."],
        ["RECORD", "All access attempts are logged and reviewed."]], note="The notice establishes a boundary. It does not reveal what is behind it."),
    "arrival": dict(session=3, title="Two arrival estimates", tag="FLIGHT / PRIVILEGED FACT", image="", fields=[
        ["ESTIMATE A", "37 DAYS"], ["ESTIMATE B", "102 DAYS"], ["ROUTE CHANGE", "NONE RECORDED"]],
        note="Fact: the navigation estimates change without a route change. An explanation is still an inference."),
    "lensing": dict(session=3, title="K-17 anomaly readout", tag="SCIENCE / PRIVILEGED FACT", image="anomaly.jpg", fields=[
        ["GRAVITATIONAL LENSING", "+317%"], ["RADIATION SPIKE", "DETECTED"], ["SPACETIME VARIANCE", "UNSTABLE"],
        ["SIGNAL ORIGIN", "UNKNOWN"]], note="The mass and lensing readings cannot be reconciled under normal physics. What can you establish from these observations?"),
    "clocks": dict(session=3, title="Unsynchronized clocks", tag="ENGINEERING / PRIVILEGED FACT", image="clocks.jpg", fields=[
        ["SHIP", "14:27"], ["EARTH / UTC", "14:32"], ["K-17", "14:19"], ["MEDBAY", "14:31"],
        ["HARDWARE CHECK", "The clocks are functioning correctly."]],
        note="Fact: the clocks function correctly, but no longer agree. What would you need to observe next?"),
    "biometric": dict(session=3, title="Biometric timing monitor", tag="COLONY / PRIVILEGED FACT", image="biometric.jpg", fields=[
        ["HEART RATE", "42 / MIN"], ["SpO₂", "97%"], ["TEMPERATURE", "35.1°C"], ["EEG", "IRREGULAR"],
        ["OBSERVATION", "Biological clocks / cellular timing are drifting differently from ship time."]],
        note="Biological timing differs from ship time. Keep the observation separate from an explanation of its cause."),
    "both": dict(session=3, title="Which one is right?", tag="IRIS / TWO CORRECT READINGS", image="", fields=[
        ["ARRIVAL A", "37 DAYS"], ["ARRIVAL B", "102 DAYS"], ["IRIS", "Both."]],
        note="The contradiction is confirmed. The cause remains unresolved."),
    "packet": dict(session=3, title="Incoming packet", tag="DEEP-SPACE COMMUNICATIONS", image="", fields=[
        ["SOURCE", "CSV-01 PIONEER"], ["TIMESTAMP", "+103 DAYS"], ["STATUS", "SEALED / CONTENT NOT OPENED"]],
        note="Only the source and timestamp are available. The contents remain sealed."),
}

scenes = [
    scene("s1_terminal",1,"The last room on Earth","terminal",[
        cue("2247 / Cohort 01", "Earth is not dying. That is what makes leaving harder. Ahead waits CSV-01 Pioneer. Why does your character leave?"),
        cue("A beginning", people['venn']['opening'], "venn"),
        cue("Want and need", "What does your character WANT? What might they NEED to learn? What do they fear losing? Keep one object from Earth.", clue="mission")],
        npcs=["juno","venn","iris"], clues=["mission","badges"], focus="Ensemble • given circumstances • want and need",
        notes="Bible pp.4–6. Earth is healthy. Character work stays on paper / in live performance. Do not make navigation depend on a form. Keep Earth objects in your own notes for later callbacks."),
    scene("s1_boarding",1,"The boarding threshold","terminal",[
        cue("Thirty seconds to board", "One character wants to look back. One wants to move. One hides nervousness. Someone notices something strange."),
        cue("Cross together", "Create a stage picture, then physically cross a line that represents leaving Earth. What did the ensemble communicate before anybody spoke?", clue="badges")],
        npcs=["juno","venn"], clues=["mission","badges"], start=1760, focus="Stage picture • status • ensemble",
        notes="The crossing is performed in the classroom. Nothing is timed automatically. Once each company has a clear crossing moment, cut to launch. Student choice remains open."),
    scene("s1_launch",1,"Launch","launch",[
        cue("Take your places", "The restraints lock. The launch tower waits beyond the glass. Take one last breath of the world you know."),
        cue("Ignition", "Vibration. Pressure. The impossible sight of Earth dropping beneath you.", effect="rumble", sfx=1),
        cue("The tower falls away", "The cities are still lit. The oceans still move. Everything familiar grows smaller behind the glass.", effect="ascent"),
        cue("Engine cutoff", "The engines cut. A pen lifts from a console. Somebody laughs. Somebody else does not.", effect="float", sfx=3),
        cue("One ship. One floor.", "Welcome aboard Pioneer.", "venn", effect="float")], npcs=["iris"], focus="Wonder • visible action and silent reaction",
        notes="Launch BEFORE the tour: teacher-confirmed chronology. Every beat is manually held. The pen floats only after cutoff. No countdown or automatic failure."),
    scene("s1_habitation",1,"A place aboard Pioneer","habitation",[
        cue("Meet the crew", "Juno Reyes / student liaison. Chief Tomas Rhee / engineering. Dr Nia Okafor / medical. Your shipmates are ready to meet you."),
        cue("A quick orientation", "Choose one place your department expects to matter. Explain why. Keep the class together.", clue="directory"),
        cue("A room of your own", "This is your ship too. What would make a room feel like yours?", "juno"),
        cue("What we carry", "Keep the Earth object. What can it hold that the ship cannot replace?")], npcs=["juno","rhee","okafor"], clues=["directory","badges"],
        focus="Belonging • a choice with a reason", notes="Montage the ship; do not run a room-by-room dungeon. The source does not supply a numbered canonical deck map, so the six-area directory is unnumbered."),
    scene("s1_observation",1,"One impossible frame","bridge",[
        cue("Beyond the glass", "The observation glass darkens. The stars brighten. Watch in silence for a moment."),
        cue("A fleeting pattern", "For less than a second, bent light interrupts the starlight. Then the pattern is gone.", effect="seed"),
        cue("Unclassified", "insufficient image duration for classification.", "iris", clue="frame"),
        cue("Three screenplay lines", "On paper: one action line showing departure, one spoken line, and one silent visible reaction. Write what an audience can SEE and HEAR.")], npcs=["venn","iris"], clues=["frame"],
        focus="Observation • action lines • uncertainty", notes="Never confirm that the pattern was human. Preserve uncertainty. Do not explain K-17, the biological marker or the route’s hidden purpose. The writing prompt is optional presentation support, never a gate."),
    scene("s1_route",1,"The route log","bridge",[
        cue("Route log", "Route correction accepted.", "iris"),
        cue("Captain Venn", "Who entered that correction?", "venn"),
        cue("Iris", "No correction was entered.", "iris", clue="route"),
        cue("End of Session 1", "Keep the Earth objects. Keep the question open.", blackout=True)], clues=["route"],
        focus="A contradiction • the closing image", notes="Exact canonical exchange, Bible p.5. Hold after each line for student reaction. The final cut is manually advanced."),
    scene("s2_recreation",2,"An ordinary life problem","recreation",[
        cue("Almost ordinary", "Meal packets taste bad. Somebody has misplaced equipment. A recreation booking has become a ridiculous argument."),
        cue("Objective and obstacle", "Play one ordinary disagreement. What does each character want right now? What action do they take to get it?")], npcs=["juno","okafor"],
        focus="Objective • physical action", notes="Bible pp.7–9. Let personality appear before danger. Keep everyday friction under five minutes. No anomaly explanation yet."),
    scene("s2_malfunction",2,"A perfectly functional door","corridor",[
        cue("An unwanted repair", "A maintenance unit rolls through the habitation service corridor and welds a perfectly functional door shut.", effect="weld"),
        cue("Chief Rhee", "That unit is either malfunctioning or developing artistic opinions. Both are unacceptable.", "rhee", effect="weld"),
        cue("M-77", "OBSTRUCTION DETECTED. REPAIRING OBSTRUCTION.", "m77", effect="weld")], npcs=["rhee","m77"], focus="Event → choice → consequence",
        notes="The teacher confirmed M-77 as canonical, with the bible’s complete clue. The P-73 / MT-4487 visual variant is not used as a conflicting fact."),
    scene("s2_encounter",2,"Three rounds to stop the repairs","corridor",[
        cue("Protect the ship", "Stop the units before they seal three spaces or dismantle essential equipment. Hack, trap, cut power, distract, redirect, defend or use the environment.", effect="encounter", round=0),
        cue("Round 1 / the door", "A minor drone welds a door. Show a clear preparation, action and reaction. Keep stage-combat distance.", effect="round1", round=1),
        cue("Round 2 / life support", "A second drone begins dismantling a life-support access panel. The environment has changed. What tactic changes with it?", effect="round2", round=2),
        cue("Round 3 / previous repair", "PLEASE DO NOT INTERFERE WITH YOUR PREVIOUS REPAIR.", "m77", effect="round3", round=3),
        cue("Resolve the incident", "The encounter ends through shutdown, retreat or containment. The service record survives.", effect="contained", round=3)],
        npcs=["rhee","m77"], focus="Objective combat • gesture and movement", notes="Exactly three rounds, advanced by the GM. Large M-77 has TWO threat boxes; two minor repair drones have ONE each. No real contact during classroom staging. Accept negotiation, hacking and containment as valid. The clue must survive any resolution. Compression option: one unit, two rounds, then the log."),
    scene("s2_record",2,"A repair from tomorrow","corridor",[
        cue("The service history", "Rhee opens the service history. His expression changes before he says anything.", effect="contained"),
        cue("Maintenance ticket", "Completed by Cohort 01. Tomorrow at 14:32.", clue="ticket", effect="contained"),
        cue("Chief Rhee", "Machines lie less often than people. That does not mean they never lie.", "rhee", effect="contained"),
        cue("Captain Venn", "Nobody deletes the record.", "venn", effect="contained"),
        cue("Event / choice / consequence", "What happened? What choice did your company make? What followed? On paper, capture a 6–8 line scene with one gesture before the first spoken reaction.", effect="contained")],
        npcs=["rhee","iris"], clues=["ticket"], focus="Consequence • an impossible timestamp", notes="Must reach: the repaired-by-Cohort record dated tomorrow. Keep the exact M-77 / TOMORROW 14:32 / unrecorded passenger text. Required clues never depend on winning a perception or combat roll."),
    scene("s2_restricted",2,"A boundary aboard your ship","restricted",[
        cue("Restricted access", "All access attempts are logged and reviewed.", clue="restricted"),
        cue("What changed?", "Who now trusts machines more, less, or differently? Keep the maintenance record as evidence.")], npcs=["rhee","iris"], clues=["restricted","ticket"],
        focus="A boundary • a relationship changes", notes="PPT slides 19–20. Show the notice without opening classified files or introducing later revelations. This is an optional compressible beat; the tomorrow record remains Session 2’s essential endpoint."),
    scene("s3_observation",3,"The first anomaly","k17",[
        cue("Four observations", "The departments have different evidence. Keep the whole class together. Investigate, then report one FACT, one INFERENCE and one QUESTION."),
        cue("Look before explaining", "A fact is what the evidence shows. An inference is an explanation you draw from it. A question names what remains unknown.")], npcs=["vale","okafor","iris"],
        focus="Voice • evidence sharing", notes="Bible pp.10–11. Synchronized investigation, not four separate adventures. Give each department its privileged fact. Do not present the later explanation as established truth."),
    scene("s3_evidence",3,"Four departments, four anomalies","k17",[
        cue("Flight", "Navigation changes between 37 and 102 days to Asteria without a route change.", clue="arrival"),
        cue("Science", "K-17 mass and lensing readings cannot be reconciled under normal physics.", clue="lensing"),
        cue("Engineering", "The clocks are functioning correctly. They are no longer synchronized.", clue="clocks"),
        cue("Colony", "Biological clocks and cellular timing are drifting differently from ship time.", clue="biometric")],
        npcs=["vale","okafor","rhee"], clues=["arrival","lensing","clocks","biometric"], focus="Privileged facts • four evidence cards",
        notes="Use each clue independently and visibly. The v14 display readings are retained as prop observations, not a newly proven mechanism. The medical readings describe fictional crew. Keep later explanations out of this presentation."),
    scene("s3_council",3,"The evidence council","k17",[
        cue("Fact first", "Each company states exactly one FACT. If a theory is offered as fact, rephrase it as an INFERENCE."),
        cue("A question worth asking", "What do we know? What do we think? What would we need to observe next?"),
        cue("Dr Vale", "If the instrument is wrong, tell me how. If physics is wrong, I need a longer lunch.", "vale"),
        cue("Dr Okafor", "Your cells do not know they are supposed to agree with the ship clock.", "okafor")],
        npcs=["vale","okafor","rhee"], clues=["arrival","lensing","clocks","biometric"], focus="Fact • inference • question",
        notes="This is the academic heart of the investigation. A multiple-futures theory can be offered as a model, but is not confirmed. Ask for evidence. The clue board only shows cards you have explicitly revealed."),
    scene("s3_iris",3,"Which one is right?","k17",[
        cue("Iris", "Estimated time to Asteria: thirty-seven days.", "iris"),
        cue("The crew", "Navigation says one hundred and two.", "crew"),
        cue("Iris", "Correct.", "iris"),
        cue("The crew", "Which one is right?", "crew"),
        cue("Iris", "Both.", "iris", clue="both"),
        cue("A frame of reference", "Correct according to what frame of reference?", "venn"),
        cue("Iris", "Yes.", "iris")], npcs=["iris","venn"], clues=["arrival","both"], focus="Pace • pause • pitch • volume • emphasis",
        notes="The iconic exchange is manually cued line by line. Pause before ‘Both.’ Crew lines belong to the live class, not a generated student voice. Do not give a tidy explanation."),
    scene("s3_lensing",3,"The pattern returns","k17",[
        cue("Look again", "Behind Iris, the observation window catches K-17. Watch the distorted starlight."),
        cue("A recurrence", "The lensing ripple briefly takes the same almost-human geometry. This time several people can notice it. Then the stars snap back.", effect="recurrence"),
        cue("Uncertainty", "What did the audience see? Which part of your explanation remains an inference?")], npcs=["iris","vale"], clues=["frame","both"],
        focus="Recognition • reaction • uncertainty", notes="Second visual seed only; do not name a Fracture Entity or confirm a person. Normal background motion must not imitate this clue before you cue it."),
    scene("s3_craft",3,"Dialogue under uncertainty","k17",[
        cue("Make uncertainty audible", "Replay the exchange using one deliberate vocal choice: pace, pause, pitch, volume or emphasis. Explain its effect."),
        cue("Capture the evidence", "On paper: what do we KNOW, what do we THINK, and what QUESTION should the characters investigate next?")],
        npcs=["vale","okafor"], clues=["arrival","lensing","clocks","biometric","both"], focus="Voice • subtext • evidence language",
        notes="Capture the individual check before the sealed packet. The bible requires an immediate cut after the +103 DAYS header. No writing input or assessment gate exists in the game."),
    scene("s3_packet",3,"A packet from Pioneer","k17",[
        cue("Incoming", "A packet arrives through deep-space communications."),
        cue("The header", "Source: CSV-01 Pioneer. Timestamp: plus one hundred and three days.", clue="packet"),
        cue("End of Session 3", "The packet remains sealed.", blackout=True)], clues=["packet"],
        focus="The cliffhanger • stop before the contents", notes="Bible p.11. End immediately on the header. Keep the packet sealed. This draft stops before all later-session material."),
]

glossary = [
    ["given circumstances", "The established situation a character enters.", "既定情境", "주어진 상황", "与えられた状況"],
    ["ensemble", "Performers working together to tell the story.", "集体配合", "앙상블 / 단체 협력", "アンサンブル"],
    ["stage picture", "The meaning created by bodies and positions on stage.", "舞台画面", "무대 구도", "舞台構図"],
    ["status", "A character’s power or position in a relationship.", "人物地位", "인물의 지위", "人物の立場"],
    ["objective", "What the character is trying to achieve now.", "行动目标", "행동 목표", "行動目標"],
    ["obstacle", "What stands in the way of the objective.", "阻碍", "장애물", "障害"],
    ["tactic", "An action used to pursue an objective.", "策略", "전술", "戦術"],
    ["consequence", "What follows from an event or choice.", "后果", "결과", "結果"],
    ["gesture", "A physical action that communicates meaning.", "姿态与动作", "몸짓", "身振り"],
    ["reaction", "An observable response to an event.", "反应", "반응", "反応"],
    ["fact", "Something the available evidence establishes.", "事实", "사실", "事実"],
    ["inference", "An explanation drawn from evidence.", "推断", "추론", "推論"],
    ["evidence", "Observations or information supporting a claim.", "证据", "증거", "証拠"],
    ["uncertainty", "What remains unresolved or unknown.", "不确定性", "불확실성", "不確実性"],
    ["contradiction", "Two statements or observations that do not agree.", "矛盾", "모순", "矛盾"],
    ["pace", "How quickly or slowly a performer speaks.", "语速", "말의 속도", "話す速さ"],
    ["pause", "A deliberate break that creates meaning.", "停顿", "멈춤", "間"],
    ["pitch", "How high or low a voice sounds.", "音高", "음높이", "声の高さ"],
    ["volume", "The controlled loudness of a voice.", "音量", "목소리 크기", "声量"],
    ["emphasis", "Giving a word or action extra importance.", "强调", "강조", "強調"],
    ["subtext", "Meaning suggested beneath the spoken words.", "潜台词", "숨은 의미", "サブテキスト"],
]


def build():
    DEST.mkdir(parents=True, exist_ok=True)
    campaign = dict(version=2, title="The Far Horizon", mode="GM visual aid", sessions=[
        dict(id=1,title="Welcome to Pioneer",must="Board, launch, keep an Earth object, glimpse an anomaly and end on the route log."),
        dict(id=2,title="The Pioneer",must="Resolve the maintenance incident and reveal the repair record from tomorrow."),
        dict(id=3,title="The First Anomaly",must="Connect four anomalies, hear Iris say ‘Both,’ and end on the sealed +103 DAYS packet.")],
        characters=people, clues=clues, scenes=scenes,
        glossary=[dict(term=x[0],definition=x[1],zh=x[2],ko=x[3],ja=x[4]) for x in glossary],
        provenance=dict(bible="GM Master Bible v12, pp.4–11",visuals="Visual Aid v14, slides 1–28 only",confirmed=["M-77 / tomorrow 14:32 / unrecorded passenger", "Launch before introduction/tour"]))
    (DEST / "campaign.json").write_text(json.dumps(campaign,indent=2,ensure_ascii=False)+"\n")
    print(f"Authored {len(scenes)} GM scenes, {len(clues)} clue cards, {len(people)} speakers and {len(glossary)} academic terms.")


if __name__ == "__main__":
    build()
