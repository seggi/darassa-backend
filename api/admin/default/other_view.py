from this import s
from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.database.model_marsh import ClassesSchema, CurrencySchema, LanguageSchema, ModulesSchema
from api.database.models import Classes, Currency, Language, Modules
from ... import db
from api.utils.responses import Response, response_with
from api.utils import responses as resp

default_data = Blueprint("default_data", __name__,
                         url_prefix="/api/user/admin")

language_schema = LanguageSchema()
currency_schema = CurrencySchema()
module_schema = ModulesSchema()


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


@default_data.post('/add-module')
@jwt_required(refresh=True)
def add_module():
    try:
        request_data = request.json

        module = db.session.query(Modules).filter(
            Modules.name == request_data["name"]).first()

        if request_data['name'] is None:
            return response_with(resp.INVALID_INPUT_422)

        if module:
            return Response.success(message="Module already added.")

        new_data = {
            "name": request_data["name"],
        }

        modules = Modules(**new_data)
        db.session.add(modules)
        db.session.commit()

        return Response.created(message="Module added with success.")

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@default_data.get('/retrieve-default-data')
@jwt_required(refresh=True)
def retrieve_module():
    module_data = []
    currency_data = []
    languages = []
    try:
        module_default_data = db.session.query(
            Modules.name, Modules.id).all()
        for module in module_default_data:
            module_data.append({
                **module_schema.dump(module)
            })

        language_default_data = db.session.query(
            Language.name, Language.id).all()
        for language in language_default_data:
            languages.append({
                **language_schema.dump(language),
            })

        currency_default_data = db.session.query(
            Currency.code, Currency.id).all()
        for currency in currency_default_data:
            currency_data.append({
                **currency_schema.dump(currency)
            })

        default_data = {
            "module": module_data,
            "currency_data": currency_data,
            "languages": languages
        }

        return Response.success(message="success", data=default_data)

    except Exception as e:
        print(e)
        return response_with(resp.BAD_REQUEST_400)
