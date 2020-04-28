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

   $("#preference-form").on("submit", function() {
      if (document.activeElement.id === 'profSubmit') {
         submitPreferences()
         return false;
      }
   });

   $("#cancelProfSubmit").on("click", function() {
         window.close()
   });

   $("#submit_preferences_form").on("click", function() {
      const draggables = document.querySelectorAll('.prof_preference')
      updatePreferenceList(draggables)

      url = '/profPreferences?'
      url += 'first=' + prof_preference_list[0]
      url += '&second=' + prof_preference_list[1]
      url += '&third=' + prof_preference_list[2]
      url += '&fourth=' + prof_preference_list[3]
      window.open(url)
      return false
   });

   $("#closeProfLimitAlert").on("click", function() {
      $('#profLimitAlert').hide('fade');
      return false;
   });

   $("#submissionSuccessAlertClose").on("click", function() {
      $('#submissionSuccessAlert').hide('fade');
      return false;
   });
}

function addProfPreference(name){
   if (prof_preference_list.length == 4) {
      $('#profLimitAlert').show('fade');
   }
   if (!prof_preference_list.includes(name)) {
      prof_preference_list.unshift(name);
   }
   prof_preference_list = prof_preference_list.slice(0, 4)
   addProfs();
}

function createProfPreference(name) {
    const div = document.createElement('div')
    div.setAttribute('class', 'prof_preference')
    div.setAttribute('draggable', 'true')
    div.setAttribute('data-item', name)
    const span = document.createElement('span')
    span.innerHTML = name;
    const closeIcon = document.createElement('i')
    closeIcon.setAttribute('class', 'material-icons')
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
    prof_preference_list.forEach(function(profname) {
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

 function updatePreferenceList(draggables) {
   prof_preference_list = ['', '', '', '']

   var i = 0
   draggables.forEach(draggable =>{
      if (i==4) {
         return
      }
      prof_preference_list[i] = String(draggable.getAttribute('data-item'))
      i++
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

 function submitPreferences() {

    Advisor1 = $('#firstAdvisorChoice').val()
    Advisor2 = $('#secondAdvisorChoice').val()
    Advisor3 = $('#thirdAdvisorChoice').val()
    Advisor4 = $('#fourthAdvisorChoice').val()

    Advisor1Comments = $('#firstAdvisorChoiceComments').val()
    Advisor2Comments = $('#secondAdvisorChoiceComments').val()
    Advisor3Comments = $('#thirdAdvisorChoiceComments').val()
    Advisor4Comments = $('#fourthAdvisorChoiceComments').val()

    courseSelection = $('#preference-form input:radio:checked').val()

    url = '/submitPreferences?'
    url += 'Advisor1=' + Advisor1
    url += '&Advisor2=' + Advisor2
    url += '&Advisor3=' + Advisor3
    url += '&Advisor4=' + Advisor4

    url += '&Advisor1Comments=' + Advisor1Comments
    url += '&Advisor2Comments=' + Advisor2Comments
    url += '&Advisor3Comments=' + Advisor3Comments
    url += '&Advisor4Comments=' + Advisor4Comments

    url += '&courseSelection=' + courseSelection

    request = null

    if (request != null)
         request.abort();
         request = $.ajax(
      {
         type: "GET",
         url: url,
         success: handleSubmit
      }
   );
 }

 function handleSubmit(response) {

   if (response === "Successful Add") {
      $('#submissionSuccessAlert').show('fade');    
   } else if (response === "Successful Update"){
      $('#submissionSuccessAlert').html("Professor preferences successfully updated!")
      $('#submissionSuccessAlert').show('fade');    
   }  else {
      $('#submissionFailureAlert').show('fade');    
   }

    console.log(response)
 }

 $('document').ready(setup);
