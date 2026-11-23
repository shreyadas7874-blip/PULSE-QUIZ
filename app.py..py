import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

APP_NAME = "PULSE QUIZ"
BEST_FILE = "pulse_quiz_best.json"

# Add more questions here. Each question needs:
# category, difficulty, question, options (4), answer (exactly matching one option), hint.
QUESTIONS = [
    # FOOD
    {"category":"Food","difficulty":"Easy","question":"Which fruit is known as the 'king of fruits' in many parts of India?","options":["Mango","Apple","Banana","Orange"],"answer":"Mango","hint":"It is especially popular during summer."},
    {"category":"Food","difficulty":"Easy","question":"Which ingredient is used to make traditional guacamole?","options":["Potato","Avocado","Carrot","Cucumber"],"answer":"Avocado","hint":"It is a creamy green fruit."},
    {"category":"Food","difficulty":"Medium","question":"Which spice gives many dishes their yellow colour?","options":["Black pepper","Turmeric","Cumin","Clove"],"answer":"Turmeric","hint":"It is also called haldi."},
    {"category":"Food","difficulty":"Medium","question":"Tofu is mainly made from which ingredient?","options":["Milk","Soybeans","Rice","Wheat"],"answer":"Soybeans","hint":"It is commonly used in vegetarian dishes."},
    {"category":"Food","difficulty":"Hard","question":"Which country is widely credited with originating sushi?","options":["China","Thailand","Japan","Vietnam"],"answer":"Japan","hint":"Think of an East Asian island nation."},

    # SPORTS
    {"category":"Sports","difficulty":"Easy","question":"How many players from one team are on the field in football (soccer)?","options":["9","10","11","12"],"answer":"11","hint":"The goalkeeper is included."},
    {"category":"Sports","difficulty":"Easy","question":"Which sport uses a shuttlecock?","options":["Tennis","Badminton","Hockey","Squash"],"answer":"Badminton","hint":"Players use lightweight racquets."},
    {"category":"Sports","difficulty":"Medium","question":"How many rings are there on the Olympic symbol?","options":["4","5","6","7"],"answer":"5","hint":"The rings are interlinked."},
    {"category":"Sports","difficulty":"Medium","question":"In cricket, what is the term for scoring 100 runs by one batter?","options":["Half-century","Century","Maiden","Hat-trick"],"answer":"Century","hint":"It represents one hundred."},
    {"category":"Sports","difficulty":"Hard","question":"In which country did the modern Olympic Games begin in 1896?","options":["France","Greece","Italy","United Kingdom"],"answer":"Greece","hint":"The first modern games were held in Athens."},

    # MUSIC
    {"category":"Music","difficulty":"Easy","question":"How many strings does a standard guitar usually have?","options":["4","5","6","7"],"answer":"6","hint":"It is an even number."},
    {"category":"Music","difficulty":"Easy","question":"Which instrument has black and white keys?","options":["Flute","Piano","Drum","Violin"],"answer":"Piano","hint":"It is often used for melodies and chords."},
    {"category":"Music","difficulty":"Medium","question":"Which family does the violin belong to?","options":["Brass","Percussion","String","Woodwind"],"answer":"String","hint":"It is played with a bow."},
    {"category":"Music","difficulty":"Medium","question":"What does 'a cappella' mean?","options":["Singing without instruments","Singing very loudly","Instrumental music","A slow rhythm"],"answer":"Singing without instruments","hint":"Only voices are used."},
    {"category":"Music","difficulty":"Hard","question":"How many semitones are there in an octave in standard Western music?","options":["10","11","12","13"],"answer":"12","hint":"Count the notes from one note to its octave, including sharps/flats."},

    # SCIENCE
    {"category":"Science","difficulty":"Easy","question":"Which planet is known as the Red Planet?","options":["Venus","Mars","Jupiter","Mercury"],"answer":"Mars","hint":"Its surface has a reddish appearance."},
    {"category":"Science","difficulty":"Easy","question":"What gas do plants absorb from the atmosphere?","options":["Oxygen","Nitrogen","Carbon dioxide","Hydrogen"],"answer":"Carbon dioxide","hint":"Plants use it during photosynthesis."},
    {"category":"Science","difficulty":"Medium","question":"What is the chemical symbol for gold?","options":["Ag","Au","Go","Gd"],"answer":"Au","hint":"It comes from the Latin word aurum."},
    {"category":"Science","difficulty":"Medium","question":"Which part of the human cell contains most of its genetic material?","options":["Nucleus","Cell wall","Ribosome","Cytoplasm"],"answer":"Nucleus","hint":"It is often called the cell's control centre."},
    {"category":"Science","difficulty":"Hard","question":"What is the approximate speed of light in a vacuum?","options":["30,000 km/s","150,000 km/s","300,000 km/s","3,000,000 km/s"],"answer":"300,000 km/s","hint":"It is about 3 × 10^5 kilometres per second."},

    # TECHNOLOGY
    {"category":"Technology","difficulty":"Easy","question":"What does CPU stand for?","options":["Central Processing Unit","Computer Personal Unit","Core Program Utility","Central Power Utility"],"answer":"Central Processing Unit","hint":"It is often called the brain of a computer."},
    {"category":"Technology","difficulty":"Easy","question":"Which of these is a web browser?","options":["Python","Chrome","Windows","Excel"],"answer":"Chrome","hint":"It is used to visit websites."},
    {"category":"Technology","difficulty":"Medium","question":"Which language is commonly used to style web pages?","options":["HTML","CSS","SQL","C"],"answer":"CSS","hint":"It controls colours, layout and fonts."},
    {"category":"Technology","difficulty":"Medium","question":"What does URL stand for?","options":["Uniform Resource Locator","Universal Reading Link","United Reference List","User Route Location"],"answer":"Uniform Resource Locator","hint":"It is the address of a web resource."},
    {"category":"Technology","difficulty":"Hard","question":"Which data structure follows the Last In, First Out (LIFO) principle?","options":["Queue","Stack","Tree","Graph"],"answer":"Stack","hint":"Think of a pile of plates."},

    # MOVIES
    {"category":"Movies","difficulty":"Easy","question":"Which animated film features a snowman named Olaf?","options":["Moana","Frozen","Coco","Up"],"answer":"Frozen","hint":"It includes the song 'Let It Go'."},
    {"category":"Movies","difficulty":"Easy","question":"What is the name of the wizarding school in Harry Potter?","options":["Narnia","Hogwarts","Nevermore","Camelot"],"answer":"Hogwarts","hint":"Harry receives a letter inviting him there."},
    {"category":"Movies","difficulty":"Medium","question":"Which film series features the character Jack Sparrow?","options":["The Matrix","Pirates of the Caribbean","Jurassic Park","Fast & Furious"],"answer":"Pirates of the Caribbean","hint":"It is about pirates and the sea."},
    {"category":"Movies","difficulty":"Medium","question":"Which Indian film industry is commonly associated with Mumbai?","options":["Kollywood","Bollywood","Tollywood","Sandalwood"],"answer":"Bollywood","hint":"Its name combines Bombay and Hollywood."},
    {"category":"Movies","difficulty":"Hard","question":"Which director made the film 'Inception'?","options":["Steven Spielberg","Christopher Nolan","James Cameron","Peter Jackson"],"answer":"Christopher Nolan","hint":"He also directed The Dark Knight trilogy."},

    # GENERAL KNOWLEDGE
    {"category":"General Knowledge","difficulty":"Easy","question":"What is the capital of India?","options":["Mumbai","New Delhi","Kolkata","Chennai"],"answer":"New Delhi","hint":"It is where the Parliament of India is located."},
    {"category":"General Knowledge","difficulty":"Easy","question":"How many days are there in a leap year?","options":["364","365","366","367"],"answer":"366","hint":"February has 29 days in that year."},
    {"category":"General Knowledge","difficulty":"Medium","question":"Which is the largest ocean on Earth?","options":["Atlantic","Indian","Arctic","Pacific"],"answer":"Pacific","hint":"It lies between Asia/Australia and the Americas."},
    {"category":"General Knowledge","difficulty":"Medium","question":"Which is the currency of Japan?","options":["Won","Yuan","Yen","Baht"],"answer":"Yen","hint":"Its symbol is ¥."},
    {"category":"General Knowledge","difficulty":"Hard","question":"Which gas makes up the largest share of Earth's atmosphere?","options":["Oxygen","Nitrogen","Carbon dioxide","Argon"],"answer":"Nitrogen","hint":"It makes up roughly 78% of the atmosphere."},
]

BG = "#101827"
PANEL = "#1b2940"
PANEL2 = "#243650"
TEXT = "#f4f7fb"
MUTED = "#a9b7ca"
ACCENT = "#6ee7d8"
YELLOW = "#ffd166"
GREEN = "#69db9a"
RED = "#ff7777"

class PulseQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Pulse Quiz - Challenge Your Mind")
        self.root.geometry("900x650")
        self.root.minsize(760, 570)
        self.root.configure(bg=BG)
        self.best_scores = self.load_best_scores()
        self.timer_job = None
        self.show_home()

    def load_best_scores(self):
        try:
            with open(BEST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}

    def save_best_scores(self):
        try:
            with open(BEST_FILE, "w", encoding="utf-8") as f:
                json.dump(self.best_scores, f, indent=2)
        except OSError:
            pass

    def clear(self):
        self.stop_timer()
        for widget in self.root.winfo_children():
            widget.destroy()

    def heading(self, parent, title, subtitle=""):
        tk.Label(parent, text=title, bg=parent.cget("bg"), fg=TEXT,
                 font=("Segoe UI", 27, "bold")).pack(pady=(10, 4))
        if subtitle:
            tk.Label(parent, text=subtitle, bg=parent.cget("bg"), fg=MUTED,
                     font=("Segoe UI", 11)).pack(pady=(0, 14))

    def make_button(self, parent, text, command, color=ACCENT, fg=BG, width=18):
        return tk.Button(parent, text=text, command=command, bg=color, fg=fg,
                         activebackground=color, activeforeground=fg,
                         font=("Segoe UI", 11, "bold"), relief="flat",
                         cursor="hand2", width=width, padx=10, pady=10)

    def show_home(self):
        self.clear()
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=35, pady=22)
        self.heading(outer, "⚡ PULSE QUIZ", "Think fast. Learn more. Beat your best score!")
        card = tk.Frame(outer, bg=PANEL, padx=28, pady=22)
        card.pack(fill="x", pady=12)
        tk.Label(card, text="Set up your challenge", bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 16))

        row = tk.Frame(card, bg=PANEL)
        row.pack(fill="x", pady=7)
        tk.Label(row, text="Your name", bg=PANEL, fg=MUTED, font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.name_var = tk.StringVar(value="Player")
        name_entry = tk.Entry(row, textvariable=self.name_var, font=("Segoe UI", 11), width=24,
                              bg=PANEL2, fg=TEXT, insertbackground=TEXT, relief="flat")
        name_entry.grid(row=0, column=1, sticky="w", ipady=7, padx=5)

        row2 = tk.Frame(card, bg=PANEL)
        row2.pack(fill="x", pady=12)
        tk.Label(row2, text="Category", bg=PANEL, fg=MUTED, font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", padx=(0, 20))
        categories = ["All Categories"] + sorted({q["category"] for q in QUESTIONS})
        self.category_var = tk.StringVar(value="All Categories")
        ttk.Style().configure("TCombobox", padding=6)
        self.category_box = ttk.Combobox(row2, textvariable=self.category_var, values=categories, state="readonly", width=22, font=("Segoe UI", 10))
        self.category_box.grid(row=0, column=1, sticky="w", padx=5)

        row3 = tk.Frame(card, bg=PANEL)
        row3.pack(fill="x", pady=12)
        tk.Label(row3, text="Difficulty", bg=PANEL, fg=MUTED, font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.difficulty_var = tk.StringVar(value="All Levels")
        self.difficulty_box = ttk.Combobox(row3, textvariable=self.difficulty_var,
                                           values=["All Levels", "Easy", "Medium", "Hard"],
                                           state="readonly", width=22, font=("Segoe UI", 10))
        self.difficulty_box.grid(row=0, column=1, sticky="w", padx=5)

        row4 = tk.Frame(card, bg=PANEL)
        row4.pack(fill="x", pady=12)
        tk.Label(row4, text="Number of questions", bg=PANEL, fg=MUTED, font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", padx=(0, 20))
        self.count_var = tk.StringVar(value="10")
        self.count_box = ttk.Combobox(row4, textvariable=self.count_var,
                                      values=["5", "10", "15", "20", "All available"],
                                      state="readonly", width=22, font=("Segoe UI", 10))
        self.count_box.grid(row=0, column=1, sticky="w", padx=5)

        self.best_label = tk.Label(outer, text=self.best_summary(), bg=BG, fg=YELLOW, font=("Segoe UI", 10))
        self.best_label.pack(pady=10)
        buttons = tk.Frame(outer, bg=BG)
        buttons.pack(pady=8)
        self.make_button(buttons, "START QUIZ", self.start_quiz, width=18).pack(side="left", padx=8)
        self.make_button(buttons, "HOW TO PLAY", self.show_help, color=PANEL2, fg=TEXT, width=18).pack(side="left", padx=8)
        tk.Label(outer, text="Features: timer • hints • 50:50 lifeline • skip • answer review • saved best score",
                 bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(pady=18)

    def best_summary(self):
        if not self.best_scores:
            return "🏆 Best score: Play your first quiz to set a record!"
        best = max(self.best_scores.values())
        return f"🏆 Your best saved score: {best}%"

    def show_help(self):
        messagebox.showinfo("How to play",
            "• Choose a category, difficulty and number of questions.\n"
            "• Each question has a 20-second timer.\n"
            "• Correct answer: +10 points. Wrong/timeout: 0 points.\n"
            "• 50:50 removes two wrong options (once per quiz).\n"
            "• Hint gives a clue (once per quiz).\n"
            "• Skip moves to the next question (once per quiz).\n"
            "• Your best percentage is saved on this laptop.")

    def start_quiz(self):
        category = self.category_var.get()
        difficulty = self.difficulty_var.get()
        pool = [q.copy() for q in QUESTIONS
                if (category == "All Categories" or q["category"] == category)
                and (difficulty == "All Levels" or q["difficulty"] == difficulty)]
        if not pool:
            messagebox.showwarning("No questions", "There are no questions for this selection yet.")
            return
        random.shuffle(pool)
        count_text = self.count_var.get()
        count = len(pool) if count_text == "All available" else int(count_text)
        self.questions = pool[:min(count, len(pool))]
        self.index = 0
        self.score = 0
        self.correct_count = 0
        self.answers = []
        self.seconds_left = 20
        self.used_fifty = False
        self.used_hint = False
        self.used_skip = False
        self.selected = tk.StringVar(value="")
        self.show_question()

    def show_question(self):
        self.clear()
        q = self.questions[self.index]
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=28, pady=18)

        top = tk.Frame(outer, bg=BG)
        top.pack(fill="x")
        tk.Label(top, text=f"{q['category']}  •  {q['difficulty']}", bg=BG, fg=ACCENT,
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(top, text=f"Question {self.index + 1} of {len(self.questions)}",
                 bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(side="right")

        self.progress = ttk.Progressbar(outer, maximum=len(self.questions), value=self.index, length=700)
        self.progress.pack(fill="x", pady=(12, 18))

        info = tk.Frame(outer, bg=PANEL, padx=18, pady=12)
        info.pack(fill="x")
        self.timer_label = tk.Label(info, text="⏱ 20 sec", bg=PANEL, fg=YELLOW, font=("Segoe UI", 12, "bold"))
        self.timer_label.pack(side="left")
        tk.Label(info, text=f"Score: {self.score}", bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(side="right")

        qcard = tk.Frame(outer, bg=PANEL, padx=24, pady=24)
        qcard.pack(fill="x", pady=18)
        tk.Label(qcard, text=q["question"], bg=PANEL, fg=TEXT, wraplength=760,
                 justify="left", font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(0, 18))

        self.option_buttons = []
        options = q["options"][:]
        random.shuffle(options)
        for option in options:
            rb = tk.Radiobutton(qcard, text=option, variable=self.selected, value=option,
                                bg=PANEL2, fg=TEXT, selectcolor="#35506e",
                                activebackground=PANEL2, activeforeground=TEXT,
                                font=("Segoe UI", 12), anchor="w", padx=12, pady=10,
                                relief="flat", indicatoron=False, width=65)
            rb.pack(fill="x", pady=5)
            self.option_buttons.append(rb)

        tools = tk.Frame(outer, bg=BG)
        tools.pack(fill="x", pady=5)
        self.fifty_btn = self.make_button(tools, "50:50", self.use_fifty, color=PANEL2, fg=TEXT, width=10)
        self.fifty_btn.pack(side="left", padx=4)
        self.hint_btn = self.make_button(tools, "HINT", self.use_hint, color=PANEL2, fg=TEXT, width=10)
        self.hint_btn.pack(side="left", padx=4)
        self.skip_btn = self.make_button(tools, "SKIP", self.skip_question, color=PANEL2, fg=TEXT, width=10)
        self.skip_btn.pack(side="left", padx=4)
        self.next_btn = self.make_button(tools, "SUBMIT ANSWER", self.submit_answer, width=19)
        self.next_btn.pack(side="right", padx=4)

        self.status_label = tk.Label(outer, text="", bg=BG, fg=MUTED, font=("Segoe UI", 10))
        self.status_label.pack(pady=8)

        if self.used_fifty:
            self.fifty_btn.config(state="disabled")
        if self.used_hint:
            self.hint_btn.config(state="disabled")
        if self.used_skip:
            self.skip_btn.config(state="disabled")
        self.start_timer()

    def start_timer(self):
        self.seconds_left = 20
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"⏱ {self.seconds_left} sec")
        if self.seconds_left <= 0:
            self.submit_answer(timeout=True)
        else:
            self.timer_job = self.root.after(1000, self.tick_timer)

    def tick_timer(self):
        self.seconds_left -= 1
        self.update_timer()

    def stop_timer(self):
        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except tk.TclError:
                pass
            self.timer_job = None

    def use_fifty(self):
        if self.used_fifty:
            return
        q = self.questions[self.index]
        wrong = [b for b in self.option_buttons if b.cget("text") != q["answer"]]
        for button in random.sample(wrong, min(2, len(wrong))):
            button.config(state="disabled", text="—")
        self.used_fifty = True
        self.fifty_btn.config(state="disabled")
        self.status_label.config(text="50:50 used — two incorrect options removed.", fg=ACCENT)

    def use_hint(self):
        if self.used_hint:
            return
        self.used_hint = True
        self.hint_btn.config(state="disabled")
        self.status_label.config(text="💡 Hint: " + self.questions[self.index]["hint"], fg=YELLOW)

    def skip_question(self):
        if self.used_skip:
            return
        self.used_skip = True
        self.answers.append({"question": self.questions[self.index]["question"],
                             "chosen": "Skipped", "correct": self.questions[self.index]["answer"],
                             "result": "Skipped"})
        self.next_question()

    def submit_answer(self, timeout=False):
        self.stop_timer()
        q = self.questions[self.index]
        chosen = self.selected.get()
        if timeout:
            chosen = "No answer (time up)"
        if not timeout and not chosen:
            messagebox.showwarning("Choose an answer", "Please select an option before submitting.")
            self.start_timer()
            return
        is_correct = chosen == q["answer"]
        if is_correct:
            self.score += 10
            self.correct_count += 1
            result = "Correct"
            color = GREEN
        else:
            result = "Incorrect"
            color = RED
        self.answers.append({"question": q["question"], "chosen": chosen,
                             "correct": q["answer"], "result": result})
        self.status_label.config(text=("✓ Correct! +10 points" if is_correct else f"✗ {result}. Correct answer: {q['answer']}"),
                                 fg=color)
        self.next_btn.config(text="NEXT QUESTION", command=self.next_question)
        for button in self.option_buttons:
            button.config(state="disabled")
        self.fifty_btn.config(state="disabled")
        self.hint_btn.config(state="disabled")
        self.skip_btn.config(state="disabled")

    def next_question(self):
        self.stop_timer()
        self.index += 1
        if self.index >= len(self.questions):
            self.show_result()
        else:
            self.show_question()

    def show_result(self):
        self.clear()
        total = len(self.questions)
        percent = round((self.correct_count / total) * 100) if total else 0
        category_key = self.category_var.get() + " | " + self.difficulty_var.get()
        old_best = self.best_scores.get(category_key, 0)
        new_record = percent > old_best
        if new_record:
            self.best_scores[category_key] = percent
            self.save_best_scores()

        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=35, pady=25)
        self.heading(outer, "QUIZ COMPLETED!", f"Well played, {self.name_var.get().strip() or 'Player'}!")
        card = tk.Frame(outer, bg=PANEL, padx=30, pady=24)
        card.pack(fill="x", pady=12)
        tk.Label(card, text=f"{percent}%", bg=PANEL, fg=ACCENT,
                 font=("Segoe UI", 42, "bold")).pack()
        tk.Label(card, text=f"{self.score} / {total * 10} points", bg=PANEL, fg=TEXT,
                 font=("Segoe UI", 16, "bold")).pack(pady=4)
        tk.Label(card, text=f"Correct: {self.correct_count}    Incorrect or skipped: {total - self.correct_count}",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 11)).pack(pady=6)
        if new_record:
            record_text = "🏆 New personal best!"
        else:
            record_text = f"Personal best for this selection: {max(old_best, percent)}%"
        tk.Label(card, text=record_text, bg=PANEL, fg=YELLOW,
                 font=("Segoe UI", 11, "bold")).pack(pady=8)

        if percent >= 80:
            message = "Excellent work! You're a quiz champion."
        elif percent >= 50:
            message = "Good effort! Keep practising and improve your score."
        else:
            message = "Keep learning — your next attempt can be even better."
        tk.Label(outer, text=message, bg=BG, fg=TEXT, font=("Segoe UI", 12)).pack(pady=10)

        buttons = tk.Frame(outer, bg=BG)
        buttons.pack(pady=12)
        self.make_button(buttons, "REVIEW ANSWERS", self.show_review, color=PANEL2, fg=TEXT, width=18).pack(side="left", padx=7)
        self.make_button(buttons, "PLAY AGAIN", self.show_home, width=16).pack(side="left", padx=7)
        self.make_button(buttons, "EXIT", self.root.destroy, color="#3a4658", fg=TEXT, width=10).pack(side="left", padx=7)

    def show_review(self):
        self.clear()
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=25, pady=18)
        self.heading(outer, "ANSWER REVIEW", "Check your answers and learn from every question.")
        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=BG)
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=800)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        for i, item in enumerate(self.answers, 1):
            box = tk.Frame(content, bg=PANEL, padx=15, pady=12)
            box.pack(fill="x", pady=6)
            color = GREEN if item["result"] == "Correct" else RED
            tk.Label(box, text=f"{i}. {item['question']}", bg=PANEL, fg=TEXT,
                     wraplength=740, justify="left", font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(box, text=f"Your answer: {item['chosen']}", bg=PANEL, fg=color,
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(6, 0))
            tk.Label(box, text=f"Correct answer: {item['correct']}", bg=PANEL, fg=ACCENT,
                     font=("Segoe UI", 10)).pack(anchor="w")
        self.make_button(outer, "BACK TO HOME", self.show_home, width=18).pack(pady=12)


if __name__ == "__main__":
    root = tk.Tk()
    app = PulseQuiz(root)
    root.mainloop()
