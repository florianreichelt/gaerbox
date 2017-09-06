timer = null;

function blubb() {
	console.log('hello from blubb()')
    data = { 'cmd' : 'getTemperature' }; 
    $.ajax({
        type: 'GET',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json',
        url: '/ajax',
        success: function(response) {
            console.log('success');
            try {
            	//var result = JSON.parse(response);
            	var temp = response.value.temp;
            	console.log("AJAX received temperature: " + temp.toString());
            	
            	$("#idCurrentTemp").text(temp)            	
            } catch (e) {
            	console.log("error: can't parse AJAX JSON response. Reponse was: " + response);
            }
            
        },
        error: function(xhr, status, error) {
        	console.log('ajax error')
        	console.log(status)
        	console.log(error)
        }
    });
}


$(document).ready(function() {
	blubb();
	console.log("Registering timeout 10s");
	timer = setInterval(function() {
		console.log("triggered");
		blubb();
	}, 5000);
});


//timer = window.setTimeout(function(){
//	
//}, 5)


//$(document).ready(function() {
//	console.log('main.js hello')
//    data = {};
//    data.cmd = 'getTemperature'; 
//    $.ajax({
//        type: 'GET',
//        data: JSON.stringify(data),
//        dataType: 'json',
//        contentType: 'application/json',
//        url: '/ajax',
//        success: function(data) {
//            console.log('success');
//            console.log(JSON.stringify(data));
//        },
//        error: function(xhr, status, error) {
//        	console.log('ajax error')
//        	console.log(status)
//        	console.log(error)
//        }
//    });
//})
