def sort_by_deadline(subjects):
    return sorted(subjects, key=lambda x: x["deadline"])


def is_plan_possible(subjects, daily_hours):
    total_required = sum(s["hours"] for s in subjects)
    max_days = max(s["deadline"] for s in subjects)
    return total_required <= max_days * daily_hours


def generate_day_plan(subjects, daily_hours, current_day):
    subjects = sort_by_deadline(subjects)
    remaining_daily_hours = daily_hours
    day_plan = []

    for subject in subjects:
        if subject["hours"] <= 0:
            continue
        if current_day > subject["deadline"]:
            continue

        remaining_days = subject["deadline"] - current_day + 1
        required_today = subject["hours"] / remaining_days
        study_time = min(required_today, remaining_daily_hours)

        if study_time <= 0:
            continue

        subject["hours"] -= study_time
        remaining_daily_hours -= study_time
        day_plan.append((subject["name"], study_time))

        if remaining_daily_hours <= 0:
            break

    return day_plan
