import os
from flask import jsonify, Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from api.cors.path import create_path
from api.database.model_marsh import UserSchema

from api.database.models import User, UserProfile
from api.utils.constants.default import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

from .. import db
from api.utils.responses import response_with
from api.utils import responses as resp


profile_view = Blueprint("profile_view", __name__,
                         url_prefix="/api/user")
user_schema = UserSchema()


@profile_view.post('/profile')
@jwt_required()
def user_update_profile():
    user_id = get_jwt_identity()['id']
    try:
        request_data = request.json
        user = User.query.filter_by(id=user_id).first()
        if user:
            user_info = user_schema.dump(user)
            if user_info['is_school'] == True:
                if request_data['name'] is None or request_data["username"] is None or request_data['picture'] is None:
                    return response_with(resp.INVALID_INPUT_422)
                update_user = {
                    "name": request_data['name'],
                    "username": request_data['username'],
                }
                save_profile = {
                    "user_id": user_id,
                    "country": request_data['country'],
                    "state": request_data['state'],
                    "city": request_data['city'],
                    "street": request_data['street']
                }
                User.query.filter_by(id=user_id).update(update_user)
                new_user_info = UserProfile(**save_profile)
                db.session.add(new_user_info)
                db.session.commit()
            return jsonify({
                "code": "success",
                "message": "Profile saved successfully. Now you can start your operation!"
            })
        else:
            return response_with(resp.UNAUTHORIZED_403)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_view.post('/upload-profile-image')
@jwt_required(refresh=True)
def upload_profile_image():
    user_id = get_jwt_identity()['id']
    request_file = request.files

    if 'file' not in request_file:
        resp = jsonify({
            "code": "Error",
            "message": "No file part in the request"
        })
        resp.status_code = 400
        return resp

    file = request.files['file']

    if file.filename == '':
        resp = jsonify({
            'message': 'No file selected for uploading'
        })
        resp.status_code = 400
        return resp

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path_name = {'user_id': user_id,
                     'picture': f'{UPLOAD_FOLDER}/{user_id}/{filename}'}

        path = create_path(directory=f'{UPLOAD_FOLDER}/{user_id}')
        if path == 200:
            picture = UserProfile.query.filter_by(
                picture=path_name['picture']).first()
            if picture:
                resp = jsonify({'message': 'File already exist.'})
                resp.status_code = 200
                return resp

            file.save(os.path.join(f'{UPLOAD_FOLDER}/{user_id}', filename))
            resp = jsonify({'message': 'File saved with success.'})
            user_picture = UserProfile(**path_name)
            db.session.add(user_picture)
            db.session.commit()

            resp.status_code = 201
            return resp

        picture = UserProfile.query.filter_by(
            picture=path_name['picture']).first()
        if picture:
            resp = jsonify({'message': 'File already exist.'})
            resp.status_code = 200
            return resp

        file.save(os.path.join(f'{UPLOAD_FOLDER}/{user_id}', filename))
        resp = jsonify({'message': 'File saved with success.'})
        user_picture = UserProfile(**path_name)
        db.session.add(user_picture)
        db.session.commit()

        resp.status_code = 201
        return resp

    else:
        resp = jsonify({
            'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'
        })
        resp.status_code = 400
        return resp
