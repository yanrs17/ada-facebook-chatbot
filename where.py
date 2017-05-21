from flask import Flask
from pymongo import *

def getLocation(second):
    db_url = "mongodb://utzhushou:ada23333@ds019836.mlab.com:19836/utzhushou"
    # TODO SUPPORT MULTIPLE
    # rest = tokens[1:]
    loc = second.upper()              # e.g. query = 'where BA', then loc = 'BA'
    client = MongoClient(db_url)
    db = client.utzhushou
    addresses = db['buildings']
    address = addresses.find_one({"code": loc})
    if address:
        long_url = 'http://maps.google.com?q=' + str(address['lat']) + ',' + str(address['lng'])
        client.close()
        return "Location of " + second + ": " + long_url
    else:
        return "Building not found"
