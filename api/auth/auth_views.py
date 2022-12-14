from tabnanny import check
from ..utils.sms.sms import send_bulk_sms
from ..utils.sms.response import response, error_response
from ..utils.sms.request import validate_body
from api.utils.token import confirm_verification_token, generate_verification_token
from api.utils import responses as resp
from api.utils.responses import Response, response_with

from .. import db
from flask import Blueprint, request, jsonify, url_for, render_template_string
from dotenv import load_dotenv
from api.database.model_marsh import AdminAddEmployeeSchema, UserSchema
from api.database.models import AdminAddEmployee, User
from api.utils.email import send_email
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

load_dotenv()

auth = Blueprint("auth", __name__, url_prefix="/api/user")

user_schema = UserSchema()
admin_add_employee_schema = AdminAddEmployeeSchema()


@auth.post('/signup')
def login():
    try:
        data = {
            "email": request.json["email"],
            "phone": request.json["phone"],
            "name": request.json['name'],
            "is_school": request.json['is_school'],
            "is_parent": request.json['is_parent'],
            "is_employee": request.json["is_employee"],
            "username": request.json["username"],
            "password": request.json["password"]
        }

        if data["email"] is None or data['username'] is None:
            return response_with(resp.INVALID_INPUT_422)
        if data["phone"] is None or data['password'] is None:
            return response_with(resp.INVALID_INPUT_422)

        data['password'] = User.generate_hash(data['password'])

        user_data = user_schema.load(data, partial=True)
        token = generate_verification_token(data['email'])

        # Send Email

        verification_email = url_for(
            'auth.verify_email', token=token, _external=True)

        html = render_template_string(
            """
            <div>
                <h2>Welcome to  DARASSA</h2>
                <p>
                    Thank you for sign up to our app.
                    Please click the button below to activate your account:
                </p>
                <p>
                    <a href='{{ verification_email }}'
                        style='padding: 8px; background: blue; width: 20px; color: white; text-decoration: none;'>Confirm Signup</a>
                </p>
                <br/>
                <p> Thanks!</p>
            </div>
            """, verification_email=verification_email)

        subject = "Please Verify your email"
        send_email(user_data.email, subject, html)

        # Send SMS
        message = "Thank you for sign up to DARASSA APP"
        send_bulk_sms(data['phone'], message)
        user_data.create()
        return response_with(resp.SUCCESS_200)

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)


@auth.post('/employee-set-password')
def employee_set_pwd():
    try:
        request_data = request.json

        if request_data["email"] is None or request_data['password'] is None:
            return response_with(resp.INVALID_INPUT_422)

        hash_password = User.generate_hash(request_data['password'])
        new_request_data = {
            "username": request_data["username"],
            "password": hash_password,
            "confirmed": True
        }

        user = db.session.query(User.id).filter(
            User.email == request_data["email"]).first()
        user_data = user_schema.dump(user)
        if user:
            User.query.filter_by(
                id=user_data['id']).update(new_request_data)
            AdminAddEmployee.query.filter_by(
                employee_id=user_data['id']).update({"login_status": True})
            db.session.commit()
            return Response.success('Password updated.')

        return Response.failed(message="User not found.")

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

# Verification token


@auth.get('/confirm/<token>')
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except:
        return response_with(resp.SERVER_ERROR_404)

    user = User.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        return response_with(resp.INVALID_INPUT_422)
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        return render_template_string("<p>E-mail verified, you can proceed to login now.<p/>")


# Refresh token

@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

# Login


@auth.post('/login')
def sign_in_user():
    try:
        data = {
            "email": request.json["email"],
            "password": request.json["password"]
        }

        if data['email']:
            current_user = User.find_by_email(data['email'])
            user_info = user_schema.dump(current_user)

            if user_info['is_employee'] == True:
                check_status = db.session.query(AdminAddEmployee).filter(
                    AdminAddEmployee.employee_id == user_info['id']).first()
                status = admin_add_employee_schema.dump(check_status)

                if status['login_status'] == False:
                    return Response.success(message="You have to set your password.", data=[{'status': False}])

        if not current_user:
            return response_with(resp.SERVER_ERROR_404)

        if current_user and not current_user.confirmed:
            return response_with(resp.BAD_REQUEST_400)

        if User.verify_hash(data['password'], current_user.password):
            user = User.query.filter_by(email=data['email']).first()
            access_token = create_access_token(
                identity={"id": user.id, "email": data["email"]})
            access_fresh_token = create_refresh_token(
                identity={"id": user.id, "email": data["email"]})

            return response_with(resp.
                                 SUCCESS_201, value={'message': f'{current_user.username}',
                                                     "access_token": access_token,
                                                     "access_fresh_token": access_fresh_token,
                                                     "data": {
                                                         "username": user.username,
                                                         "status": user.status,
                                                         "user_id": user.id
                                                     }
                                                     }
                                 )
        else:
            return response_with(resp.UNAUTHORIZED_403)

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
