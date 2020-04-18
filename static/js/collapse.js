function collapse(id) {
    let panel = document.getElementById("panel-" + id)
    let img = document.getElementById("img-" + id)
    if (panel.style.maxHeight){
        panel.style.maxHeight = null;
        panel.style.marginBottom = null;
        img.src = "static/plus.png"
    } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
        panel.style.marginBottom = "1%";
        img.src = "static/minus.png"
    }
}
