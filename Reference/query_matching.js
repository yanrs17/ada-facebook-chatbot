
var utschedule = require("./components/utschedule");
// var bot = require("./components/chatbot");
var opentime = require("./components/opentime");

/*
  Main if-else function block. Forward different demands to corresponding component files under components/ directory.
 */

var SPECIAL_WORDS = {
   "苟利国家生死以": "岂因祸福避趋之",
   "岂": "岂因祸福避趋之",
   "苟利": "祸福",
   "苟": "苟利国家生死以",
   "狗": "汪",
   "ada娘": "诶"
}

var MENU = [
    "time - 查询lecture, tutorial的时间教师安排, (比如: time csc108)",
    "where - 各大建筑物的位置, (比如: where ba)",
    "book - 各课程课本信息, (比如: book mat244)",
    "lib - 各大图书馆的开放时间, (比如: lib gerstein)",
    "亲 - 匹配小助手历史文章, (比如: 亲 美食)"
];

exports.matching = function (query, callback) {

    var words = query.split(/\s+/);
    // TODO .toLowerCase()
    // var mo = "苟利国家生死以";
    var pattern = new RegExp(words);

    // FINAL EXAM SCHEDULE 期末考时间表
    if (words[0] == 'final' || words[0] == 'exam') {
        utschedule.exam(query, callback);
    }

    // TIMETABLE 时间表
    else if (words[0] == 'time' || words[0] == 'timetable' || words[0] == 'calendar' ||
     words[0] == 'cal' || words[0] == 'des' || words[0] == 'description') {
        utschedule.timetable(query, callback);
    }

    // else if (words[0] == 'calendar' || words[0] == 'cal' || words[0] == 'des' || words[0] == 'description') {
    //     utschedule.calendar(query, callback);
    // }

    // COURSES 课程介绍
    else if (words[0].match('[a-zA-Z][a-zA-Z][a-zA-Z][0-9][0-9][0-9]')) {
        callback('"final ' + words[0] + '" for final exam\n' + '"time ' + words[0] + '" for course time\n' + '"des ' + words[0] + '" for course description\n');
    }

    // LOCATION 教室地点
    else if (words[0] == 'where' || words[0] == 'loc' || words[0] == 'location' || words[0] == '找'){
        utschedule.location(query, callback);
    }

    // Library 图书馆
    else if (words[0] == 'lib' || words[0] == 'library' || words[0] == '图书馆' || words[0] == '圖書館') {
        opentime.library(query, callback);
    }


    // TEXTBOOK 教材
    else if (words[0] == 'book' || words[0] == 'textbook' || words[0] == '課本' || words[0] == '教科書' || words[0] == '書' || words[0] == '课本' || words[0] == '教科书' || words[0] == '书') {
        utschedule.textbook(query, callback);
    }

    // FOOD 食物
    else if (words[0] == 'food') {
        utschedule.food(query, callback);
    }

    // CLASS 课程具体的时间地点
    else if (words[0] == 'class') {
        utschedule.class(query, callback);
    }

    // else if (pattern.test(mo)) {
    //     match_article.too_young(query, callback);
    // }

    // HAVE NOT BEEN IMPLEMENTED 功能尚未实现
    else {
        // TODO 保存用户输入的内容,以便以后添加
        //callback('尚未實現該功能。');
        // 用户可能只是单纯输入一些文字反馈，不需要任何功能，加这行导致用户输入任何都会输出尚未实现该功能
    }

};
