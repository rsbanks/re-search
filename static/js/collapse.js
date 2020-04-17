function collapse(id) {
    let panel = document.getElementById("panel-" + id)
    let img = document.getElementById("img-" + id)
    if (panel.style.maxHeight){
        panel.style.maxHeight = null;
        img.src = "static/plus.png"
    } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
        img.src = "static/minus.png"
    }
}
