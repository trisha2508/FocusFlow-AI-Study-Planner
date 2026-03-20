import json
import os 
def get_subjects():
    subjects = []
    n = int(input("Enter number of subjects: "))

    for i in range(n):
        print(f"\nSubject {i+1}")
        name = input("Name: ")
        hours = float(input("Total hours required: "))
        deadline = int(input("Deadline (days from today): "))

        subjects.append({
            "name": name,
            "hours": hours,
            "deadline": deadline
        })

    return subjects

def sort_by_deadline(subjects):
    return sorted(subjects, key=lambda x: x["deadline"])

def is_plan_possible(subjects, daily_hours):
    total_required = sum(s["hours"] for s in subjects)

    max_days = max(s["deadline"] for s in subjects)
    total_available = max_days * daily_hours

    return total_required <= total_available

def generate_day_plan(subjects, daily_hours, current_day):
    subjects = sort_by_deadline(subjects)

    day_plan = []
    remaining_daily_hours = daily_hours

    for subject in subjects:
        if subject["hours"] <= 0:
            continue

        if current_day > subject["deadline"]:
            continue

        remaining_days = subject["deadline"] - current_day + 1
        if remaining_days <= 0:
            continue

        # 🔥 CORE INTELLIGENCE
        required_today = subject["hours"] / remaining_days
        if required_today > daily_hours:
            print(
                f"\n⚠️ WARNING: {subject['name']} requires "
                f"{required_today:.2f} hrs/day, but only "
                f"{daily_hours} hrs/day available."
            )

        study_time = min(required_today, remaining_daily_hours)

        if study_time <= 0:
            continue

        subject["hours"] -= study_time
        remaining_daily_hours -= study_time

        day_plan.append((subject["name"], study_time))

        if remaining_daily_hours <= 0:
            break

    return day_plan




def print_schedule(schedule):
    print("\n📅 Generated Study Schedule:\n")
    for day, plans in schedule.items():
        print(day + ":")
        if not plans:
            print("  Rest / Buffer Day")
        for subject, hours in plans:
            print(f"  {subject} – {hours:.1f} hrs")
        print()

def update_progress(subjects, day_plan):
    print("\n📌 Progress Update")

    for subject_name, planned_hours in day_plan:
        studied = float(input(
            f"How many hours did you actually study for {subject_name}? (planned {planned_hours}): "
        ))

        missed = planned_hours - studied

        if missed > 0:
            for s in subjects:
                if s["name"] == subject_name:
                    s["hours"] += missed


def remaining_days(subject, current_day):
    return subject["deadline"] - current_day

def save_state(subjects, current_day):
    data = {
        "current_day": current_day,
        "subjects": subjects
    }

    with open("planner_data.json", "w") as f:
        json.dump(data, f, indent=4)

def load_state():
    if not os.path.exists("planner_data.json"):
        return None, None

    with open("planner_data.json", "r") as f:
        data = json.load(f)

    return data["subjects"], data["current_day"]

def ask_resume():
    if os.path.exists("planner_data.json"):
        choice = input("Resume previous study plan? (y/n): ").lower()
        return choice == "y"
    return False

def get_study_mode():
    print("\nChoose study technique:")
    print("1. Pomodoro (25 min study + 5 min break)")
    print("2. Deep Work (50 min study + 10 min break)")
    print("3. No structured breaks")

    choice = input("Enter choice (1/2/3): ")

    if choice == "1":
        return ("pomodoro", 25, 5)
    elif choice == "2":
        return ("deep", 50, 10)
    else:
        return ("none", None, None)

def convert_to_sessions(hours, study_minutes):
    total_minutes = hours * 60
    return int(total_minutes // study_minutes)

def display_with_breaks(day_plan, mode, study_mins, break_mins):
    print("\n🧠 Detailed Study Plan:")

    for subject, hours in day_plan:
        print(f"\n📘 {subject}")

        if mode == "none":
            print(f"  Study for {hours:.1f} hours")
            continue

        sessions = convert_to_sessions(hours, study_mins)

        for i in range(1, sessions + 1):
            print(f"  Session {i}: Study {study_mins} min")
            print(f"  Break: {break_mins} min")

        leftover = (hours * 60) - (sessions * study_mins)
        if leftover > 0:
            print(f"  Final focus: {int(leftover)} min")

def main():
    # ===== Load or create plan =====
    if ask_resume():
        subjects, start_day = load_state()
        daily_hours = float(input("Enter daily free study hours: "))
        mode, study_mins, break_mins = get_study_mode()
    else:
        subjects = get_subjects()
        daily_hours = float(input("\nEnter daily free study hours: "))
        mode, study_mins, break_mins = get_study_mode()
        start_day = 1

    total_days = max(s["deadline"] for s in subjects)

    # ===== Daily loop =====
    for day in range(start_day, total_days + 1):
        print(f"\n========== DAY {day} ==========")

        day_plan = generate_day_plan(subjects, daily_hours, day)

        if not day_plan:
            print("🛌 Rest / Buffer Day")
        else:
            display_with_breaks(day_plan, mode, study_mins, break_mins)
            update_progress(subjects, day_plan)

        # Save progress after each day
        save_state(subjects, day + 1)



if __name__ == "__main__":
    main()
