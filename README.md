# Student Registration System (OOP)

A Student Registration System built with Python and Tkinter for an Object-Oriented Programming course. It lets users register students through a GUI, view all registered students, and save/load their data to and from a file.

## Features

- Register a student through a form (name, age, ID, email, GPA, major, gender)
- View all registered students in the app
- Save registered students to a file
- Load previously saved students back into the app
- Input validation with custom exceptions for missing data, invalid age, and invalid GPA

## Classes

**Person** (parent class)
Attributes: name, age, id, email
Methods: getters for each attribute, `set_age()`, `is_adult()`, `display_info()`

**Student** (inherits from Person)
Additional attributes: gpa, major, gender
Additional methods: getters, `set_major()`, `can_graduate()`, overrides `display_info()`

**Course** (supporting class)
Attributes: course_code, course_name, credits
Methods: `update_credits()`, `display_info()`, `is_high_credit()`

## Exception Handling

Custom exceptions used to validate student data during registration:
- `MissingDataError` — required field left empty
- `InvalidAgeError` — age is zero or negative
- `NegativeGPAError` — GPA below zero
- `LowGPAError` — GPA below the 2.0 minimum

## File I/O

Student records are saved to `students.txt` in a consistent delimited format and can be fully reloaded back into working Student objects, not just displayed as text.

## How to Run

Requires Python 3 with Tkinter (included by default on most systems).

```bash
python oop_code.py
```

## Team

Joud Bawazir, R.E., L.A.
