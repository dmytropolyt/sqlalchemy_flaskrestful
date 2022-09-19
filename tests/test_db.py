import pytest
from src.models import session, Student
from src.app import Queries


def test_add_student(dbsession):
    Queries(dbsession, first_name='Dmytro', last_name='Konstantinov').add_student()
    Queries(session, first_name='Dmytro', last_name='Konstantinov').add_student()
    a = session.query(Student.first_name, Student.last_name).order_by(Student.id.desc()).first()
    b = dbsession.query(Student.first_name, Student.last_name).order_by(Student.id.desc()).first()
    assert a == b

def test_del_student(dbsession):
    Queries(dbsession, first_name='Dmytro', last_name='Konstantinov').add_student()
    a = dbsession.query(Student.id).filter(
        Student.first_name == 'Dmytro', Student.last_name == 'Konstantinov'
    ).one()
    b = session.query(Student.id).filter(
        Student.first_name == 'Dmytro', Student.last_name == 'Konstantinov'
    ).one()
    Queries(dbsession, student_id=a[0]).del_student()
    Queries(session, student_id=b[0]).del_student()
    assert dbsession.query(Student).get(a[0]) == session.query(Student).get(b[0])