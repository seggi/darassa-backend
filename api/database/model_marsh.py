from marshmallow import fields

from .. import db
from .. import marsh

from .models import (
    AdminAddEmployee, BussAttendance, BussSubscription,
    CashReport, ChatImageContent, ChatMessageContent,
    ChatVideoContent, ClassModules,
    Classes, Currency,
    EmployeePayment, EmployeeSalary,
    FeeType, Gender, Language, MarksEvaluation,
    ParentAddStudentSchool, ParentFollowUpChat,
    PaymentCategory, SalaryType, SchoolLevel, Modules,
    SchoolLevelOrganize, StudentAddress, StudentLevel,
    StudentParent, StudentPayment, Students, TeacherClasses,
    TeacherModules, User, UserDefaultCurrency, UserProfile,
    UserSpokenLanguage)


class LanguageSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Language
        include_relationships = True
        load_instance = True


class CurrencySchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Currency
        include_relationships = True
        load_instance = True


class LanguageSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Language
        include_relationships = True
        load_instance = True


class GenderSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Gender
        include_relationships = True
        load_instance = True


class UserSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
        include_relationships = True
        load_instance = True
        include_fk = True


class UserProfileSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserProfile
        sqla_session = db.session
        include_relationships = True
        load_instance = True
        include_fk = True


class AdminAddEmployeeSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = AdminAddEmployee
        sqla_session = db.session
        include_relationships = True
        load_instance = True
        include_fk = True


class ModulesSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Modules
        include_relationships = True
        load_instance = True


class SalaryTypeSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = SalaryType
        include_relationships = True
        load_instance = True


class FeeTypeSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = FeeType
        include_relationships = True
        load_instance = True


class PaymentCategorySchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = PaymentCategory
        include_relationships = True
        load_instance = True


class SchoolLevelSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = SchoolLevel
        include_relationships = True
        load_instance = True


class SchoolLevelOrganizeSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = SchoolLevelOrganize
        include_relationships = True
        load_instance = True


class UserDefaultCurrencySchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDefaultCurrency
        include_relationships = True
        load_instance = True


class UserSpokenLanguageSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserSpokenLanguage
        include_relationships = True
        load_instance = True


class ClassesSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Classes
        include_relationships = True
        load_instance = True


class ClassModulesSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ClassModules
        include_relationships = True
        load_instance = True


class StudentsSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Students
        include_relationships = True
        load_instance = True


class StudentAddressSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentAddress
        include_relationships = True
        load_instance = True


class StudentParentSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentParent
        include_relationships = True
        load_instance = True


class StudentPaymentSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentPayment
        include_relationships = True
        load_instance = True


class StudentLevelSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentLevel
        include_relationships = True
        load_instance = True


class MarksEvaluationSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = MarksEvaluation
        include_relationships = True
        load_instance = True


class TeacherClassesSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = TeacherClasses
        include_relationships = True
        load_instance = True


class TeachModulesSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = TeacherModules
        include_relationships = True
        load_instance = True


class EmployeeSalarySchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeeSalary
        include_relationships = True
        load_instance = True


class EmployeePaymentSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = EmployeePayment
        include_relationships = True
        load_instance = True


class CashReportSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = CashReport
        include_relationships = True
        load_instance = True


class ParentAddStudentSchoolSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ParentAddStudentSchool
        include_relationships = True
        load_instance = True


class BussSubscriptionSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = BussSubscription
        include_relationships = True
        load_instance = True


class BussAttendanceSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = BussAttendance
        include_relationships = True
        load_instance = True


class ParentFollowUpChatSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ParentFollowUpChat
        include_relationships = True
        load_instance = True


class ChatMessageContentSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ChatMessageContent
        include_relationships = True
        load_instance = True


class ChatVideoContentSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ChatVideoContent
        include_relationships = True
        load_instance = True


class ChatImageContentSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ChatImageContent
        include_relationships = True
        load_instance = True
