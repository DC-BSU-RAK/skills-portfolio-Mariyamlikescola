# Student Marks Manager
# A simple program I made for my programming assignment
# It reads student marks from the text file in the Resources folder
# and lets the teacher/me view results nicely with a pink menu (yes, I like pink)

import tkinter as tk
from tkinter import ttk, messagebox
import os

class StudentApp:
    def __init__(self):
        # setting up the main window
        self.window = tk.Tk()
        self.window.title("Student Marks System")
        self.window.geometry("1100x700")
        self.window.configure(bg="#f8f8f8")

        self.all_students = []          # this will hold all the student info
        self.load_marks_from_file()     # trying to read the file when program starts
        self.build_interface()          

    def load_marks_from_file(self):
        # The file is inside "A1 - Resources" folder, not next to this .py file
        # So we need to go up one folder then into Resources

        script_folder = os.path.dirname(os.path.abspath(__file__))        # where is this py file?
        resources_folder = os.path.join(script_folder, "..", "A1 - Resources")
        file_location = os.path.join(resources_folder, "studentMarks.txt")

        # just in case there are weird slashes on Windows/Mac
        file_location = os.path.normpath(file_location)

        try:
            with open(file_location, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if len(lines) == 0:
                messagebox.showerror("Oops", "The file is empty!")
                return

            how_many = int(lines[0].strip())        # first line = number of students

            for i in range(1, how_many + 1):
                parts = lines[i].strip().split(",")

                code = int(parts[0])
                name = parts[1].strip()
                cw1 = int(parts[2])
                cw2 = int(parts[3])
                cw3 = int(parts[4])
                exam = int(parts[5])

                coursework_total = cw1 + cw2 + cw3
                total_marks = coursework_total + exam
                percentage = (total_marks / 160) * 100

                # deciding the grade
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

                # storing everything in a dictionary and adding to the big list
                student = {
                    "code": code,
                    "name": name,
                    "coursework": coursework_total,
                    "exam": exam,
                    "percentage": round(percentage, 2),
                    "grade": grade
                }
                self.all_students.append(student)

        except FileNotFoundError:
            messagebox.showerror("File missing",
                f"Can't find studentMarks.txt!\n\n"
                f"I was looking here:\n{file_location}\n\n"
                f"Put the file in the 'A1 - Resources' folder.")
        except Exception as e:
            messagebox.showerror("Something went wrong", f"Error: {e}")

    def build_interface(self):
        # Pink sidebar on the left — matches the example picture
        sidebar = tk.Frame(self.window, bg="#ff69b4", width=300)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # title at the top
        tk.Label(sidebar, text="Student Records", font=("Arial", 20, "bold"),
                 bg="#ff69b4", fg="white", pady=25).pack()

        # the four menu buttons
        buttons = [
            ("1. View all student records", self.show_all_students),
            ("2. View individual student record", self.search_one_student),
            ("3. Show student with highest total score", self.show_highest_student),
            ("4. Show student with lowest total score", self.show_lowest_student)
        ]

        for button_text, function in buttons:
            btn = tk.Button(sidebar, text=button_text, font=("Arial", 12),
                            bg="#ff1493", fg="white", activebackground="#ff69b4",
                            height=2, bd=0, command=function)
            btn.pack(fill="x", padx=25, pady=10)

        # Right side — where the table goes
        right_side = tk.Frame(self.window, bg="#f8f8f8")
        right_side.pack(fill="both", expand=True, padx=20, pady=20)

        # Table (Treeview) setup
        columns = ("Code", "Name", "Coursework", "Exam", "Overall %", "Grade")
        self.table = ttk.Treeview(right_side, columns=columns, show="headings", height=20)

        # adding column headings and widths
        self.table.heading("Code", text="Code")
        self.table.heading("Name", text="Student Name")
        self.table.heading("Coursework", text="Coursework (/60)")
        self.table.heading("Exam", text="Exam (/100)")
        self.table.heading("Overall %", text="Overall %")
        self.table.heading("Grade", text="Grade")

        self.table.column("Code", width=100, anchor="center")
        self.table.column("Name", width=250, anchor="w")
        self.table.column("Coursework", width=140, anchor="center")
        self.table.column("Exam", width=140, anchor="center")
        self.table.column("Overall %", width=120, anchor="center")
        self.table.column("Grade", width=100, anchor="center")

        self.table.pack(fill="both", expand=True)

        # labelling at the bottom for averages and messages
        self.info_label = tk.Label(right_side, text="", font=("Arial", 12, "italic"),
                                   bg="#f8f8f8", fg="#333")
        self.info_label.pack(pady=15)

    def clear_table(self):
        # removing everything currently shown
        for row in self.table.get_children():
            self.table.delete(row)
        self.info_label.config(text="")

    def add_student_row(self, student):
        # putting one student into the table
        self.table.insert("", "end", values=(
            student["code"],
            student["name"],
            f"{student['coursework']}/60",
            f"{student['exam']}/100",
            f"{student['percentage']}%",
            student["grade"]
        ))


    def show_all_students(self):
        self.clear_table()
        for s in self.all_students:
            self.add_student_row(s)

        # calculating average for the whole class
        if self.all_students:
            avg = sum(s["percentage"] for s in self.all_students) / len(self.all_students)
            self.info_label.config(text=f"Total students: {len(self.all_students)}   |   Class average: {avg:.2f}%")

    def search_one_student(self):
        if not self.all_students:
            messagebox.showinfo("Empty", "No students loaded yet.")
            return

        # little pop-up window to type name or code
        popup = tk.Toplevel(self.window)
        popup.title("Search Student")
        popup.geometry("380x220")
        popup.configure(bg="#ffffff")

        tk.Label(popup, text="Enter student code or name:", font=("Arial", 12), bg="#ffffff").pack(pady=25)

        search_box = tk.Entry(popup, font=("Arial", 12), width=30)
        search_box.pack(pady=10)

        def do_search():
            text = search_box.get().strip().lower()
            found = None
            for s in self.all_students:
                if str(s["code"]) == text or text in s["name"].lower():
                    found = s
                    break

            if found:
                self.clear_table()
                self.add_student_row(found)
                self.info_label.config(text=f"Found → {found['name']} ({found['code']})")
                popup.destroy()
            else:
                messagebox.showinfo("Not found", "No student matches that name/code.")

        tk.Button(popup, text="Search", command=do_search,
                  bg="#ff69b4", fg="white", font=("Arial", 11)).pack(pady=20)

    def show_highest_student(self):
        if not self.all_students:
            return
        top = max(self.all_students, key=lambda x: x["percentage"])
        self.clear_table()
        self.add_student_row(top)
        self.info_label.config(text=f"HIGHEST → {top['name']} with {top['percentage']}% (Grade {top['grade']})")

    def show_lowest_student(self):
        if not self.all_students:
            return
        bottom = min(self.all_students, key=lambda x: x["percentage"])
        self.clear_table()
        self.add_student_row(bottom)
        self.info_label.config(text=f"LOWEST → {bottom['name']} with {bottom['percentage']}% (Grade {bottom['grade']})")

    def run(self):
        self.window.mainloop()


# Starting the program
if __name__ == "__main__":
    my_app = StudentApp()
    my_app.run()