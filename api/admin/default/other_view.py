from this import s
from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.database.model_marsh import ClassesSchema, LanguageSchema
from api.database.models import Classes, Language
from ... import db
from api.utils.responses import Response, response_with
from api.utils import responses as resp

default_data = Blueprint("default_data", __name__,
                         url_prefix="/api/user/admin")

language_schema = LanguageSchema()


@default_data.post('/add-language')
@jwt_required(refresh=True)
def add_languages():
    try:
        request_data = request.json

        language = db.session.query(Language).filter(
            Language.name == request_data["name"]).first()

        if request_data['name'] is None:
            return response_with(resp.INVALID_INPUT_422)

        if language:
            return Response.success(message="Language name already added.")

        new_data = {
            "name": request_data["name"],
        }

        languages = Language(**new_data)
        db.session.add(languages)
        db.session.commit()

        return Response.created(message="Language added with success.")

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@default_data.get('/retrieve-language')
@jwt_required(refresh=True)
def retrieve_languages():
    languages = []
    try:
        language_default_data = db.session.query(Language.name).all()
        for language in language_default_data:
            languages.append({
                **language_schema.dump(language),
            })

        return Response.success(message="success", data=languages)

    except Exception as e:
        return response_with(resp.BAD_REQUEST_400)
