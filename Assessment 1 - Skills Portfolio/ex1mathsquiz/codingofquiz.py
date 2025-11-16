from PIL import Image, ImageTk
import tkinter as tk
import tkinter as tk
import random

# main window stuff
root = tk.Tk()
root.title("Survive the Ghost's Quiz")
root.attributes("-fullscreen", True)   # yeah its fullscreen cuz its cooler
root.configure(bg="black")
root.bind("<Escape>", lambda x: root.destroy())  # esc to run away fast

# all the variables i need to remember
score = 0
question_count = 0
level = ""
n1 = 0
n2 = 0
sign = ""
tries = 0

# removes everything when i change screens
def clear_all():
    for widget in root.winfo_children():
        widget.pack_forget()
        widget.grid_forget()
        widget.place_forget()
        widget.destroy()

# little X button up top cuz sometimes esc doesnt work
def close_btn():
    btn = tk.Button(root, text="X", font=("Arial", 22, "bold"),
                    bg="darkred", fg="white", bd=0, relief="flat",
                    command=root.destroy)
    btn.place(relx=0.98, rely=0.02, anchor="ne")

# first screen you see


def home():
    global bg_img

    # correct long relative path from your working directory
    img_path = (r"Assessment 1 - Skills Portfolio\ex1mathsquiz\scarybg.jpg")

    # load JPG using Pillow
    img = Image.open(img_path)
    bg_img = ImageTk.PhotoImage(img)

    # display image as background
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # text / buttons on top of background
    tk.Label(root, text="SURVIVE THE", font=("Chiller", 85, "bold"),
             fg="red", bg="#00000000").pack(pady=120)

    tk.Label(root, text="GHOST'S QUIZ", font=("Chiller", 85, "bold"),
             fg="red", bg="#00000000").pack()



# instructions screen
def how_to():
    clear_all()
    close_btn()

    tk.Label(root, text="HOW TO NOT DIE", font=("Chiller", 70),
             fg="red", bg="black").pack(pady=80)

    # UPDATED INSTRUCTIONS TEXT
    text = """1. Choose your difficulty: Easy, Medium, or Hard.
2. You must answer 10 math problems chosen by the ghost.
3. Only + and - questions... for now.
4. First try correct = +10 points.
5. Second try correct = +5 points.
6. Two wrong tries and the ghost reveals the answer.
7. You must score AT LEAST 70/100 to survive.
8. If you fail... the ghost collects your soul.
"""

    tk.Label(root, text=text, font=("Courier", 22), fg="#cccccc",
             bg="black", justify="left").pack(pady=50)

    tk.Button(root, text="BACK", font=("Courier", 22), bg="#444", fg="white",
              command=home).pack(pady=60)

# choose difficulty screen
def pick_level():
    clear_all()
    close_btn()

    tk.Label(root, text="PICK YOUR FATE", font=("Chiller", 65),
             fg="red", bg="black").pack(pady=100)

    tk.Button(root, text="EASY", font=("Courier", 30), bg="green", fg="black",
              width=20, height=2, command=lambda: start("easy")).pack(pady=25)
    tk.Button(root, text="MEDIUM", font=("Courier", 30), bg="orange", fg="black",
              width=20, height=2, command=lambda: start("medium")).pack(pady=25)
    tk.Button(root, text="HARD", font=("Courier", 30), bg="red", fg="white",
              width=20, height=2, command=lambda: start("hard")).pack(pady=25)

    tk.Button(root, text="back", font=("Courier", 18), bg="#555", fg="white",
              command=home).pack(pady=70)

# numbers depending on difficulty
def make_numbers(diff):
    if diff == "easy":
        return random.randint(1, 12), random.randint(1, 12)
    elif diff == "medium":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(100, 999), random.randint(100, 999)

# actually start the quiz
def start(diff):
    global level, score, question_count
    level = diff
    score = 0
    question_count = 0
    next_q()

# show one question
def next_q():
    global n1, n2, sign, tries, question_count

    clear_all()
    close_btn()

    if question_count >= 10:
        game_over()
        return

    question_count += 1
    tries = 0

    n1, n2 = make_numbers(level)
    sign = random.choice(["+", "-"])

    tk.Label(root, text=f"Question {question_count}/10", font=("Courier", 28),
             fg="red", bg="black").pack(pady=40)

    tk.Label(root, text=f"{n1} {sign} {n2} =", font=("Courier", 55, "bold"),
             fg="white", bg="black").pack(pady=100)

    box = tk.Entry(root, font=("Courier", 35), justify="center", width=10)
    box.pack(pady=20)
    box.focus()

    msg = tk.Label(root, text="", font=("Courier", 24), fg="yellow", bg="black")
    msg.pack(pady=20)

    def check_answer():
        nonlocal msg
        try:
            ans = int(box.get())
        except:
            msg.config(text="type a number dummy", fg="orange")
            return

        correct = n1 + n2 if sign == "+" else n1 - n2
        global score, tries
        tries += 1

        if ans == correct:
            if tries == 1:
                score += 10
                msg.config(text="nice +10", fg="lime")
            else:
                score += 5
                msg.config(text="ok but 2nd try +5", fg="yellow")
            root.after(1300, next_q)
        else:
            if tries == 1:
                msg.config(text="wrong lol try again", fg="red")
            else:
                msg.config(text=f"nope it was {correct}", fg="red")
                root.after(1800, next_q)

    tk.Button(root, text="ANSWER", font=("Courier", 28), bg="red", fg="white",
              command=check_answer).pack(pady=20)

    box.bind("<Return>", lambda e: check_answer())

    tk.Button(root, text="i give up", font=("Courier", 16), bg="#333", fg="white",
              command=pick_level).pack(pady=10)

# end screen
def game_over():
    clear_all()
    close_btn()

    tk.Label(root, text="GAME OVER", font=("Chiller", 90),
             fg="red", bg="black").pack(pady=80)

    tk.Label(root, text=f"Score: {score}/100", font=("Courier", 40),
             fg="white", bg="black").pack(pady=30)

    if score >= 70:
        tk.Label(root, text="you lived... barely", font=("Chiller", 50),
                 fg="green", bg="black").pack(pady=80)
    else:
        tk.Label(root, text="GHOST GOT YOU", font=("Chiller", 70, "bold"),
                 fg="red", bg="black").pack(pady=80)

        # scary flashing when you die
        def scary_flash():
            if root.cget("bg") == "black":
                root.config(bg="#330000")
            else:
                root.config(bg="black")
            root.after(200, scary_flash)
        scary_flash()

    tk.Button(root, text="PLAY AGAIN", font=("Courier", 28), bg="#222", fg="white",
              command=home).pack(pady=50)
    tk.Button(root, text="QUIT", font=("Courier", 28), bg="darkred", fg="white",
              command=root.destroy).pack(pady=20)

# start everything
home()
root.mainloop()
