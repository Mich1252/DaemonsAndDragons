



function goHome() {
	location.href = "home.html";
}

function createEncounter() {
	location.href = "createEncounter.html";
}

function loadEncounter() {
	const files = document.getElementById("encounter_loadInput")

	files.click();
}

function loadCombat() {
	const files = document.getElementById("combat_loadInput")
	files.click();
}

function saveCombat() {
	const files = document.getElementById("combat_saveInput")
	files.click();
}