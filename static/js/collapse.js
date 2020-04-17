function collapse(id) {
    let bio = document.getElementById("bio-" + id)
    if (bio.style.maxHeight){
        bio.style.maxHeight = null;
        bio.style.marginBottom = null;
    } else {
        bio.style.maxHeight = bio.scrollHeight + "px";
        bio.style.marginBottom = "2vh"
    }
}
