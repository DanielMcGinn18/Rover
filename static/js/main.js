
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
	            document.getElementById("sensor1").innerHTML = x[1]
	            document.getElementById("sensor2").innerHTML = x[2]
	            setTimeout(requestData, 1000);
	        });
        }

/* Display Connection Status */

var connected = document.getElementById('connected').innerHTML;
  if (connected == 'True') {
  document.getElementById("dot").className = "dotGreen";
  document.getElementById("connectionStatus").className = "green";
  document.getElementById("connectionStatus").innerHTML = 'Connected';
  document.getElementById("return").style.display = "none";
} else {
  document.getElementById("dot").className = "dotRed";
  document.getElementById("connectionStatus").className = "red";
  document.getElementById("connectionStatus").innerHTML = 'Not Connected';
  document.getElementById("return").style.display = "initial";
}

/* Display Speed */

document.getElementById("Speed").addEventListener("change", submit);
function submit() {
	document.getElementById('speedFormText').value = 
	document.getElementById('Speed').value 
	document.getElementById('speedForm').submit();
} 
// var slide = document.getElementById('Speed'),
// slide.onchange = function() {
// 	document.getElementById('speedSlider').submit();
// }
document.getElementById("Speed").value =
document.getElementById("SpeedSetting").innerHTML;
document.getElementById("SpeedText").innerHTML = 
'Speed:'+document.getElementById("SpeedSetting").innerHTML+'/100';