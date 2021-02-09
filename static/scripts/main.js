function remove(url, index) {
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
            url: url,
        },
    });
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

function downloadString(text, fileType, fileName) {
    text = text.join("\n")
    var blob = new Blob([text], {type: fileType});
    var a = document.createElement('a');
    a.download = fileName;
    a.href = URL.createObjectURL(blob);
    a.dataset.downloadurl = [fileType, a.download, a.href].join(':');
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () {
        URL.revokeObjectURL(a.href);
    }, 1500);
}