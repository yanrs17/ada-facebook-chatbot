# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib

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