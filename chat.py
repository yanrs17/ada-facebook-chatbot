if __name__ == '__main__':
	import sys
	import requests
	import json
	data = {
		"object": "page",
		"entry": [{
			"id": 1,
			"time": 1,
			"messaging": [
				{
					"sender": {
						"id": 1
					},
					"recipient": {
						"id": 2
					},
					"timestamp": 123,
					"message": {
						"mid": 1,
						"text": sys.argv[1]
					}
				}
			]
		}]
	}
	requests.post("http://localhost:8000/webhook", data=json.dumps(data))
	