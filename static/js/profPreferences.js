// drag and drop functionality inspired by https://www.youtube.com/watch?v=jfYWwQrtzzY

var prof_preference_list = []

function setup() {
   // on close icon clicked (prof_preference)
   document.addEventListener('click', function(e) {
      if (e.target.id === 'closeIconProfPrefence') {
         const value = e.target.getAttribute('data-item');
         const index = prof_preference_list.indexOf(value);
         prof_preference_list = 
            [...prof_preference_list.slice(0, index), ...prof_preference_list.slice(index+1)];
         addProfs();
      }
   })
}

function addProfPreference(name){
    if (!prof_preference_list.includes(name)) {
        prof_preference_list.push(name);
    }
    addProfs();
}

function createProfPreference(name) {
    const div = document.createElement('div');
    div.setAttribute('class', 'prof_preference');
    div.setAttribute('draggable', 'true')
    const span = document.createElement('span');
    span.innerHTML = name;
    const closeIcon = document.createElement('i');
    closeIcon.setAttribute('class', 'material-icons');
    closeIcon.setAttribute('id', 'closeIconProfPrefence')
    closeIcon.setAttribute('data-item', name)
    closeIcon.innerHTML = 'close';

    div.appendChild(span);
    div.appendChild(closeIcon);
    
    return div;
 }

// clear profs
function reset_profs() {
    document.querySelectorAll('.prof_preference').forEach(function(prof) {
       prof.parentElement.removeChild(prof)
    })
 }

 function addProfs() {
    reset_profs();
    prof_preference_list.slice().reverse().forEach(function(profname) {
       const input = createProfPreference(profname);
       $('#profPreferencesDiv').append(input)
    })

    const draggables = document.querySelectorAll('.prof_preference')
    const container = document.querySelector('.profPreferencesDiv')

    draggables.forEach(draggable =>{
      draggable.addEventListener('dragstart', () => {
         draggable.classList.add('dragging')
      })
      draggable.addEventListener('dragend', () => {
         draggable.classList.remove('dragging');
      })
    })

    container.addEventListener('dragover',e  => {
       e.preventDefault()
       const afterElement = getDragAfterElement(container, e.clientY)
       const draggable = document.querySelector('.dragging')
       if (afterElement == null) {
         container.appendChild(draggable)
       } else {
          container.insertBefore(draggable, afterElement)
       }
    })

 }

 function getDragAfterElement(container, y) {
    draggableElements = [...container.querySelectorAll('.prof_preference:not(.dragging)')]

    return draggableElements.reduce((closest, child) => {
       const box = child.getBoundingClientRect()
       const offset = y - box.top - box.height/2
       if (offset < 0 && offset > closest.offset) {
          return { offset: offset, element: child }
       }
       else {
          return closest
       }
    }, {offset: Number.NEGATIVE_INFINITY}).element
 }

 $('document').ready(setup);
