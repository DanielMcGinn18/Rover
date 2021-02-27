
// Button
$(function() {
  $('a#test').on('click', function(e) {
    e.preventDefault()
    $.getJSON('/background_process',
        function(data) {
      //do nothing
    });
    return false;
  });
});

// Request Data
function requestData()
      {
          // Ajax call to get the Data from Flask
          var requests = $.get('/data');
          var tm = requests.done(function (result)
          {
            /*var x = JSON.stringify(requests);
            document.getElementById("sensor1").innerHTML = x*/
            var x = requests.responseJSON
            document.getElementById("actuator1").innerHTML = x[1]
            setTimeout(requestData, 1000);
        });
      }