from this import s
from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.database.model_marsh import ClassesSchema
from api.database.models import Classes
from ... import db
from api.utils.responses import Response, response_with
from api.utils import responses as resp

setup_static_info = Blueprint("setup_static_info", __name__,
                              url_prefix="/api/user/admin")

class_schema = ClassesSchema()


@setup_static_info.post('/setup-classes')
@jwt_required(refresh=True)
def setup_classes():
    school_id = get_jwt_identity()['id']
    try:
        request_data = request.json

        school_class = db.session.query(Classes).filter(
            Classes.name == request_data["name"]).first()

        if request_data['name'] is None:
            return response_with(resp.INVALID_INPUT_422)

        if school_class:
            return Response.success(message="Class name already added.")

        new_data = {
            "school_id": school_id,
            "name": request_data["name"],
            "level_id": request_data["level_id"]
        }

        school_classes = Classes(**new_data)
        db.session.add(school_classes)
        db.session.commit()

        return Response.created(message="Class added with success.")

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@setup_static_info.get('/retrieve-classes')
@jwt_required(refresh=True)
def retrieve_classes():
    school_id = get_jwt_identity()['id']
    school_data = []
    try:
        school_default_data = db.session.query(Classes.name).filter(
            Classes.school_id == school_id).all()

        for school_class in school_default_data:
            school_data.append({
                **class_schema.dump(school_class),
            })

        return Response.success(message="success", data=school_data)

    except Exception as e:
        return response_with(resp.BAD_REQUEST_400)
