function collapse(id) {
    let bio = document.getElementById("bio-" + id)
    let img = document.getElementById("img-" + id)
    if (bio.style.maxHeight){
        bio.style.maxHeight = null;
        img.src = "static/plus.png"
    } else {
        bio.style.maxHeight = bio.scrollHeight + "px";
        img.src = "static/minus.png"
    }
}
