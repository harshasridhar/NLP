module.exports = function(io) {
	var express = require('express');
	var router = express.Router();
	var cp = require("child_process");

	/* GET home page. */
	router.get('/', function(req, res, next) {
	  res.render('index', { title: 'Express' });
	});

	io.on("connection", function(socket){
		console.log("connected");
		socket.on("correct_request", function(data){
			console.log(data);
			var q = 'python main.py "'+data+'"';
			console.log(q);
			cp.exec(q, function(err, stdout, stderr){
				// console.log(stdout);
				if(!stdout){
					stdout = "I'm still in Beta, calm down!";
				}
				socket.emit("correct_response", stdout);
				console.log("socket emitted");
			});
		});
	});

	return router;
};

