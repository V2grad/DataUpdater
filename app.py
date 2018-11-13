# Import request module
from urllib import request
from bs4 import BeautifulSoup
import json
from flask import Flask

app = Flask(__name__)


def parse_peroid(peroid):
    # Get all the detialed data from the given period
    type = peroid["type"]
    instructor = peroid["instructor"]
    start = peroid["start"]
    end = peroid["end"]
    location = peroid["location"]
    days = peroid.find_all("day")

    # Deal with instructors.
    instructor = instructor.split("/")

    result = list()

    for day in days:
        D = dict()
        day = int(day.text)+1

        D["type"] = type
        D["instructor"] = instructor
        D["start"] = start
        D["end"] = end
        D["location"] = location
        D["day"] = day

        result.append(D)

    return result


def parse_section(section):
    crn = section["crn"]
    shortname = section["num"]
    seats_taken = section["students"]
    seats = section["seats"]

    periods = section.find_all("period")

    periods_list = list()
    instructors_set = set()

    for period in periods:
        parse_peroid_result = parse_peroid(period)
        periods_list = periods_list + parse_peroid_result

        for single_period in parse_peroid_result:
            for instructor in single_period["instructor"]:
                if(instructor != "Staff"):
                    instructors_set.add(instructor)

    instructors_list = list(instructors_set)

    result = dict()
    result["crn"] = crn
    result["shortname"] = shortname
    result["seats_taken"] = seats_taken
    result["seats"] = seats
    result["instructors"] = instructors_list
    result["periods"] = periods_list

    return result




def parse_course(course):
    longname = course["name"]
    short_name = course["num"]
    min_credits = course["credmin"]
    max_credits = course["credmax"]

    sections = course.find_all("section")

    sections_list = list()

    for section in sections:
        sections_list.append(parse_section(section))

    result = dict()
    result["longname"] = longname
    result["shortname"] = short_name

    result["min_credits"] = min_credits
    result["max_credits"] = max_credits
    result["sections"] = sections_list

    return result


@app.route('/<semester>')
def return_result(semester):
    URL = "https://sis.rpi.edu/reg/rocs/{}.xml".format(semester)

    with request.urlopen(URL) as rawRequest:
        if(str(rawRequest.status) != "200"):
            return "Incorrect URL"
        data = rawRequest.read()

    soup = BeautifulSoup(data, 'lxml')
    courses = soup.find_all("course")
    D = dict()
    subjects = list()

    for course in courses:
        shortname = course["dept"]
        if shortname not in D:
            D[shortname] = list()
        D[shortname].append(parse_course(course))

    for shortname in D:
        subjects.append({"shortname": shortname, "listings": D[shortname]})

    result = {"subjects": subjects}

    return json.dumps(result)


if __name__ == '__main__':
    app.run()





