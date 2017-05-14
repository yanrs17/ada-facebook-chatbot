var express = require('express');
var bodyParser = require('body-parser');
var app = express()
var port = process.env.PORT || 3000;

app.use(bodyParser.urlencoded({ extended: true }));
app.listen(port, function() {
	console.log('Slack bot listening on port ' + port);
});

// error page
app.use(function (err, req, res, next) {
	console.error(err.stack);
	res.status(400).send(err.message);
});


// Hello world page

app.get('/', function(req, res) {
	s = 'Hello slackbot!';
	res.status(200).send(s);
	});


// Input: POST containing user_name, output "Hello username"
var hellobot = require('./hellobot');
app.post('/hello', hellobot);


// Chatbot
var chatbot = require('./chatbot');
app.post('/chatbot', chatbot);

/*curl --data "user_name='Zining'&user_id='666'&trigger_word='bot'&text='botCan you hear me?'" http://127.0.0.1:3000/chatbot
 *
 * */
