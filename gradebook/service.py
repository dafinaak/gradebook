"""Business logic for the gradebook application."""

from .models import Student, Course, Enrollment
from .storage import load_data, save_data


def _next_student_id(data: dict) -> int:
    """Return the next available student ID."""
    if not data["students"]:
        return 1
    return max(s["id"] for s in data["students"]) + 1


def add_student(name: str) -> int:
    """Add a new student and return their assigned ID.

    Args:
        name: The student's name.

    Returns:
        The new student's ID.
    """
    data = load_data()
    new_id = _next_student_id(data)
    student = Student(new_id, name)
    data["students"].append(student.to_dict())
    save_data(data)
    return new_id


def add_course(code: str, title: str) -> None:
    """Add a new course.

    Args:
        code: Course code (e.g., 'CS101').
        title: Course title.

    Raises:
        ValueError: If a course with this code already exists.
    """
    code = code.strip().upper()
    data = load_data()
    if any(c["code"] == code for c in data["courses"]):
        raise ValueError(f"Course '{code}' already exists")
    course = Course(code, title)
    data["courses"].append(course.to_dict())
    save_data(data)


def enroll(student_id: int, course_code: str) -> None:
    """Enroll a student in a course.

    Args:
        student_id: The student's ID.
        course_code: The course code.

    Raises:
        ValueError: If student or course not found, or already enrolled.
    """
    course_code = course_code.strip().upper()
    data = load_data()
    if not any(s["id"] == student_id for s in data["students"]):
        raise ValueError(f"Student with ID {student_id} not found")
    if not any(c["code"] == course_code for c in data["courses"]):
        raise ValueError(f"Course '{course_code}' not found")
    if any(
        e["student_id"] == student_id and e["course_code"] == course_code
        for e in data["enrollments"]
    ):
        raise ValueError(
            f"Student {student_id} is already enrolled in '{course_code}'"
        )
    enrollment = Enrollment(student_id, course_code)
    data["enrollments"].append(enrollment.to_dict())
    save_data(data)


def add_grade(student_id: int, course_code: str, grade: float) -> None:
    """Add a grade for a student in a course.

    Args:
        student_id: The student's ID.
        course_code: The course code.
        grade: Numeric grade (0-100).

    Raises:
        ValueError: If the enrollment is not found.
    """
    course_code = course_code.strip().upper()
    data = load_data()
    for e in data["enrollments"]:
        if e["student_id"] == student_id and e["course_code"] == course_code:
            enrollment = Enrollment.from_dict(e)
            enrollment.add_grade(grade)
            e["grades"] = enrollment.grades
            save_data(data)
            return
    raise ValueError(
        f"Student {student_id} is not enrolled in '{course_code}'"
    )


def list_students(sort_by: str = "id") -> list:
    """Return all students, sorted by the given key.

    Args:
        sort_by: Sort key — 'id' or 'name'.
    """
    data = load_data()
    students = [
        Student.from_dict(s) for s in data["students"]
    ]
    if sort_by == "name":
        return sorted(
            students, key=lambda s: s.name.lower()
        )
    return sorted(students, key=lambda s: s.id)


def list_courses(sort_by: str = "code") -> list:
    """Return all courses, sorted by the given key.

    Args:
        sort_by: Sort key — 'code' or 'title'.
    """
    data = load_data()
    courses = [
        Course.from_dict(c) for c in data["courses"]
    ]
    if sort_by == "title":
        return sorted(
            courses, key=lambda c: c.title.lower()
        )
    return sorted(courses, key=lambda c: c.code)


def list_enrollments() -> list:
    """Return all enrollments sorted by student_id then course_code."""
    data = load_data()
    enrollments = [Enrollment.from_dict(e) for e in data["enrollments"]]
    return sorted(enrollments, key=lambda e: (e.student_id, e.course_code))


def compute_average(student_id: int, course_code: str) -> float:
    """Compute the average grade for a student in a course.

    Args:
        student_id: The student's ID.
        course_code: The course code.

    Returns:
        The average grade.

    Raises:
        ValueError: If enrollment not found or no grades recorded.
    """
    course_code = course_code.strip().upper()
    data = load_data()
    for e in data["enrollments"]:
        if (e["student_id"] == student_id and
                e["course_code"] == course_code):
            grades = e.get("grades", [])
            if not grades:
                raise ValueError(
                    f"No grades for student {student_id}"
                    f" in '{course_code}'"
                )
            return sum(grades) / len(grades)
    raise ValueError(
        f"Student {student_id} is not enrolled"
        f" in '{course_code}'"
    )


def compute_gpa(student_id: int) -> float:
    """Compute GPA as the simple mean of all course averages for a student.

    Args:
        student_id: The student's ID.

    Returns:
        The GPA (mean of course averages).

    Raises:
        ValueError: If the student has no enrollments or no grades.
    """
    data = load_data()
    if not any(s["id"] == student_id for s in data["students"]):
        raise ValueError(f"Student with ID {student_id} not found")
    student_enrollments = [
        e for e in data["enrollments"] if e["student_id"] == student_id
    ]
    if not student_enrollments:
        raise ValueError(
            f"Student {student_id} has no enrollments"
        )
    course_avgs = {
        e["course_code"]: sum(e["grades"]) / len(e["grades"])
        for e in student_enrollments
        if e.get("grades")
    }
    if not course_avgs:
        raise ValueError(
            f"Student {student_id} has no grades"
            " in any course"
        )
    return sum(course_avgs.values()) / len(course_avgs)
