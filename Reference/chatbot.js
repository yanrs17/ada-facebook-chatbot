var async = require('async');
var request = require('request');
var dbEntry = require('./dbEntry');

exports.chatbot = function(query, callback){
	var text = query.split(' ').slice(1).join(' ');
	dbEntry.count({}, function(err, count) {
		numEntries = count;
		qwords = text.split(" ");
		var qid = parseInt(qwords[0]);
		if (isNaN(qid)) { // Mode (a) : ask question
			ques = text; 
			/*
			  Question here is in Chinese, we want to convert it into english.
			 */
			request.post(
			    'http://localhost:3050/',
			    { form: { text: ques } },
			    function (error, response, body) {
			    	var result = JSON.parse(body);
			        console.log("translate to: ", result['text']); // if user input Chinese, then return corresponding English words, otherwise, return -1.
			        if(result['text'] == -1){
			        	/*
			        	  User input non-Chinese words.
			        	 */
			        	var ans = "输入中文哦， 亲~";
			        	callback(ans);
			        }
			        else{
						dbEntry.count({'question': result['text']}, function(err, cnt) {
						if (cnt == 0) { // mode (a, 2)
							entry = dbEntry({'qid': numEntries, 'question': result['text']});
							entry.save(function(err) {
								if (err) {
									console.log('(a, 2) adding entry failed!');
								} else {
									console.log('(a, 2) adding entry success!');
								}
							});
							var response = numEntries + ": " + ques;
							callback(response);
						} else { // mode (a, 1)
							// get the first answer of that question.
							dbEntry.findOne({'question': ques}, function(err, question) {
								var ans = question.answer[question.answer.length - 1];
								callback(ans)
							});
							}
						});
			        }
			    }
			);
		}
		else { // Mode (b) : input answer
			if (qid >= 0 && qid < numEntries) {// Mode (b, 1)
				var ques;
				var ans_arr;
				async.series([
					function(cb) {
						dbEntry.findOne({ 'qid': qid }).select("question").exec(function(err, question) {
							ques = question.question;
							console.log('ques: ' + ques);
							cb(null, 'question get!');
						});
					},
					function(cb) {
						dbEntry.findOne({ 'qid': qid }).select('-_id answer').exec(function(err, answer) {
							ans_arr = answer.answer;
							console.log('ans_arr: ' + ans_arr);
							cb(null, ' answer get!');
						});
					},
					function(cb) {
						text = qwords.slice(1).join(" ");
						// ans is the answer to that question without qid at the front.
						var ans = text;
						if (ans_arr.length == 0) {
							ans_arr = [ans];
						} else {
							ans_arr = [ans_arr[0], ans];
							// Limits the array length to <= 2.
						}
						console.log('new ans_arr: ' + JSON.stringify(ans_arr));
						dbEntry.findOneAndUpdate({'qid': qid},
							{'question': ques, 'answer': ans_arr},
							function(err, dbentry) {
								if (err) {
									console.log('(b, 1): error: ' + err);
									cb(null, ' (b, 1) updating error!');
								} else {
									cb(null, ' answer posted to db!');
								}
							});
						callback(qid + ': Q: ' + ques + '; A: ' + JSON.stringify(ans_arr));
					}
				], function(err, results) {
					console.log('mode (b) async results:' + results);
				});
			}
			else { // Mode(b, 2)
				console.log('(b, 2) qid ' + qid + ' not found');
				callback('qid ' + qid + ' not found');
			}
		}
	});
}

