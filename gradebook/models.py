"""Core data models for the gradebook application."""


class Student:
    """Represents a student with a unique ID and name."""

    def __init__(self, student_id: int, name: str):
        """Initialize a Student.

        Args:
            student_id: Unique integer identifier.
            name: Non-empty student name.

        Raises:
            ValueError: If name is empty or student_id is not positive.
        """
        if not isinstance(student_id, int) or student_id < 1:
            raise ValueError("student_id must be a positive integer")
        if not name or not name.strip():
            raise ValueError("name must be a non-empty string")
        self.id = student_id
        self.name = name.strip()

    def __str__(self):
        return f"Student(id={self.id}, name='{self.name}')"

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Student from a dictionary."""
        return cls(student_id=data["id"], name=data["name"])


class Course:
    """Represents a course with a code and title."""

    def __init__(self, code: str, title: str):
        """Initialize a Course.

        Args:
            code: Non-empty course code (e.g., 'CS101').
            title: Non-empty course title.

        Raises:
            ValueError: If code or title is empty.
        """
        if not code or not code.strip():
            raise ValueError("code must be a non-empty string")
        if not title or not title.strip():
            raise ValueError("title must be a non-empty string")
        self.code = code.strip()
        self.title = title.strip()

    def __str__(self):
        return f"Course(code='{self.code}', title='{self.title}')"

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {"code": self.code, "title": self.title}

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Course from a dictionary."""
        return cls(code=data["code"], title=data["title"])


class Enrollment:
    """Represents a student's enrollment in a course with grades."""

    def __init__(self, student_id: int, course_code: str, grades: list = None):
        """Initialize an Enrollment.

        Args:
            student_id: The enrolled student's ID.
            course_code: The course code.
            grades: List of numeric grades (0-100). Defaults to empty list.

        Raises:
            ValueError: If student_id or course_code is invalid,
                or grades out of range.
        """
        if not isinstance(student_id, int) or student_id < 1:
            raise ValueError("student_id must be a positive integer")
        if not course_code or not course_code.strip():
            raise ValueError("course_code must be a non-empty string")
        self.student_id = student_id
        self.course_code = course_code.strip()
        self.grades = []
        if grades:
            for g in grades:
                self._validate_grade(g)
            self.grades = list(grades)

    @staticmethod
    def _validate_grade(grade):
        """Validate that a grade is a number between 0 and 100."""
        if isinstance(grade, bool) or not isinstance(grade, (int, float)):
            raise ValueError(
                f"Grade must be a number, got {type(grade).__name__}"
            )
        if grade < 0 or grade > 100:
            raise ValueError(f"Grade must be between 0 and 100, got {grade}")

    def add_grade(self, grade):
        """Add a validated grade to this enrollment."""
        self._validate_grade(grade)
        self.grades.append(grade)

    def __str__(self):
        return (
            f"Enrollment(student_id={self.student_id}, "
            f"course_code='{self.course_code}', grades={self.grades})"
        )

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "student_id": self.student_id,
            "course_code": self.course_code,
            "grades": self.grades,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create an Enrollment from a dictionary."""
        return cls(
            student_id=data["student_id"],
            course_code=data["course_code"],
            grades=data.get("grades", []),
        )
