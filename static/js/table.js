const forbiddenWords = ["unknown", "airing", "n/a"]

function sortTable(n) {
    console.log(n)
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("tableStats");
    switching = true;
    //Set the sorting direction to ascending:
    dir = "asc";
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /*Loop through all table rows (except the
        first, which contains table headers):*/
        for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            /*check if the two rows should switch place,
            based on the direction, asc or desc:*/
            if (dir == "asc") {
                if (compare(x.innerHTML.toLowerCase(), y.innerHTML.toLowerCase(), n)) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (compare(y.innerHTML.toLowerCase(), x.innerHTML.toLowerCase(), n)) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /*If a switch has been marked, make the switch
            and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            //Each time a switch is done, increase this count by 1:
            switchcount++;
        } else {
            /*If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again.*/
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

function compare(a, b, n) {
    if (n == 0) { // Name
        var sorted = [a, b].sort()
        return a == sorted[0]
    }

    if (forbiddenWords.includes(a)) {
        return false
    }
    if (forbiddenWords.includes(b)) {
        return true
    }

    switch (n) {
        case 1: // Air Date
            return a > b
        case 2: // Score
            return a > b
        case 3: // Episodes
            return parseInt(a) > parseInt(b)
        case 4: // Total Duration
            let reggie = /(^(\d*) days?, )?(\d*):(\d*):(\d*)$/

            var dateA = toDate(a)
            var dateB = toDate(b)

            return dateA > dateB
    }
}

function toDate(a) {
    let reggie = /(^(\d*) days?, )?(\d*):(\d*):(\d*)$/
    var a_ = reggie.exec(a)
    var days = 0
    if (a_[2]) {
        days = a_[2]
    }
    return new Date(0, days, a_[3], a_[4], a_[5])
}