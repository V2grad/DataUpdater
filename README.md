# Data Updater

## Description

A Web API to fetch course data from RPI Course Database.

## Requirements

- Python 3
- Beautiful Soup 4
- Flask

## Usage

```bash
git clone https://github.com/V2grad/DataUpdater
cd DataUpdater
pip3 install -r requirements.txt
python3 app.py
```

Then visiting http://127.0.0.1:5000/<semester>

## Different Semesters

- **Fall 2018**: 201809 http://127.0.0.1:5000/201809
- **Spring 2019**: 201901 http://127.0.0.1:5000/201901
- **Fall 2019**: 201909 http://127.0.0.1:5000/201909

## Example

See [example.json](./example.json)

## Return Data Template

See [template.json](./template.json)

```json
{
  "subjects": [{
    "shortname": "CSCI",
    "longname": "Computer Science",
    "listings": [{
      "shortname": "1200",
      "sections": [{
        "subject_shortname": "",
        "course_shortname": "",
        "shortname": "01",
        "instructors": ["Turner", "Moorthy"],
        "crn": "5550123",
        "seats": 100,
        "seats_taken": 25,
        "periods": [{
          "day": 1,
          "start": "1200",
          "end": "1450",
          "type": "lecture",
          "location": "DCC 328"
        }]
      }]
    }]
  }]
}
```