from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.database.model_marsh import UserProfileSchema, UserSchema
from api.database.models import AdminAddEmployee, User, UserProfile

from .. import db
from api.utils.responses import Response, response_with
from api.utils import responses as resp

admin_view = Blueprint("admin_view", __name__,
                       url_prefix="/api/user/admin")

user_schema = UserSchema()
user_profile_schema = UserProfileSchema()


@admin_view.post('/admin-create-employee')
@jwt_required(refresh=True)
def create_employee_account():
    user_id = get_jwt_identity()['id']
    try:
        request_data = request.json

        if request_data["username"] is None or request_data["email"] is None:
            return response_with(resp.INVALID_INPUT_422)

        check_user = db.session.query(User).filter(
            User.email == request_data['email']).first()
        if check_user:
            return Response.success(message="User already exist.")

        new_request_data = {
            "first_name": request_data['first_name'],
            "last_name": request_data['last_name'],
            "email": request_data['email'],
            "is_employee": True
        }

        new_user = User(**new_request_data)
        db.session.add(new_user)
        db.session.commit()

        add_employee = AdminAddEmployee(**{
            "school_id": user_id,
            "employee_id": new_user.id
        })
        db.session.add(add_employee)
        db.session.commit()

        add_employee = UserProfile(**{
            "user_id": new_user.id,
        })
        db.session.add(add_employee)
        db.session.commit()

        return Response.created(message="User created.")

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)


@admin_view.get('/retrieve-employee')
@jwt_required(refresh=True)
def retrieve_employees():
    school_id = get_jwt_identity()['id']
    employee_list = []
    try:
        employees = db.session.query(
            User.first_name, User.last_name,
            User.id, User.email, User.birth_date,
            UserProfile.picture,
            AdminAddEmployee).\
            join(User, AdminAddEmployee.employee_id == User.id).\
            join(UserProfile, User.id == UserProfile.user_id).\
            filter(AdminAddEmployee.school_id == school_id).all()

        for employee in employees:
            employee_list.append({
                **user_schema.dump(employee),
                **user_profile_schema.dump(employee)
            })

        return Response.success(message="Success", data=employee_list)

    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_500)
