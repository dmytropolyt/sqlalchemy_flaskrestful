from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

config = {'user': 'postgres',
          'password': '121212q',
          'host': '127.0.0.1',
          'port': '5432',
          'db': 'university'}

engine = create_engine(
    f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}"
)
Base = declarative_base()

association = Table(
    'association', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    students = relationship("Student", back_populates='group')

    def __repr__(self):
        return f'Group(id = {self.id})'

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    first_name = Column(String)
    last_name = Column(String)

    group = relationship('Group', back_populates='students')
    courses = relationship(
        'Course', secondary=association,
        back_populates='students'
    )

    def __repr__(self):
        return f'Student(id = {self.id})'

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    students = relationship(
        'Student', secondary=association,
        back_populates='courses'
    )

    def __repr__(self):
        return f'Course(id = {self.id}'

Base.metadata.create_all(engine)

session = sessionmaker()(bind=engine)


