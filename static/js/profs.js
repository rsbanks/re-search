function setup()
{
   $('#nameNetid').focus();
   $('#searchInput').on('input', getResults);

   // Do not refresh page when enter key is pressed
   $('#searchInput').keypress(function(event){
      var keycode = (event.keyCode ? event.keyCode : event.which);
      if(keycode == '13') {
         event.preventDefault();
      }
  });

   let request = null

   // show all profs on load
   let url = '/searchResults'
   if (request != null)
      request.abort();
   request = $.ajax(
      {
         type: "GET",
         url: url,
         success: handleResponse
      }
   );

   // on enter key pressed in Research Area form
   $('#tagInput').keypress(function(event){
      var keycode = (event.keyCode ? event.keyCode : event.which);
      if(keycode == '13') {
         label = $('#newTagInput').val()
         if (label.length != 0) {
            if (!tags.includes(label)) {
               tags.push(label);
               addTags();
               getResults();
            }
            $('#newTagInput').val("");
         }
      }
  });

  // on close icon clicked (tag)
  document.addEventListener('click', function(e) {
   if (e.target.tagName === 'I') {
      const value = e.target.getAttribute('data-item');
      const index = tags.indexOf(value);
      tags = [...tags.slice(0, index), ...tags.slice(index+1)];
      addTags();
      getResults();
   }
})

}

function handleResponse(response)
{ 
   document.getElementById('results').innerHTML = response;
}

request = null

function getResults()
{   
   let name_netid = $('#nameNetid').val();
   let url = '/searchResults?nameNetid=' + name_netid

   if (tags.length != 0) {
      url += '&area=';
      tags.forEach(function(tag) {
         url += tag + ",";
      })
      url = url.slice(0, url.length-1);
   }

   if (request != null)
      request.abort();
   request = $.ajax(
      {
         type: "GET",
         url: url,
         success: handleResponse
      }
   );
}

var tags = [];

function createTag(label) {
   const div = document.createElement('div');
   div.setAttribute('class', 'tag');
   const span = document.createElement('span');
   span.innerHTML = label
   const closeIcon = document.createElement('i');
   closeIcon.setAttribute('class', 'material-icons');
   closeIcon.setAttribute('id', 'closeIcon')
   closeIcon.setAttribute('data-item', label)
   closeIcon.innerHTML = 'close';

   div.appendChild(span);
   div.appendChild(closeIcon);
   
   return div;
}

// clear tags
function reset() {
   document.querySelectorAll('.tag').forEach(function(tag) {
      tag.parentElement.removeChild(tag);
   })
}

function addTags() {
   reset();
   tags.slice().reverse().forEach(function(tag) {
      const input = createTag(tag);
      $('#tag-input-div').prepend(input);
   })
}

$('document').ready(setup);