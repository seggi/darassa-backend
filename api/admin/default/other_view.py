from this import s
from flask import Blueprint, jsonify
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from itsdangerous import json
from api.cors.language import ManageLanguage
from api.database.model_marsh import ClassesSchema, CurrencySchema, FeeTypeSchema, GenderSchema, LanguageSchema, ModulesSchema, PaymentCategorySchema, SalaryTypeSchema, SchoolLevelSchema
from api.database.models import Classes, Currency, FeeType, Gender, Language, Modules, PaymentCategory, SalaryType, SchoolLevel
from ... import db
from api.utils.responses import Response, response_with
from api.utils import responses as resp

default_data = Blueprint("default_data", __name__,
                         url_prefix="/api/user/admin")

language_schema = LanguageSchema()
currency_schema = CurrencySchema()
module_schema = ModulesSchema()
salary_type_schema = SalaryTypeSchema()
gender_schema = GenderSchema()
fee_type_schema = FeeTypeSchema()
payment_schema = PaymentCategorySchema()
school_level_schema = SchoolLevelSchema()


@default_data.post('/add-language/<string:language>')
# @jwt_required(refresh=True)
def add_languages(language):
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

        selected_language = ManageLanguage(
            language, 'Language added with success.')
        return Response.created(message=selected_language.manage_language())

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


@default_data.post('/add-salary-type')
@jwt_required(refresh=True)
def add_salary_type():
    try:
        request_data = request.json

        salary_type = db.session.query(SalaryType).filter(
            SalaryType.name == request_data["name"]).first()

        if request_data['name'] is None:
            return response_with(resp.INVALID_INPUT_422)

        if salary_type:
            return Response.success(message="Salary type already added.")

        new_data = {
            "name": request_data["name"],
        }

        salary_types = SalaryType(**new_data)
        db.session.add(salary_types)
        db.session.commit()

        return Response.created(message="Salary type added with success.")

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@default_data.post('/add-fee-type')
@jwt_required(refresh=True)
def add_fee_type():
    try:
        request_data = request.json

        fee_type = db.session.query(FeeType).filter(
            FeeType.name == request_data["name"]).first()

        if request_data['name'] is None:
            return response_with(resp.INVALID_INPUT_422)

        if fee_type:
            return Response.success(message="Fee type already added.")

        new_data = {
            "name": request_data["name"],
        }

        fee_types = FeeType(**new_data)
        db.session.add(fee_types)
        db.session.commit()

        return Response.created(message="Fee type added with success.")

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@default_data.post('/add-payment-category')
@jwt_required(refresh=True)
def add_payment_category():
    try:
        request_data = request.json

        payment_category = db.session.query(PaymentCategory).filter(
            PaymentCategory.name == request_data["name"]).first()

        if request_data['name'] is None:
            return response_with(resp.INVALID_INPUT_422)

        if payment_category:
            return Response.success(message="Payment category already added.")

        new_data = {
            "name": request_data["name"],
        }

        payment_category = PaymentCategory(**new_data)
        db.session.add(payment_category)
        db.session.commit()

        return Response.created(message="Payment category added with success.")

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@default_data.get('/retrieve-default-data')
@jwt_required(refresh=True)
def retrieve_module():
    module_data = []
    currency_data = []
    languages = []
    salary_type_data = []
    gender_data_list = []
    fee_type_data_list = []
    payment_category = []
    school_levels = []
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

        salary_type_default_data = db.session.query(
            SalaryType.name, SalaryType.id).all()
        for salary_type in salary_type_default_data:
            salary_type_data.append({
                **salary_type_schema.dump(salary_type)
            })

        gender_data = db.session.query(
            Gender.name, Gender.id).all()
        for gender_data in gender_data:
            gender_data_list.append({
                **gender_schema.dump(gender_data)
            })

        fee_type_data = db.session.query(
            FeeType.name, FeeType.id).all()
        for fee_data in fee_type_data:
            fee_type_data_list.append({
                **fee_type_schema.dump(fee_data)
            })

        payment_category_data = db.session.query(
            PaymentCategory.name, PaymentCategory.id).all()
        for payment_data in payment_category_data:
            payment_category.append({
                **payment_schema.dump(payment_data)
            })

        school_level_data = db.session.query(
            SchoolLevel.name, SchoolLevel.id).all()
        for school_level in school_level_data:
            school_levels.append({
                **school_level_schema.dump(school_level)
            })

        default_data = {
            "module": module_data,
            "currency_data": currency_data,
            "languages": languages,
            "gender": gender_data_list,
            "fee_type": fee_type_data_list,
            "payment_category": payment_category,
            "school_level": school_levels
        }

        return Response.success(message="success", data=default_data)

    except Exception as e:
        print(e)
        return response_with(resp.BAD_REQUEST_400)
