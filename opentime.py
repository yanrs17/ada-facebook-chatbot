# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
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

def getOpentime(second):
	if second == "ba":
            #return "24/7/365, 程序员不用休息哒（¯﹃¯）<br/>"
            return "Everyday!!! Computer scientist do not need a break~（¯﹃¯）<br/>"

        # If the library entered is not in the DICT, then ask the user to enter library again
        if second not in DICT_OF_LIBRARIES:
            #return "抱歉哦,小助手找不到你输入的图书馆,你是不是要找以下的图书馆呢?>_<<br/>" + getSuggestedLibraries() + "请输入图书馆简称哦 (e.g.: library kf) _(:3 」∠)_ "
            return "Sorry, the library you entered is not valid.<br/> Please re-enter the  library you are looking for using the abbreviation. (i.e. lib rb)<br/>" + getSuggestedLibraries()
        # If the library is in the DICT, then parser the web for information
        else:
            lib_dic = getInfo()
            name = DICT_OF_LIBRARIES[second].encode(encoding="utf-8", errors="strict")
            hour = lib_dic[name][0].encode(encoding="utf-8", errors="strict")
            url = lib_dic[name][1].encode(encoding="utf-8", errors="strict")

            if url == "Please contact library for hours.":
                return " Open Time for {}: <br/>{}.<br/>To look for open time for future, please check here:<br/>{}".format(name, hour, url)
            else:
                return " Open Time for {}: <br/>{}<br/>To look for open time for future, please check here:<br/><a href =\"{}\">{}</a>".format(name, hour, url, url)

#==========helper function==========
def getInfo():
    URL_BASE = 'http://resource.library.utoronto.ca/hours/'
    r = urllib.urlopen(URL_BASE).read()
    soup = BeautifulSoup(r, "html.parser")

    all_libs = soup.findAll("div", class_ = "library-row" )
    dic = {}

    for lib in all_libs:
        name = lib.find("div",  class_ = "library").find("h2").find("a").get_text().strip()
        hour = lib.find("div", class_ = "library-hours").get_text().strip()
        url_source = lib.find("div", class_ = "library-month").find("a")
        if url_source != None:
            url = URL_BASE + url_source.get('href')
        else:
            url = "Please contact library for hours."
        dic[name] = [hour, url]
    return dic

def getSuggestedLibraries():
    return '<br/>'.join(LIST_OF_LIBRARIES)
