import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class StudentManager:
    def __init__(self):
        # main window setup
        self.root = tk.Tk()
        self.root.title("Student Manager - Pink Edition")
        self.root.geometry("1300x750")
        self.root.configure(bg="#fff0f8")

        # my favourite shades of pink
        self.main_pink = "#ff69b4"
        self.button_pink = "#ff1493"
        self.bg_color = "#fff0f8"

        self.students = []  # this will hold all student dictionaries
        self.filepath = self.find_the_file()

        self.load_all_students()
        self.make_the_gui()

    # finds the studentMarks.txt file even if the script is somewhere else
    def find_the_file(self):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        resources = os.path.join(current_folder, "..", "A1 - Resources")
        full_path = os.path.join(resources, "studentMarks.txt")
        return os.path.normpath(full_path)

    # reads the file when the program starts
    def load_all_students(self):
        if not os.path.exists(self.filepath):
            messagebox.showerror("File missing", f"Can't find the file!\nI expected it here:\n{self.filepath}")
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                all_lines = file.readlines()

            if len(all_lines) < 1:
                return

            how_many = int(all_lines[0].strip())
            self.students = []

            # starting from line 1 because line 0 is just the count
            for line in all_lines[1:1+how_many]:
                data = line.strip().split(",")
                if len(data) != 6:
                    continue  

                code = int(data[0])
                name = data[1].strip()
                cw1 = int(data[2])
                cw2 = int(data[3])
                cw3 = int(data[4])
                exam = int(data[5])

                coursework_total = cw1 + cw2 + cw3
                overall = coursework_total + exam
                percentage = round((overall / 160) * 100, 2)

                # grade logic – I always forget the order so I wrote it clearly
                if percentage >= 70:
                    grade = "A"
                elif percentage >= 60:
                    grade = "B"
                elif percentage >= 50:
                    grade = "C"
                elif percentage >= 40:
                    grade = "D"
                else:
                    grade = "F"

                student_dict = {
                    "code": code,
                    "name": name,
                    "cw1": cw1, "cw2": cw2, "cw3": cw3,
                    "exam": exam,
                    "coursework": coursework_total,
                    "percentage": percentage,
                    "grade": grade
                }
                self.students.append(student_dict)

        except Exception as e:
            messagebox.showerror("Oops", f"Something broke while reading the file:\n{e}")

    # writing everything back to the txt file – super important for add/delete/update
    def save_back_to_file(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(f"{len(self.students)}\n")  # first line = number of students
                for s in self.students:
                    f.write(f"{s['code']},{s['name']},{s['cw1']},{s['cw2']},{s['cw3']},{s['exam']}\n")
            messagebox.showinfo("Saved", "All changes saved to studentMarks.txt")
        except:
            messagebox.showerror("Error", "Couldn't save the file. Check permissions?")

    # building the whole interface
    def make_the_gui(self):
        # making the treeview look nice
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background=self.button_pink, foreground="white")
        style.configure("Treeview", rowheight=35)

        # left pink sidebar
        sidebar = tk.Frame(self.root, bg=self.main_pink, width=360)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Student Manager", font=("Arial", 22, "bold"),
                 bg=self.main_pink, fg="white", pady=30).pack()

        # all the buttons
        buttons = [
            ("1. View All Students", self.show_everybody),
            ("2. Search a Student", self.search_student),
            ("3. Highest Score", self.show_the_best),
            ("4. Lowest Score", self.show_the_lowest),
            ("5. Sort Records", self.sort_them),
            ("6. Add New Student", self.add_new_kid),
            ("7. Delete Student", self.remove_kid),
            ("8. Update Student", self.edit_kid),
        ]

        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, font=("Arial", 12, "bold"),
                            bg=self.button_pink, fg="white", height=2, bd=0,
                            activebackground="#ff69b4", command=command)
            btn.pack(fill="x", padx=35, pady=9)

        # right side – where the table lives
        right_frame = tk.Frame(self.root, bg=self.bg_color)
        right_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("Code", "Name", "Coursework", "Exam", "Overall %", "Grade")
        self.table = ttk.Treeview(right_frame, columns=columns, show="headings")

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=150, anchor="center")
        self.table.column("Name", width=300, anchor="w")
        self.table.pack(fill="both", expand=True)

        # little status message at the bottom
        self.status_label = tk.Label(right_frame, text="Ready – pick something from the menu",
                                     font=("Arial", 12, "italic"), bg=self.bg_color, fg="#666")
        self.status_label.pack(pady=12)

    # clears whatever is currently in the table
    def empty_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

    # puts one student into the table
    def put_student_in_table(self, student):
        self.table.insert("", "end", values=(
            student["code"],
            student["name"],
            f"{student['coursework']}/60",
            f"{student['exam']}/100",
            f"{student['percentage']}%",
            student["grade"]
        ))

    # MENU 1 – show everyone
    def show_everybody(self):
        self.empty_table()
        for kid in self.students:
            self.put_student_in_table(kid)

        if self.students:
            average = sum(s["percentage"] for s in self.students) / len(self.students)
            self.status_label.config(text=f"{len(self.students)} students | Class average: {average:.2f}%")

    # MENU 2 – search
    def search_student(self):
        search = simpledialog.askstring("Search", "Type part of name or student code:")
        if not search:
            return

        search = search.lower()
        matches = []
        for s in self.students:
            if search in str(s["code"]) or search in s["name"].lower():
                matches.append(s)

        self.empty_table()
        if matches:
            for m in matches:
                self.put_student_in_table(m)
            self.status_label.config(text=f"Found {len(matches)} student(s)")
        else:
            self.status_label.config(text="Nobody found")
            messagebox.showinfo("Not found", "No student matches that search")

    # MENU 3 & 4 – best and worst
    def show_the_best(self):
        if not self.students:
            return
        best = max(self.students, key=lambda x: x["percentage"])
        self.empty_table()
        self.put_student_in_table(best)
        self.status_label.config(text=f"Best student: {best['name']} – {best['percentage']}%")

    def show_the_lowest(self):
        if not self.students:
            return
        worst = min(self.students, key=lambda x: x["percentage"])
        self.empty_table()
        self.put_student_in_table(worst)
        self.status_label.config(text=f"Lowest: {worst['name']} – {worst['percentage']}%")

    # MENU 5 – sort
    def sort_them(self):
        if not self.students:
            messagebox.showinfo("Empty", "Nothing to sort!")
            return

        what = simpledialog.askstring("Sort", "Sort by: name / code / percentage / grade\nAdd ' desc' for descending")
        if not what:
            return

        descending = "desc" in what.lower()
        field = what.lower().replace(" desc", "").strip()

        if field == "name":
            self.students.sort(key=lambda x: x["name"].lower(), reverse=descending)
        elif field == "code":
            self.students.sort(key=lambda x: x["code"], reverse=descending)
        elif field == "percentage":
            self.students.sort(key=lambda x: x["percentage"], reverse=descending)
        elif field == "grade":
            order = {"A":0, "B":1, "C":2, "D":3, "F":4}
            self.students.sort(key=lambda x: order[x["grade"]], reverse=descending)
        else:
            messagebox.showerror("Nope", "I only know name, code, percentage, grade")
            return

        self.show_everybody()
        direction = "descending" if descending else "ascending"
        self.status_label.config(text=f"Sorted by {field} ({direction})")

    # MENU 6 – add student
    def add_new_kid(self):
        code = simpledialog.askinteger("Code", "Student code (1000-9999):", minvalue=1000, maxvalue=9999)
        if not code:
            return
        if any(s["code"] == code for s in self.students):
            messagebox.showerror("Duplicate", "That code already exists!")
            return

        name = simpledialog.askstring("Name", "Full name:")
        if not name:
            return

        # getting the marks one by one
        cw1 = simpledialog.askinteger("CW1", "Coursework 1 (out of 20):", minvalue=0, maxvalue=20)
        cw2 = simpledialog.askinteger("CW2", "Coursework 2 (out of 20):", minvalue=0, maxvalue=20)
        cw3 = simpledialog.askinteger("CW3", "Coursework 3 (out of 20):", minvalue=0, maxvalue=20)
        exam = simpledialog.askinteger("Exam", "Exam mark (out of 100):", minvalue=0, maxvalue=100)
        if None in (cw1,cw2,cw3,exam):
            return

        coursework = cw1 + cw2 + cw3
        total = coursework + exam
        perc = round((total/160)*100, 2)
        grade = "A" if perc>=70 else "B" if perc>=60 else "C" if perc>=50 else "D" if perc>=40 else "F"

        new_kid = {
            "code": code, "name": name.strip(),
            "cw1": cw1, "cw2": cw2, "cw3": cw3,
            "exam": exam, "coursework": coursework,
            "percentage": perc, "grade": grade
        }

        self.students.append(new_kid)
        self.save_back_to_file()
        self.show_everybody()
        messagebox.showinfo("Yes!", f"{name} has been added!")

    # MENU 7 – delete
    def remove_kid(self):
        who = simpledialog.askstring("Delete", "Name or code of student to delete:")
        if not who:
            return

        found = None
        for s in self.students:
            if who.lower() in str(s["code"]) or who.lower() in s["name"].lower():
                found = s
                break

        if not found:
            messagebox.showinfo("Not found", "Couldn't find that student")
            return

        if messagebox.askyesno("Sure?", f"Really delete {found['name']} ({found['code']})?"):
            self.students.remove(found)
            self.save_back_to_file()
            self.show_everybody()
            messagebox.showinfo("Gone", "Student deleted")

    # MENU 8 – update
    def edit_kid(self):
        who = simpledialog.askstring("Update", "Name or code of student to edit:")
        if not who:
            return

        student = None
        for s in self.students:
            if who.lower() in str(s["code"]) or who.lower() in s["name"].lower():
                student = s
                break

        if not student:
            messagebox.showinfo("Not found", "No student with that name/code")
            return

        # little submenu in a messagebox because it's easier
        options = "What do you want to change?\n\n1. Name\n2. Coursework 1\n3. Coursework 2\n4. Coursework 3\n5. Exam mark"
        choice = simpledialog.askinteger("Choose", options, minvalue=1, maxvalue=5)
        if not choice:
            return

        if choice == 1:
            new = simpledialog.askstring("New name", "Enter new name:")
            if new:
                student["name"] = new.strip()
        elif choice <= 4:
            new = simpledialog.askinteger("New mark", f"New mark for Coursework {choice-1} (0-20):", minvalue=0, maxvalue=20)
            if new is not None:
                student[f"cw{choice-1}"] = new
        else:
            new = simpledialog.askinteger("New exam", "New exam mark (0-100):", minvalue=0, maxvalue=100)
            if new is not None:
                student["exam"] = new

        # recalculating everything
        student["coursework"] = student["cw1"] + student["cw2"] + student["cw3"]
        total = student["coursework"] + student["exam"]
        student["percentage"] = round((total/160)*100, 2)
        student["grade"] = "A" if student["percentage"]>=70 else "B" if student["percentage"]>=60 else "C" if student["percentage"]>=50 else "D" if student["percentage"]>=40 else "F"

        self.save_back_to_file()
        self.show_everybody()
        messagebox.showinfo("Updated", "Record updated successfully!")

    # starting the app
    def run(self):
        self.root.mainloop()


# code to actually run the thing
if __name__ == "__main__":
    app = StudentManager()
    app.run()