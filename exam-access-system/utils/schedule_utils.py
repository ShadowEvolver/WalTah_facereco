import os
import json

SCHEDULE_PATH = "schedules/exam_schedule.json"
if not os.path.exists(SCHEDULE_PATH):
    os.makedirs(os.path.dirname(SCHEDULE_PATH), exist_ok=True)
    # initialize with empty list
    with open(SCHEDULE_PATH, 'w') as f:
        json.dump([], f)

def load_schedule():
    with open(SCHEDULE_PATH, 'r') as f:
        return json.load(f)


def get_exams_for_examiner(username):
    """Return list of exam entries for given examiner."""
    data = load_schedule()
    return [e for e in data if e.get('examiner') == username]


def get_schedule_entry(exams, hall, timeslot):
    for e in exams:
        if e.get('hall') == hall and e.get('timeslot') == timeslot:
            return e
    return None