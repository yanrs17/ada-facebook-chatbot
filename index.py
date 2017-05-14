# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)

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
    return '<br/>'.join(LIST_OF_LIBRARIES)

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
        if first == 'lib' or first == 'library':
            return "你要找哪些图书馆呢？<br/>" + getSuggestedLibraries()
        else:
            return 'Not implemented yet'
    second = tokens[1]
    if second == "ba":
        return "24/7/365, 程序员不用休息哒（¯﹃¯）";
    if second not in DICT_OF_LIBRARIES: #输入的内容无法在dict中找到，直接查找不转换
        return "抱歉哦,小助手找不到你输入的图书馆,你是不是要找以下的图书馆呢?>_<<br/>" + getSuggestedLibraries() + "请输入图书馆简称哦 (e.g.: library kf) _(:3 」∠)_ "
#             return;
    else: #输入的内容可以在DICT找得到，先转换成全称
        # TODO WEBSCRAPER
        return "The Open Time for {} is {} today.".format(DICT_OF_LIBRARIES[second], "10 am to 5 pm")

if __name__ == '__main__':
    app.debug = True
    app.run()