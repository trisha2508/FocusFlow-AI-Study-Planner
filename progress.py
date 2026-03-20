def update_progress(subjects, day_plan):
    actual_study = {}

    print("\n📌 Progress Update")

    for subject_name, planned_hours in day_plan:
        studied = float(input(
            f"How many hours did you actually study for {subject_name}? (planned {planned_hours:.1f}): "
        ))

        actual_study[subject_name] = studied

        missed = planned_hours - studied
        if missed > 0:
            for s in subjects:
                if s["name"] == subject_name:
                    s["hours"] += missed

    return actual_study
