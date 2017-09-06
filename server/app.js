var express = require("express");
var bodyParser = require("body-parser");
var path = require('path');
var stylus = require('stylus');
var fs = require('fs');
var app = express();


//view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(stylus.middleware(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/ajax',function(req,res){
//  var cmd = req.cmd;
//  console.log("cmd = " + cmd);
  data = { "temp" : 25.4 };
//  res.send(data);
  
  var controlReq = JSON.stringify({ "cmd" :  "getTemperature" });
  console.log("JSON request: " + controlReq);
  
  var fd = fs.openSync("/tmp/gaerboxReqFifo", "w");
   
  if (fd) {
	  console.log("opened FIFO for writing");
	  var written = fs.writeSync(fd, controlReq);
	  if (written == controlReq.length) {
		  console.log("written");
	  } else {
		  console.log("error: during writing");
	  }
  } else {
	  console.log("error: opening FIFO for writing");
  }
  fs.closeSync(fd)

  data = fs.readFileSync("/tmp/gaerboxRespFifo")
  
  console.log("Read response from FIFO: " + data)

  res.send(data);
});

app.get('/', function(req, res, next) {
  res.render('index', { title: 'Gaerbox - Home' });
});

app.listen(3000,function(){
  console.log("Started on PORT 3000");
})



module.exports = app;
