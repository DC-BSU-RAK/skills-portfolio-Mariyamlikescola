import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import cv2

# Setting up the main window for the game to be more understandable
root = tk.Tk()
root.title("Survive the Ghost's Quiz")
# I want this to feel immersive, so I madethe window fill the screen
root.attributes("-fullscreen", True)
root.config(bg="black")

# Letting the player leave the game quickly by pressing Escape
root.bind("<Escape>", lambda e: root.destroy())

# Keeping track of the game state with a few global variables
difficulty = None      # The difficulty the player chose
score = 0             
question_number = 0      
num1, num2, operation = 0, 0, "+"  
attempts = 0            # How many tries the current question took

#remove everything on the screen so I can load a new screen quickly
def clearWindow():
    for widget in root.winfo_children():
        widget.destroy()

        # -------------------- BACKGROUND IMAGE OR VIDEO FUNCTIONS --------------------

# (Optional) still-image background for non-quiz screens
def setBackground():
    global bg_label, bg_image
    image = Image.open(r"Assessment 1 - Skills Portfolio\ex1mathsquiz\scarybg.jpg")   # change file name if needed
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    image = image.resize((screen_width, screen_height))
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Video background for the quiz
def playVideoBackground(video_path):
    global video_capture, video_label, update_video
    video_capture = cv2.VideoCapture(video_path)

    video_label = tk.Label(root)
    video_label.place(x=0, y=0, relwidth=1, relheight=1)

    def update_frame():
        ret, frame = video_capture.read()
        if not ret:
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video_capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (root.winfo_screenwidth(), root.winfo_screenheight()))
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        video_label.img = img
        video_label.config(image=img)
        global update_video
        update_video = root.after(33, update_frame)  # ~30 FPS
    update_frame()

# Stop the video (for when the quiz ends)
def stopVideo():
    global video_capture, update_video
    try:
        root.after_cancel(update_video)
        video_capture.release()
        video_label.destroy()
    except:
        pass



# Add a spooky background image across all screens
def setBackground():
    global bg_label, bg_image
    # Load and resize image to fit screen
    image = Image.open(r"Assessment 1 - Skills Portfolio\ex1mathsquiz\scarybg.jpg")   # change name if needed
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    image = image.resize((screen_width, screen_height))
    bg_image = ImageTk.PhotoImage(image)
    
    # Place as background label (behind all widgets)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


#adding a small close button at the top-right so players can quit easily
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


# This is where players pick what they want to do: start, read instructions, or quit
def homeScreen():
    clearWindow()
    setBackground()
    addCloseButton()

    tk.Label(root, text="SURVIVE THE GHOST'S QUIZ", fg="red", bg="black",
             font=("Chiller", 60, "bold")).pack(pady=80)

    tk.Button(root, text="START GAME", font=("Courier", 24), bg="red", fg="white",
              width=20, command=difficultyMenu).pack(pady=20)

    tk.Button(root, text="INSTRUCTIONS", font=("Courier", 24), bg="#222", fg="white",
              width=20, command=instructionsPage).pack(pady=20)

    tk.Button(root, text="EXIT", font=("Courier", 24), bg="darkred", fg="white",
              width=20, command=root.destroy).pack(pady=20)

# Here I explaied the rules in a concise, friendly way
def instructionsPage():
    clearWindow()
    setBackground()
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

    # A way back to the home screen
    tk.Button(root, text="BACK", font=("Courier", 18), bg="#333", fg="white",
              width=15, command=homeScreen).pack(pady=30)


# Letting the player pick Easy, Moderate, or Advanced
def difficultyMenu():
    clearWindow()
    setBackground()
    addCloseButton()

    tk.Label(root, text="CHOOSE YOUR DIFFICULTY", fg="red", bg="black",
             font=("Chiller", 60, "bold")).pack(pady=40)

    # The three difficulty options
    tk.Button(root, text="EASY", font=("Courier", 24), bg="#222", fg="white",
              width=20, command=lambda: startQuiz("easy")).pack(pady=20)
    tk.Button(root, text="MODERATE", font=("Courier", 24), bg="#222", fg="white",
              width=20, command=lambda: startQuiz("moderate")).pack(pady=20)
    tk.Button(root, text="ADVANCED", font=("Courier", 24), bg="#222", fg="white",
              width=20, command=lambda: startQuiz("advanced")).pack(pady=20)

    # A back option if they change their mind
    tk.Button(root, text="BACK", font=("Courier", 18), bg="#333", fg="white",
              width=15, command=homeScreen).pack(pady=40)


# I generated two numbers, their size depends on the chosen difficulty
def randomInt(level):
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        # Advanced is the hard mode
        return random.randint(1000, 9999), random.randint(1000, 9999)

# Deciding whether the current question is addition or subtraction
def decideOperation():
    return random.choice(["+", "-"])

#QUIZ
# This resets the game state and kicks off the first question
def startQuiz(level):
    global difficulty, score, question_number
    difficulty = level
    score = 0
    question_number = 0
    nextQuestion()

# Building the next math problem screen
def nextQuestion():
    global num1, num2, operation, attempts, question_number
    clearWindow()
    playVideoBackground(r"Assessment 1 - Skills Portfolio\ex1mathsquiz\scarybg2.mp4")  # your video filename here
    addCloseButton()


    # If we've already asked 10 questions, end the quiz
    if question_number >= 10:
        displayResults()
        return

    question_number += 1
    attempts = 0

    # Get a fresh problem
    num1, num2 = randomInt(difficulty)
    operation = decideOperation()

    # A tiny header to show progress
    tk.Label(root, text=f"Question {question_number}/10", fg="red",
             bg="black", font=("Courier", 24)).pack(pady=10)

    # The actual math problem the player must solve
    tk.Label(root, text=f"{num1} {operation} {num2} = ?", fg="white",
             bg="black", font=("Courier", 40, "bold")).pack(pady=40)

    # Where the player types their answer
    answer_entry = tk.Entry(root, font=("Courier", 28), justify="center")
    answer_entry.pack(pady=20)

    # A space to give feedback like "Correct!" or "Try again"
    feedback = tk.Label(root, text="", fg="red", bg="black", font=("Courier", 20))
    feedback.pack(pady=10)

    # What happens when the player hits Submit
    def submit():
        nonlocal feedback
        user_answer = answer_entry.get()
        # Quick check: ensure this is a number (could be negative)
        if not user_answer.lstrip("-").isdigit():
            feedback.config(text="Enter a valid number!", fg="orange")
            return
        isCorrect(int(user_answer), feedback)

    # Adding the  submit button
    tk.Button(root, text="SUBMIT", font=("Courier", 22), bg="red", fg="white",
              width=15, command=submit).pack(pady=20)

    # A back option if they want to rethink the difficulty
    tk.Button(root, text="BACK", font=("Courier", 18), bg="#333", fg="white",
              width=10, command=difficultyMenu).pack(pady=10)


# Compare the player's answer to the correct one and move forward
def isCorrect(user_answer, feedback_label):
    global score, attempts
    attempts += 1

    correct_answer = num1 + num2 if operation == "+" else num1 - num2

    if user_answer == correct_answer:
        if attempts == 1:
            score += 10  # first try bonus
            feedback_label.config(text="Correct! +10 points", fg="green")
        else:
            score += 5   # second attempt earns a smaller prize
            feedback_label.config(text="Correct (2nd try)! +5 points", fg="yellow")

        # Waiting a moment, then move to the next question
        root.after(1000, nextQuestion)
    else:
        if attempts == 1:
            feedback_label.config(text="Wrong... try again!", fg="red")
        else:
            feedback_label.config(text=f"Wrong again! The ghost laughs...\nAnswer was {correct_answer}.", fg="red")
            root.after(1500, nextQuestion)

# Showing results and a little ghost-themed ending based on score
def displayResults():
    stopVideo()
    clearWindow()
    setBackground()   # optional – puts your static background back
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

    # A little extra flair depending on how well the user did
    if score >= 70:
        msg = "You survived… for now."
        color = "green"
        tk.Label(root, text=msg, fg=color, bg="black",
                 font=("Chiller", 40, "bold")).pack(pady=50)
    else:
        # If the score was too low, the ghost tracks you down visually
        msg_label = tk.Label(root, text="THE GHOST FOUND YOU 💀", fg="red",
                             bg="black", font=("Chiller", 50, "bold"))
        msg_label.pack(pady=50)

        # Quick flashing effect to amp up the spooky vibe
        def flash_bg():
            current = root.cget("bg")
            root.config(bg="darkred" if current == "black" else "black")
            root.after(300, flash_bg)

        flash_bg()

    # Options after finishing
    tk.Button(root, text="PLAY AGAIN", font=("Courier", 20), bg="#222", fg="white",
              width=15, command=homeScreen).pack(pady=20)
    tk.Button(root, text="EXIT", font=("Courier", 20), bg="red", fg="white",
              width=15, command=root.destroy).pack(pady=10)

homeScreen()
root.mainloop()
