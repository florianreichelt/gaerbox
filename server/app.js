var express = require("express");
var bodyParser = require("body-parser");
var path = require('path');
var stylus = require('stylus');
var fs = require('fs');
var app = express();


//view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

//app.use(bodyParser.urlencoded({ extended: false }));
// required for JSON based POST requests
app.use(bodyParser.json());
//app.use(bodyParser.urlencoded({ extended : true }));

app.use(stylus.middleware(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public')));

app.use("/js", express.static(path.join(__dirname, "/node_modules/bootstrap/dist/js")));
app.use("/js", express.static(path.join(__dirname, "/node_modules/jquery/dist")));
app.use("/js", express.static(path.join(__dirname, "/node_modules/popper.js/dist")));
app.use("/css", express.static(path.join(__dirname, "/node_modules/bootstrap/dist/css")));


app.get('/ajax', function(req, res) {
	console.log("AJAX GET handler ...");
	
	var controlReq = JSON.stringify(req.query);
	console.log("  received data: " +  controlReq);

    var data = requestControlDaemon(controlReq, data);

	res.send(data);
});

app.post('/ajax', function(req, res) {
    console.log("AJAX POST handler ...");
	
	var controlReq = JSON.stringify(req.body);
	console.log("  received data: " +  controlReq);

    var data = requestControlDaemon(controlReq, data);

	res.send(data);
});

function requestControlDaemon(request, response) {
    var fd = fs.openSync("/tmp/gaerboxReqFifo", "w");
   
	if (fd) {
		console.log("opened FIFO for writing");
		var written = fs.writeSync(fd, request);
		if (written == request.length) {
			console.log("successfully written");
		} else {
			console.log("error: couldn't write data");
		}
	} else {
		console.log("error: could't open FIFO");
	}
	fs.closeSync(fd);

	var data = fs.readFileSync("/tmp/gaerboxRespFifo");
	console.log("got response from controlDaemon: " + data);
    return data;
}

app.get('/', function(req, res, next) {
	res.render('index', { title: 'Gaerbox Control' });
});

app.listen(3000,function(){
	console.log("Started on PORT 3000");
})



module.exports = app;
