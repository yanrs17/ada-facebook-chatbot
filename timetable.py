import requests
import json
import time

def getCourseTimetable(course_list):
    time_select = 0
    if course_list[0] == "summer":
        time_select = 5
    elif course_list[0] == "fall" or course_list[0] == "winter":
        time_select = 9
    response = ""
    for course in course_list:
        response += get_timetable(course, time_select)
    return response

def get_timetable(course, time_select):
    result_s = ""
    current_time = time.strftime("%d/%m/%Y")
    time_token = current_time.split("/")
    current_month = int(time_token[1])
    if time_select != 0:
        time_s = time_token[2] + str(time_select)
    else:
        if current_month >= 5 and current_month < 9:
            time_s = time_token[2] + '5'
        else:
            time_s = time_token[2] + '9'
    url = 'https://timetable.iit.artsci.utoronto.ca/api/'+ time_s + '/courses?org=' \
          '&code=' + course \
          + '&section=&studyyear=&daytime=&weekday=&prof=&breadth=&online=&waitlist=&available=&title='
    r = requests.get(url)
    result = json.loads(r.text)
    for course in result:
        result_s += course + '<br/ >'
        for meeting in result[course]['meetings']:
            result_s += meeting + '<br />'
            result_s += schedule_parser(result[course]['meetings'][meeting]['schedule']) + '<br />'
        result_s += '<br />'
    return result_s

def schedule_parser(schedules):
    result = ""
    spot = 0
    for schedule in schedules:
        spot += 1
        schedule_json = schedules[schedule]
        if schedule_json['meetingDay']:
            meetingDay = {
                'MO': 'Monday',
                'TU': 'Tuesday',
                'WE': 'Wednesday',
                'TH': 'Thursday',
                'FR': 'Friday'
            }[schedule_json['meetingDay']]
        else:
            meetingDay = "-"
        meetingStartTime = schedule_json['meetingStartTime']
        if not meetingStartTime:
            meetingStartTime = "-"
        meetingEndTime = schedule_json['meetingEndTime']
        if not meetingEndTime:
            meetingEndTime = "-"
        room1 = schedule_json['assignedRoom1']
        if not room1:
            room1 = ""
        room2 = schedule_json['assignedRoom2']
        if not room2:
            room2 = ""
        if meetingDay == "-":
            result += "no schedule available"
        else:
            result += "spot" + str(spot) + ": <br />" + "    " + meetingDay + ": " + meetingStartTime + " - " \
                      + meetingEndTime + "<br />" + "Room1: " + room1 + "<br />Room2: " + room2 + "<br />"
    return result


