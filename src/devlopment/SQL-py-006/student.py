class Student:
    def __init__(self, student_id, name, age, course_id, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course_id = course_id
        self.marks = marks

    def validate(self):
        # Student ID validation
        if not isinstance(self.student_id, int):
            raise ValueError("Student ID must be an integer.")

        # Name validation
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name cannot be empty.")

        # Age validation
        if not isinstance(self.age, int) or self.age <= 0:
            raise ValueError("Age must be greater than 0.")

        # Course ID validation
        if not isinstance(self.course_id, int):
            raise ValueError("Course ID must be an integer.")

        # Marks validation
        if not isinstance(self.marks, (int, float)):
            raise ValueError("Marks must be a number.")

        if self.marks < 0 or self.marks > 100:
            raise ValueError("Marks must be between 0 and 100.")

        return True