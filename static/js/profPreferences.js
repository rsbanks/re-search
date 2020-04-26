var prof_preference_list = []

function addProfPreference(name){
    if (!prof_preference_list.includes(name)) {
        prof_preference_list.push(name);
    }
    addProfs();
}

function createProfPreference(name) {
    const div = document.createElement('div');
    div.setAttribute('class', 'prof_preference');
    const span = document.createElement('span');
    span.innerHTML = name;

    div.appendChild(span);
    
    return div;
 }

// clear profs
function reset_profs() {
    document.querySelectorAll('.prof_preference').forEach(function(prof) {
       prof.parentElement.removeChild(prof);
    })
 }

 function addProfs() {
    reset_profs();
    prof_preference_list.slice().reverse().forEach(function(profname) {
       const input = createProfPreference(profname);
       $('#profPreferencesDiv').prepend(input);
    })
 }