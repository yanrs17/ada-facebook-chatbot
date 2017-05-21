# -*- coding: utf-8 -*-
import requests
import json

def search_book(param_list):
    url = "https://cobalt.qas.im/api/1.0/textbooks?key=LrCC7Jj8knSAMPWPsDhf8l9h90QCMOsx"
    response = requests.get(url).text
    books = json.loads(response)
    book_name = param_list[0] if len(param_list) == 1 else " ".join(param_list)
    sentinel = False 

    for item in books:
       for course in item["courses"]:
           if book_name in course["code"]:
               sentinel = True 

       if item["title"] == book_name or sentinel:
            text = ""
            for key in item:
                if key != "courses":
                    text += key+": "+str(item[key])+"<br/>" 
            return text
    return "cannot find book"