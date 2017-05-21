# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
from where import getLocation
from opentime import getOpentime
from timetable import getCourseTimetable
from library_data import *

import datetime
import requests
import json

@app.route('/')
def getHomePage():
    return "Welcome to the homepage!"

@app.route('/<query>')
def output(query):
    tokens = query.split(' ')
    first = tokens[0]
    # TODO SUPPORT MULTIPLE
    # rest = tokens[1:]

    if (len(tokens) == 1): # If there is only one token
        if (first.upper() == 'LIB' or first.upper() == "LIBRARY"):
            return "Please enter the library you are looking for.(ie. lib rb)<br/>" + getSuggestedLibraries()
        elif first.upper() == 'TIMETABLE':
            return "What course do you want to find?<br/>"
        elif (first.upper() == 'WHERE' or first.upper() == "LOC" or first.upper() == "LOCATION" or first == "找"):
            return "Which building do you want to find?<br/>"
        else:
            return 'Not implemented yet'

    if len(tokens) >= 2 and (first.upper() == 'WHERE' or first.upper() == "LOC" or first.upper() == "LOCATION" or first == "找"):
        return getLocation(tokens[1])

    if len(tokens) >= 2 and (first.upper() == 'TIMETABLE'):
        return getCourseTimetable(tokens[1:])

    if len(tokens) >= 2 and (first.upper() == 'LIB' or first.upper() == "LIBRARY"):
        return getOpentime(tokens[1])

@app.route('/books/<book_name>')
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


if __name__ == '__main__':
    app.debug = True
    app.run()
