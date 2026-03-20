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


def display_with_breaks(day_plan, mode, study_mins, break_mins):
    print("\n🧠 Detailed Study Plan:")

    for subject, hours in day_plan:
        print(f"\n📘 {subject}")

        if mode == "none":
            print(f"  Study for {hours:.1f} hours")
            continue

        total_minutes = int(hours * 60)
        sessions = total_minutes // study_mins

        for i in range(1, sessions + 1):
            print(f"  Session {i}: Study {study_mins} min")
            print(f"  Break: {break_mins} min")

        leftover = total_minutes - (sessions * study_mins)
        if leftover > 0:
            print(f"  Final focus: {leftover} min")
