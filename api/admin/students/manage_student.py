from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.database.model_marsh import StudentsSchema, UserSchema
from api.database.models import Students, User

from ... import db
from api.utils.responses import Response, response_with
from api.utils import responses as resp

manage_student = Blueprint("manage_student", __name__,
                           url_prefix="/api/user/admin")

user_schema = UserSchema()
student_schema = StudentsSchema()


@manage_student.post('/register-student')
@jwt_required(refresh=True)
def register_student():
    school_id = get_jwt_identity()['id']
    try:
        request_data = request.json

        if request_data['first_name'] is None or request_data['last_name'] is None or \
                request_data['birth_date'] is None:
            return response_with(resp.INVALID_INPUT_422)

        student = Students.query.filter_by(first_name=request_data['first_name'],
                                           last_name=request_data['last_name'], birth_date=request_data['birth_date']).first()

        if student:
            return Response.success(message="Student with this name already exist")

        new_data = {
            "school_id": school_id,
            "first_name": request_data['first_name'],
            "last_name": request_data["last_name"],
            "birth_date": request_data["birth_date"],
            "picture": request_data["picture"],
            "birth_country": request_data["birth_country"],
            "birth_city_village": request_data["birth_city_village"],
            "is_current_student": True,
        }
        register_student = Students(**new_data)
        db.session.add(register_student)
        db.session.commit()

        return Response.created(message="Student registered with success")

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)


@manage_student.put('/update-student/<int:student_id>')
@jwt_required(refresh=True)
def update_student(student_id):
    try:
        request_data = request.json

        if request_data['first_name'] is None or request_data['last_name'] is None or \
                request_data['birth_date'] is None:
            return response_with(resp.INVALID_INPUT_422)

        new_data = {
            "first_name": request_data['first_name'],
            "last_name": request_data["last_name"],
            "birth_date": request_data["birth_date"],
            "picture": request_data["picture"],
            "birth_country": request_data["birth_country"],
            "birth_city_village": request_data["birth_city_village"],
            "is_current_student": request_data["status"],
        }
        Students.query.filter_by(id=student_id).update(new_data)
        db.session.commit()

        return Response.created(message="Student Updated with success.")

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)


@manage_student.get('/retrieve-student')
@jwt_required(refresh=True)
def retrieve_student():
    school_id = get_jwt_identity()['id']
    student_data = []
    try:
        students = db.session.query(
            Students.first_name, Students.last_name,
            Students.birth_date, Students.id, Students.picture).\
            filter(Students.school_id == school_id).all()

        for student in students:
            student_data.append(student_schema.dump(student))

        return Response.success(message="Success", data=student_data)
    except Exception as e:
        print(e)
        return response_with(resp.BAD_REQUEST_400)
