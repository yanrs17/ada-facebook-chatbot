# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import pprint
app = Flask(__name__)
from where import getLocation
from opentime import getOpentime
from timetable import getCourseTimetable
from book import getBook 
from library_data import getSuggestedLibraries
from library_data import *

from chatbot.chatbotmanager import ChatbotManager 

import datetime
import requests
import json 
import os

@app.route('/')
def getHomePage():
    print "hi home"
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
                    print "Webhook received unknown event"
    return "OK", 200

def receivedMessage(event):
    senderID = int(event['sender']['id'])
    recipientID = int(event['recipient']['id'])
    timeOfMessage = int(event['timestamp'])
    message = event['message']

    print "Received message for user %d and page %d at %d with message:" \
        % (senderID, recipientID, timeOfMessage)
    print str(message)

    messageId = message.get('mid')
    messageText = message.get('text')
    messageAttachments = message.get('attachments')

    # if (messageText):
    #     if messageText == 'generic':
    #         sendGenericMessage(senderID)
    #     else:
    #         sendTextMessage(senderID, messageText)
    # elif (messageAttachments):
    #     sendTextMessage(senderID, "Message with attachment received")

    if (messageText):
        print "go into messageText"
        responseText = respondToQuery(messageText)
        print "get responseText"
        sendTextMessage(senderID, responseText)
    elif (messageAttachments):
        sendTextMessage(senderID, "Message with attachment received")

def matchQuery(token):
    ''' Generate response for a query with one token.

    Arguments:
        token: the query token 

    Outputs:
        a query response for valid tokens or None   
    '''
    if (token.upper() == 'LIB' or token.upper() == 'LIBRARY'):
        return "Please enter the library you are looking for.(ie. lib rb)<br/>" + getSuggestedLibraries()
    elif token.upper() == 'TIMETABLE':
        return "What course do you want to find?<br/>"
    elif (token.upper() == 'WHERE' or first.upper() == "LOC" or token.upper() == "LOCATION" or first == "找"):
        return "Which building do you want to find?<br/>"
    elif (token.upper() == 'BOOK' or token.upper() == 'BOOKS'):
        return "Please enter the book you are looking for.<br/>"
    else:
        return None

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
        response = matchQuery(first)
        if response != None:
            return response 
    elif len(tokens) >= 2:  # If there is one token + argument 
        if first.upper() == 'WHERE' or first.upper() == "LOC" or first.upper() == "LOCATION" or first == "找":
            return getLocation(tokens[1])
        elif first.upper() == 'TIMETABLE':
            return getCourseTimetable(tokens[1:])
        elif first.upper() == 'LIB' or first.upper() == "LIBRARY":
            return getOpentime(tokens[1])
        elif first.upper() == 'BOOK' or first.upper() == 'BOOKS':
            return getBook(tokens[1:])     
    else:
        return ChatbotManager.callBot(messageText)  

def sendTextMessage(recipientId, messageText):
    print "Send to user" + str(recipientId)
    response_msg = json.dumps({"recipient":{"id":recipientId}, "message":{"text":"hahah"}})
    callSendAPI(response_msg)

def callSendAPI(messageData):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + os.environ['PAGE_ACCESS_TOKEN']
    
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=messageData)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(status.json())


if __name__ == '__main__':
    # initialize chatbot (only once per server session)
    print "initialize chatbot "
    ChatbotManager()
    print "after bot initialization"
    app.debug = True
    app.run()
