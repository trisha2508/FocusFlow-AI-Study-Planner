def initialize_analytics():
    return {
        "total_planned": 0,
        "total_studied": 0,
        "total_missed": 0,
        "study_streak": 0,
        "days_completed": 0,
        "daily_planned": [],
        "daily_studied": [],
        "daily_missed": []
    }



def update_analytics(analytics, day_plan, actual_study):
    planned_today = sum(h for _, h in day_plan)
    studied_today = sum(actual_study.values())
    missed_today = max(0, planned_today - studied_today)

    analytics["total_planned"] += planned_today
    analytics["total_studied"] += studied_today
    analytics["total_missed"] += missed_today

    analytics["daily_planned"].append(planned_today)
    analytics["daily_studied"].append(studied_today)
    analytics["daily_missed"].append(missed_today)

    analytics["days_completed"] += 1

    if studied_today > 0:
        analytics["study_streak"] += 1
    else:
        analytics["study_streak"] = 0


def display_analytics(analytics):
    print("\n📊 STUDY ANALYTICS")
    print(f"✔ Total Planned Hours : {analytics['total_planned']:.1f}")
    print(f"✔ Total Studied Hours : {analytics['total_studied']:.1f}")
    print(f"✘ Total Missed Hours  : {analytics['total_missed']:.1f}")
    print(f"🔥 Current Streak     : {analytics['study_streak']} days")

import matplotlib.pyplot as plt


def plot_planned_vs_studied(analytics):
    days = range(1, len(analytics["daily_planned"]) + 1)

    plt.figure()
    plt.plot(days, analytics["daily_planned"], label="Planned Hours")
    plt.plot(days, analytics["daily_studied"], label="Studied Hours")
    plt.xlabel("Day")
    plt.ylabel("Hours")
    plt.title("Planned vs Studied Hours")
    plt.legend()
    plt.show()


def plot_missed_hours(analytics):
    days = range(1, len(analytics["daily_missed"]) + 1)

    plt.figure()
    plt.plot(days, analytics["daily_missed"])
    plt.xlabel("Day")
    plt.ylabel("Missed Hours")
    plt.title("Missed Study Hours Over Time")
    plt.show()
