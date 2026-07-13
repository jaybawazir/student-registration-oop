import tkinter as tk
from tkinter import messagebox

DATA_FILE = "students.txt"
LOG_FILE = "log.txt"
FIELD_SEP = "|"


# classes
class Person:
    def __init__(self, name, age, id, email):
        self._name = name
        self._age = age
        self._id = id
        self._email = email + '@dah.edu.sa'

    def get_name(self):
        return self._name

    def get_age(self):
        return self._age

    def get_id(self):
        return self._id

    def get_email(self):
        return self._email

    def set_age(self, new_age):
        self._age = new_age

    def is_adult(self):
        if self._age >= 18:
            return True
        else:
            return False

    def display_info(self):
        return f"ID: {self._id} | Name: {self._name} | Age: {self._age} | Email: {self._email}"


class Student(Person):
    def __init__(self, name, age, id, email, gpa, major, gender):
        Person.__init__(self, name, age, id, email)
        self._gpa = gpa
        self._major = major
        self._gender = gender

    def get_gpa(self):
        return self._gpa

    def get_major(self):
        return self._major

    def get_gender(self):
        return self._gender

    def set_major(self, new_major):
        self._major = new_major

    def can_graduate(self):
        if self._gpa >= 2.0:
            return True
        else:
            return False

    def display_info(self):
        return f"Student {self._id} | {self._name} | Major: {self._major} | GPA: {self._gpa:.2f}"


# Additional class
class Course:
    def __init__(self, course_code, course_name, credits):
        self.course_code = course_code
        self.course_name = course_name
        self.credits = credits

    def update_credits(self, new_credits):
        self.credits = new_credits

    def display_info(self):
        return f"{self.course_code} - {self.course_name} ({self.credits} credits)"

    def is_high_credit(self):
        if self.credits >= 3:
            return True
        else:
            return False


# exceptions
class NegativeGPAError(Exception):
    pass


class LowGPAError(Exception):
    pass


class InvalidAgeError(Exception):
    pass


class MissingDataError(Exception):
    pass


def student_infos(name, age, student_id, email, gpa, major, gender):
    """Validate and build a Student. Returns (student, error_message).
    error_message is None on success, so the caller (the GUI) can show
    the exact reason to the user instead of it only reaching the console."""
    student = None
    error_message = None

    try:
        if not name or not student_id or not email:
            raise MissingDataError("Name, ID, and Email are required.")

        if age <= 0:
            raise InvalidAgeError("Age must be positive.")

        if gpa < 0:
            raise NegativeGPAError("GPA can't be negative.")

        if gpa < 2.0:
            raise LowGPAError("GPA is below the university requirement.")

    except MissingDataError as m:
        print("Missing Data Error:", m)
        error_message = f"Missing Data Error: {m}"

    except InvalidAgeError as i:
        print("Invalid Age Error:", i)
        error_message = f"Invalid Age Error: {i}"

    except NegativeGPAError as n:
        print("Invalid GPA Error:", n)
        error_message = f"Invalid GPA Error: {n}"

    except LowGPAError as l:
        print("Low GPA Error:", l)
        error_message = f"Low GPA Error: {l}"

    else:
        student = Student(name, age, student_id, email, gpa, major, gender)
        print("Student registered successfully.")

    finally:
        print("Student registration attempt is complete.")

    return student, error_message


# file I/O
def save_student_infos(student):
    """Append one student's full record to the data file, one field per line,
    using getters only (no direct attribute access)."""
    try:
        with open(DATA_FILE, "a") as file:
            file.write(student.get_name() + "\n")
            file.write(str(student.get_age()) + "\n")
            file.write(student.get_id() + "\n")
            file.write(student.get_email() + "\n")
            file.write(str(student.get_gpa()) + "\n")
            file.write(student.get_major() + "\n")
            file.write(student.get_gender() + "\n")

        print("Student information saved successfully!")

    except FileNotFoundError:
        print("Error: The students file doesn't exist.")
    except Exception:
        print("Unexpected Error while saving the student information.")


def load_student_infos():
    """Print the raw saved student data (one field per line) to the console."""
    try:
        with open(DATA_FILE, "r") as file:
            print("Student Data:\n")
            for line in file:
                print(line.rstrip())

    except FileNotFoundError:
        print("Error: The students.txt file wasn't found.")
    except Exception:
        print("Unexpected Error while loading students file.")


def save_students_to_file(students, filename=DATA_FILE):
    """Save a list of Student objects to file in one consistent,
    delimited format so the exact same file can be reloaded later."""
    try:
        with open(filename, "w") as file:
            for s in students:
                fields = [
                    s.get_id(), s.get_name(), str(s.get_age()), s.get_email(),
                    str(s.get_gpa()), s.get_major(), s.get_gender(),
                ]
                file.write(FIELD_SEP.join(fields) + "\n")
        return True
    except Exception:
        return False


def load_students_from_file(filename=DATA_FILE):
    """Read the delimited file back and rebuild real Student objects,
    not just text, so the loaded data can keep being used in the program."""
    loaded = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(FIELD_SEP)
                if len(parts) != 7:
                    continue
                student_id, name, age, email, gpa, major, gender = parts
                email_username = email.split('@')[0]
                student = Student(name, int(age), student_id, email_username,
                                   float(gpa), major, gender)
                loaded.append(student)
        return loaded, True
    except FileNotFoundError:
        return [], False
    except Exception:
        return [], False


def save_log(message):
    try:
        with open(LOG_FILE, "a") as file:
            file.write(message + "\n")
    except Exception:
        print("Error writing log.")


class StudentRegistrationGUI:
    def __init__(self):
        self.mainWindow = tk.Tk()
        self.mainWindow.title("Student Registration System")
        self.mainWindow.geometry("900x500")

        form_frame = tk.LabelFrame(self.mainWindow, text="Student Information")
        form_frame.pack(padx=20, pady=15, fill="x")

        self.students = []

        tk.Label(form_frame, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Age").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.age_entry = tk.Entry(form_frame)
        self.age_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="ID").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.id_entry = tk.Entry(form_frame)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Email (username)").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="GPA").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.gpa_entry = tk.Entry(form_frame)
        self.gpa_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Major").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.major_entry = tk.Entry(form_frame)
        self.major_entry.grid(row=2, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Gender").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.gender_entry = tk.Entry(form_frame)
        self.gender_entry.grid(row=3, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self.mainWindow)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Add Student", command=self.add_student).pack(side="left", padx=15)
        tk.Button(button_frame, text="Show All", command=self.show_all).pack(side="left", padx=15)
        tk.Button(button_frame, text="Save", command=self.save_students).pack(side="left", padx=15)
        tk.Button(button_frame, text="Load", command=self.load_students).pack(side="left", padx=15)

        output_frame = tk.LabelFrame(self.mainWindow, text="Registered Students")
        output_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.output = tk.Text(output_frame, height=8)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def add_student(self):
        try:
            student, error_message = student_infos(
                self.name_entry.get(),
                int(self.age_entry.get()),
                self.id_entry.get(),
                self.email_entry.get(),
                float(self.gpa_entry.get()),
                self.major_entry.get(),
                self.gender_entry.get()
            )

            if student:
                self.students.append(student)
                save_log(f"Added student {student.get_id()} - {student.get_name()}")
                messagebox.showinfo("Success", "Student added successfully")
            else:
                messagebox.showerror("Registration Error", error_message)

        except ValueError:
            messagebox.showerror("Error", "Age and GPA must be numbers")

    def show_all(self):
        self.output.delete("1.0", tk.END)
        for s in self.students:
            self.output.insert(tk.END, s.display_info() + "\n")

    def save_students(self):
        success = save_students_to_file(self.students)
        if success:
            save_log(f"Saved {len(self.students)} student(s) to {DATA_FILE}")
            messagebox.showinfo("Saved", "Students saved successfully")
        else:
            messagebox.showerror("Error", "Could not save students")

    def load_students(self):
        loaded, success = load_students_from_file()
        if success:
            self.students = loaded
            self.show_all()
            save_log(f"Loaded {len(self.students)} student(s) from {DATA_FILE}")
            messagebox.showinfo("Loaded", "Students loaded successfully")
        else:
            messagebox.showerror("Error", "students.txt not found")


if __name__ == "__main__":
    app = StudentRegistrationGUI()
    app.mainWindow.mainloop()
