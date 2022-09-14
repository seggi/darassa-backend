from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.database.model_marsh import StudentsSchema, UserSchema
from api.database.models import Students, User

from .. import db
from api.utils.responses import Response, response_with
from api.utils import responses as resp

manage_student = Blueprint("manage_student", __name__,
                           url_prefix="/api/student")

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
