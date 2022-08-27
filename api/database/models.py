from datetime import datetime
from email.policy import default
from pydoc import describe
from tokenize import group
from sqlalchemy import (
    Column, Integer, DateTime, Boolean, String, Float, Text, ForeignKey, LargeBinary
)
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import backref


from .. import db


class Country(db.Model):
    __tablename__ = "country"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class State(db.Model):
    __tablename__ = "state"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class Cities(db.Model):
    __tablename__ = "cities"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    state_id = Column(Integer, ForeignKey("state.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class Language(db.Model):
    __tablename__ = "languages"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    default = Column(Boolean(), default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())


class Currency(db.Model):
    __tablename__ = "currency"
    id = Column('id', Integer, primary_key=True)
    code = Column(String(10), nullable=False)
    description = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())


class Modules(db.Model):
    __tablename__ = "modules"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class SalaryType(db.Model):
    __tablename__ = "salary_type"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class Gender(db.Model):
    __tablename__ = "gender"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


# ! Fee , Transport  and etc

class FeeType(db.Model):
    __tablename__ = "fee_type"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class PaymentCategory(db.Model):
    __tablename__ = "payment_category"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class User(db.Model):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    username = Column(String(20), nullable=True, unique=False)
    email = Column(String(128), unique=True, nullable=True)
    first_name = Column(String(50), unique=False, nullable=True)
    last_name = Column(String(50), unique=False, nullable=True)
    birth_date = Column(String(10), unique=False, nullable=False)
    phone = Column(String(20), nullable=True, unique=True)
    is_admin = Column(Boolean(), default=False)
    is_parent = Column(Boolean(), default=False)
    is_employee = Column(Boolean(), default=False)
    status = Column(Boolean(), default=False)
    language = Column(Integer, ForeignKey("languages.id"), nullable=True)
    password = Column(Text(), nullable=True)
    status = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())
    confirmed = Column(Boolean(), nullable=False, default=False)
    confirmed_on = Column(DateTime(timezone=True),
                          default=func.now(), nullable=True)
    profile = db.relationship("UserProfile", backref="user", lazy=True)
    expense = db.relationship(
        "Expenses", backref=backref("users", lazy="joined"))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserProfile(db.Model):
    __tablename__ = "user_profile"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    gender = Column(String(8), nullable=True)
    country = Column(Integer, ForeignKey("country.id"), nullable=True)
    state = Column(Integer, ForeignKey('state.id'), nullable=True)
    city = Column(Integer, ForeignKey('cities.id'), nullable=True)
    picture = Column(Text(), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class UserDefaultCurrency(db.Model):
    __tablename__ = "user_default_currency"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)


class UserSpokenLanguage(db.Model):
    __tablename__ = "user_spoken_language"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    languages_id = Column(Integer, ForeignKey('languages.id'))
    created_at = Column(DateTime(timezone=True), default=func.now())


class Classes(db.Model):
    __tablename__ = 'classes'
    id = Column('id', Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())
    deleted_at = Column(DateTime(timezone=True), default=func.now())


class ClassModules(db.Model):
    __tablename__ = "class_modules"
    id = Column('id', Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    name = Column(String(200), nullable=True)
    hours = Column(String(200), nullable=True)
    grades = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())
    deleted_at = Column(DateTime(timezone=True))


class Students(db.Model):
    __tablename__ = "students"
    id = Column('id', Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    first_name = Column(String(50), unique=False, nullable=True)
    last_name = Column(String(50), unique=False, nullable=True)
    birth_date = Column(String(10), unique=False, nullable=True)
    picture = Column(String(500), nullable=True)
    birth_country = Column(String(200), nullable=True)
    birth_city_village = Column(String(200), nullable=True)
    is_current_student = Column(Boolean(), default=False)
    left_at = Column(DateTime(timezone=True))
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class StudentAddress(db.Model):
    __tablename__ = "student_address"
    id = Column('id', Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    country = Column(String(200), nullable=True)
    state = Column(String(200), nullable=True)
    city = Column(String(200), nullable=True)
    street = Column(String(200), nullable=True)
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class StudentParent(db.Model):
    __tablename__ = "student_parent"
    id = Column('id', Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    father_full_name = Column(String(500), nullable=True)
    mother_full_name = Column(String(500), nullable=True)
    email = Column(String(200), nullable=True)
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class BussSubscription(db.Model):
    __tablename__ = "buss_subscription"
    id = Column('id', Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=True)
    left_at = Column(DateTime(timezone=True))
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class BussAttendance(db.Model):
    __tablename__ = "buss_attendance"
    id = Column('id', Integer, primary_key=True)
    student_scr_id = Column(Integer, ForeignKey(
        'buss_attendance.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    picked = Column(Boolean(), default=False)
    arrived = Column(Boolean(), default=False)
    picked_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    arrived_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class StudentPayment(db.Model):
    __tablename__ = "student_payment"
    id = Column('id', Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=True)
    fee_type_id = Column(Integer, ForeignKey('fee_type.id'), nullable=True)
    payment_category = Column(Integer, ForeignKey(
        'payment_category.id'), nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    amount = Column(Float(),  nullable=True)
    description = Column(String(500), nullable=True)
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class StudentLevel(db.Model):
    __tablename__ = "student_level"
    id = Column('id', Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=True)
    current_level = Column(Boolean(), default=False)
    year_range = Column(String(200), nullable=True)
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class MarksEvaluation(db.Model):
    __tablename__ = "marks_evaluation"
    id = Column('id', Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=True)
    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    score = Column(Float(), nullable=True)
    grade = Column(Float(), nullable=True)
    year_range = Column(String(200), nullable=True)
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class TeacherClasses(db.Model):
    __tablename__ = "teacher_class"
    id = Column('id', Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class TeacherModules(db.Model):
    __tablename__ = "teacher_modules"
    id = Column('id', Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    teacher_class_id = Column(Integer, ForeignKey(
        'teacher_class.id'), nullable=True)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class EmployeeSalary(db.Model):
    __tablename__ = "employee_salary"
    id = Column('id', Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float(),  nullable=True)
    month = Column(String(20),  nullable=True)
    salary_type_id = Column(Integer, ForeignKey(
        'salary_type.id'), nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class EmployeePayment(db.Model):
    __tablename__ = "employee_payment"
    id = Column('id', Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float(),  nullable=True)
    description = Column(String(500), nullable=True)
    month = Column(String(20),  nullable=True)
    year = Column(String(20), nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())


class CashReport(db.Model):
    __tablename__ = "cash_report"
    id = Column('id', Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    debit = Column(Float(),  nullable=True)
    credit = Column(Float(),  nullable=True)
    amount = Column(Float(),  nullable=True)
    description = Column(String(500), nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
    updated_at = deleted_at = Column(
        DateTime(timezone=True), default=func.now())
