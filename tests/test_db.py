import pytest
from src.models import session, Student
from src.app import Queries


def test_db_data(dbsession):
    assert dbsession.query(
        Student.group_id, Student.first_name, Student.last_name
    ).all() == session.query(Student.group_id, Student.first_name, Student.last_name).all()

def test_add_student(dbsession):
    Queries(dbsession, first_name='Dmytro', last_name='Konstantinov').add_student()
    Queries(session, first_name='Dmytro', last_name='Konstantinov').add_student()
    assert dbsession.query(Student).get(201) == session.query(Student).get(201)

def test_del_student(dbsession):
    Queries(dbsession, student_id=201).del_student()
    Queries(session, student_id=201).del_student()
    assert dbsession.query(Student).get(201) == session.query(Student).get(201)