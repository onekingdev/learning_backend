import os
import random
import sys
import graphene
from django.contrib.auth import get_user_model
from django.db import transaction, DatabaseError
from graphene import ID
from users.schema import UserSchema, UserProfileSchema
from organization.schema import ClassroomSchema, TeacherSchema
from organization.models import School, Group, Teacher, Classroom
from graphql_jwt.shortcuts import create_refresh_token, get_token
from payments.models import DiscountCode
from kb.models.grades import Grade
from audiences.models import Audience
from django.contrib.auth.models import User


class CreateTeacher(graphene.Mutation):
    teacher = graphene.Field(TeacherSchema)
    user = graphene.Field(UserSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        school_id = graphene.ID(required=True)
        zip = graphene.String(required=True)
        country = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        coupon_code = graphene.String(required=False)


    def mutate(
        self,
        info,
        first_name,
        last_name,
        school_id,
        zip,
        country,
        email,
        password,
        username,
        coupon_code=None,
    ):

        try:
            with transaction.atomic():
                school = School.objects.get(pk=school_id)
                user = get_user_model()(
                    username=username,
                )
                user.set_password(password)
                user.email = email
                user.save()

                teacher, new = Teacher.objects.get_or_create(
                    user=user,
                    name=first_name,
                    last_name=last_name,
                    school=school,
                    zip=zip,
                    country=country,
                )
                if coupon_code:
                    coupon_code = coupon_code.upper()
                    discount = DiscountCode.objects.get(code=coupon_code)
                    teacher.discountCode = discount

                teacher.save();
                
                token = get_token(user)
                refresh_token = create_refresh_token(user)
                
                return CreateTeacher(
                    teacher = teacher,
                    user = user,
                    token = graphene.String(),
                    refresh_token = graphene.String()
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateClassroom(graphene.Mutation):
    user = graphene.Field(UserSchema)
    classroom = graphene.Field(ClassroomSchema)
    class Arguments:
        name = graphene.String(required=True)
        grade_id = graphene.ID(required=True)
        teacher_id = graphene.ID(required=False)
        language = graphene.String(required=True)
        audience_id = graphene.ID(required=True)

    def mutate(
        self,
        info,
        name,
        grade_id,
        language,
        audience_id,
        teacher_id=None,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                grade = Grade.objects.get(pk=grade_id)
                audience = Audience.objects.get(pk=audience_id)
                if teacher_id:
                    teacher = Teacher.objects.get(pk=teacher_id)
                else:
                    teacher = user.schoolpersonnel;
                classroom, new = Classroom.objects.get_or_create(
                    name=name,
                    grade=grade,
                    language=language,
                    audience=audience,
                )
                classroom.teacherSet = teacher
                classroom.save()
                user = User.objects.get(pk=user.id)
                return CreateTeacher(
                    user = user,
                    classroom = classroom
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class Mutation(graphene.ObjectType):
    create_teacher = CreateTeacher.Field()