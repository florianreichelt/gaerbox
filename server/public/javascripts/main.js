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
        type: 'POST',
        data: JSON.stringify(value),
        dataType: 'json',
        contentType: 'application/json',
        url: '/ajax',
        success: function(response) {
            console.log('success1');
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
		
		console.log("input value: " + value);
		
		$("#labelSetTemperatureResponse").text("");
		
		if (value > 0 && !isNaN(value)) {
			var data = { 
					'cmd' : 'setTemperature', 
					'value' : value
				}; 
			    $.ajax({
			        type: 'POST',
			        data: JSON.stringify(data),
			        dataType: 'json',
			        contentType: 'application/json',
			        url: '/ajax',
			        success: function(response) {
			            console.log('success2');
			            try {
			            	console.log("AJAX received response: " + response.response);
			            	
			            	$("#labelSetTemperatureResponse").text(response.response)            	
			            } catch (e) {
			            	console.log("error: can't parse AJAX JSON response. Reponse was: " + text);
			            }
			        },
			        error: ajaxError
			    });	
		} else {
			console.log("  error: NaN value typed");
		}
	} catch (e) {
		console.log("error: catched exception in ajaxSetTemp()");
	}	
}


$(document).ready(function() {
	ajaxGetTemp();
	console.log("Registering interval 10s");
	timer = setInterval(function() {
//		console.log("triggered");
		ajaxGetTemp();
	}, 5000);
	
	$("#btnSetTemp").on("click", function(e) {		
		console.log("Button clicked");
		ajaxSetTemp();
	});

});
