"""Gradebook CLI — command-line interface for managing
students, courses, and grades."""

import argparse
import logging
import os
import sys

from gradebook.service import (
    add_student,
    add_course,
    enroll,
    add_grade,
    list_students,
    list_courses,
    list_enrollments,
    compute_average,
    compute_gpa,
)


def parse_grade(value: str) -> float:
    """Parse and validate a grade value from string input.

    Args:
        value: String representation of the grade.

    Returns:
        The grade as a float.

    Raises:
        ValueError: If the value is not a number or not in 0-100.
    """
    try:
        grade = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"'{value}' is not a valid number")
    if grade < 0 or grade > 100:
        raise ValueError(f"Grade must be between 0 and 100, got {grade}")
    return grade


def parse_student_id(value: str) -> int:
    """Parse and validate a student ID from string input.

    Args:
        value: String representation of the student ID.

    Returns:
        The student ID as an integer.

    Raises:
        ValueError: If the value is not a positive integer.
    """
    try:
        sid = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"'{value}' is not a valid student ID")
    if sid < 1:
        raise ValueError("Student ID must be a positive integer")
    return sid


def setup_logging():
    """Configure logging to write to logs/app.log."""
    log_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "logs"
    )
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, "app.log"),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s"
               " %(name)s: %(message)s",
    )


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="gradebook",
        description="Gradebook CLI — manage students,"
                    " courses, and grades.",
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )

    sp = subparsers.add_parser(
        "add-student", help="Add a new student"
    )
    sp.add_argument(
        "--name", required=True, help="Student name"
    )

    sp = subparsers.add_parser(
        "add-course", help="Add a new course"
    )
    sp.add_argument(
        "--code", required=True,
        help="Course code (e.g., CS101)"
    )
    sp.add_argument(
        "--title", required=True,
        help="Course title"
    )

    sp = subparsers.add_parser(
        "enroll",
        help="Enroll a student in a course"
    )
    sp.add_argument(
        "--student-id", required=True,
        help="Student ID"
    )
    sp.add_argument(
        "--course", required=True, help="Course code"
    )

    sp = subparsers.add_parser(
        "add-grade",
        help="Add a grade for a student"
    )
    sp.add_argument(
        "--student-id", required=True,
        help="Student ID"
    )
    sp.add_argument(
        "--course", required=True, help="Course code"
    )
    sp.add_argument(
        "--grade", required=True, help="Grade (0-100)"
    )

    sp = subparsers.add_parser(
        "list",
        help="List students, courses, or enrollments"
    )
    sp.add_argument(
        "entity",
        choices=["students", "courses", "enrollments"],
        help="What to list",
    )
    sp.add_argument(
        "--sort", default=None,
        help="Sort key (name for students,"
             " code for courses)"
    )

    sp = subparsers.add_parser(
        "avg", help="Compute average grade"
    )
    sp.add_argument(
        "--student-id", required=True,
        help="Student ID"
    )
    sp.add_argument(
        "--course", required=True, help="Course code"
    )

    sp = subparsers.add_parser(
        "gpa", help="Compute GPA for a student"
    )
    sp.add_argument(
        "--student-id", required=True,
        help="Student ID"
    )

    return parser


def main(argv=None):
    """Entry point for the CLI."""
    setup_logging()
    logger = logging.getLogger("gradebook.cli")

    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "add-student":
            sid = add_student(args.name)
            print(
                f"Added student '{args.name}'"
                f" with ID {sid}."
            )
            logger.info(
                "Added student '%s' with ID %d",
                args.name, sid
            )

        elif args.command == "add-course":
            add_course(args.code, args.title)
            print(
                f"Added course"
                f" '{args.code}: {args.title}'."
            )
            logger.info("Added course %s", args.code)

        elif args.command == "enroll":
            student_id = parse_student_id(
                args.student_id
            )
            enroll(student_id, args.course)
            print(
                f"Enrolled student {student_id}"
                f" in '{args.course}'."
            )
            logger.info(
                "Enrolled student %d in %s",
                student_id, args.course
            )

        elif args.command == "add-grade":
            student_id = parse_student_id(
                args.student_id
            )
            grade = parse_grade(args.grade)
            add_grade(student_id, args.course, grade)
            print(
                f"Added grade {grade} for student"
                f" {student_id} in '{args.course}'."
            )
            logger.info(
                "Added grade %.1f for student"
                " %d in %s",
                grade, student_id, args.course
            )

        elif args.command == "list":
            if args.entity == "students":
                sort_by = args.sort if args.sort in (
                    "name",
                ) else "id"
                students = list_students(
                    sort_by=sort_by
                )
                if not students:
                    print("No students found.")
                for s in students:
                    print(f"  [{s.id}] {s.name}")

            elif args.entity == "courses":
                sort_by = args.sort if args.sort in (
                    "code",
                ) else "code"
                courses = list_courses(
                    sort_by=sort_by
                )
                if not courses:
                    print("No courses found.")
                for c in courses:
                    print(
                        f"  [{c.code}] {c.title}"
                    )

            elif args.entity == "enrollments":
                enrollments = list_enrollments()
                if not enrollments:
                    print("No enrollments found.")
                for e in enrollments:
                    if e.grades:
                        grades_str = ", ".join(
                            str(g)
                            for g in e.grades
                        )
                    else:
                        grades_str = "none"
                    print(
                        f"  Student {e.student_id}"
                        f" -> {e.course_code}"
                        f" (grades: {grades_str})"
                    )

        elif args.command == "avg":
            student_id = parse_student_id(
                args.student_id
            )
            avg = compute_average(
                student_id, args.course
            )
            print(
                f"Average for student {student_id}"
                f" in '{args.course}': {avg:.2f}"
            )

        elif args.command == "gpa":
            student_id = parse_student_id(
                args.student_id
            )
            gpa = compute_gpa(student_id)
            print(
                f"GPA for student {student_id}:"
                f" {gpa:.2f}"
            )

    except ValueError as e:
        print(f"Error: {e}")
        logger.error("ValueError: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
