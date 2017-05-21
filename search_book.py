# -*- coding: utf-8 -*-
import requests
import json

def search_book(book_name):
    url = "https://cobalt.qas.im/api/1.0/textbooks?key=LrCC7Jj8knSAMPWPsDhf8l9h90QCMOsx"
    response = requests.get(url).text
    books = json.loads(response)
    # print(b)
    # print(type(b))
    for item in books:
       if item["title"] == book_name:
        text = ""
        for key in item:
            if key != "courses":
                text += key+": "+str(item[key])+"<br/>" 
        return text
    return "cannot find book"