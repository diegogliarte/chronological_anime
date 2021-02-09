function toggleAdvancedOptions() {
    var advancedOptions = document.getElementById("advancedTextDiv")
    var advancedText = document.getElementById("advancedIconText")
    var advancedIcon = document.getElementById("advancedIcon")
    if (advancedOptions.hidden) {
        advancedOptions.hidden = false // Show
        advancedText.innerText = "Hide advanced options"

    } else {
        advancedOptions.hidden = true // Hide
        advancedText.innerText = "Show advanced options"
    }
    advancedIcon.classList.toggle("fa-plus-circle")
    advancedIcon.classList.toggle("fa-minus-circle")
}

window.onload = function() {
    document.getElementById('excluded').addEventListener('keypress', (e) => addOption(e, "exclude"));
    document.getElementById('included').addEventListener('keypress', (e) => addOption(e, "include"));
}

function addOption(e, option) { // TODO Exclude and Include
    if (e.key === "Enter") {
        if (option === "exclude") {

        } else {

        }
    }
}