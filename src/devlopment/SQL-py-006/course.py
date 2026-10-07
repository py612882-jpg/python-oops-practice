class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name

    def validate(self):
        # Course ID validation
        if not isinstance(self.course_id, int):
            raise ValueError("Course ID must be an integer.")

        # Course name validation
        if not isinstance(self.course_name, str):
            raise ValueError("Course name must be a string.")

        if not self.course_name.strip():
            raise ValueError("Course name cannot be empty.")

        return True