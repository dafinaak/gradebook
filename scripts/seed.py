"""Seed script — populates the gradebook with sample data.

Run from project root:
    python -m scripts.seed
"""

from gradebook.storage import save_data
from gradebook.service import add_student, add_course, enroll, add_grade


def main():
    """Create sample students, courses, enrollments, and grades."""
    save_data({"students": [], "courses": [], "enrollments": []})

    students = ["Elena Martinez", "James Carter", "Mia Thompson"]
    student_ids = {}
    for name in students:
        sid = add_student(name)
        student_ids[name] = sid
        print(f"  Added student '{name}' (ID {sid})")

    courses = [
        ("CS101", "Intro to Computer Science"),
        ("MATH200", "Calculus II"),
    ]
    for code, title in courses:
        add_course(code, title)
        print(f"  Added course '{code}: {title}'")

    grade_data = {
        ("Elena Martinez", "CS101"): [92, 88, 95],
        ("Elena Martinez", "MATH200"): [78, 82],
        ("James Carter", "CS101"): [70, 75, 80],
        ("James Carter", "MATH200"): [90, 85],
        ("Mia Thompson", "CS101"): [60, 65],
    }

    for (name, course_code), grades in grade_data.items():
        sid = student_ids[name]
        enroll(sid, course_code)
        for grade in grades:
            add_grade(sid, course_code, grade)
        print(
            f"  Enrolled student {sid} in"
            f" '{course_code}' with grades {grades}"
        )

    print("\nSample data seeded to data/gradebook.json")
    print(
        f"  {len(students)} students,"
        f" {len(courses)} courses,"
        f" {len(grade_data)} enrollments"
    )


if __name__ == "__main__":
    main()
