from database import Database
from student import Student
from course import Course


def display_students(students):
    if not students:
        print("No students found.")
        return

    print("\nID | Name | Age | Course ID | Marks")
    print("-" * 45)

    for student in students:
        print(
            f"{student[0]} | "
            f"{student[1]} | "
            f"{student[2]} | "
            f"{student[3]} | "
            f"{student[4]}"
        )


def display_courses(courses):
    if not courses:
        print("No courses found.")
        return

    print("\nCourse ID | Course Name")
    print("-" * 30)

    for course in courses:
        print(f"{course[0]} | {course[1]}")


def main():

    db = Database()

    while True:

        print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
        print("1. Add Course")
        print("2. View Courses")
        print("3. Add Student")
        print("4. View All Students")
        print("5. Search Student")
        print("6. Search Students by Course")
        print("7. Search Students by Marks")
        print("8. Sort Students")
        print("9. Top N Students")
        print("10. Update Student")
        print("11. Delete Student")
        print("12. Student Statistics")
        print("13. Course-wise Statistics")
        print("14. Courses Without Students")
        print("15. Exit")

        choice = input("\nEnter your choice: ")

        # 1. Add Course
        if choice == "1":

            try:
                course_id = int(input("Enter course ID: "))
                course_name = input("Enter course name: ")

                course = Course(course_id, course_name)

                if db.add_course(course):
                    print("Course added successfully.")

            except ValueError as error:
                print("Error:", error)

        # 2. View Courses
        elif choice == "2":

            courses = db.get_all_courses()
            display_courses(courses)

        # 3. Add Student
        elif choice == "3":

            try:
                student_id = int(input("Enter student ID: "))
                name = input("Enter name: ")
                age = int(input("Enter age: "))
                course_id = int(input("Enter course ID: "))
                marks = float(input("Enter marks: "))

                student = Student(
                    student_id,
                    name,
                    age,
                    course_id,
                    marks
                )

                if db.add_student(student):
                    print("Student added successfully.")

            except ValueError as error:
                print("Error:", error)

        # 4. View All Students
        elif choice == "4":

            students = db.get_all_students()
            display_students(students)

        # 5. Search Student
        elif choice == "5":

            try:
                student_id = int(input("Enter student ID: "))

                student = db.get_student_by_id(student_id)

                if student:
                    print("\nStudent Found:")
                    print("ID:", student[0])
                    print("Name:", student[1])
                    print("Age:", student[2])
                    print("Course ID:", student[3])
                    print("Marks:", student[4])
                else:
                    print("Student not found.")

            except ValueError:
                print("Invalid student ID.")

        # 6. Search Students by Course
        elif choice == "6":

            course_name = input("Enter course name: ")

            students = db.get_students_by_course(course_name)

            if students:
                print("\nName | Course | Marks")
                print("-" * 35)

                for student in students:
                    print(f"{student[0]} | {student[1]} | {student[2]}")
            else:
                print("No students found.")

        # 7. Search Students by Marks
        elif choice == "7":

            try:
                marks = float(input("Enter minimum marks: "))

                students = db.search_students_by_marks(marks)

                display_students(students)

            except ValueError:
                print("Invalid marks.")

        # 8. Sort Students
        elif choice == "8":

            print("\nSort by:")
            print("1. Name")
            print("2. Age")
            print("3. Marks")

            sort_choice = input("Enter choice: ")

            columns = {
                "1": "name",
                "2": "age",
                "3": "marks"
            }

            if sort_choice in columns:

                students = db.sort_students(columns[sort_choice])
                display_students(students)

            else:
                print("Invalid choice.")

        # 9. Top N Students
        elif choice == "9":

            try:
                n = int(input("Enter N: "))

                students = db.top_n_students(n)

                display_students(students)

            except ValueError:
                print("Invalid number.")

        # 10. Update Student
        elif choice == "10":

            try:
                student_id = int(input("Enter student ID: "))
                name = input("Enter new name: ")
                age = int(input("Enter new age: "))
                course_id = int(input("Enter new course ID: "))
                marks = float(input("Enter new marks: "))

                if db.update_student(
                    student_id,
                    name,
                    age,
                    course_id,
                    marks
                ):
                    print("Student updated successfully.")
                else:
                    print("Student not found.")

            except ValueError as error:
                print("Error:", error)

        # 11. Delete Student
        elif choice == "11":

            try:
                student_id = int(input("Enter student ID: "))

                if db.delete_student(student_id):
                    print("Student deleted successfully.")
                else:
                    print("Student not found.")

            except ValueError:
                print("Invalid student ID.")

        # 12. Student Statistics
        elif choice == "12":

            statistics = db.student_statistics()

            print("\nStudent Statistics")
            print("Total Students:", statistics[0])
            print("Average Marks:", statistics[1])
            print("Highest Marks:", statistics[2])
            print("Lowest Marks:", statistics[3])

        # 13. Course-wise Statistics
        elif choice == "13":

            statistics = db.get_course_statistics()

            print("\nCourse Statistics")
            print("-" * 75)

            for row in statistics:
                print(
                    f"Course: {row[0]} | "
                    f"Students: {row[1]} | "
                    f"Average: {row[2]} | "
                    f"Highest: {row[3]} | "
                    f"Lowest: {row[4]}"
                )

        # 14. Courses Without Students
        elif choice == "14":

            courses = db.get_courses_without_students()

            if courses:
                print("\nCourses Without Students:")

                for course in courses:
                    print(course[0])

            else:
                print("Every course has students.")

        # 15. Exit
        elif choice == "15":

            print("Thank you for using Student Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()