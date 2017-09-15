timer = null;

function ajaxError(xhr, status, error) {
	console.log('ajax error')
	console.log(status)
	console.log(error)
}

function ajaxGetTemp() {
	console.log('hello from blubb()')
    value = { 'cmd' : 'getTemperature' }; 
    $.ajax({
        type: 'GET',
        data: value,
        dataType: 'json',
        contentType: 'application/json; charset=utf8',
        url: '/ajaxGet',
        success: function(response) {
            console.log('received: ' + JSON.stringify(response));

            try {
            	var temp = response.value.temp;
            	console.log("AJAX received temperature: " + temp.toString());
            
            	$("#idCurrentTemp").text(temp)            	
            } catch (e) {
            	console.log("error: can't parse AJAX JSON response. Reponse was: " + response);
            }
            
        },
        error: ajaxError
    });
}

function ajaxSetTemp() {
	console.log('hello from blubb2()')
		
	try {
		var value = parseInt($("#inputSetTemperature").val());
		$("#inputSetTemperature").val("");
		
		console.log("input value: " + value);
		
		if (value > 0 && !isNaN(value)) {
			$("#btnSetTemperature").prop("disabled", true);
			
			$("#alertSetTemperature").text("Submitting ...");
			$("#alertSetTemperature").show();
			
			var data = { 
					'cmd' : 'setTemperature', 
					'value' : value
				}; 
			    $.ajax({
			        type: 'POST',
			        data: JSON.stringify(data),
			        dataType: 'json',
			        contentType: 'application/json',
			        url: '/ajaxPost',
			        success: function(response) {
			        	$("#btnSetTemperature").prop("disabled", false);
			        	
			            try {
			            	console.log("AJAX received response: " + response.response);
			            	
			            	if (response.response === "ack") {
			            		$("#alertSetTemperature").text("Gaerbox temperature successfully updated");
			            		$("#alertSetTemperature").show();
			            	}           	
			            } catch (e) {
			            	console.log("error: can't parse AJAX JSON response. Reponse was: " + text);
			            }
			        },
			        error: function(xhr, status, error) {
			        	$("#btnSetTemperature").prop("disabled", false);
			        	
			        	ajaxError(xhr, status, error);
			        }
			    });	
		} else {
			console.log("  error: NaN value typed");
			$("#alertSetTemperature").text("Input error");
			$("#alertSetTemperature").show();
		}
	} catch (e) {
		console.log("error: catched exception in ajaxSetTemp()");
		
		$("#alertSetTemperature").text("Internal error");
		$("#alertSetTemperature").show();
	}	
}


$(document).ready(function() {
	ajaxGetTemp();
//	console.log("Registering interval 5s");
	timer = setInterval(function() {
		ajaxGetTemp();
	}, 5000);
	
	$("#btnSetTemperature").on("click", function(e) {		
//		console.log("Button clicked");
		ajaxSetTemp();
	});
});
