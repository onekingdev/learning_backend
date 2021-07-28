from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from graphene_django import DjangoObjectType
from api.models import profile
from graphql_jwt.shortcuts import create_refresh_token, get_token
from students.models import Student
from guardians.models import Guardian, GuardianStudent
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import graphene


class UserSchema(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserProfileSchema(DjangoObjectType):
    class Meta:
        model = profile


# Send mail with django-mailer
class SendMail(graphene.Mutation):
    email = graphene.String()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        send_mail(
            'Subject',
            'Message.',
            settings.SENDGRID_DEFAULT_SENDER,
            [email],
            fail_silently=False,
        )

        return SendMail(email=email)


class SendMailSendgrid(graphene.Mutation):
    email = graphene.String()
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        message = Mail(
            from_email=settings.SENDGRID_DEFAULT_SENDER,
            to_emails=[email],
            subject='Subject',
            plain_text_content='Message.',
        )
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            return str(e)

        return SendMailSendgrid(email=email, message=message)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserSchema)
    profile = graphene.Field(UserProfileSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=False)

    def mutate(self, info, username, password):
        user = get_user_model()(
            username=username,
        )
        user.set_password(password)
        user.save()

        profile_obj = profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateUser(user=user, profile=profile_obj, token=token, refresh_token=refresh_token)


class CreateGuardian(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    user = graphene.Field(UserSchema)
    profile = graphene.Field(UserProfileSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=False)

    def mutate(self, info, username, password):
        user = get_user_model()(
            username=username,
        )
        user.set_password(password)
        user.save()

        guardian = Guardian(
            user=user,
        )
        guardian.save()

        profile_obj = profile.objects.get(user=user.id)
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return CreateGuardian(
            guardian=guardian,
            user=user, profile=profile_obj,
            token=token,
            refresh_token=refresh_token
        )


class CreateStudent(graphene.Mutation):
    student = graphene.Field('students.schema.StudentSchema')
    user = graphene.Field(UserSchema)
    profile = graphene.Field(UserProfileSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        school = graphene.ID(required=False)
        grade = graphene.ID(required=True)
        group = graphene.ID(required=True)

    def mutate(self, info, first_name, last_name, username, password, school, grade, group):
        user = get_user_model()(
            username=username,
        )
        user.set_password(password)
        user.save()

        student = Student(
            user=user,
            first_name=first_name,
            last_name=last_name,
        )
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


class CreateGuardianStudent(graphene.Mutation):
    guardian_student = graphene.List('guardians.schema.GuardianStudentSchema')

    class Arguments:
        guardian = graphene.ID(required=True)
        students = graphene.List(graphene.NonNull(graphene.ID))

    def mutate(self, info, guardian, students):
        guardian = Guardian.objects.get(id=guardian)
        guardian_students = []

        for student_id in students:
            student = Student.objects.get(id=student_id)
            guardian_student = GuardianStudent(
                guardian=guardian,
                student=student
            )
            guardian_student.save()
            guardian_students.append(guardian_student)

        return CreateGuardianStudent(
            guardian_student=guardian_students,
        )


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_guardian = CreateGuardian.Field()
    create_student = CreateStudent.Field()
    create_guardian_student = CreateGuardianStudent.Field()
    send_mail = SendMail.Field()
    send_mail_sendgrid = SendMailSendgrid.Field()


class Query(graphene.ObjectType):
    whoami = graphene.Field(UserSchema)
    users = graphene.List(UserSchema)

    def resolve_whoami(root, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure')
        return user

    def resolve_users(root, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure')
        if user.profile.role != 'manager':
            raise Exception('Role Failure')
        return get_user_model().objects.all()
