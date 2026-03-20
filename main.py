from input_handler import get_subjects, ask_resume
from scheduler import generate_day_plan, is_plan_possible
from progress import update_progress
from study_modes import get_study_mode, display_with_breaks
from persistence import save_state, load_state
from analytics import initialize_analytics, update_analytics, display_analytics


def main():
    if ask_resume():
        subjects, start_day, analytics = load_state()
        daily_hours = float(input("Enter daily free study hours: "))
    else:
        subjects = get_subjects()
        daily_hours = float(input("\nEnter daily free study hours: "))
        analytics = initialize_analytics()
        start_day = 1

    mode, study_mins, break_mins = get_study_mode()

    if not is_plan_possible(subjects, daily_hours):
        print("\n❌ This plan is not feasible.")
        return

    total_days = max(s["deadline"] for s in subjects)

    for day in range(start_day, total_days + 1):
        print(f"\n========== DAY {day} ==========")

        day_plan = generate_day_plan(subjects, daily_hours, day)

        if not day_plan:
            print("🛌 Rest / Buffer Day")
        else:
            display_with_breaks(day_plan, mode, study_mins, break_mins)
            actual = update_progress(subjects, day_plan)
            update_analytics(analytics, day_plan, actual)
            display_analytics(analytics)

        save_state(subjects, day + 1, analytics)

    show = input("\n📈 Do you want to see your study analytics graphs? (y/n): ").lower()
    if show == "y":
        from analytics import plot_planned_vs_studied, plot_missed_hours
        plot_planned_vs_studied(analytics)
        plot_missed_hours(analytics)

if __name__ == "__main__":
    main()
