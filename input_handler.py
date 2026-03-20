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


def ask_resume():
    import os
    if os.path.exists("planner_data.json"):
        choice = input("Resume previous study plan? (y/n): ").lower()
        return choice == "y"
    return False
