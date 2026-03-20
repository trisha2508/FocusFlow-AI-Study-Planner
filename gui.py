import tkinter as tk
from tkinter import ttk 
import json
import os


# ---------- COLORS ---------- 
BG_COLOR = "#f5f6fa"
SIDEBAR_COLOR = "#2f3640"
ACCENT_COLOR = "#40739e"
TEXT_COLOR = "#2d3436"
SAVE_FILE = "planner_state.json"



class StudyPlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Study Planner")
        self.root.geometry("1000x600")
        self.root.configure(bg=BG_COLOR)

        self.setup_styles()
        self.create_layout()
        self.show_setup_page()
        self.subjects = []
        self.daily_hours = 0
        self.study_mode_selected = "Pomodoro" 
        self.current_day = 1
        self.today_study_log = {} 
        self.show_setup_page()
        if self.load_state():
            self.show_plan_page()
        else:
            self.show_setup_page() 




    # ---------- STYLES ----------
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Card.TFrame", background="white", relief="raised")

    # ---------- LAYOUT ----------
    def create_layout(self):
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)

        # ---- SIDEBAR ----
        self.sidebar = tk.Frame(self.main_container, bg=SIDEBAR_COLOR, width=220)
        self.sidebar.pack(side="left", fill="y")

        title = tk.Label(
            self.sidebar,
            text="AI\nStudy\nPlanner",
            bg=SIDEBAR_COLOR,
            fg="white",
            font=("Segoe UI", 16, "bold"),
            justify="left"
        )
        title.pack(pady=30, padx=20, anchor="w")

        # Main navigation
        self.setup_btn = self.create_sidebar_button("Setup", self.show_setup_page)
        self.plan_btn = self.create_sidebar_button("Plan", self.show_plan_page)
        self.analytics_btn = self.create_sidebar_button("Analytics", self.show_analytics_page)

        # Divider
        tk.Label(
            self.sidebar,
            text="FOCUS TOOLS",
            bg=SIDEBAR_COLOR,
            fg="#b2bec3",
            font=("Segoe UI", 9, "bold")
        ).pack(pady=(25, 5), padx=15, anchor="w")

        self.pomodoro_btn = self.create_sidebar_button(
            "Pomodoro Timer",
            self.show_pomodoro_page
        )

        self.deep_focus_btn = self.create_sidebar_button(
            "Deep Focus Timer",
            self.show_deep_focus_page
        )

        # ---- CONTENT AREA ----
        self.content = ttk.Frame(self.main_container)
        self.content.pack(side="right", fill="both", expand=True, padx=30, pady=30)

    # ---------- SIDEBAR BUTTON ----------
    def create_sidebar_button(self, text, command):
        btn = tk.Button(
            self.sidebar,
            text=text,
            bg=SIDEBAR_COLOR,
            fg="white",
            font=("Segoe UI", 11),
            relief="flat",
            activebackground=ACCENT_COLOR,
            activeforeground="white",
            bd=0,
            padx=20,
            pady=12,
            command=command
        )

        btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_COLOR))
        btn.bind("<Leave>", lambda e: btn.config(bg=SIDEBAR_COLOR))

        btn.pack(fill="x", padx=15, pady=5)
        return btn

    # ---------- UTILS ----------
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ---------- SETUP PAGE ----------
    def show_setup_page(self):
        self.clear_content()

        card = ttk.Frame(self.content, style="Card.TFrame", padding=25)
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Setup Your Study Plan", style="Title.TLabel").pack(anchor="w")

        ttk.Label(
            card,
            text="Add subjects, deadlines, and choose how you want to study.",
            wraplength=750
        ).pack(anchor="w", pady=(5, 20))

        form = ttk.Frame(card)
        form.pack(fill="x", pady=10)

        ttk.Label(form, text="Subject Name").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="Total Hours").grid(row=0, column=1, sticky="w", padx=10)
        ttk.Label(form, text="Deadline (days)").grid(row=0, column=2, sticky="w")

        self.subject_name = ttk.Entry(form, width=20)
        self.subject_hours = ttk.Entry(form, width=10)
        self.subject_deadline = ttk.Entry(form, width=15)

        self.subject_name.grid(row=1, column=0, pady=5)
        self.subject_hours.grid(row=1, column=1, padx=10)
        self.subject_deadline.grid(row=1, column=2)

        ttk.Button(form, text="Add Subject", command=self.add_subject_ui)\
            .grid(row=1, column=3, padx=15)

        ttk.Label(card, text="Subjects Added", style="Header.TLabel")\
            .pack(anchor="w", pady=(20, 5))

        self.subject_list_box = tk.Listbox(card, height=5)
        self.subject_list_box.pack(fill="x", pady=5)

        settings = ttk.Frame(card)
        settings.pack(fill="x", pady=20)

        ttk.Label(settings, text="Daily Study Hours").grid(row=0, column=0, sticky="w")
        self.daily_hours_entry = ttk.Entry(settings, width=10)
        self.daily_hours_entry.grid(row=0, column=1, padx=10)

        ttk.Label(settings, text="Study Mode").grid(row=0, column=2, sticky="w", padx=(30, 5))
        self.study_mode = ttk.Combobox(
            settings,
            values=["Pomodoro", "Deep Study"],
            state="readonly",
            width=15
        )
        self.study_mode.current(0)
        self.study_mode.grid(row=0, column=3)

        ttk.Button(card, text="Start Planning", command=self.start_planning_ui)\
            .pack(anchor="e", pady=20)

    # ---------- UI ACTIONS ----------
    def add_subject_ui(self):
        name = self.subject_name.get()
        hours = self.subject_hours.get()
        deadline = self.subject_deadline.get()
    
        if not name or not hours or not deadline:
            return
    
        try:
            hours = float(hours)
            deadline = int(deadline)
        except ValueError:
            return
    
        subject_data = {
            "name": name,
            "remaining_hours": hours,
            "deadline": deadline
        }
    
        self.subjects.append(subject_data)
    
        self.subject_list_box.insert(
            "end", f"{name} — {hours} hrs, {deadline} days"
        )
    
        self.subject_name.delete(0, "end") 
        self.subject_hours.delete(0, "end")
        self.subject_deadline.delete(0, "end")


    def start_planning_ui(self):
        if not self.subjects:
            return
    
        try:
            self.daily_hours = float(self.daily_hours_entry.get())
        except ValueError:
            return
    
        self.study_mode_selected = self.study_mode.get()
    
        print("SETUP COMPLETE")
        print("Subjects:", self.subjects)
        print("Daily Hours:", self.daily_hours)
        print("Study Mode:", self.study_mode_selected)
        self.save_state()

    
        self.show_plan_page()
    def generate_today_plan(self):
        plan = []
        hours_left = self.daily_hours
    
        subjects_sorted = sorted(
            self.subjects,
            key=lambda s: s["deadline"]
        )
    
        for subject in subjects_sorted:
            if hours_left <= 0:
                break
    
            if subject["remaining_hours"] <= 0:
                continue
    
            allocated = min(subject["remaining_hours"], hours_left)
            plan.append((subject["name"], allocated))
            hours_left -= allocated
    
        return plan
    
    def end_day(self):
        for subject in self.subjects:
            subject["deadline"] -= 1
    
        # Remove completed + expired subjects
        self.subjects = [
            s for s in self.subjects
            if not (s["deadline"] <= 0 and s["remaining_hours"] <= 0)
        ]
    
        print("Day ended. Deadlines updated.")
        self.save_state()
        self.show_plan_page()


    # ---------- OTHER PAGES ----------
    def show_plan_page(self):
        self.clear_content()
    
        # Page Title
        ttk.Label(
            self.content,
            text="Today's Study Plan",
            style="Title.TLabel"
        ).pack(anchor="w", pady=(0, 20))
        ttk.Button(
        self.content,
        text="End Day →",
        command=self.end_day
    ).pack(anchor="e", pady=(0, 15))

    
        # Scrollable area
        canvas = tk.Canvas(self.content, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
    
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
    
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
    
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        # ---------- REAL DATA ----------
        today_plan = self.generate_today_plan()
    
        if not today_plan:
            ttk.Label(
                self.content,
                text="🎉 No study planned for today!",
                font=("Segoe UI", 14)
            ).pack(pady=50)
            return
    
        # ---------- SUBJECT CARDS ----------
        for subject, hours in today_plan:
            card = ttk.Frame(scroll_frame, style="Card.TFrame", padding=20)
            card.pack(fill="x", pady=10)
    
            ttk.Label(
                card,
                text=subject,
                font=("Segoe UI", 14, "bold")
            ).grid(row=0, column=0, sticky="w")
    
            ttk.Label(
                card,
                text=f"Planned: {hours:.1f} hrs",
                foreground="#636e72"
            ).grid(row=1, column=0, sticky="w", pady=(5, 10))
    
            progress_bar = ttk.Progressbar(
                card,
                orient="horizontal",
                length=280,
                mode="determinate",
                maximum=hours
            )
            progress_bar.grid(row=2, column=0, pady=(0, 10), sticky="w")
    
            slider = ttk.Scale(
                card,
                from_=0,
                to=hours,
                orient="horizontal",
                length=280
            )
            slider.grid(row=3, column=0, pady=(0, 10), sticky="w")
    
            # ✅ Correct slider → progress binding
            slider.config(
                command=lambda val, bar=progress_bar: bar.config(value=float(val))
            )
    
            ttk.Button(
                card,
                text="Save Progress",
                command=lambda s=subject, sl=slider: self.log_progress(
                    s, round(sl.get(), 2)
                )
            ).grid(row=0, column=1, rowspan=4, padx=20) 
            ttk.Button(
            self.content,
            text="End Day & Update Plan",
            style="Accent.TButton" if "Accent.TButton" in ttk.Style().theme_names() else None,
            command=self.end_day
        ).pack(anchor="e", pady=20)




    def log_progress(self, subject_name, studied_hours):
        # Store today's studied hours
        self.today_study_log[subject_name] = studied_hours
    
        print(f"[DAY {self.current_day}] {subject_name}: {studied_hours} hrs logged")
    
        
        print(f"[LOG] {subject_name}: studied {studied_hours} hrs")
        self.show_plan_page() 
        self.save_state()

        
    def end_day(self):
        today_plan = self.generate_today_plan()
    
        for subject_name, planned_hours in today_plan:
            studied = self.today_study_log.get(subject_name, 0)
    
            for subject in self.subjects:
                if subject["name"] == subject_name:
                    missed = planned_hours - studied
                    subject["remaining_hours"] -= studied
    
                    if subject["remaining_hours"] < 0:
                        subject["remaining_hours"] = 0
    
                    # Missed hours automatically carry forward
                    if missed > 0:
                        print(f"[MISSED] {subject_name}: {missed:.1f} hrs carried forward")
    
        self.today_study_log.clear()
        self.current_day += 1
    
        print(f"----- DAY {self.current_day - 1} CLOSED -----")
        self.show_plan_page() 


    def save_state(self):
        data = {
            "subjects": self.subjects,
            "daily_hours": self.daily_hours,
            "study_mode": self.study_mode_selected
        }
    
        with open("planner_state.json", "w") as f:
            json.dump(data, f, indent=4)

    def show_analytics_page(self):
        self.clear_content()
        data = self.get_analytics_data()
        card = ttk.Frame(self.content, style="Card.TFrame", padding=30)
        card.pack(fill="both", expand=True)
        
        ttk.Label(card, text="📊 Study Analytics", style="Title.TLabel")\
            .pack(anchor="w", pady=(0, 20)) 
        stats = ttk.Frame(card)
        stats.pack(fill="x", pady=10)

        def stat(label, value, row):
            ttk.Label(stats, text=label, font=("Segoe UI", 12))\
                .grid(row=row, column=0, sticky="w", pady=8)
            ttk.Label(stats, text=value, font=("Segoe UI", 12, "bold"))\
                .grid(row=row, column=1, sticky="e", padx=20)
        
        stat("📚 Total Subjects", f"{data['total_subjects']}", 0)
        stat("✅ Subjects Completed", f"{data['completed_subjects']}", 1)
        stat("⏳ Total Hours Remaining", f"{data['total_remaining']} hrs", 2)
        stat("📅 Max Deadline Left", f"{data['days_left']} days", 3) 


        # ---------- POMODORO LOGIC ----------
        # ---------- POMODORO LOGIC ----------
    def get_analytics_data(self):
        total_remaining = sum(s["remaining_hours"] for s in self.subjects)
        completed_subjects = sum(1 for s in self.subjects if s["remaining_hours"] == 0)
        total_subjects = len(self.subjects)
        max_deadline = max((s["deadline"] for s in self.subjects), default=0)
    
        return {
            "total_remaining": round(total_remaining, 2),
            "completed_subjects": completed_subjects,
            "total_subjects": total_subjects,
            "days_left": max_deadline
        } 

    def start_pomodoro(self):
        if not self.pomodoro_running:
            self.pomodoro_running = True
            self.update_pomodoro()

    def pause_pomodoro(self):
        self.pomodoro_running = False

    def reset_pomodoro(self):
        self.pomodoro_running = False
        self.pomodoro_mode = "work"
        self.pomodoro_seconds = 25 * 60
        self.update_timer_label()
        self.update_mode_label()

    def update_pomodoro(self):
        if self.pomodoro_running:
            if self.pomodoro_seconds > 0:
                self.pomodoro_seconds -= 1
                self.update_timer_label()
                self.root.after(1000, self.update_pomodoro)
            else:
                self.switch_mode()

    def switch_mode(self):
        if self.pomodoro_mode == "work":
            self.pomodoro_mode = "break"
            self.pomodoro_seconds = 5 * 60
        else:
            self.pomodoro_mode = "work"
            self.pomodoro_seconds = 25 * 60

        self.update_mode_label()
        self.update_timer_label()
        self.root.after(1000, self.update_pomodoro)

    def update_timer_label(self):
        minutes = self.pomodoro_seconds // 60
        seconds = self.pomodoro_seconds % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def update_mode_label(self):
        if self.pomodoro_mode == "work":
            self.mode_label.config(text="WORK SESSION", foreground="#e17055")
        else:
            self.mode_label.config(text="BREAK TIME", foreground="#00b894")

    def show_pomodoro_page(self):
        self.clear_content()

        self.pomodoro_running = False
        self.pomodoro_mode = "work"
        self.pomodoro_seconds = 25 * 60

        card = ttk.Frame(self.content, style="Card.TFrame", padding=30)
        card.pack(fill="both", expand=True)

        ttk.Label(
            card,
            text="Pomodoro Timer",
            style="Title.TLabel"
        ).pack(anchor="w")

        self.mode_label = ttk.Label(
            card,
            text="WORK SESSION",
            font=("Segoe UI", 14, "bold"),
            foreground="#e17055"
        )
        self.mode_label.pack(anchor="w", pady=(5, 20))

        self.timer_label = ttk.Label(
            card,
            text="25:00",
            font=("Segoe UI", 52, "bold"),
            foreground=ACCENT_COLOR
        )
        self.timer_label.pack(pady=20)

        btn_frame = ttk.Frame(card)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Start", width=12,
                   command=self.start_pomodoro).grid(row=0, column=0, padx=10)

        ttk.Button(btn_frame, text="Pause", width=12,
                   command=self.pause_pomodoro).grid(row=0, column=1, padx=10)

        ttk.Button(btn_frame, text="Reset", width=12,
                   command=self.reset_pomodoro).grid(row=0, column=2, padx=10)



    def show_deep_focus_page(self):
        self.clear_content()

        self.deep_running = False
        self.deep_mode = "focus"
        self.deep_seconds = 90 * 60

        card = ttk.Frame(self.content, style="Card.TFrame", padding=30)
        card.pack(fill="both", expand=True)

        ttk.Label(
            card,
            text="Deep Focus Mode",
            style="Title.TLabel"
        ).pack(anchor="w")

        self.deep_mode_label = ttk.Label(
            card,
            text="DEEP FOCUS SESSION",
            font=("Segoe UI", 14, "bold"),
            foreground="#6c5ce7"
        )
        self.deep_mode_label.pack(anchor="w", pady=(5, 20))

        self.deep_timer_label = ttk.Label(
            card,
            text="90:00",
            font=("Segoe UI", 52, "bold"),
            foreground=ACCENT_COLOR
        )
        self.deep_timer_label.pack(pady=20)

        btn_frame = ttk.Frame(card)
        btn_frame.pack(pady=20)

        ttk.Button(
            btn_frame,
            text="Start",
            width=12,
            command=self.start_deep_focus
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            btn_frame,
            text="Pause",
            width=12,
            command=self.pause_deep_focus
        ).grid(row=0, column=1, padx=10)

        ttk.Button(
            btn_frame,
            text="Reset",
            width=12,
            command=self.reset_deep_focus
        ).grid(row=0, column=2, padx=10)

    
        # ---------- DEEP FOCUS LOGIC ----------
    def start_deep_focus(self):
        if not self.deep_running:
            self.deep_running = True
            self.update_deep_focus()
    
    def pause_deep_focus(self):
        self.deep_running = False
    
    def reset_deep_focus(self):
        self.deep_running = False
        self.deep_mode = "focus"
        self.deep_seconds = 90 * 60
        self.update_deep_timer_label()
        self.update_deep_mode_label()
    
    def update_deep_focus(self):
        if self.deep_running:
            if self.deep_seconds > 0:
                self.deep_seconds -= 1
                self.update_deep_timer_label()
                self.root.after(1000, self.update_deep_focus)
            else:
                self.switch_deep_mode()
    
    def switch_deep_mode(self):
        if self.deep_mode == "focus":
            self.deep_mode = "break"
            self.deep_seconds = 15 * 60
        else:
            self.deep_mode = "focus"
            self.deep_seconds = 90 * 60
    
        self.update_deep_mode_label()
        self.update_deep_timer_label()
        self.root.after(1000, self.update_deep_focus)
    
    def update_deep_timer_label(self):
        minutes = self.deep_seconds // 60
        seconds = self.deep_seconds % 60
        self.deep_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
    
    def update_deep_mode_label(self):
        if self.deep_mode == "focus":
            self.deep_mode_label.config(
                text="DEEP FOCUS SESSION",
                foreground="#6c5ce7"
            )
        else:
            self.deep_mode_label.config(
                text="RECOVERY BREAK",
                foreground="#00b894"
            )
    def save_state(self):
        data = {
            "subjects": self.subjects,
            "daily_hours": self.daily_hours,
            "study_mode": self.study_mode_selected,
            "current_day": getattr(self, "current_day", 1)
        }
    
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)
    
    def load_state(self):
        if not os.path.exists(SAVE_FILE):
            return False
    
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
    
        self.subjects = data.get("subjects", [])
        self.daily_hours = data.get("daily_hours", 0)
        self.study_mode_selected = data.get("study_mode", "Pomodoro")
        self.current_day = data.get("current_day", 1)
    
        return True




# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = StudyPlannerGUI(root)
    root.mainloop()
