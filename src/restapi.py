from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, reqparse, abort
from models import session, Student
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)

app.config['SWAGGER'] = {
    'title': 'University API',
    'uiversion': 2
}
swagger = Swagger(app)

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

@api.resource('/students')
class ToDoList(Resource):

    def get(self):
        """
        This returns an array of student model from database
        ---
        responses:
          200:
            description: An array of student model from database
        """
        students = session.query(Student).all()
        todos = [[student.id, student.group_id, student.first_name, student.last_name] for student in students]

        return todos

@api.resource('/students/<int:student_id>')
class StudentAPI(Resource):

    @marshal_with(resource_fields)
    def get(self, student_id):
        """
        This returns a student row by id from student model in database
        ---
        parameters:
          - in: path
            name: student_id
            type: integer
            required: true
        responses:
          200:
            description: A single user item
            schema:
              id: User
              properties:
                student_id:
                  type: integer
                  description: info about student
                  default: Steven Wilson
        """
        student = session.query(Student).get(student_id)
        if not student:
            abort(404, message="Could not find student with that id")

        return student

    @marshal_with(resource_fields)
    def post(self):
        """
        Add a student to database
        ---
        parameters:
          - in: body
            name: student
            description: student to create
            schema:
              type: object
              required:
                - first_name
                - last_name
              properties:
                first_name:
                  type: string
                last_name:
                  type: string
        responses:
          201:
            description: Student has been created
        """
        args = post_parser.parse_args()

        todo = Student(**args)
        session.add(todo)
        session.commit()
        student = session.query(Student).filter(
            Student.first_name == args['first_name'], Student.last_name == args['last_name']
        ).first()
        return student, 201

    @marshal_with(resource_fields)
    def put(self, student_id):
        """
        Update a student from database
        ---
        parameters:
          - in: body
            name: student
            description: data to update
            schema:
              type: object
              required:
                - first_name
                - last_name
              properties:
                first_name:
                  type: string
                last_name:
                  type: string
          - in: path
            name: student_id
            type: integer
            required: true
        responses:
          201:
            description: Student has been updated
        """
        args = put_parser.parse_args()
        student = session.query(Student).filter_by(id=student_id).first()
        if not student:
            abort(404, message='Student do not exist, cannot update')
        if args['first_name']:
            student.first_name = args['first_name']
        if args['last_name']:
            student.last_name = args['last_name']
        session.commit()
        student = session.query(Student).get(student_id)
        return student, 201

    def delete(self, student_id):
        """
        Deletes a student from student model
        ---
        parameters:
          - in: path
            name: student_id
            type: string
            required: true
        responses:
          204:
            description: Student deleted
        """
        session.query(Student).filter(Student.id == student_id).delete()
        session.commit()

        return 'Student has been deleted', 204


if __name__ == '__main__':
    app.run(debug=True)