var loading = false

function remove(id, index) {
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

function reverseSort(sort_option) {
    axios({
        method: 'post',
        url: '/sort_reverse',
        data: {
            sort_option: sort_option,
        },
    }).then(response => location.reload());
}

function checkForm(id) {
    var element = document.getElementById(id)
    element.style.color = "#1F1F1F"
    element.style.background = "#EFEFEF"
    element.value = 'LOADING...'
    element.disabled = true
    document.getElementById("submitter").value = element.name
    element.form.submit();
}

function checkStep(id, name) {
    checkFirst(id)
    axios({
        method: 'post',
        url: '/process',
        data: {
            data: name,
        },
    });
}
