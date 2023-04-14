

function Load() {
	const files = document.getElementById("file_input")
	files.onchange = function() {
		location.href = "combatPage.html";
    };
	files.click();
}