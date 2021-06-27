// Request Data
function requestData()
      {
          // Ajax call to get the Data from Flask
          var requests = $.get('/data');
          var tm = requests.done(function (result)
          {
            /*var y = JSON.stringify(requests);
            document.getElementById("test").innerHTML = y*/
            var x = requests.responseJSON
            document.getElementById("actuator2").innerHTML = x[1]
            document.getElementById("Speed").value = x[1]
            setTimeout(requestData, 1000);
        });
      }