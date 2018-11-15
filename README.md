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
  "subjects": [ // optionmal
    {
      "shortname": "CSCI", // required, unique
      "longname": "Computer Science", // required, unique
      "listings": [ // optional
        {
          "shortname": "1200", // required, unique-per-subject
          "sections": [ // optional
            {
              "subject_shortname": "", // new! optional?
              "course_shortname": "", // new! optional?
              "shortname": "01", // required, must be unique-per-listing
              "instructors": ["Turner", "Moorthy"], // optional
              "crn": "5550123", // required, registration number/id, unique-per-term
              "seats": 100, // optional, total seats in section
              "seats_taken": 25, // optional, seats taken in section (available = seats - seats_taken)
              "periods": [ // optional, but needed for scheduling
                {
                  "day": 1, // required, day of week (Sunday = 0, Saturday = 6)
                  "start": "1200", // required, start time (24hr)
                  "end": "1450", // required, end time (24hr)
                  "type": "lecture", // optional, but please be consistent in naming if used
                  "location": "DCC 328" // optional, but please abbreviate if used
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

