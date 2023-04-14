
// Create a function to add a new player to the list
function addPlayer() {
	// Get the player information from the input fields
	var name = document.getElementById("player-name").value;
	var playerClass = document.getElementById("player-class").value;
	var level = document.getElementById("player-level").value;
	var list = document.getElementById("player-list");

	// Create a new list item for the player
	var li = document.createElement("li");
	li.style.color = "white";
	li.onclick = function () {
		var addedPlayers = list.getElementsByTagName("li");
		for (var i = 0; i < addedPlayers.length; ++i) {
			addedPlayers[i].style.backgroundColor = "black";
			}
		this.style.backgroundColor = "#35d5de";
		selection = this;
	};
	li.innerHTML = name + " - " + playerClass + " - Level " + level;

	// Add the new player to the list
	document.getElementById("player-list").appendChild(li);

	// Reset the input fields
	document.getElementById("player-name").value = "";
	document.getElementById("player-class").selectedIndex = 0;
	document.getElementById("player-level").value = "";
}


function removePlayer() {
	selection.parentElement.removeChild(selection);
}

function finishParty() {
	location.href = "combatPage.html"; 
}