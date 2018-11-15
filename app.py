# Import request module
import urllib
from bs4 import BeautifulSoup
import json
from flask import Flask
import time

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
        # Create a Dictionary to store the data for different days.
        D = dict()
        day = int(day.text)+1   # Remember to increase the day value by 1


        D["type"] = type
        D["instructor"] = instructor
        D["start"] = start
        D["end"] = end
        D["location"] = location
        D["day"] = day

        # Append to the result list
        result.append(D)

    return result


def parse_section(section):
    crn = section["crn"]
    shortname = section["num"]
    seats_taken = section["students"]
    seats = section["seats"]

    # Find all the sub-periods
    periods = section.find_all("period")

    # Create a list to store the periods after analyzing
    periods_list = list()

    # Store the professors that teach this course.
    instructors_set = set()

    for period in periods:
        # Fetch  and save all the period information.
        parse_peroid_result = parse_peroid(period)
        periods_list = periods_list + parse_peroid_result

        # Deal with the professor set.
        for single_period in parse_peroid_result:
            for instructor in single_period["instructor"]:
                if(instructor != "Staff"):
                    instructors_set.add(instructor)

    # Turn set to a list finnally.
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

    # Find all the sub sections
    sections = course.find_all("section")

    # create a list to store the parsed section information
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

def fetch_data(URL):

    # Try to fetch the data from the given URL,
    # If the URL doesn't exisit, return "Incorrect URL"
    try:
        data=urllib.request.urlopen(URL).read()
    except urllib.error.HTTPError as error:
        return "Incorrect URL"

    # Create a soup for the whole page.
    soup = BeautifulSoup(data, 'lxml')

    # Store all the sub-courses to courses.
    courses = soup.find_all("course")
    D = dict()
    subjects = list()

    # Deal with every course
    for course in courses:
        shortname = course["dept"]
        if shortname not in D:
            D[shortname] = list()
        D[shortname].append(parse_course(course))

    # Transform data type
    for shortname in D:
        subjects.append({"shortname": shortname, "listings": D[shortname]})

    result = {"subjects": subjects}

    return json.dumps(result)


@app.route('/<semester>')
def return_result(semester):

    # Check if the semester is made of digits
    if not semester.isdigit():
        return "Incorrect URL"

    URL = "https://sis.rpi.edu/reg/rocs/{}.xml".format(semester)

    return fetch_data(URL)

if __name__ == '__main__':
    app.run()





