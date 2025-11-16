import tkinter as tk
from tkinter import messagebox
import random

# -------------------- MAIN WINDOW SETUP --------------------
root = tk.Tk()
root.title("Survive the Ghost's Quiz")
root.attributes("-fullscreen", True)  # Fullscreen horror mode
root.config(bg="black")

# Press ESC anytime to instantly quit
root.bind("<Escape>", lambda e: root.destroy())

# -------------------- GLOBAL VARIABLES --------------------
difficulty = None
score = 0
question_number = 0
num1, num2, operation = 0, 0, "+"
attempts = 0

# -------------------- FUNCTIONS --------------------
def clearWindow():
    for widget in root.winfo_children():
        widget.destroy()

# Floating close button for every screen
def addCloseButton():
    close_btn = tk.Button(
        root,
        text="X",
        font=("Courier", 18, "bold"),
        bg="darkred",
        fg="white",
        command=root.destroy,
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )
    close_btn.place(relx=0.98, rely=0.02, anchor="ne")

def homeScreen():
    clearWindow()
    addCloseButton()

    tk.Label(root, text="SURVIVE THE GHOST'S QUIZ", fg="red", bg="black",
             font=("Chiller", 60, "bold")).pack(pady=80)

    tk.Button(root, text="START GAME", font=("Courier", 24), bg="red", fg="white",
              width=20, command=difficultyMenu).pack(pady=20)
    tk.Button(root, text="INSTRUCTIONS", font=("Courier", 24), bg="#222", fg="white",
              width=20, command=instructionsPage).pack(pady=20)
    tk.Button(root, text="EXIT", font=("Courier", 24), bg="darkred", fg="white",
              width=20, command=root.destroy).pack(pady=20)

def instructionsPage():
    clearWindow()
    addCloseButton()

    tk.Label(root, text="INSTRUCTIONS", fg="red", bg="black",
             font=("Chiller", 60, "bold")).pack(pady=40)

    instructions = (
        "1. Choose your difficulty (Easy / Moderate / Advanced)\n"
        "2. You’ll face 10 math problems: + or -\n"
        "3. First correct try: +10 points\n"
        "4. Second correct try: +5 points\n"
        "5. Score 70 or higher to survive...\n"
        "6. Fail, and the ghost will find you 💀"
    )
    tk.Label(root, text=instructions, fg="white", bg="black",
             font=("Courier", 18), justify="left").pack(pady=20)

    tk.Button(root, text="BACK", font=("Courier", 18), bg="#333", fg="white",
              width=15, command=homeScreen).pack(pady=30)

def difficultyMenu():
    clearWindow()
    addCloseButton()

    tk.Label(root, text="CHOOSE YOUR DIFFICULTY", fg="red", bg="black",
             font=("Chiller", 60, "bold")).pack(pady=40)

    tk.Button(root, text="EASY", font=("Courier", 24), bg="#222", fg="white",
              width=20, command=lambda: startQuiz("easy")).pack(pady=20)
    tk.Button(root, text="MODERATE", font=("Courier", 24), bg="#222", fg="white",
              width=20, command=lambda: startQuiz("moderate")).pack(pady=20)
    tk.Button(root, text="ADVANCED", font=("Courier", 24), bg="#222", fg="white",
              width=20, command=lambda: startQuiz("advanced")).pack(pady=20)

    tk.Button(root, text="BACK", font=("Courier", 18), bg="#333", fg="white",
              width=15, command=homeScreen).pack(pady=40)

def randomInt(level):
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)

def decideOperation():
    return random.choice(["+", "-"])

def startQuiz(level):
    global difficulty, score, question_number
    difficulty = level
    score = 0
    question_number = 0
    nextQuestion()

def nextQuestion():
    global num1, num2, operation, attempts, question_number
    clearWindow()
    addCloseButton()

    if question_number >= 10:
        displayResults()
        return

    question_number += 1
    attempts = 0
    num1, num2 = randomInt(difficulty)
    operation = decideOperation()

    tk.Label(root, text=f"Question {question_number}/10", fg="red",
             bg="black", font=("Courier", 24)).pack(pady=10)
    tk.Label(root, text=f"{num1} {operation} {num2} = ?", fg="white",
             bg="black", font=("Courier", 40, "bold")).pack(pady=40)

    answer_entry = tk.Entry(root, font=("Courier", 28), justify="center")
    answer_entry.pack(pady=20)

    feedback = tk.Label(root, text="", fg="red", bg="black", font=("Courier", 20))
    feedback.pack(pady=10)

    def submit():
        nonlocal feedback
        user_answer = answer_entry.get()
        if not user_answer.lstrip("-").isdigit():
            feedback.config(text="Enter a valid number!", fg="orange")
            return
        isCorrect(int(user_answer), feedback)

    tk.Button(root, text="SUBMIT", font=("Courier", 22), bg="red", fg="white",
              width=15, command=submit).pack(pady=20)
    tk.Button(root, text="BACK", font=("Courier", 18), bg="#333", fg="white",
              width=10, command=difficultyMenu).pack(pady=10)

def isCorrect(user_answer, feedback_label):
    global score, attempts
    attempts += 1

    correct_answer = num1 + num2 if operation == "+" else num1 - num2

    if user_answer == correct_answer:
        if attempts == 1:
            score += 10
            feedback_label.config(text="Correct! +10 points", fg="green")
        else:
            score += 5
            feedback_label.config(text="Correct (2nd try)! +5 points", fg="yellow")
        root.after(1000, nextQuestion)
    else:
        if attempts == 1:
            feedback_label.config(text="Wrong... try again!", fg="red")
        else:
            feedback_label.config(text=f"Wrong again! The ghost laughs...\nAnswer was {correct_answer}.", fg="red")
            root.after(1500, nextQuestion)

def displayResults():
    clearWindow()
    addCloseButton()

    tk.Label(root, text="QUIZ COMPLETE", fg="red", bg="black",
             font=("Chiller", 60, "bold")).pack(pady=40)
    tk.Label(root, text=f"Your final score: {score}/100", fg="white", bg="black",
             font=("Courier", 28)).pack(pady=20)

    if score >= 90:
        rank = "A+"
    elif score >= 80:
        rank = "A"
    elif score >= 70:
        rank = "B"
    elif score >= 60:
        rank = "C"
    else:
        rank = "F"

    tk.Label(root, text=f"Rank: {rank}", fg="yellow", bg="black",
             font=("Courier", 24)).pack(pady=10)

    # Ghost ending
    if score >= 70:
        msg = "You survived… for now."
        color = "green"
        tk.Label(root, text=msg, fg=color, bg="black",
                 font=("Chiller", 40, "bold")).pack(pady=50)
    else:
        msg_label = tk.Label(root, text="THE GHOST FOUND YOU 💀", fg="red",
                             bg="black", font=("Chiller", 50, "bold"))
        msg_label.pack(pady=50)

        def flash_bg():
            current = root.cget("bg")
            root.config(bg="darkred" if current == "black" else "black")
            root.after(300, flash_bg)

        flash_bg()

    tk.Button(root, text="PLAY AGAIN", font=("Courier", 20), bg="#222", fg="white",
              width=15, command=homeScreen).pack(pady=20)
    tk.Button(root, text="EXIT", font=("Courier", 20), bg="red", fg="white",
              width=15, command=root.destroy).pack(pady=10)

# -------------------- START PROGRAM --------------------
homeScreen()
root.mainloop()
