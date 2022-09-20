import pytest
import json
from src.models import session, Student
from src.utils import Queries
from src.restapi import app


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

def test_api_students():
    students = session.query(Student).all()
    students = [[student.id, student.group_id, student.first_name, student.last_name] for student in students]
    response = app.test_client().get('/students')
    assert response.status_code == 200
    assert json.loads(response.data.decode("utf-8")) == students

@pytest.mark.parametrize("url, id", [('/students/' + str(i), i) for i in range(1, 50)])
def test_api_student_id_get(url: str, id: int):
    a = session.query(
        Student.id, Student.group_id, Student.first_name, Student.last_name
    ).filter(Student.id == id).first()
    student = {
        "id": a.id,
        "group_id": a.group_id,
        "first_name": a.first_name,
        "last_name": a.last_name
    }
    response = app.test_client().get(url)
    assert response.status_code == 200
    assert json.loads(response.data.decode("utf-8")) == student


