import json
import os
from analytics import initialize_analytics


def save_state(subjects, current_day, analytics):
    data = {
        "current_day": current_day,
        "subjects": subjects,
        "analytics": analytics
    }
    with open("planner_data.json", "w") as f:
        json.dump(data, f, indent=4)


def load_state():
    if not os.path.exists("planner_data.json"):
        return None, None, None

    with open("planner_data.json", "r") as f:
        data = json.load(f)

    analytics = data.get("analytics", initialize_analytics())
    return data["subjects"], data["current_day"], analytics
