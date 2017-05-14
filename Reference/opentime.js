// Imports
var request = require("request");
var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
var querystring = require('querystring');
var cheerio = require('cheerio');

// var URL_OF_LIBRARY_API = "https://ajax.googleapis.com/ajax/services/feed/load?v=1.0\u0026amp;num=-1\u0026amp;q=http://www.feed43.com/2343747281410148.xml";
var URL_OF_LIBRARY_API = "http://52.44.150.99/users/1/web_requests/15/library.json";

// Libraries
var LIST_OF_LIBRARIES = [
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
    "smc - St. Michael’s College - John M. Kelly Library",
    "kelly - St. Michael’s College - John M. Kelly Library",
    "trinity -  Trinity College Library (John W Graham Library)",
    "emmanuel - Victoria University - Emmanuel College Library",
    "ba - Bahen Centre o(*////▽////*)q",
    "rom - Royal Ontario Museum Library \u0026amp; Archives",
    "oi - OISE Library",
    "gerstein - Gerstein Science Information Centre",
    "ej - E J Pratt Library",
    "rb - Robarts Library",
];

/* All values in "DICT_OF_LIBRARIES" must also be in "LIST_OF_LIBRARIES" */
var DICT_OF_LIBRARIES = {
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
    "smc": "St. Michael’s College - John M. Kelly Library",
    "trinity": "Trinity College Library (John W Graham Library)",
    "oi": "OISE Library",
    "kelly": "St. Michael’s College - John M. Kelly Library",
    "rb": "Robarts Library",
    "gerstein": "Gerstein Science Information Centre",
    "ej": "Victoria University - E J Pratt Library",
    "emmanuel": "Victoria University - Emmanuel College Library"
};

// Get all libraries -- can be simplified
function getSuggestedLibraries() {
    var suggested_libraries = '';
    for (var i = 0; i < LIST_OF_LIBRARIES.length; i++) {
        suggested_libraries += LIST_OF_LIBRARIES[i];
        suggested_libraries += '\n\n';
    }
    return suggested_libraries;
}

// Get output according to input
exports.library = function(query, callback) {
    var prefix = query.split(/\s+/)[0]; // "lib" in "lib rb"
    var libInput = query.split(/\s+/)[1]; // "rb" in "lib rb"
    var newInput = '';
    if (libInput == undefined) { // If only one token
        callback("你要找哪些图书馆呢？\n" + getSuggestedLibraries());
        return;
    }

    /* Some surprise */
    if(libInput == "ba"){
        callback("24/7/365, 程序员不用休息哒（¯﹃¯）");
        return;
    }

    if (DICT_OF_LIBRARIES[libInput] == undefined) { //输入的内容无法在dict中找到，直接查找不转换
            // console.log("DEBUG: NOT FOUND IN DICT");
            callback("抱歉哦,小助手找不到你输入的图书馆,你是不是要找以下的图书馆呢?>_<\n " + getSuggestedLibraries() + "请输入图书馆简称哦 (e.g.: library kf) _(:3 」∠)_ ");
            return;
    } else { //输入的内容可以在DICT找得到，先转换成全称
        newInput = DICT_OF_LIBRARIES[libInput];
        var URL_BASE = 'http://resource.library.utoronto.ca/hours/';
        var options = {
          url: URL_BASE,
          headers: {
            'User-Agent': 'request' // need a user agent to scrape page correctly.
          }
        };
        request(options, function (error, response, html) {
          if (!error && response.statusCode == 200) {
            // console.log(html);
            var $ = cheerio.load(html);
            var libLst = [];

            $('div.library-row').each(function(i, element){
                var name = $(this).children('div.library').children('h2').text().trim();
                var time = $(this).children('div.library-hours').text().trim() || "unavailable";
                var info = $(this).children('div.library').children('div.librarynotes').text().trim() || "";
                var url = URL_BASE + $(this).children('div.library-month').children('a').attr('href') || "";
                libLst.push({
                    "name": name,
                    "time": time,
                    "info": info,
                    "url": url
                });
            });

            /*
              Given libLst, match with newInput and return stats.
             */
            for (var i = 0; i < libLst.length; i++) {
                var lib_title = libLst[i]["name"];
                var lib_notes = libLst[i]["info"] ? "\n提示：" + libLst[i]["info"] : "";
                if (lib_title == newInput) {
                    callback("Open time for " + lib_title.split("&amp;").join("") + ":\n" +  libLst[i]["time"] + lib_notes + "\n查看未来几天的开放时间，看这里哦：\n" + libLst[i]["url"]);
                    return;
                }
            }
            callback("找不到该图书馆。");
            return;
          };
        });
    }
}
