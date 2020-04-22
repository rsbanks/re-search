function setup() {
    $("#searchInputForm").on("submit", function() {
        $('#netidAlert').show('fade');
        getProf();
        return false;
    });

    $("#closeAlert").on("click", function() {
        $('#netidAlert').hide('fade');
        return false;
    });

}

function handleResponse(response)
{ 
   document.getElementById('profResult').innerHTML = response;
}

let request = null;

function getProf()
{   
   let netid = $('#netid').val();
   let url = '/profinfo?netid=' + netid

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

$(document).ready(setup)