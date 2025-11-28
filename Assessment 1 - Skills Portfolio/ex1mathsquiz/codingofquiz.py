import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import cv2

# ==================== MAIN WINDOW SETUP ====================
root = tk.Tk()
root.title("Survive the Ghost's Quiz")
root.attributes("-fullscreen", True)
root.config(bg="black")
root.bind("<Escape>", lambda e: root.destroy())

# ==================== GLOBAL VARIABLES ====================
difficulty = None
score = 0
question_number = 0
num1, num2, operation = 0, 0, "+"
attempts = 0

# Video background globals (fixed!)
video_capture = None
video_label = None
video_after_id = None

# ==================== HELPER FUNCTIONS ====================
def clearWindow():
    for widget in root.winfo_children():
        widget.destroy()

def setBackground():
    global bg_label, bg_image
    try:
        image = Image.open(r"Assessment 1 - Skills Portfolio\ex1mathsquiz\scarybg.jpg")
        image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        bg_label = tk.Label(root, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        root.config(bg="black")  # fallback

def playVideoBackground(video_path):
    global video_capture, video_label, video_after_id

    stopVideo()  # safety: stop any previous video

    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print("Video file not found! Using black background.")
        return

    video_label = tk.Label(root)
    video_label.place(x=0, y=0, relwidth=1, relheight=1)

    def update_frame():
        global video_after_id
        ret, frame = video_capture.read()
        if not ret:
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video_capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (root.winfo_screenwidth(), root.winfo_screenheight()))
            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            video_label.configure(image=img)
            video_label.image = img  # keep reference

        video_after_id = root.after(40, update_frame)  # ~25 FPS = smooth & light

    video_after_id = root.after(40, update_frame)

def stopVideo():
    global video_after_id, video_capture, video_label
    try:
        if video_after_id:
            root.after_cancel(video_after_id)
            video_after_id = None
        if video_capture:
            video_capture.release()
            video_capture = None
        if video_label and video_label.winfo_exists():
            video_label.destroy()
            video_label = None
    except:
        pass

def addCloseButton():
    close_btn = tk.Button(
        root, text="X", font=("Courier", 18, "bold"), bg="darkred", fg="white",
        command=root.destroy, bd=0, highlightthickness=0, cursor="hand2"
    )
    close_btn.place(relx=0.98, rely=0.02, anchor="ne")

# ==================== SCREENS ====================
def homeScreen():
    clearWindow()
    stopVideo()
    setBackground()
    addCloseButton()

    tk.Label(root, text="SURVIVE THE GHOST'S QUIZ", fg="red", bg="black",
             font=("Chiller", 70, "bold")).pack(pady=100)

    tk.Button(root, text="START GAME", font=("Courier", 28), bg="red", fg="white",
              width=20, height=2, command=difficultyMenu).pack(pady=20)
    tk.Button(root, text="INSTRUCTIONS", font=("Courier", 28), bg="#333", fg="white",
              width=20, height=2, command=instructionsPage).pack(pady=15)
    tk.Button(root, text="EXIT", font=("Courier", 28), bg="darkred", fg="white",
              width=20, height=2, command=root.destroy).pack(pady=15)

def instructionsPage():
    clearWindow()
    stopVideo()
    setBackground()
    addCloseButton()

    tk.Label(root, text="INSTRUCTIONS", fg="red", bg="black",
             font=("Chiller", 70, "bold")).pack(pady=60)

    instructions = (
        "• Choose your difficulty\n"
        "• Answer 10 math questions (addition & subtraction)\n"
        "• First try correct = +10 points\n"
        "• Second try correct = +5 points\n"
        "• Score 70+ to survive the ghost...\n"
        "• Fail and he will find you..."
    )
    tk.Label(root, text=instructions, fg="white", bg="black",
             font=("Courier", 22), justify="left").pack(pady=40)

    tk.Button(root, text="BACK", font=("Courier", 20), bg="#444", fg="white",
              command=homeScreen).pack(pady=50)

def difficultyMenu():
    clearWindow()
    stopVideo()
    setBackground()
    addCloseButton()

    tk.Label(root, text="CHOOSE YOUR DIFFICULTY", fg="red", bg="black",
             font=("Chiller", 60, "bold")).pack(pady=80)

    tk.Button(root, text="EASY", font=("Courier", 30), bg="#006400", fg="white",
              width=18, height=2, command=lambda: startQuiz("easy")).pack(pady=20)
    tk.Button(root, text="MODERATE", font=("Courier", 30), bg="#8B8000", fg="white",
              width=18, height=2, command=lambda: startQuiz("moderate")).pack(pady=20)
    tk.Button(root, text="ADVANCED", font=("Courier", 30), bg="darkred", fg="white",
              width=18, height=2, command=lambda: startQuiz("advanced")).pack(pady=20)

    tk.Button(root, text="BACK", font=("Courier", 20), bg="#333", fg="white",
              command=homeScreen).pack(pady=60)

# ==================== QUIZ LOGIC ====================
def randomInt(level):
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:  # advanced
        return random.randint(100, 999), random.randint(10, 999)

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

    if question_number >= 10:
        displayResults()
        return

    clearWindow()
    playVideoBackground(r"Assessment 1 - Skills Portfolio\ex1mathsquiz\scarybg2.mp4")
    addCloseButton()

    question_number += 1
    attempts = 0

    num1, num2 = randomInt(difficulty)
    operation = decideOperation()

    tk.Label(root, text=f"Question {question_number}/10", fg="red", bg="black",
             font=("Courier", 26, "bold")).pack(pady=20)

    tk.Label(root, text=f"{num1} {operation} {num2} = ?", fg="white", bg="black",
             font=("Courier", 50, "bold")).pack(pady=80)

    answer_entry = tk.Entry(root, font=("Courier", 36), justify="center", width=10)
    answer_entry.pack(pady=20)
    answer_entry.focus()

    feedback = tk.Label(root, text="", fg="yellow", bg="black", font=("Courier", 22))
    feedback.pack(pady=20)

    def submit():
        try:
            user_answer = int(answer_entry.get())
            checkAnswer(user_answer, feedback)
        except:
            feedback.config(text="Please enter a number!", fg="orange")

    submit_btn = tk.Button(root, text="SUBMIT", font=("Courier", 24), bg="red", fg="white",
                           width=12, height=2, command=submit)
    submit_btn.pack(pady=20)

    root.bind('<Return>', lambda e: submit())

    tk.Button(root, text="QUIT TO MENU", font=("Courier", 16), bg="#333", fg="white",
              command=lambda: [stopVideo(), homeScreen()]).pack(pady=10)

def checkAnswer(user_answer, feedback_label):
    global score, attempts
    attempts += 1
    correct = num1 + num2 if operation == "+" else num1 - num2

    if user_answer == correct:
        if attempts == 1:
            score += 10
            feedback_label.config(text="CORRECT! +10 points", fg="#00ff00")
        else:
            score += 5
            feedback_label.config(text="Correct on 2nd try! +5 points", fg="yellow")
        root.after(1200, nextQuestion)
    else:
        if attempts == 1:
            feedback_label.config(text="Wrong! Try again...", fg="red")
        else:
            feedback_label.config(text=f"Out of tries! Answer was {correct}", fg="red")
            root.after(2000, nextQuestion)

# ==================== RESULTS SCREEN ====================
def displayResults():
    stopVideo()
    clearWindow()
    setBackground()
    addCloseButton()

    tk.Label(root, text="QUIZ COMPLETE", fg="red", bg="black",
             font=("Chiller", 70, "bold")).pack(pady=60)

    tk.Label(root, text=f"Final Score: {score}/100", fg="white", bg="black",
             font=("Courier", 40)).pack(pady=30)

    if score >= 90:
        result = "LEGENDARY SURVIVOR"
        color = "#00ff00"
    elif score >= 70:
        result = "YOU SURVIVED... barely"
        color = "yellow"
    else:
        result = "THE GHOST FOUND YOU"
        color = "red"

    msg = tk.Label(root, text=result, fg=color, bg="black",
                   font=("Chiller", 50, "bold"))
    msg.pack(pady=50)

    if score < 70:
        def flash():
            root.config(bg="red" if root.cget("bg") == "black" else "black")
            root.after(250, flash)
        root.after(500, flash)

    tk.Button(root, text="PLAY AGAIN", font=("Courier", 24), bg="#222", fg="white",
              width=15, height=2, command=homeScreen).pack(pady=30)
    tk.Button(root, text="EXIT", font=("Courier", 24), bg="darkred", fg="white",
              width=15, height=2, command=root.destroy).pack(pady=10)

# ==================== START THE GAME ====================
homeScreen()
root.mainloop()