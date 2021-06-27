
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
	            document.getElementById("sensor2").innerHTML = x[1]
	            document.getElementById("actuator2").innerHTML = x[2]
            	document.getElementById("Speed").value = x[2]
            	document.getElementById("actuator1").innerHTML = x[3]
            	document.getElementById("direction").innerHTML = x[4]
	            setTimeout(requestData, 1000);
	        });
        }