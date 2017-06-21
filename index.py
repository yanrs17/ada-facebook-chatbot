# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import pprint
app = Flask(__name__)
from where import getLocation
from opentime import getOpentime
from timetable import getCourseTimetable
from book import getBook 

# from chatbot.chatbotmanager import ChatbotManager 

import datetime
import requests
import json 
import os

# Libraries
LIST_OF_LIBRARIES = [
    "kf - Academic Success Centre, Koffler Centre",
    "koffler - Academic Success Centre, Koffler Centre",
    "astronomy - Astronomy \u0026amp; Astrophysics Library",
    "chem - Chemistry Library (A D Allen)",
    "allen - Chemistry Library (A D Allen)",
    "art - Department of Art Library",
    "engineering - Engineering \u0026amp; Computer Science Library",
    "aerospace - Engineering \u0026amp; Computer Science Library - Aerospace Resource Centre",
    "medicine - Family \u0026amp; Community Medicine Library",
    "newman - Industrial Relations and Human Resources Library (Newman)",
    "law - Law Library (Bora Laskin)",
    "map - Map and Data Library: Collection Access",
    "music - Music Library",
    "new - New College Library (Ivey)",
    "petro - Petro Jacyk Central \u0026amp; East European Resource Centre",
    "regis - Regis College Library",
    "hk - Richard Charles Lee Canada-Hong Kong Library",
    "smc - St. Michael's College - John M. Kelly Library",
    "kelly - St. Michael's College - John M. Kelly Library",
    "trinity -  Trinity College Library (John W Graham Library)",
    "emmanuel - Victoria University - Emmanuel College Library",
    "ba - Bahen Centre",
    "rom - Royal Ontario Museum Library \u0026amp; Archives",
    "oi - OISE Library",
    "gerstein - Gerstein Science Information Centre",
    "ej - E J Pratt Library",
    "rb - Robarts Library",
];

# All values in "DICT_OF_LIBRARIES" must also be in "LIST_OF_LIBRARIES" */
DICT_OF_LIBRARIES = {
    "kf": "Academic Success Centre, Koffler Centre",
    "koffler": "Academic Success Centre, Koffler Centre",
    "academic": "Academic Success Centre, Koffler Centre",
    "astronomy": "Astronomy \u0026amp; Astrophysics Library",
    "astrophysics": "Astronomy \u0026amp; Astrophysics Library",
    "chem": "Chemistry Library (A D Allen)",
    "chemistry": "Chemistry Library (A D Allen)",
    "allen": "Chemistry Library (A D Allen)",
    "art": "Department of Art Library",
    "engineering": "Engineering \u0026amp; Computer Science Library",
    "aerospace": "Engineering \u0026amp; Computer Science Library - Aerospace Resource Centre",
    "family": "Family \u0026amp; Community Medicine Library",
    "medicine": "Family \u0026amp; Community Medicine Library",
    "newman": "Industrial Relations and Human Resources Library (Newman)",
    "law": "Law Library (Bora Laskin)",
    "map": "Map and Data Library: Collection Access",
    "music": "Music Library",
    "new": "New College Library (Ivey)",
    "ivey": "New College Library (Ivey)",
    "petro": "Petro Jacyk Central \u0026amp; East European Resource Centre",
    "regis": "Regis College Library",
    "richard": "Richard Charles Lee Canada-Hong Kong Library",
    "hk": "Richard Charles Lee Canada-Hong Kong Library",
    "robarts": "Robarts Library",
    "rl": "Robarts Library",
    "rom": "Royal Ontario Museum Library \u0026amp; Archives",
    "rare": "Thomas Fisher Rare Book Library",
    "smc": "St. Michael's College - John M. Kelly Library",
    "trinity": "Trinity College Library (John W Graham Library)",
    "oi": "OISE Library",
    "kelly": "St. Michael's College - John M. Kelly Library",
    "rb": "Robarts Library",
    "gerstein": "Gerstein Science Information Centre",
    "ej": "Victoria University - E J Pratt Library",
    "emmanuel": "Victoria University - Emmanuel College Library"
};

def getSuggestedLibraries():
    return '\n'.join(LIST_OF_LIBRARIES[:5])

@app.route('/')
def getHomePage():
    # print "hi home"
    print("hi home")
    return "Welcome to the homepage!"

# @app.route('/webhook', methods=['GET'])
# def challenge():
#   if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == "ada_chatbot":
#     print("Validating webhook")
#     return request.args.get('hub.challenge'), 200
#   else:
#     print("Failed validation. Make sure the validation tokens match.")
#     return 403

@app.route('/webhook', methods=['POST'])
def receive_message():
    data = json.loads(request.data.encode('utf-8'))
    if (data['object'] == 'page'):
        for entry in data['entry']:
            pageID = entry['id']        
            timeOfEvent = entry['time']
            for event in entry['messaging']:
                if ('message' in event and event['message']):
                    receivedMessage(event)
                else:
                    # print "Webhook received unknown event"
                    print("Webhook received unknown event")
    return "OK", 200

def receivedMessage(event):
    senderID = int(event['sender']['id'])
    recipientID = int(event['recipient']['id'])
    timeOfMessage = int(event['timestamp'])
    message = event['message']

    # print "Received message for user %d and page %d at %d with message:" \
    #     % (senderID, recipientID, timeOfMessage)
    # print str(message)
     
    print("Received message for user %d and page %d at %d with message:" \
        % (senderID, recipientID, timeOfMessage))
    print(str(message))

    messageId = message.get('mid')
    messageText = message.get('text')
    messageAttachments = message.get('attachments')

    # if (messageText):
    #     if messageText == 'generic':
    #         sendTextMessage(senderID, messageText+" lol")
    #     else:
    #         sendTextMessage(senderID, messageText)
    # elif (messageAttachments):
    #     sendTextMessage(senderID, "Message with attachment received")

    if (messageText):
        # print "go into messageText"
        responseText = respondToQuery(messageText)
        # print "get responseText"
        sendTextMessage(senderID, responseText)
    elif (messageAttachments):
        sendTextMessage(senderID, "Message with attachment received")


########################################################################

def respondToQuery(messageText):
    ''' Generate response to a general query. If token is a non-chatting request, call helper functions
        to process the request, otherwise render to the chatbot to start chatting.

    Arguments:
        messageText: the query message

    Outputs:
        a response string 
    '''
    tokens = messageText.split(' ')
    first = tokens[0]
    # TODO SUPPORT MULTIPLE
    # rest = tokens[1:]

    if len(tokens) == 1: # If there is only one token
        return matchQuery(first)
        # if response != None:
        #     return response 
    else:  # If there is one token + argument 
        if first.upper() == 'WHERE' or first.upper() == "LOC" or first.upper() == "LOCATION":
            return getLocation(tokens[1])
        elif first.upper() == 'TIMETABLE':
            return getCourseTimetable(tokens[1:])
        elif first.upper() == 'LIB' or first.upper() == "LIBRARY":
            return getOpentime(tokens[1])
        elif first.upper() == 'BOOK' or first.upper() == 'BOOKS':
            return getBook(tokens[1:])     
        else:
            return "not yet" #ChatbotManager.callBot(messageText)  

def matchQuery(token):
    ''' Generate response for a query with one token.

    Arguments:
        token: the query token 

    Outputs:
        a query response for valid tokens or None   
    '''
    if (token.upper() == 'LIB' or token.upper() == 'LIBRARY'):
        return "Please enter the library you are looking for.(ie. lib rb)" + getSuggestedLibraries()
    elif token.upper() == 'TIMETABLE':
        return "What course do you want to find?"
    elif (token.upper() == 'WHERE' or token.upper() == "LOC" or token.upper() == "LOCATION"):
        return "Which building do you want to find?"
    elif (token.upper() == 'BOOK' or token.upper() == 'BOOKS'):
        return "Please enter the book you are looking for."
    else:
        return "not implemented"

############################################################################

def sendTextMessage(recipientId, messageText):
    # print "Send to user" + str(recipientId)
    print("Send to user" + str(recipientId))
    response_msg = json.dumps({"recipient":{"id":recipientId}, "message":{"text":messageText}})
    callSendAPI(response_msg)

def callSendAPI(messageData):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + os.environ['PAGE_ACCESS_TOKEN']
    
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=messageData)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(status.json())

# def output(query):
#     tokens = query.split(' ')
#     first = tokens[0]
#     # TODO SUPPORT MULTIPLE
#     # rest = tokens[1:]

#     if (len(tokens) == 1): # If there is only one token
#         if first == 'lib' or first == 'library':
#             return "Please enter the library you are looking for.(ie. lib rb)<br/>" + getSuggestedLibraries()
#         elif first == 'timetable':
#             return "What course do you want to find?<br/>"
#         else:
#             return 'Not implemented yet'

#     if len(tokens) >= 2 and (first.upper() == 'WHERE' or first.upper() == "LOC" or first.upper() == "LOCATION" or first == "找"):
#         return getLocation(tokens[1])
    
#     if len(tokens) >= 2 and (first.upper() == 'TIMETABLE'):
#         return getCourseTimetable(tokens[1:])
    
#     if len(tokens) >= 2 and (first.upper() == 'LIB' or first.upper() == "LIBRARY"):
#         return getOpentime(tokens[1])

# @app.route('/books/<book_name>')
# def search_book(book_name):
#     url = "https://cobalt.qas.im/api/1.0/textbooks?key=LrCC7Jj8knSAMPWPsDhf8l9h90QCMOsx"
#     response = requests.get(url).text
#     books = json.loads(response)
#     # print(b)
#     # print(type(b))
#     for item in books:
#        if item["title"] == book_name:
#         text = ""
#         for key in item:
#             if key != "courses":
#                 text += key+": "+str(item[key])+"<br/>" 
#         return text
#     return "cannot find book"

if __name__ == '__main__':
    # ChatbotManager()
    app.debug = True
    app.run()