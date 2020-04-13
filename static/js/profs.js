function setup()
{
   $('#nameNetid').focus();
   $('#searchInput').on('input', getResults);

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
}

function handleResponse(response)
{ 
   $('#results').html(response);
}

let request = null

function getResults()
{   
   let name_netid = $('#nameNetid').val();
   // name_netid = encodeURIComponent(name);
   let url = '/searchResults?nameNetid=' + name_netid
   console.log(url)
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

$('document').ready(setup);