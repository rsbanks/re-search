function setup() {
    $("#searchInputForm").on("submit", function() {
        getProf();
        return false;
    });

    $("#closeFailureAlert").on("click", function() {
        $('#netidAlertFailure').hide('fade');
        return false;
    });

    $("#closeSuccessAlert").on("click", function() {
        $('#netidAlertSuccess').hide('fade');
        return false;
    });

    $("#closeSuccessDeleteAlert").on("click", function() {
        $('#netidAlertDeleteSuccess').hide('fade');
        return false;
    });

    $("#confirmDelete").on("click", function() {
        deleteProf();
        $('#deleteProfModal').modal('hide')
     });

}

function handleResponse(response)
{ 
    $('#netidAlertFailure').hide();

    document.getElementById('profResult').innerHTML = response;
    $("#saveForm").on("submit", function() {
        if (document.activeElement.id == 'Save') {
            displayProf();
        } else if(document.activeElement.id == 'Cancel') {
            $('#netidSearch').focus();
            document.getElementById('profResult').innerHTML = null;
            $('#netidAlertSuccess').hide('fade');
            $('#netidAlertDeleteSuccess').hide('fade');
            $('#netidAlertDeleteFailure').hide('fade');
        } else if(document.activeElement.id == 'Delete') {
            $('#deleteProfModalBody').html('Are you sure you want to delete'  +
            ' the professor with netid \'' + $('#netidSearch').val() + '\' ?')
            $('#deleteProfModal').modal()
        }
            return false;
        });

        window.addEventListener('load', function() {
        document.querySelector('input[type="file"]').addEventListener('change', function() {
            console.log('file hello');
            if (this.files && this.files[0]) {
                var img = document.querySelector('img');  // $('img')[0]
                img.src = URL.createObjectURL(this.files[0]); // set src to blob url
                img.onload = imageIsLoaded;
            }
        });
        });
        
        function imageIsLoaded() { 
        alert(this.src);  // blob url
        // update width and height ...
        }
}

function handleResponseDisplay(response)
{ 
    $('#netidAlertSuccess').show('fade');
    document.getElementById('profResult').innerHTML = response;

    $("#editOtherForm").on("submit", function() {
        document.getElementById('profResult').innerHTML = null;
        $('#netidAlertFailure').hide('fade');
        $('#netidAlertSuccess').hide('fade');
        $('#netidSearch').focus();
        return false;
    });
}

function handleDelete(response) 
{
    $('#netidAlertDeleteSuccess').show('fade');
    document.getElementById('profResult').innerHTML = null;
}

function handleGetPreferences(response) 
{
   console.log("Download request recieved");
   download("preferences.csv", response);
}

function handleGetMatches(response) 
{
   console.log("Download request recieved");
   download("matches.csv", response);
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
  }

let request = null;

function getProf()
{   
   let netid = $('#netidSearch').val();
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

function deleteProf() 
{
    url = '/deleteprof?netid=' + $('#netid').val();
    if (request != null)
        request.abort();
    request = $.ajax(
        {
            type: "GET",
            url: url,
            success: handleDelete
        }
    );
}

function getPreferences() 
{
    url = '/getPreferences';
    if (request != null)
        request.abort();
    request = $.ajax(
        {
            type: "GET",
            url: url,
            success: handleGetPreferences
        }
    );
}

function getMatches() 
{
    url = '/getMatches';
    if (request != null)
        request.abort();
    request = $.ajax(
        {
            type: "GET",
            url: url,
            success: handleGetMatches
        }
    );
}

$(document).ready(setup)