# Gradebook CLI

A lightweight command-line application for managing students, courses, enrollments, and grades. Built entirely with Python's standard library — no external dependencies required.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Seed Sample Data](#seed-sample-data)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Design Decisions & Limitations](#design-decisions--limitations)

---

## Overview

Gradebook CLI is a terminal-based application that demonstrates core Python fundamentals including object-oriented programming, file I/O, exception handling, modular design, and command-line argument parsing. Data is persisted locally in a JSON file, making it fully portable with no database setup required.

---

## Project Structure

```
gradebook/
├── gradebook/
│   ├── __init__.py      
│   ├── models.py       
│   ├── storage.py       
│   └── service.py      
├── tests/
│   ├── __init__.py
│   └── test_service.py  
├── scripts/
│   ├── __init__.py
│   └── seed.py         
├── data/
│   └── gradebook.json   
├── logs/
│   └── app.log         
├── .gitignore
├── main.py             
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/dafinaak/gradebook.git
cd gradebook
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

No packages need to be installed. The project uses only the Python standard library.

---

## Seed Sample Data

To populate the database with example students, courses, and grades, run:

```bash
python -m scripts.seed
```

This resets and repopulates `data/gradebook.json` with 3 students, 2 courses, and 5 enrollments including grades.

---

### Add a student

```bash
python main.py add-student --name "Elena Martinez"
# Output: Added student 'Elena Martinez' with ID 1.
```

### Add a course

```bash
python main.py add-course --code CS101 --title "Intro to Computer Science"
# Output: Added course 'CS101: Intro to Computer Science'.
```

### Enroll a student in a course

```bash
python main.py enroll --student-id 1 --course CS101
# Output: Enrolled student 1 in 'CS101'.
```

### Add a grade

```bash
python main.py add-grade --student-id 1 --course CS101 --grade 95
# Output: Added grade 95.0 for student 1 in 'CS101'.
```

### List records

```bash
# List all students (default sort: id)
python main.py list students

# List students sorted by name
python main.py list students --sort name

# List all courses (default sort: code)
python main.py list courses

# List all enrollments
python main.py list enrollments
```

### Compute course average

```bash
python main.py avg --student-id 1 --course CS101
# Output: Average for student 1 in 'CS101': 91.67
```

### Compute GPA

```bash
python main.py gpa --student-id 1
# Output: GPA for student 1: 85.83
```

---

## Running Tests

```bash
python -m unittest tests.test_service -v
```

Expected output:

```
test_add_grade_happy_path (tests.test_service.TestService) ... ok
test_add_grade_invalid_enrollment (tests.test_service.TestService) ... ok
test_add_student_empty_name (tests.test_service.TestService) ... ok
test_add_student_returns_incrementing_ids (tests.test_service.TestService) ... ok
test_compute_average_happy_path (tests.test_service.TestService) ... ok
test_compute_average_no_grades (tests.test_service.TestService) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.01s

OK
```

---

## Design Decisions & Limitations

### Architecture

I organized the project into four layers, each with a clear job:

| Layer | Module | Responsibility |
|---|---|---|
| Data | `models.py` | Define and validate data structures |
| Persistence | `storage.py` | Read and write JSON; handle I/O errors |
| Logic | `service.py` | All business rules and data mutations |
| Interface | `main.py` | Argument parsing, input validation, and user-facing output |

Each layer only talks to the one below it, which made testing a lot easier — I could test the service logic without touching the CLI at all.

### Key decisions

**JSON for persistence.** I went with JSON because it's simple and you can open the file and see exactly what's in it. It works fine for a small project like this. If the dataset were much larger, something like SQLite would make more sense.

**All changes go through service.py.** Whether it's the CLI or the seed script, everything goes through the same functions. That way validation always runs and nothing can sneak in bad data by writing to the JSON directly.

**Course codes are always uppercase.** I normalize course codes to uppercase on input so `cs101` and `CS101` are treated as the same course. Seemed better than letting case mismatches cause confusing errors.

**Student IDs auto-increment.** Each new student gets `max(existing ids) + 1`. Since there's no delete, IDs never get reused.

**GPA is a simple average.** GPA is just the mean of all course averages. No credit-hour weighting — kept it simple as the project didn't require it.

### Limitations

- No update or delete — you can only add data, which was enough for the scope of this project.
- The whole file loads into memory on every operation, so it wouldn't scale well with a very large dataset.
- No concurrency handling — if two processes tried to write at the same time, things could break.
- No authentication or multi-user support — it's a single-user local tool.
