function setup() {
    $("#searchInputForm").on("submit", function() {
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
    if (response == '') {
        $('#netidAlert').show('fade');
    }
    else {
        document.getElementById('profResult').innerHTML = response;

        $("#saveForm").on("submit", function() {
             displayProf();
             return false;
         });
    }
}

function handleResponseDisplay(response)
{ 
    document.getElementById('profResult').innerHTML = response;

    $("#editAnotherBtn").on("submit", function() {
        window.location.href("index_tara.html");
    });
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

function displayProf()
{   
   let netid = $('#netid').val();
   let url = '/displayprof?netid=' + netid;
   url += '&title=' + $('#title').val()
   url += '&firstname=' + $('#firstname').val()
   url += '&lastname=' + $('#lastname').val()
   url += '&email=' + $('#email').val()
   url += '&phone=' + $('#phone').val()
   url += '&website=' + $('#website').val()
   url += '&rooms=' + $('#rooms').val()
   url += '&department=' + $('#department').val()
   url += '&areas=' + $('#areas').val()
   url += '&bio=' + $('#bio').val()

   if (request != null)
      request.abort();
   request = $.ajax(
      {
         type: "GET",
         url: url,
        success: handleResponseDisplay
      }
   );
}


$(document).ready(setup)