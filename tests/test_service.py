"""Unit tests for gradebook.service module."""

import json
import os
import tempfile
import unittest

from gradebook import storage
from gradebook.service import (
    add_student,
    add_course,
    enroll,
    add_grade,
    compute_average,
)

EMPTY_DATA = {"students": [], "courses": [], "enrollments": []}


class TestService(unittest.TestCase):
    """Tests for service functions using a temporary data file."""

    def setUp(self):
        """Create a temp JSON file and patch storage."""
        self.tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        json.dump(EMPTY_DATA, self.tmp)
        self.tmp.close()
        self._orig_path = storage.DEFAULT_PATH
        storage.DEFAULT_PATH = self.tmp.name

    def tearDown(self):
        """Restore original path and clean up temp file."""
        storage.DEFAULT_PATH = self._orig_path
        os.unlink(self.tmp.name)

    def test_add_student_returns_incrementing_ids(self):
        """add_student should return sequential IDs starting from 1."""
        id1 = add_student("Alice")
        id2 = add_student("Bob")
        self.assertEqual(id1, 1)
        self.assertEqual(id2, 2)

    def test_add_grade_happy_path(self):
        """add_grade should append a grade to the enrollment."""
        add_student("Alice")
        add_course("CS101", "Intro to CS")
        enroll(1, "CS101")
        add_grade(1, "CS101", 90)
        add_grade(1, "CS101", 80)
        avg = compute_average(1, "CS101")
        self.assertAlmostEqual(avg, 85.0)

    def test_add_grade_invalid_enrollment(self):
        """add_grade should raise ValueError for unenrolled student."""
        add_student("Alice")
        add_course("CS101", "Intro to CS")
        with self.assertRaises(ValueError):
            add_grade(1, "CS101", 90)

    def test_compute_average_happy_path(self):
        """compute_average should return the mean of grades."""
        add_student("Alice")
        add_course("CS101", "Intro to CS")
        enroll(1, "CS101")
        add_grade(1, "CS101", 80)
        add_grade(1, "CS101", 90)
        add_grade(1, "CS101", 100)
        avg = compute_average(1, "CS101")
        self.assertAlmostEqual(avg, 90.0)

    def test_compute_average_no_grades(self):
        """compute_average should raise ValueError when there are no grades."""
        add_student("Alice")
        add_course("CS101", "Intro to CS")
        enroll(1, "CS101")
        with self.assertRaises(ValueError):
            compute_average(1, "CS101")

    def test_add_student_empty_name(self):
        """add_student should raise ValueError for empty name."""
        with self.assertRaises(ValueError):
            add_student("")


if __name__ == "__main__":
    unittest.main()
