import tkinter as tk
from tkinter import ttk
import os

class StudentManager:
    def __init__(self):
        # Main application window setup
        self.root = tk.Tk()
        self.root.title("Student Manager")
        self.root.geometry("1350x780")
        self.root.configure(bg="#fff0f8")
# kept the color scheme in a very pinkish way since it is my favorite color:)
        self.main_pink   = "#ff69b4"
        self.button_pink = "#ff1493"
        self.bg_color    = "#fff0f8"
        self.text_pink   = "#d81b60"

        self.students = [] # Will hold all student records
        self.filepath = self.find_the_file()# Locate the data file relative to script

        self.load_all_students()
        self.make_the_gui()

    def find_the_file(self):
        where = os.path.dirname(os.path.abspath(__file__))
        resources = os.path.join(where, "..", "A1 - Resources")
        full = os.path.join(resources, "studentMarks.txt")
        return os.path.normpath(full)

    def load_all_students(self):
        # Loading student records from the text file
        if not os.path.exists(self.filepath):
            self.pink_message("oh nooo", f"can't find the file here:\n{self.filepath}", error=True)
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if not lines:
                return

            total = int(lines[0].strip())
            self.students = []

# Reading exactly the number of students specified in the first line
            for line in lines[1:1+total]:
                bits = line.strip().split(",")
                if len(bits) != 6:
                    continue

                code = int(bits[0])
                name = bits[1].strip()
                cw1 = int(bits[2])
                cw2 = int(bits[3])
                cw3 = int(bits[4])
                exam = int(bits[5])

                coursework = cw1 + cw2 + cw3
                percent = round((coursework + exam) / 160 * 100, 2)
                grade = "A" if percent >= 70 else "B" if percent >= 60 else "C" if percent >= 50 else "D" if percent >= 40 else "F"

                kid = {
                    "code": code, "name": name,
                    "cw1": cw1, "cw2": cw2, "cw3": cw3,
                    "exam": exam, "coursework": coursework,
                    "percentage": percent, "grade": grade
                }
                self.students.append(kid)

        except Exception as e:
            self.pink_message("help", f"something broke:\n{e}", error=True)

    def save_back_to_file(self):
        # Writing all current student records back to the original file
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(f"{len(self.students)}\n")
                for s in self.students:
                    f.write(f"{s['code']},{s['name']},{s['cw1']},{s['cw2']},{s['cw3']},{s['exam']}\n")
            self.pink_message("saved!", "everything is safe now")
        except:
            self.pink_message("NOOO", "couldn't save... close excel maybe??", error=True)

    #designing the popups so they don't look like every casual popup
    def create_pink_dialog(self, title, message, options=None):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("480x340")
        popup.configure(bg="#fff0f8")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
# Centering the dialog over the main window
        popup.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 480) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 340) // 2
        popup.geometry(f"+{x}+{y}")

        tk.Label(popup, text=title, font=("Comic Sans MS", 20, "bold"),
                 bg="#fff0f8", fg=self.text_pink).pack(pady=25)

        tk.Label(popup, text=message, font=("Arial", 12), bg="#fff0f8", fg="#555",
                 wraplength=420, justify="center").pack(pady=10)

        result = {"value": None}
        def close(val):
            result["value"] = val
            popup.destroy()

        if options is None:
            entry = tk.Entry(popup, font=("Arial", 14), width=28, justify="center",
                             relief="flat", highlightthickness=2, highlightcolor=self.main_pink)
            entry.pack(pady=20)
            entry.focus()

            def ok():
                close(entry.get().strip() or None)
            entry.bind("<Return>", lambda e: ok())

            btns = tk.Frame(popup, bg="#fff0f8")
            btns.pack(pady=10)
            tk.Button(btns, text="OK", font=("Arial", 11, "bold"), bg=self.button_pink,
                      fg="white", width=10, command=ok).pack(side="left", padx=12)
            tk.Button(btns, text="Cancel", font=("Arial", 11), bg="#ffb6c1",
                      fg="#333", width=10, command=lambda: close(None)).pack(side="right", padx=12)
        else:
            for val, txt in options:
                tk.Button(popup, text=txt, font=("Arial", 11, "bold"),
                          bg=self.main_pink, fg="white", width=30, height=2,
                          command=lambda v=val: close(v)).pack(pady=7)

        popup.wait_window()
        return result["value"]

    def pink_message(self, title, message, error=False):
        box = tk.Toplevel(self.root)
        box.title(title)
        box.geometry("420x240")
        box.configure(bg="#fff0f8")
        box.resizable(False, False)

# putting slight offset from center for visual comfort
        x = self.root.winfo_x() + 460
        y = self.root.winfo_y() + 250
        box.geometry(f"+{x}+{y}")

        color = "#c51162" if error else self.text_pink
        tk.Label(box, text=title, font=("Comic Sans MS", 18, "bold"),
                 bg="#fff0f8", fg=color).pack(pady=25)
        tk.Label(box, text=message, font=("Arial", 12), bg="#fff0f8", fg="#555",
                 wraplength=380, justify="center").pack(pady=10)

        tk.Button(box, text="okay okay", font=("Arial", 11, "bold"), bg=self.button_pink,
                  fg="white", width=14, command=box.destroy).pack(pady=20)

    def make_the_gui(self):
        # Configuring Treeview appearance
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background=self.button_pink, foreground="white")
        style.configure("Treeview", rowheight=38, background="white")
        style.map("Treeview", background=[("selected", "#ff99cc")])

# Adding a sidebar with navigation buttons
        sidebar = tk.Frame(self.root, bg=self.main_pink, width=370)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="my pink manager", font=("Comic Sans MS", 24, "bold"),
                 bg=self.main_pink, fg="white", pady=35).pack()

        buttons = [
            ("View everyone", self.show_everybody),
            ("Search any student", self.search_student),
            ("Highest overall mark", self.show_the_best),
            ("Lowest overall mark", self.show_the_lowest),
            ("Sort student records", self.sort_them),
            ("add new student", self.add_new_kid),
            ("delete student", self.remove_kid),
            ("update marks", self.edit_kid),
        ]

        for txt, cmd in buttons:
            b = tk.Button(sidebar, text=txt.upper(), font=("Arial", 12, "bold"),
                          bg=self.button_pink, fg="white", height=2, bd=0,
                          activebackground="#ff69b4", command=cmd)
            b.pack(fill="x", padx=40, pady=10)

    # Main content area with table
        main = tk.Frame(self.root, bg=self.bg_color)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        cols = ("Code", "Name", "Coursework", "Exam", "Overall %", "Grade")
        self.table = ttk.Treeview(main, columns=cols, show="headings")

        for c in cols:
            self.table.heading(c, text=c)
            self.table.column(c, width=150, anchor="center")
        self.table.column("Name", width=320, anchor="w")
        self.table.pack(fill="both", expand=True)

        # Status bar at the bottom
        self.status_label = tk.Label(main, text="heyy pick something",
                                     font=("Arial", 12, "italic"), bg=self.bg_color, fg="#777")
        self.status_label.pack(pady=15)

    def empty_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

    def put_student_in_table(self, student):
        self.table.insert("", "end", values=(
            student["code"], student["name"],
            f"{student['coursework']}/60", f"{student['exam']}/100",
            f"{student['percentage']}%", student["grade"]
        ))

    def show_everybody(self):
        self.empty_table()
        for s in self.students:
            self.put_student_in_table(s)
        if self.students:
            avg = sum(s["percentage"] for s in self.students) / len(self.students)
            self.status_label.config(text=f"{len(self.students)} kids • avg {avg:.1f}%")

    def search_student(self):
        q = self.create_pink_dialog("Search Student", "Enter name or code:")
        if not q:
            return
        q = q.lower()
        matches = [s for s in self.students if q in str(s["code"]) or q in s["name"].lower()]
        self.empty_table()
        for m in matches:
            self.put_student_in_table(m)
        self.status_label.config(text=f"found {len(matches)}" if matches else "nobody")

    def show_the_best(self):
        if not self.students: return
        best = max(self.students, key=lambda x: x["percentage"])
        self.empty_table()
        self.put_student_in_table(best)
        self.status_label.config(text=f"Star Student: {best['name']} – {best['percentage']}%")

    def show_the_lowest(self):
        if not self.students: return
        low = min(self.students, key=lambda x: x["percentage"])
        self.empty_table()
        self.put_student_in_table(low)
        self.status_label.config(text=f"{low['name']}  – {low['percentage']}%")

    def sort_them(self):
        if not self.students:
            self.pink_message("oops", "no students to sort yet!")
            return

    
        choice = self.create_pink_dialog(
            "sort by what?",
            "choose how to sort the class:",
            options=[
                ( ("name", False),       "Name (A → Z)" ),
                ( ("name", True),        "Name (Z → A)" ),
                ( ("code", False),       "Code (low → high)" ),
                ( ("code", True),        "Code (high → low)" ),
                ( ("percentage", True),  "Percentage (best → worst)" ),
                ( ("percentage", False), "Percentage (worst → best)" ),
                ( ("grade", False),      "Grade (A → F)" ),
                ( ("grade", True),       "Grade (F → A)" ),
            ]
        )
        if not choice:
            return 

        field, descending = choice

        if field == "name":
            self.students.sort(key=lambda x: x["name"].lower(), reverse=descending)
        elif field == "code":
            self.students.sort(key=lambda x: x["code"], reverse=descending)
        elif field == "percentage":
            self.students.sort(key=lambda x: x["percentage"], reverse=descending)
        elif field == "grade":
            order = {"A":0, "B":1, "C":2, "D":3, "F":4}
            self.students.sort(key=lambda x: order[x["grade"]], reverse=descending)

        self.show_everybody()
        direction = "Z→A / high→low / worst→best" if descending else "A→Z / low→high / best→worst"
        self.status_label.config(text=f"sorted by {field} – {direction}")

    # FIXED – proper indentation, no semicolons
    def add_new_kid(self):
        code_text = self.create_pink_dialog("new student!", "student code (1000-9999):")
        if not code_text or not code_text.isdigit():
            return
        code = int(code_text)
        if any(s["code"] == code for s in self.students):
            self.pink_message("nope", "that code is taken!", error=True)
            return

        name = self.create_pink_dialog("name?", "full name please:")
        if not name:
            return

        def get_mark(what, maxx):
            while True:
                m = self.create_pink_dialog(what, f"mark (0-{maxx}):")
                if m is None:
                    return None
                if m.isdigit() and 0 <= int(m) <= maxx:
                    return int(m)
                self.pink_message("oops", f"only numbers 0-{maxx} please")

        cw1 = get_mark("coursework 1", 20)
        if cw1 is None: return
        cw2 = get_mark("coursework 2", 20)
        if cw2 is None: return
        cw3 = get_mark("coursework 3", 20)
        if cw3 is None: return
        exam = get_mark("exam", 100)
        if exam is None: return

        coursework = cw1 + cw2 + cw3
        percent = round((coursework + exam) / 160 * 100, 2)
        grade = "A" if percent >= 70 else "B" if percent >= 60 else "C" if percent >= 50 else "D" if percent >= 40 else "F"

        new_kid = {
            "code": code, "name": name.strip(),
            "cw1": cw1, "cw2": cw2, "cw3": cw3,
            "exam": exam, "coursework": coursework,
            "percentage": percent, "grade": grade
        }

        self.students.append(new_kid)
        self.save_back_to_file()
        self.show_everybody()
        self.pink_message("welcome!!", f"{name} is here")

    def remove_kid(self):
        who = self.create_pink_dialog("Delete Student", "name or code to delete:")
        if not who: return
        who = who.lower()
        target = next((s for s in self.students if who in str(s["code"]) or who in s["name"].lower()), None)
        if not target:
            self.pink_message("not found", "No student matches the search.")
            return

        sure = self.create_pink_dialog("really?", f"delete {target['name']} forever?",
                                      options=[(True, "yes"), (False, "Cancel")])
        if not sure: return

        self.students.remove(target)
        self.save_back_to_file()
        self.show_everybody()
        self.pink_message("done", "Student record has been removed.")

    def edit_kid(self):
        who = self.create_pink_dialog("who to edit?", "name or code:")
        if not who: return
        who = who.lower()
        kid = next((s for s in self.students if who in str(s["code"]) or who in s["name"].lower()), None)
        if not kid:
            self.pink_message("not found", "No matching student found.")
            return

        choice = self.create_pink_dialog("what to change?", "choose:",
            options=[(1,"1 → name"),(2,"2 → cw1"),(3,"3 → cw2"),(4,"4 → cw3"),(5,"5 → exam")])
        if not choice: return

        if choice == 1:
            new = self.create_pink_dialog("new name", "type it:")
            if new: kid["name"] = new.strip()
        elif choice <= 4:
            new = self.create_pink_dialog(f" Update coursework {choice-1}", "new mark (0-20):")
            if new and new.isdigit(): kid[f"cw{choice-1}"] = int(new)
        else:
            new = self.create_pink_dialog("Update exam", "new exam mark (0-100):")
            if new and new.isdigit(): kid["exam"] = int(new)

# Recalculating totals
        kid["coursework"] = kid["cw1"] + kid["cw2"] + kid["cw3"]
        total = kid["coursework"] + kid["exam"]
        kid["percentage"] = round(total/160*100, 2)
        kid["grade"] = "A" if kid["percentage"]>=70 else "B" if kid["percentage"]>=60 else "C" if kid["percentage"]>=50 else "D" if kid["percentage"]>=40 else "F"

        self.save_back_to_file()
        self.show_everybody()
        self.pink_message("Updated!", "all good now")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StudentManager()
    app.run()