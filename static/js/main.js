
/* Request Data */

function requestData()
        {
            // Ajax call to get the Data from Flask
            var requests = $.get('/data');
            var tm = requests.done(function (result)
            {
	            /*var x = JSON.stringify(requests);
	            document.getElementById("sensor1").innerHTML = x*/
	            var x = requests.responseJSON
	            document.getElementById("sensor1").innerHTML = '<i class="fas fa-satellite-dish"></i>' + x[1]
	            document.getElementById("sensor2").innerHTML = '<i class="fab fa-raspberry-pi"></i>' + x[2]
	            setTimeout(requestData, 1000);
	        });
        }