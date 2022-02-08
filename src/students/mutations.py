import os
import sys
import graphene
from django.contrib.auth import get_user_model
from django.db import transaction, DatabaseError
from api.models import profile
from graphql_jwt.shortcuts import create_refresh_token, get_token
from .models import Student
from plans.models import StudentPlan
from organization.models import School, Group
from kb.models.grades import Grade
from audiences.models import Audience
from users.schema import UserSchema, UserProfileSchema


class CreateStudent(graphene.Mutation):
    student = graphene.Field('students.schema.StudentSchema')
    user = graphene.Field(UserSchema)
    profile = graphene.Field(UserProfileSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=False)
        password = graphene.String(required=False)
        school = graphene.ID(required=False)
        grade = graphene.ID(required=False)
        group = graphene.ID(required=False)
        dob = graphene.Date(required=False)
        student_plan = graphene.ID(required=False)

    def mutate(
            self,
            info,
            first_name,
            last_name,
            username,
            password,
            school,
            grade,
            group,
            dob,
            student_plan):

        try:
            with transaction.atomic():
                user = get_user_model()()
                student = Student(
                    first_name=first_name,
                    last_name=last_name,
                    full_name=first_name + ' ' + last_name
                )

                if username:
                    user.username = username
                else:
                    count = 1
                    while True:
                        if get_user_model().objects.get(username=username).exists():
                            count += 1
                        else:
                            break
                    user.username = first_name + last_name + count

                if password:
                    user.set_password(password)
                else:
                    user.set_unusable_password()

                user.save()

                student.user = user

                if dob:
                    student.dob = dob

                student.save()

                # Student Plan
                if student_plan:
                    pass
                elif school:
                    student_plan = School.objects.get(school).student_plan
                elif group:
                    audience = Group.objects.get(group).audience
                    student_plan = Audience.objects.get(audience).student_plan
                elif grade:
                    audience = Grade.objects.get(grade).audience
                    student_plan = Audience.objects.get(audience).student_plan
                else:
                    student_plan = StudentPlan.objects.get_or_create(
                        name='Default Plan')

                student_plan = StudentPlan.objects.get(pk=student_plan)
                student.student_plan.add(student_plan)

                student.save()

                profile_obj = profile.objects.get(user=user.id)
                token = get_token(user)
                refresh_token = create_refresh_token(user)

                return CreateStudent(
                    student=student,
                    user=user,
                    profile=profile_obj,
                    token=token,
                    refresh_token=refresh_token
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


class ChangeStudentPassword(graphene.Mutation):
    student = graphene.Field('students.schema.StudentSchema')
    user = graphene.Field(UserSchema)
    profile = graphene.Field(UserProfileSchema)

    class Arguments:
        student_id = graphene.ID(required=True)
        password = graphene.String(required=True)

    def mutate(
            self,
            info,
            student_id,
            password):
        try:
            with transaction.atomic():
                student = Student.objects.get(pk=student_id)
                student.user.set_password(password)
                student.user.save()

                profile_obj = profile.objects.get(user=student.user.id)

                return ChangeStudentPassword(
                    student=student,
                    user=student.user,
                    profile=profile_obj,
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


# class ChangeStudentGrade(graphene.Mutation):
#     student = graphene.Field('students.schema.StudentSchema')
#
#     class Arguments:
#         student_id = graphene.ID(required=True)
#         grade_id = graphene.ID(required=True)
#
#     def mutate(
#             self,
#             info,
#             student_id,
#             password):
#         try:
#             with transaction.atomic():
#                 student = Student.objects.get(pk=student_id)
#                 student.user.set_password(password)
#                 student.user.save()
#
#                 profile_obj = profile.objects.get(user=student.user.id)
#
#                 return ChangeStudentPassword(
#                     student=student,
#                     user=student.user,
#                     profile=profile_obj,
#                 )
#         except (Exception, DatabaseError) as e:
#             transaction.rollback()
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
#             return e


class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    change_student_password = ChangeStudentPassword.Field()
