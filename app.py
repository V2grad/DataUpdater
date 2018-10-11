from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

#Data Dictionary is used to store data.
Data = dict()

# Prepare Fall Semester Data
File = open("fall.html", "r")
Content = File.read()
soup = BeautifulSoup(Content, 'lxml')
Result=list(soup.find_all("td"))

for i in range(len(Result)):
    xspan = Result[i].span
    strx=str(xspan)
    if strx.find("left: 0.0pt")!=-1:
        # Locate all data and get them
        CourseTitleLine = str(xspan.text)
        CourseTitle=( CourseTitleLine.split(" ")[1].split("-")[0]  + "-" +CourseTitleLine.split(" ")[1].split("-")[1])
        CourseName = str(Result[i+1].span.text)
        CreditHours = str(Result[i + 3].span.text)
        
        # Save to Data Dictionary in format :{"Course Name": XXX, "Credit Hours:" :xxx}
        Data[CourseTitle]=dict()
        Data[CourseTitle]["CourseName"]=CourseName
        Data[CourseTitle]["CreditHours"] = CreditHours
        
File.close()

# Prepare Spring Semester
File = open("spring.html", "r")
Content = File.read()
soup = BeautifulSoup(Content, 'lxml')

Result=list(soup.find_all("td"))
for i in range(len(Result)):
    xspan = Result[i].span
    strx=str(xspan)
    # Locate all data and get them
    if strx.find("left: 0.0pt")!=-1:

        CourseTitleLine = str(xspan.text)
        CourseTitle=( CourseTitleLine.split(" ")[1].split("-")[0]  + "-" +CourseTitleLine.split(" ")[1].split("-")[1])
        CourseName = str(Result[i+1].span.text)
        CreditHours = str(Result[i + 3].span.text)
        
        # Save to Data Dictionary in format :{"Course Name": XXX, "Credit Hours:" :xxx}
        Data[CourseTitle]=dict()
        Data[CourseTitle]["CourseName"]=CourseName
        Data[CourseTitle]["CreditHours"] = CreditHours
        
File.close()

# Change the data format to : 
#    [
#        {"Course Name": XXX, "Credit Hours:" :xxx},
#        {"Course Name": XXX, "Credit Hours:" :xxx},
#        .....
#    ]
#
# Create the list
Data_list = list()

# Transfer data
for x in Data:
    tmpDict = dict()
    tmpDict["CourseTitle"] = x
    tmpDict["CourseName"] = Data[x]["CourseName"]
    tmpDict["CreditHours"] = Data[x]["CreditHours"]
    Data_list.append(tmpDict)

# Dump to a json file
DumpString=json.dumps(Data_list, sort_keys=True, indent=2)
writefile = open("data.json","w")
writefile.write(DumpString)
writefile.close()
File.close()


