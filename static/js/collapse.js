function collapse(id) {
    let bio = document.getElementById("bio-" + id)
    if (bio.style.maxHeight){
        bio.style.maxHeight = null;
    } else {
        bio.style.maxHeight = bio.scrollHeight + "px";
    }
}
