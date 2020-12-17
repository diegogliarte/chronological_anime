var loading = false

function remove(id, index){
    var anime = document.getElementById("new" + index)
    if (anime.style.textDecoration === "line-through") {
        anime.style.textDecoration = "none"
        anime.style.color = "#EFEFEF"
    } else {
        anime.style.textDecoration = "line-through"
        anime.style.color = "#808080"
    }
    axios({
        method: 'post',
        url: '/delete',
        data: {
            id: id,
        },
    });
}

function reverseSort(sort_option){
    axios({
        method: 'post',
        url: '/sort_reverse',
        data: {
          sort_option: sort_option,
        },
    }).then(response => location.reload());
}

function loadingForm(id) {
    var button = document.getElementById(id)
    button.type = "text"
    button.readOnly = true
}
