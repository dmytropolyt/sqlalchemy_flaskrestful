from models import Group, Student, Course, session
from string import ascii_uppercase, digits
from random import choice, randint, sample

# takes a db session and fill db with 20 random named groups, 200 random named students and 10 courses
def fill_base(session):
    from faker import Faker

    fake = Faker()

    courses_to = [
        'math', 'biology', 'chemistry', 'computer science', 'physics',
        'philosophy', 'history', 'geography', 'economics', 'statistics'
    ]

    with session as session:

        counter = 0
        for i in range(10):
            group_to = Group(name=f'{choice(ascii_uppercase)+choice(ascii_uppercase)}-{choice(digits)+choice(digits)}')
            course_to = Course(name=courses_to[i])
            session.add(course_to)

            if counter <= 200:
                students_list = []

                for j in range(randint(10, 30)):
                    if counter == 200:
                        break
                    else:
                        students_list.append(Student(first_name=fake.first_name(), last_name=fake.last_name()))
                        counter += 1

                group_to.students.extend(students_list)
                for s in students_list:
                    session.add(s)
                session.add(group_to)
            else:
                session.add(group_to)

        if session.query(Student.id).count() < 200:
            for i in range(session.query(Student.id).count(), 200):
                session.add(Student(first_name=fake.first_name(), last_name=fake.last_name()))

        courses = [session.get(Course, i) for i in range(1, session.query(Course).count() + 1)]
        for s in session.query(Student):
            s.courses.extend(sample(courses, choice([1, 2, 3])))

        session.commit()


class Queries:
    '''
    It's class for queries
    Enter your parameters and get result
    First of all enter a database session parameter!
    There are 6 methods:
    1. groups_with_less_or_equal_students - returns list of groups with less or equal number of students
    by parameter 'number_of_students' that you passed, by default it's 10
    2. related_students_to_course - returns a list of students related to a course that you passed
    by parameter 'course'
    3. add_student - adds a student to Student model in db by parameters 'first_name' and 'last_name'
    4. del_student - delete a student from db by 'student_id' parameter
    5. add_student_to_course - adds student to course by 'data_list' parameter
    it should contain id of student (integer) and name of course (string)
    6. remove_student_from_course - remove student from course by 'data_list' parameter
    it should contain id of student (integer) and name of course (string)
    '''

    def __init__(
            self, dbsession=session, number_of_students: int = 10, course: str = 'math',
            first_name: str = 'Dmytro', last_name: str = 'Konstantinov', student_id: int = 1,
            data_list: list = []
    ):
        self.session = dbsession
        self.num = number_of_students
        self.course = course
        self.first_name = first_name
        self.last_name = last_name
        self.id = student_id
        self.data_list = data_list

    def groups_with_less_or_equal_students(self):
        from sqlalchemy import func

        groups = self.session.query(Group.name).join('students').group_by(Group.name).\
            having(func.count(Student.id) <= self.num).all()
        if groups:
            return [' '.join(i) for i in groups]
        else:
            raise ValueError(f'There is no group with {self.num} students')

    def related_students_to_course(self):
        if (self.course, ) in self.session.query(Course.name).all():
            query = self.session.query(Student.first_name, Student.last_name).join('courses')\
                .filter(Course.name == self.course).all()
            return [' '.join(i) for i in query]
        else:
            raise ValueError("There isn't a course with this name")

    def add_student(self):
        if self.first_name.istitle() and self.first_name.isalpha() and self.last_name.istitle() and self.last_name.isalpha():
            student = Student(first_name=self.first_name, last_name=self.last_name)
            self.session.add(student)
            self.session.commit()
            print(f'Student: {self.first_name} {self.last_name} added')
        else:
            raise ValueError('Names must be a string and start with capital letter')

    def del_student(self):
        student = self.session.query(Student).filter(Student.id == self.id)
        if student:
            student.delete()
            self.session.commit()
            print(f'Student with id = {self.id} deleted')
        else:
            raise ValueError('There is no student with that id')

    def add_student_to_course(self):
        student = self.session.query(Student).filter(
            Student.id == self.data_list[0]).one()
        course = self.session.query(Course).filter(Course.name == self.data_list[1]).one()
        if student and course:
            course.students.append(student)
            self.session.commit()
            print(f'Student - {self.data_list[0]}  added to course - {self.data_list[1]}')
        else:
            raise ValueError('There is no student or course')

    def remove_student_from_course(self):
        course = self.session.query(Course).filter(Course.name == self.data_list[1]).one()
        course.students.remove(
            self.session.query(Student).filter(Student.id == self.data_list[0])
        ).one()
        self.session.commit()
        print(f'Student - {self.data_list[0]} removed from course - {self.data_list[1]}')

a = session.query(Student).filter(Student.first_name == 'Mark', Student.last_name == 'Greer').one()
print({'id': a.id})

