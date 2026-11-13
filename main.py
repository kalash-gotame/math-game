
import random
import tkinter as tk
import math

entries = []
numbers = []
out = 0
score = 0
question = 0
time_left = 60
timer_id = None
next_id = None
exps = ["+", "-", "*", "/"]
game_over = False
answer_locked = False

BG = "#10141f"
CARD = "#1b2333"
ACCENT = "#4f8cff"
TEXT = "#f1f5f9"
MUTED = "#94a3b8"
GREEN = "#22c55e"
RED = "#ef4444"

root = tk.Tk()
root.geometry("650x510")
root.title("MindMath")
root.configure(bg=BG)
root.resizable(False, False)


def gen_4():
    return [str(random.randint(1, 10)) for _ in range(5)]


def gen_eqn(listn):
    labels = exps.copy()
    random.shuffle(labels)

    return (
        listn[0] + labels[0] + listn[1] +
        labels[1] + listn[2] + labels[2] +
        listn[3] + labels[3] + listn[4]
    )


def ans(eqn):
    return eval(eqn, {"__builtins__": None}, {})


def update_stats():
    score_label.config(text=f"SCORE: {score}")
    question_label.config(text=f"QUESTION: {question}")


def stop_timer():
    global timer_id

    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None


def cancel_next():
    global next_id

    if next_id is not None:
        root.after_cancel(next_id)
        next_id = None


def start_timer():
    global timer_id, time_left

    timer_label.config(
        text=f"00:{time_left:02d}",
        fg=RED if time_left <= 10 else ACCENT
    )

    if time_left <= 0:
        end_question()
        return

    timer_id = root.after(1000, timer_tick)


def timer_tick():
    global time_left, timer_id

    timer_id = None
    time_left -= 1

    if time_left <= 0:
        time_left = 0
        timer_label.config(text="00:00", fg=RED)
        end_question()
        return

    start_timer()


def clear_equation():
    for widget in equation_frame.winfo_children():
        widget.destroy()


def show_win():
    global entries, numbers, out, time_left
    global question, game_over, answer_locked, next_id

    stop_timer()
    cancel_next()

    game_over = False
    answer_locked = False

    numbers = gen_4()
    eqn = gen_eqn(numbers)

    out = round(float(ans(eqn)), 2)

    entries = []
    time_left = 60
    question += 1

    update_stats()
    clear_equation()

    for i in range(5):
        tk.Label(
            equation_frame,
            text=numbers[i],
            font=("Segoe UI", 23, "bold"),
            bg=CARD,
            fg=TEXT
        ).grid(row=0, column=i * 2, padx=3)

        if i < 4:
            entry = tk.Entry(
                equation_frame,
                width=2,
                font=("Segoe UI", 20, "bold"),
                justify="center",
                bg="#293449",
                fg=ACCENT,
                insertbackground=TEXT,
                relief="flat",
                bd=0
            )
            entry.grid(
                row=0,
                column=i * 2 + 1,
                padx=3,
                ipady=5
            )
            entries.append(entry)

    answer_label.config(text=f"=  {out:g}", fg=ACCENT)

    feedback_label.config(
        text="Enter the four operators",
        fg=MUTED
    )

    submit_button.config(
        state="normal",
        bg=ACCENT,
        cursor="hand2"
    )

    start_timer()
    entries[0].focus_set()


def end_question():
    global game_over

    stop_timer()
    game_over = True

    for entry in entries:
        entry.config(state="disabled")

    submit_button.config(state="disabled", cursor="arrow")

    feedback_label.config(
        text=f"TIME'S UP! Answer: {out:g}",
        fg=RED
    )


def cmd():
    global score, answer_locked, next_id

    if game_over or answer_locked:
        return

    operators = [entry.get().strip() for entry in entries]

    if any(op not in exps for op in operators):
        feedback_label.config(
            text="Use only +, -, * or /",
            fg=RED
        )
        return

    eqn = (
        numbers[0] + operators[0] +
        numbers[1] + operators[1] +
        numbers[2] + operators[2] +
        numbers[3] + operators[3] +
        numbers[4]
    )

    try:
        u_ans = float(ans(eqn))

        if not math.isfinite(u_ans):
            raise ValueError

        u_ans = round(u_ans, 2)

    except (ZeroDivisionError, ValueError, TypeError, SyntaxError):
        feedback_label.config(
            text="Invalid equation!",
            fg=RED
        )
        return

    if u_ans == out:
        score += 10
        answer_locked = True

        stop_timer()

        feedback_label.config(
            text="CORRECT! +10 POINTS",
            fg=GREEN
        )

        for entry in entries:
            entry.config(state="disabled")

        submit_button.config(state="disabled", cursor="arrow")

        update_stats()
        next_id = root.after(1000, show_win)

    else:
        feedback_label.config(
            text="WRONG! TRY AGAIN",
            fg=RED
        )


def restart():
    global score, question, game_over, answer_locked

    stop_timer()
    cancel_next()

    score = 0
    question = 0
    game_over = False
    answer_locked = False

    show_win()


def on_close():
    stop_timer()
    cancel_next()
    root.destroy()


header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=30, pady=(20, 8))

tk.Label(
    header,
    text="MINDMATH",
    font=("Segoe UI", 24, "bold"),
    bg=BG,
    fg=TEXT
).pack(side="left")

tk.Label(
    header,
    text="MENTAL MATH CHALLENGE",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=ACCENT
).pack(side="right", pady=10)


stats_frame = tk.Frame(root, bg=BG)
stats_frame.pack(fill="x", padx=30, pady=8)

score_label = tk.Label(
    stats_frame,
    text="SCORE: 0",
    font=("Segoe UI", 12, "bold"),
    bg=BG,
    fg=GREEN
)
score_label.pack(side="left")

question_label = tk.Label(
    stats_frame,
    text="QUESTION: 0",
    font=("Segoe UI", 12, "bold"),
    bg=BG,
    fg=MUTED
)
question_label.pack(side="right")


timer_label = tk.Label(
    root,
    text=f"{time_left // 60:02d}:{time_left % 60:02d}",
    font=("Segoe UI", 30, "bold"),
    bg=BG,
    fg=ACCENT
)
timer_label.pack(pady=8)


card = tk.Frame(
    root,
    bg=CARD,
    padx=15,
    pady=25
)
card.pack(fill="x", padx=25, pady=8)

tk.Label(
    card,
    text="INSERT OPERATORS TO MATCH THE ANSWER",
    font=("Segoe UI", 9, "bold"),
    bg=CARD,
    fg=MUTED
).pack(pady=(0, 22))

equation_frame = tk.Frame(card, bg=CARD)
equation_frame.pack()

answer_label = tk.Label(
    card,
    text="= 0",
    font=("Segoe UI", 23, "bold"),
    bg=CARD,
    fg=ACCENT
)
answer_label.pack(pady=(20, 0))


feedback_label = tk.Label(
    root,
    text="Enter the four operators",
    font=("Segoe UI", 11, "bold"),
    bg=BG,
    fg=MUTED
)
feedback_label.pack(pady=8)


submit_button = tk.Button(
    root,
    text="SUBMIT ANSWER",
    font=("Segoe UI", 12, "bold"),
    bg=ACCENT,
    fg="white",
    activebackground="#3674df",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=cmd,
    padx=30,
    pady=11
)
submit_button.pack(pady=7)


restart_button = tk.Button(
    root,
    text="RESTART GAME",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=MUTED,
    activebackground=BG,
    activeforeground=TEXT,
    relief="flat",
    cursor="hand2",
    command=restart
)
restart_button.pack(pady=3)


root.bind("<Return>", lambda event: cmd())
root.protocol("WM_DELETE_WINDOW", on_close)

show_win()
root.mainloop()
