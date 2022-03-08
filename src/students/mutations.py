
import os
import sys
import graphene
from django.contrib.auth import get_user_model
from django.db import transaction, DatabaseError
from graphene import ID

from api.models import profile
from graphql_jwt.shortcuts import create_refresh_token, get_token
from .models import Student, StudentGrade
from plans.models import StudentPlan
from organization.models import School, Group
from kb.models.grades import Grade
from kb.models import AreaOfKnowledge
from guardians.models import Guardian
from audiences.models import Audience
from users.schema import UserSchema, UserProfileSchema
from .schema import StudentGradeSchema
from plans.models import GuardianStudentPlan


class CreateStudent(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
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
        guardian_student_plan_id = graphene.ID(required=True)
        list_subject_id = graphene.List(ID)

    def mutate(
            self,
            info,
            first_name,
            last_name,
            guardian_student_plan_id,
            list_subject_id,
            username,
            password,
            school=None,
            grade=None,
            group=None,
            dob=None,
            student_plan=None,
    ):

        try:
            with transaction.atomic():
                user = get_user_model()()

                student = Student(
                    first_name=first_name,
                    last_name=last_name,
                    full_name=first_name + ' ' + last_name,
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

                if(grade) :
                    grade = Grade.objects.get(pk = grade)
                    student_grade = StudentGrade(
                        student=student,
                        grade=grade,
                    )
                    student_grade.save();

                guardian_student_plan = GuardianStudentPlan.objects.get(pk=guardian_student_plan_id)

                guardian_student_plan.student_id = student.id
                for subject_id in list_subject_id:
                    subject = AreaOfKnowledge.objects.get(pk=subject_id)
                    guardian_student_plan.subject.add(subject)

                guardian_student_plan.save()

                student.guardian_id = guardian_student_plan.guardian.id
                student.save()

                profile_obj = profile.objects.get(user=user.id)
                token = get_token(user)
                refresh_token = create_refresh_token(user)

                return CreateStudent(
                    guardian=student.guardian,
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
    guardian = graphene.Field('guardians.schema.GuardianSchema')
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
                # user = info.context.user
                # if not user.is_authenticated:
                #     raise Exception("Authentication credentials were not provided")
                student = Student.objects.get(pk=student_id)
                student.user.set_password(password)
                student.user.save()

                profile_obj = profile.objects.get(user=student.user.id)

                return ChangeStudentPassword(
                    guardian=student.guardian,
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


class CreateChangeStudentGrade(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    student = graphene.Field('students.schema.StudentSchema')
    grade = graphene.Field('kb.schema.GradeSchema')
    student_grade = graphene.Field(StudentGradeSchema)

    class Arguments:
        grade_id = graphene.ID(required=True)
        student_id = graphene.ID(required=True)
        is_finished = graphene.Int(required=False)
        percentage = graphene.Float(required=False)
        complete_date = graphene.Date(required=False)
        is_active = graphene.Boolean(required=False)

    def mutate(
            self,
            info,
            grade_id,
            student_id,
            is_finished=None,
            percentage=None,
            complete_date=None,
            is_active=True):
        try:
            with transaction.atomic():
                # user = info.context.user
                # if not user.is_authenticated:
                #     raise Exception("Authentication credentials were not provided")

                student_grade, created = StudentGrade.objects.get_or_create(
                    grade_id=grade_id,
                    student_id=student_id
                )

                if is_finished:
                    student_grade.is_finished = is_finished

                if percentage:
                    student_grade.percentage = percentage

                if complete_date:
                    student_grade.complete_date = complete_date

                if not is_active:
                    student_grade.is_active = False

                student_grade.save()

                return CreateChangeStudentGrade(
                    guardian=student_grade.student.guardian,
                    student_grade=student_grade,
                    grade=student_grade.grade,
                    student=student_grade.student
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

# Increase Student's level by one
# Student's info comes from logined user info
#   Input: None
#   Output: {
#               studentSchema,
#               userSchema
#   }
class LevelUp(graphene.Mutation):
    student = graphene.Field('students.schema.StudentSchema')
    user = graphene.Field(UserSchema)
    # class Arguments:
    #     pass
    def mutate(self, info):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        if not user.student:
            raise Exception("Not found student")

        level_amount = user.student.level.amount
        next_level = user.student.level.__class__.objects.get(amount=level_amount + 1);
        if next_level :
            user.student.level = next_level;
            user.student.level.save();

        return LevelUp(user= user, student= user.student)

# Set Student's point
# Student's info comes from logined user info
#   Input: Point to set( int )
#   Output: {
#               studentSchema,
#               userSchema
#   }
class setPoint(graphene.Mutation):
    student = graphene.Field('students.schema.StudentSchema')
    user = graphene.Field(UserSchema)

    class Arguments:
        point_to_set = graphene.Int(required=False)

    def mutate(self, info, point_to_set):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        if not user.student:
            raise Exception("Not found student")

        student = user.student
        student.points = point_to_set
        student.save()

        return setPoint()
    pass

class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    change_student_password = ChangeStudentPassword.Field()
    create_change_student_grade = CreateChangeStudentGrade.Field()
    level_up = LevelUp.Field()
    set_point = setPoint.Field()
