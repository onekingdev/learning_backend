import os
import random
from re import sub
import sys
import graphene
from django.contrib.auth import get_user_model
from django.db import transaction, DatabaseError
from graphene import ID
from block.models import BlockPresentation
from organization.models.schools import SchoolPersonnel, SchoolSubscriber, SchoolTeacher, Subscriber, TeacherClassroom
from users.schema import UserSchema, UserProfileSchema
from organization.schema import AdministrativePersonnelSchema, ClassroomSchema, SchoolPersonnelSchema, SchoolSchema, SubscriberSchema, TeacherSchema, GroupSchema
from organization.models import School, Group, Teacher, Classroom, AdministrativePersonnel
from graphql_jwt.shortcuts import create_refresh_token, get_token
from payments.models import DiscountCode
from kb.models.grades import Grade
from audiences.models import Audience
from users.models import User
from students.models import Student, StudentGrade
from students.schema import StudentSchema
from django.utils import timezone
from pytz import timezone as pytz_timezone
import datetime
from django.db.models.query_utils import Q
from django.db.models import Sum, Count

class CreateTeacherInput(graphene.InputObjectType):
    email = graphene.String()
    name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()
    gender = graphene.String()
    user_type = graphene.String()
    username = graphene.String()

class CreateTeacher(graphene.Mutation):
    """Create a user account for teacher API"""
    teacher = graphene.Field(TeacherSchema)
    user = graphene.Field(UserSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        school_id = graphene.ID(required=False)
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
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email = email,
                )
                user.set_password(password)
                user.save()

                teacher= Teacher(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    zip=zip,
                    country=country,
                )
                if coupon_code:
                    coupon_code = coupon_code.upper()
                    discount = DiscountCode.objects.get(code=coupon_code)
                    teacher.discountCode = discount

                teacher.save();
                SchoolTeacher.objects.create(
                    school = school,
                    teacher = teacher
                )

                if user.profile :
                    user.profile.role = "teacher"
                    user.profile.save()
                
                token = get_token(user)
                refresh_token = create_refresh_token(user)
                
                return CreateTeacher(
                    teacher = teacher,
                    user = user,
                    token = token,
                    refresh_token = refresh_token
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateClassroom(graphene.Mutation):
    """Create a classroom for a specific teacher API"""
    user = graphene.Field(UserSchema)
    classroom = graphene.Field(ClassroomSchema)
    teacher = graphene.Field(TeacherSchema)
    class Arguments:
        name = graphene.String(required=True)
        # grade_id = graphene.ID(required=True)
        teacher_id = graphene.ID(required=False)
        # language = graphene.String(required=True)
        audience_id = graphene.ID(required=True)

    def mutate(
        self,
        info,
        name,
        audience_id,
        teacher_id=None,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                # grade = Grade.objects.get(pk=grade_id)
                audience = Audience.objects.get(pk=audience_id)
                if teacher_id:
                    teacher = Teacher.objects.get(pk=teacher_id)
                else:
                    teacher = user.schoolpersonnel.teacher;
                
                classroom = Classroom(
                    name=name,
                    # grade=grade,
                    # language=language,
                    audience=audience,
                )
                # classroom.teacher = teacher
                classroom.save()
                
                teacher_classrooms = TeacherClassroom.objects.filter(teacher = teacher, classroom = None)

                if(len(teacher_classrooms) < 1):
                    raise Exception("The number of Classrooms has been exceeded! Please buy a new classroom")
                teacher_classrooms[0].classroom = classroom
                teacher_classrooms[0].save()

                return CreateClassroom(
                    user = user,
                    classroom = classroom,
                    teacher = teacher
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateSchool(graphene.Mutation):
    """Create a school with user account for subscriber of school API"""
    user = graphene.Field(UserSchema)
    school = graphene.Field(SchoolSchema)
    subscriber = graphene.Field(SubscriberSchema)
    token = graphene.String()
    refresh_token = graphene.String()
    class Arguments:
        name = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        district = graphene.String(required=True)
        type = graphene.String(required=True)
        zip = graphene.String(required=True)
        country = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        username = graphene.String(required=True)
        coupon_code = graphene.String(required=False)

    def mutate(
        self,
        info,
        name,
        first_name,
        last_name,
        district,
        type,
        zip,
        country,
        email,
        password,
        username,
        coupon_code = None
    ):

        try:
            with transaction.atomic():

                school = School(
                    name = name,
                    type_of = type,
                    zip = zip,
                    country = country,
                    district = district,
                )
                school.save()
                user = get_user_model()(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                )
                user.set_password(password)
                user.email = email
                user.save()
                subscriber = Subscriber(
                    user = user,
                    first_name = first_name,
                    last_name = last_name,
                    
                )
                if coupon_code:
                    subscriber.coupon_code = DiscountCode.objects.get(code=coupon_code)
                subscriber.save()
                SchoolSubscriber.objects.create(
                    subscriber = subscriber,
                    school = school
                )
                token = get_token(user)

                if user.profile :
                    user.profile.role = "subscriber"
                    user.profile.save()
                
                refresh_token = create_refresh_token(user)
                return CreateSchool(
                    user = user,
                    school = school,
                    subscriber = subscriber,
                    token = token,
                    refresh_token = refresh_token,
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class AddSchool(graphene.Mutation):
    """Create a school and add it to a subscriber which is current logined subscriber user API"""
    school = graphene.Field(SchoolSchema)
    subscriber = graphene.Field(SubscriberSchema)
    class Arguments:
        name = graphene.String(required=True)
        district = graphene.String(required=True)
        type = graphene.String(required=True)
        zip = graphene.String(required=True)
        country = graphene.String(required=True)
        coupon_code = graphene.String(required=True)

    def mutate(
        self,
        info,
        name,
        district,
        type,
        zip,
        country,
        coupon_code,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                if user.schoolpersonnel.subscriber is None:
                    raise Exception("You don't have permission to add a school")
                subscriber = user.schoolpersonnel.subscriber

                school = School(
                    name = name,
                    type_of = type,
                    zip = zip,
                    country = country,
                    district = district,
                )
                school.save()
                
                if coupon_code:
                    subscriber.coupon_code = DiscountCode.objects.get(code=coupon_code)

                SchoolSubscriber.objects.create(
                    subscriber = subscriber,
                    school = school
                )
                
                return AddSchool(
                    school = school,
                    subscriber = subscriber,
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateTeachersInSchool(graphene.Mutation):
    """Create any number of the teachers necessary for the school and place them in the school API"""
    school = graphene.Field(SchoolSchema)
    class Arguments:
        teachers = graphene.List(CreateTeacherInput)

    def mutate(
        self,
        info,
        teachers
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                school = user.schoolpersonnel.school
                for teacher in teachers:
                    user = get_user_model()(
                        username = teacher.username,
                        first_name = teacher.name,
                        last_name = teacher.last_name
                    )
                    user.set_password(teacher.password)
                    user.email = teacher.email
                    user.save()
                    if(teacher.user_type == "Admin"):
                        admin = AdministrativePersonnel.objects.create(
                            school = school,
                            user = user,
                            name = teacher.name,
                            last_name = teacher.last_name,
                            gender = teacher.gender,
                        )
                    else : 
                        teacher= Teacher.objects.create(
                            school=school,
                            user=user,
                            name=teacher.name,
                            last_name=teacher.last_name,
                            gender = teacher.gender,
                        )

                return CreateTeachersInSchool(
                    school = school
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class UpdateClassroomSettings(graphene.Mutation):
    """Update classroom settings API"""
    classroom = graphene.Field(ClassroomSchema)
    user = graphene.Field(UserSchema)
    class Arguments:
        classroom_id = graphene.ID()
        language = graphene.String()
        enable_game = graphene.Boolean()
        game_cost_percentage = graphene.Int()
        time_zone_value = graphene.String()
        time_zone_offset = graphene.Int()
        goal_coins_per_day = graphene.Int()
        monday_start = graphene.Time()
        monday_end = graphene.Time()
        tuesday_start = graphene.Time()
        tuesday_end = graphene.Time()
        wednesday_start = graphene.Time()
        wednesday_end = graphene.Time()
        thursday_start = graphene.Time()
        thursday_end = graphene.Time()
        friday_start = graphene.Time()
        friday_end = graphene.Time()
        saturday_start = graphene.Time()
        saturday_end = graphene.Time()
        sunday_start = graphene.Time()
        sunday_end = graphene.Time()
    def mutate(
        self,
        info,
        classroom_id,
        enable_game,
        game_cost_percentage,
        monday_start,
        monday_end,
        tuesday_start,
        tuesday_end,
        wednesday_start,
        wednesday_end,
        thursday_start,
        thursday_end,
        friday_start,
        friday_end,
        saturday_start,
        saturday_end,
        sunday_start,
        sunday_end,
        time_zone_value,
        time_zone_offset,
        language = None,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                classroom = Classroom.objects.get(pk=classroom_id)
                classroom.language = language
                classroom.enable_games = enable_game
                classroom.game_cost_percentage = game_cost_percentage
                classroom.time_zone_value = time_zone_value
                classroom.time_zone_offset = time_zone_offset
                classroom.monday_start = monday_start
                classroom.monday_end = monday_end
                classroom.tuesday_start = tuesday_start
                classroom.tuesday_end = tuesday_end
                classroom.wednesday_start = wednesday_start
                classroom.wednesday_end = wednesday_end
                classroom.thursday_start = thursday_start
                classroom.thursday_end = thursday_end
                classroom.friday_start = friday_start
                classroom.friday_end = friday_end
                classroom.saturday_start = saturday_start
                classroom.saturday_end = saturday_end
                classroom.sunday_start = sunday_start
                classroom.sunday_end = sunday_end
                classroom.save()
                return UpdateClassroomSettings(
                    classroom = classroom,
                    user = user
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class ImportStudentToClassroom(graphene.Mutation):
    classroom = graphene.Field(ClassroomSchema)
    
    class Arguments:
        username = graphene.String()
        password = graphene.String()
        classroom_id = graphene.ID()

    def mutate(
        self,
        info,
        username,
        password,
        classroom_id,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                student_user = User.objects.get(username = username)
                student = student_user.student
                pwdChkResult = student_user.check_password(password)
                if (pwdChkResult == False) :
                    raise Exception('Password of Student is wrong')
                classroom = Classroom.objects.get(pk=classroom_id)
                student.classroom = classroom
                student.audience = classroom.audience
                student.save()
                return ImportStudentToClassroom(
                    classroom = classroom
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateStudentsInputs(graphene.InputObjectType):
    classroom_id = graphene.ID()
    grade_id = graphene.ID()
    name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()
    username = graphene.String()

class CreateStudentToClassroom(graphene.Mutation):
    classroom = graphene.Field(ClassroomSchema)
    student = graphene.Field(StudentSchema)
    class Arguments:
        name = graphene.String()
        last_name = graphene.String()
        username = graphene.String()
        password = graphene.String()
        classroom_id = graphene.ID()
        grade_id = graphene.ID()

    def mutate(
        self,
        info,
        name,
        last_name,
        username,
        password,
        classroom_id,
        grade_id,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                
                user = get_user_model()(
                    username = username,
                    first_name = name,
                    last_name = last_name,
                )
                user.set_password(password)
                user.save()
                classroom = Classroom.objects.get(pk=classroom_id)
                if(len(classroom.student_set.all()) > Classroom.LIMIT_STUDENTS):
                    raise Exception("Number of students exceeded in this classroom")
                student = Student(
                    first_name=name,
                    last_name=last_name,
                    full_name=name + ' ' + last_name,
                    user = user,
                    classroom = classroom,
                    audience = classroom.audience,
                )
                student.save()
                studentGrade = StudentGrade.objects.get_or_create(
                    student = student,
                    grade_id = grade_id
                )
                return CreateStudentToClassroom(
                    classroom = classroom,
                    student = student
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateStudentsToClassroom(graphene.Mutation):
    classroom = graphene.Field(ClassroomSchema)
    class Arguments:
        students = graphene.List(CreateStudentsInputs)

    def mutate(
        self,
        info,
        students,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')

                for student_data in students:

                    user = get_user_model()(
                        username = student_data.username,
                        first_name = student_data.name,
                        last_name = student_data.last_name,
                    )
                    user.set_password(student_data.password)
                    user.save()
                    classroom = Classroom.objects.get(pk=student_data.classroom_id)
                    if(len(classroom.student_set.all()) > Classroom.LIMIT_STUDENTS):
                        raise Exception("Number of students exceeded in this classroom")
                    student = Student(
                        first_name=student_data.name,
                        last_name=student_data.last_name,
                        full_name=student_data.name + ' ' + student_data.last_name,
                        user = user,
                        classroom = classroom,
                        audience = classroom.audience,
                    )
                    student.save()
                    studentGrade = StudentGrade.objects.get_or_create(
                        student = student,
                        grade_id = student_data.grade_id
                    )
                return CreateStudentToClassroom(
                    classroom = classroom,
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class RemoveStudentFromClassroom(graphene.Mutation):
    classroom = graphene.Field(ClassroomSchema)
    class Arguments:
        classroom_id = graphene.ID()
        student_id = graphene.ID()

    def mutate(
        self,
        info,
        classroom_id,
        student_id,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                
                student = Student.objects.get(pk = student_id)
                if(student.classroom is None):
                    raise Exception("This student doesn not have a classroom")
                if(str(student.classroom.id) != str(classroom_id)):
                    raise Exception('Classroom does not exist in this student')
                
                student.classroom = None
                student.save()
                
                classroom = Classroom.objects.get(pk=classroom_id)
                return CreateStudentToClassroom(
                    classroom = classroom,
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateGroup(graphene.Mutation):
    group = graphene.Field(GroupSchema)
    teacher = graphene.Field(TeacherSchema)
    classroom = graphene.Field(ClassroomSchema)
    class Arguments:
        name = graphene.String()
        classroom_id = graphene.ID()
        studentIds = graphene.List(graphene.ID)

    def mutate(
        self,
        info,
        name,
        classroom_id,
        studentIds,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                classroom = Classroom.objects.get(pk = classroom_id)
                group = Group(
                    name = name,
                    classroom = classroom
                )
                group.save()
                for studentId in studentIds:
                    student = Student.objects.get(pk = studentId, classroom = classroom)
                    group.student_set.add(student)
                return CreateGroup(
                    group = group,
                    teacher = classroom.teacherclassroom.teacher,
                    classroom = classroom
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class StudentWithCoinsSchema(graphene.ObjectType):
    student = graphene.Field(StudentSchema)
    coins_sum = graphene.Int()

class ClassroomReport(graphene.Mutation):
    coins_today = graphene.Int()
    goal_coins_per_day = graphene.Int()
    correct_questions_count_today = graphene.Int()
    correct_questions_count_yesterday = graphene.Int()
    coins_yesterday = graphene.Int()
    class_leaders_yesterday = graphene.List(StudentWithCoinsSchema)
    coins_all = graphene.Int()
    questions_all = graphene.Int()

    class Arguments:
        classroom_id = graphene.ID()

    def mutate(
        self,
        info,
        classroom_id,
    ):
        classroom = Classroom.objects.get(pk = classroom_id)

        #--------- convert timezone to classroom time zone and get today start and yesterday start in classroom timezone -S----------#
        timezone_value = classroom.time_zone_value
        now = timezone.now()
        now = now.astimezone(pytz_timezone(timezone_value))
        today_start = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        yesterday_start = (today_start - datetime.timedelta(1))
        #--------- convert timezone to classroom time zone and get today start and yesterday start in classroom timezone -E----------#
        
        #--------- make conditions to filter only students in the classroom -S--------------#
        students = classroom.student_set.all()
        filter_condition_students = None
        for student in students:
            if filter_condition_students is None:
                filter_condition_students = Q(student=student)
            else : filter_condition_students = filter_condition_students | Q(student=student)
        #--------- make conditions to filter only students in the classroom -E--------------#
        
        query_set_block_presentations_from_yesterday = BlockPresentation.all_objects.filter(filter_condition_students).filter(update_timestamp__gt = yesterday_start)
        query_set_block_presentations_only_yesterday = query_set_block_presentations_from_yesterday.filter(update_timestamp__lte = today_start)
        query_set_block_presentations_only_today = query_set_block_presentations_from_yesterday.filter(update_timestamp__gt = today_start)
        result_yesterday_for_leaders = query_set_block_presentations_only_yesterday.values('student').annotate(coins_sum=Sum('coins')).order_by('-coins_sum')[:5]
        result_yesterday = query_set_block_presentations_only_yesterday.aggregate(Sum('coins'),Sum('hits'),Sum('total'))
        result_today = query_set_block_presentations_only_today.aggregate(Sum('coins'),Sum('hits'),Sum('total'))
        result_all = BlockPresentation.all_objects.filter(filter_condition_students).aggregate(Sum('coins'),Sum('hits'),Sum('total'))

        #----------replace student id to student schema in the leaders in the yesterday -S------#
        for key,result_yesterday_for_leader in enumerate(result_yesterday_for_leaders) :
            student_id =  result_yesterday_for_leaders[key]['student']
            student = Student.objects.get(pk = student_id)
            result_yesterday_for_leaders[key]['student'] = student
        #----------replace student id to student schema in the leaders in the yesterday -E------#

        return ClassroomReport(
            coins_today =result_today['coins__sum'] if result_today['coins__sum'] else 0,
            goal_coins_per_day = classroom.goal_coins_per_day if classroom.goal_coins_per_day else 0,
            correct_questions_count_today = result_today['hits__sum'] if result_today['hits__sum'] else 0,
            correct_questions_count_yesterday = result_yesterday['hits__sum'] if result_yesterday['hits__sum'] else 0,
            coins_yesterday = result_yesterday['coins__sum'] if result_yesterday['coins__sum'] else 0,
            class_leaders_yesterday = result_yesterday_for_leaders,
            coins_all = result_all['coins__sum'] if result_all['coins__sum'] else 0,
            questions_all = result_all['total__sum'] if result_all['total__sum'] else 0,
        )

class Mutation(graphene.ObjectType):
    create_teacher = CreateTeacher.Field()
    create_classroom = CreateClassroom.Field()
    create_school = CreateSchool.Field()
    create_teachers_in_school = CreateTeachersInSchool.Field()
    update_classroom_settings = UpdateClassroomSettings.Field()
    import_student_to_classroom = ImportStudentToClassroom.Field()
    create_student_to_classroom = CreateStudentToClassroom.Field()
    create_students_to_classroom = CreateStudentsToClassroom.Field()
    create_group = CreateGroup.Field()
    remove_student_from_classroom = RemoveStudentFromClassroom.Field()
    classroom_report = ClassroomReport.Field()
    add_school = AddSchool.Field()