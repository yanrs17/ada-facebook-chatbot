/*
  body should in string or buffer format, hash doesn't work.
 */
var request = require("request");

var form = {
	description:'数学专业'
};
var formData = JSON.stringify(form);
var contentLength = formData.length;

// request({
//     headers: {
//     	'Content-Length': contentLength,
//         'Content-Type': 'application/x-www-form-urlencoded'
//     },
//     url: 'http://airloft.org/ada/',
//     body: formData,
//     method: 'POST'
//     }, function (err, res, body) {
//     	console.log(body);
// });

request.post('http://airloft.org/ada/', {form:{description: '数学专业'}}, function(err, res, body){
	console.log(body);
});
