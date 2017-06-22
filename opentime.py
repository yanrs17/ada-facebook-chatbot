# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
#import urllib.request
import urllib

DICT_OF_LIBRARIES = {
    #"kf": "Career Resource Library, Koffler Centre",
    #"koffler": "Career Resource Library, Koffler Centre",
    "astronomy": "Astronomy & Astrophysics Library",
    "astrophysics": "Astronomy & Astrophysics Library",
    "chem": "Chemistry Library (A D Allen)",
    "chemistry": "Chemistry Library (A D Allen)",
    "allen": "Chemistry Library (A D Allen)",
    "art": "Department of Art Library",
    "engineering": "Engineering & Computer Science Library",
    "aerospace": "Engineering & Computer Science Library - Aerospace Resource Centre",
    "family": "Family & Community Medicine Library",
    "medicine": "Family & Community Medicine Library",
    "newman": "Industrial Relations and Human Resources Library (Newman)",
    "law": "Law Library (Bora Laskin)",
    #"map": "Map and Data Library",
    "music": "Music Library",
    "new": "New College Library (Ivey)",
    "ivey": "New College Library (Ivey)",
    "petro": "Petro Jacyk Central & East European Resource Centre",
    "regis": "Regis College Library",
    "richard": "Richard Charles Lee Canada-Hong Kong Library",
    "hk": "Richard Charles Lee Canada-Hong Kong Library",
    "robarts": "Robarts Library",
    "rl": "Robarts Library",
    "rom": "Royal Ontario Museum Library & Archives",
    "rare": "Thomas Fisher Rare Book Library",
    "smc": "St. Michael’s College - John M. Kelly Library",
    "trinity": "Trinity College Library (John W Graham Library)",
    "oi": "OISE Library",
    "kelly": "St. Michael’s College - John M. Kelly Library",
    "rb": "Robarts Library",
    "gerstein": "Gerstein Science Information Centre",
    "ej": "Victoria University - E J Pratt Library",
    "emmanuel": "Victoria University - Emmanuel College Library"
};

LIST_OF_LIBRARIES = [
    #"kf - Career Resource Library, Koffler Centre",
    #"koffler - Career Resource Library, Koffler Centre",
    "astronomy - Astronomy \u0026amp; Astrophysics Library",
    "chem - Chemistry Library (A D Allen)",
    "allen - Chemistry Library (A D Allen)",
    "art - Department of Art Library",
    "engineering - Engineering \u0026amp; Computer Science Library",
    "aerospace - Engineering \u0026amp; Computer Science Library - Aerospace Resource Centre",
    "medicine - Family \u0026amp; Community Medicine Library",
    "newman - Industrial Relations and Human Resources Library (Newman)",
    "law - Law Library (Bora Laskin)",
    #"map - Map and Data Library",
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

def getOpentime(second):
    if second == "ba":
        #return "24/7/365, 程序员不用休息哒（¯﹃¯）<br/>"
        return "Everyday!!! Computer scientist do not need a break~<br/>"
        #return 'pass'

    # If the library entered is not in the DICT, then ask the user to enter library again
    if second not in DICT_OF_LIBRARIES:
        #return "抱歉哦,小助手找不到你输入的图书馆,你是不是要找以下的图书馆呢?>_<<br/>" + getSuggestedLibraries() + "请输入图书馆简称哦 (e.g.: library kf) _(:3 」∠)_ "
        return "Sorry, the library you entered is not valid.<br/> Please re-enter the  library you are looking for using the abbreviation. (i.e. lib rb)<br/>" + getSuggestedLibraries()
    # If the library is in the DICT, then parser the web for information
    else:
        lib_dic = getInfo()
        name = DICT_OF_LIBRARIES[second].decode('utf-8').encode('ascii', 'ignore')
        if name not in lib_dic.keys():
            return name + " Opps! some error occurs"
        hour = lib_dic[name][0]
        website = lib_dic[name][1]

        if hour == 0:
            #return 'pass'
            return " Open Time for {}: <br/>Please contact library for hours.<br/>Library Information:<br/><a href =\"{}\">{}</a>".format(name, website, website)
        else:
            #return 'pass'
            return " Open Time for {}: <br/>{}<br/>Library Information:<br/><a href =\"{}\">{}</a>".format(name, hour, website, website)

#==========helper function==========
def getInfo():
    url = 'https://onesearch.library.utoronto.ca/visit'
    # r = urllib.request.urlopen(url).read()
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')
    
    count = 0
    lib_dic = {}
    all_libs = soup.select('div.block-content div.views-row')

    for lib in all_libs:
        name = lib.select('span h2 a')[0].get_text().encode('ascii', 'ignore')
        hour_container = lib.select('div.featured-library-home h3 a')
        if len(hour_container) < 1:
            hour = 0
        else:
            hour = hour_container[0]['href'].encode('ascii', 'ignore')
        website = url + lib.select('span h2 a')[0]['href'].encode('ascii', 'ignore')
        lib_dic[name] = [hour, website]

    return lib_dic

def getSuggestedLibraries():
    count = 0
    for item in LIST_OF_LIBRARIES:
        count += 1
    #print count
    return '<br/>'.join(LIST_OF_LIBRARIES)

if __name__ == '__main__':
    for key in DICT_OF_LIBRARIES:
        print getOpentime(key)
    #getOpentime('rb')