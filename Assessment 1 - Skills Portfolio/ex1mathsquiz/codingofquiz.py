import tkinter as tk
import random
from PIL import Image, ImageTk
import cv2

# Survive the Ghost's Quiz(I made the math quiz look like a horror game)

root = tk.Tk()
root.title("Survive the Ghost's Quiz")
root.attributes("-fullscreen", True)
root.configure(bg='black')
root.bind("<Escape>", lambda e: root.destroy())  # press esc to quit anytime

# global variables i need throughout the game
diff = None
my_score = 0
q_num = 0
n1, n2, op = 0, 0, "+"
tries = 0

# for the background video
cap = None
video_lbl = None
after_thingy = None


def delete_everything():
    # clears the whole screen when changing pages
    for widget in root.winfo_children():
        widget.destroy()


def put_scary_picture():
    # static scary image for menu screens
    try:
        path = r"Assessment 1 - Skills Portfolio\ex1mathsquiz\scarybg.jpg"
        img = Image.open(path)
        img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
        photo = ImageTk.PhotoImage(img)
        bg = tk.Label(root, image=photo)
        bg.image = photo  # important or image disappears
        bg.place(x=0, y=0)
    except:
        root.config(bg="black")  # fallback if image not found


def play_spooky_video():
    # plays the looping scary video during quiz
    global cap, video_lbl, after_thingy
    stop_spooky_video()

    video_file = r"Assessment 1 - Skills Portfolio\ex1mathsquiz\scarybg2.mp4"
    cap = cv2.VideoCapture(video_file)

    if not cap.isOpened():
        return

    video_lbl = tk.Label(root)
    video_lbl.place(x=0, y=0, relwidth=1, relheight=1)

    def update_frame():
        global after_thingy
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # loop video
            ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (root.winfo_screenwidth(), root.winfo_screenheight()))
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
            video_lbl.imgtk = imgtk
            video_lbl.configure(image=imgtk)

        after_thingy = root.after(33, update_frame)

    root.after(33, update_frame)


def stop_spooky_video():
    # stops video when going back to menu
    global after_thingy, cap, video_lbl
    try:
        if after_thingy:
            root.after_cancel(after_thingy)
        if cap:
            cap.release()
        if video_lbl:
            video_lbl.destroy()
    except:
        pass


def little_x_button():
    # close button top right
    btn = tk.Button(root, text="X", font=("Courier", 20, "bold"),
                    bg="darkred", fg="white", command=root.destroy,
                    bd=0, cursor="hand2")
    btn.place(relx=0.98, rely=0.02, anchor="ne")


# meny screens
def main_menu():
    delete_everything()
    stop_spooky_video()
    put_scary_picture()
    little_x_button()

    tk.Label(root, text="SURVIVE THE GHOST'S QUIZ",
             font=("Chiller", 72, "bold"), fg="#ff0000").pack(pady=150)

    tk.Button(root, text="START GAME", font=("Courier",32), bg="red", fg="white",
              width=20, height=2, command=choose_diff).pack(pady=30)
    tk.Button(root, text="INSTRUCTIONS", font=("Courier",28), bg="#222", fg="white",
              width=20, height=2, command=instructions).pack(pady=15)
    tk.Button(root, text="EXIT", font=("Courier",28), bg="darkred", fg="white",
              width=20, height=2, command=root.destroy).pack(pady=15)


def instructions():
    delete_everything()
    put_scary_picture()
    little_x_button()

    tk.Label(root, text="HOW TO SURVIVE", font=("Chiller",80,"bold"), fg="red").pack(pady=80)

    rules = """• Choose your difficulty
• Answer 10 math questions
• First try correct = +10 points
• Second try correct = +5 points
• Need 70+ points to survive
• Fail and... well, good luck"""

    tk.Label(root, text=rules, font=("Courier",24), fg="#cccccc", justify="left").pack(pady=60)
    tk.Button(root, text="BACK", font=("Courier",24), bg="#444", fg="white", command=main_menu).pack(pady=80)


def choose_diff():
    delete_everything()
    put_scary_picture()
    little_x_button()

    tk.Label(root, text="SELECT DIFFICULTY", font=("Chiller",65,"bold"), fg="red").pack(pady=120)

    tk.Button(root, text="EASY", font=("Courier",34), bg="green4", fg="white",
              command=lambda: start_quiz("easy")).pack(pady=25)
    tk.Button(root, text="MODERATE", font=("Courier",34), bg="#8B8000", fg="white",
              command=lambda: start_quiz("moderate")).pack(pady=25)
    tk.Button(root, text="ADVANCED", font=("Courier",34), bg="darkred", fg="white",
              command=lambda: start_quiz("advanced")).pack(pady=25)

    tk.Button(root, text="BACK", font=("Courier",20), bg="#333", fg="white", command=main_menu).pack(pady=90)


# quiz logic
def get_two_numbers(level):
    if level == "easy":
        return random.randint(1,10), random.randint(1,10)
    elif level == "moderate":
        return random.randint(10,99), random.randint(10,99)
    else:
        return random.randint(100,999), random.randint(10,999)


def plus_or_minus():
    return random.choice(["+", "-"])


def start_quiz(level):
    global diff, my_score, q_num
    diff = level
    my_score = 0
    q_num = 0
    next_question()

def next_question():
    global n1, n2, op, tries, q_num

    if q_num >= 10:
        end_screen()
        return

    delete_everything()
    play_spooky_video()
    little_x_button()

    q_num += 1
    tries = 0

    n1, n2 = get_two_numbers(diff)
    op = plus_or_minus()

    # dark overlay so we can actually read the question
    overlay = tk.Frame(root, bg="#0a0a0a")
    overlay.place(relwidth=1, relheight=1)
    overlay.lower()

    # question counter
    tk.Label(root, text=f"Question {q_num}/10", font=("Courier",34,"bold"),
             fg="#ff4444", bg="#0a0a0a").place(relx=0.5, rely=0.09, anchor="center")

    # main question - big white text on black background
    problem = f"{n1} {op} {n2} = ?"
    tk.Label(root, text=problem, font=("Courier",92,"bold"),
             fg="white", bg="#000000", relief="raised", bd=12).place(relx=0.5, rely=0.4, anchor="center")

    # answer box
    entry = tk.Entry(root, font=("Courier",48), width=11, justify="center",
                     bg="#111111", fg="white", insertbackground="white", bd=8)
    entry.place(relx=0.5, rely=0.58, anchor="center")
    entry.focus()

    # feedback text
    feedback = tk.Label(root, text="", font=("Courier",28), fg="#ffff99", bg="#0a0a0a")
    feedback.place(relx=0.5, rely=0.68, anchor="center")

    def submit_answer():
        try:
            ans = int(entry.get())
            check_answer(ans, feedback)
        except:
            feedback.config(text="Please type a number", fg="#ff6666")

    # submit button
    tk.Button(root, text="SUBMIT", font=("Courier",32,"bold"),
              bg="#990000", fg="white", command=submit_answer).place(relx=0.5, rely=0.79, anchor="center")

    root.bind("<Return>", lambda e: submit_answer())

    # back to menu button
    tk.Button(root, text="Back to Menu", font=("Courier",18), bg="#222", fg="#aaa",
              command=lambda: [stop_spooky_video(), main_menu()]).place(relx=0.5, rely=0.92, anchor="center")


def check_answer(user_answer, feedback_label):
    global my_score, tries
    tries += 1
    correct = n1 + n2 if op == "+" else n1 - n2

    if user_answer == correct:
        if tries == 1:
            my_score += 10
            feedback_label.config(text="CORRECT! +10 points", fg="#00ff00")
        else:
            my_score += 5
            feedback_label.config(text="Correct on 2nd try (+5)", fg="yellow")
        root.after(1500, next_question)
    else:
        if tries == 1:
            feedback_label.config(text="Wrong - try again", fg="red")
        else:
            feedback_label.config(text=f"No more tries! Answer: {correct}", fg="red")
            root.after(2000, next_question)


# ending the screen
def end_screen():
    stop_spooky_video()
    delete_everything()
    put_scary_picture()
    little_x_button()

    tk.Label(root, text="QUIZ COMPLETE", font=("Chiller",80,"bold"), fg="red").pack(pady=70)
    tk.Label(root, text=f"Score: {my_score}/100", font=("Courier",50), fg="white").pack(pady=40)

    if my_score >= 90:
        msg, col = "LEGENDARY SURVIVOR", "#00ff00"
    elif my_score >= 70:
        msg, col = "You survived...", "yellow"
    else:
        msg, col = "THE GHOST FOUND YOU", "red"

    tk.Label(root, text=msg, font=("Chiller",60,"bold"), fg=col).pack(pady=60)

    if my_score < 70:
        def flash_red():
            root.config(bg="red" if root.cget("bg") == "black" else "black")
            root.after(300, flash_red)
        root.after(500, flash_red)

    tk.Button(root, text="PLAY AGAIN", font=("Courier",28), bg="#222", fg="white",
              command=main_menu).pack(pady=40)
    tk.Button(root, text="EXIT", font=("Courier",28), bg="darkred", fg="white",
              command=root.destroy).pack(pady=10)


# starting the game
main_menu()
root.mainloop()