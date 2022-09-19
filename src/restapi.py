from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, reqparse, abort
from models import session, Student

app = Flask(__name__)
api = Api(app)


resource_fields = {
    "id": fields.Integer,
    "group_id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String
}

post_parser = reqparse.RequestParser()
post_parser.add_argument("first_name", type=str, help="First name is required", required=True)
post_parser.add_argument("last_name", type=str, help="Last name is required", required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument("first_name", type=str)
put_parser.add_argument("last_name", type=str)


class ToDoList(Resource):
    def get(self):
        students = session.query(Student).all()
        todos = {}
        for student in students:
            todos[student.id] = {
                "group_id": student.group_id, "first_name": student.first_name, "last_name": student.last_name
            }

        return todos

class StudentAPI(Resource):

    @marshal_with(resource_fields)
    def get(self, todo_id):
        student = session.query(Student).get(todo_id)
        if not student:
            abort(404, message="Could not find student with that id")

        return student

    @marshal_with(resource_fields)
    def post(self, todo_id):
        args = post_parser.parse_args()
        task = session.query(Student).get(todo_id)
        if task:
            abort(409, message="Student id already taken")

        todo = Student(id=todo_id, **args)
        session.add(todo)
        session.commit()
        student = session.query(Student).get(todo_id)

        return student, 201

    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = put_parser.parse_args()
        student = session.query(Student).get(todo_id)
        if not student:
            abort(404, message='Student do not exist, cannot update')
        if args['first_name']:
            student.first_name = args['first_name']
        if args['last_name']:
            student.last_name = args['last_name']
        session.commit()

        return student

    def delete(self, todo_id):
        session.query(Student).filter(Student.id == todo_id).delete()
        session.commit()

        return 'Student has been deleted', 204



api.add_resource(StudentAPI, '/students/<int:todo_id>')
api.add_resource(ToDoList, '/students')

if __name__  == '__main__':
    app.run(debug=True)